"""
Tuần 3 - Bước 1: Khám phá Dataset (EDA)
Chạy: python ai/scripts/01_explore_dataset.py

Script này sẽ:
1. Đếm số ảnh trong từng class
2. Vẽ biểu đồ phân phối
3. Hiển thị ảnh mẫu từ mỗi class
4. Kiểm tra ảnh lỗi
"""

import os
import sys
from pathlib import Path
from collections import Counter

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# === CẤU HÌNH ===
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "raw" / "skin_disease" / "Image_Dataset_for_Skin_Disease"
OUTPUT_DIR = BASE_DIR / "data" / "eda_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Nhóm các folder theo mục đích sử dụng
SKIN_TYPE_CLASSES = {
    "Oily_Skin": "Oily",
    "Dry_Skin": "Dry",
    "Normal_Skin": "Normal",
}

SKIN_ISSUE_CLASSES = {
    "Acne": "Acne",
    "Eczema": "Eczema",
    "Rashes": "Rashes",
    "Psoriasis_Pictures_Lichen_Planus_And_Related_Diseases": "Psoriasis",
    "Rosacea": "Rosacea",
    "Dermatitis": "Dermatitis",
    "Herpes": "Herpes",
    "Moles": "Moles",
    "Melanoma_Skin_Cancer_Nevi_And_Moles": "Melanoma",
    "Vitiligo": "Vitiligo",
}

IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}


def count_images(folder: Path) -> int:
    """Đếm số ảnh trong folder (đệ quy)."""
    count = 0
    for f in folder.rglob("*"):
        if f.suffix.lower() in IMG_EXTENSIONS:
            count += 1
    return count


def check_corrupted_images(folder: Path, max_check: int = 100) -> list:
    """Kiểm tra ảnh bị lỗi (không mở được)."""
    corrupted = []
    checked = 0
    for f in folder.rglob("*"):
        if f.suffix.lower() in IMG_EXTENSIONS:
            try:
                img = Image.open(f)
                img.verify()
                checked += 1
            except Exception:
                corrupted.append(str(f))
                checked += 1
            if checked >= max_check:
                break
    return corrupted


def get_image_stats(folder: Path, sample_size: int = 50) -> dict:
    """Lấy thống kê kích thước ảnh từ sample."""
    widths, heights = [], []
    count = 0
    for f in folder.rglob("*"):
        if f.suffix.lower() in IMG_EXTENSIONS:
            try:
                img = Image.open(f)
                w, h = img.size
                widths.append(w)
                heights.append(h)
                count += 1
            except Exception:
                pass
            if count >= sample_size:
                break
    if not widths:
        return {}
    return {
        "min_w": min(widths), "max_w": max(widths), "avg_w": int(np.mean(widths)),
        "min_h": min(heights), "max_h": max(heights), "avg_h": int(np.mean(heights)),
        "samples": count,
    }


def plot_distribution(class_counts: dict, title: str, filename: str):
    """Vẽ biểu đồ phân phối số ảnh theo class."""
    classes = list(class_counts.keys())
    counts = list(class_counts.values())

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(classes, counts, color=plt.cm.viridis(np.linspace(0.3, 0.9, len(classes))))

    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                str(count), va='center', fontsize=9)

    ax.set_xlabel('Number of Images')
    ax.set_title(title)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=150)
    plt.close()
    print(f"  📊 Saved: {OUTPUT_DIR / filename}")


def main():
    print("=" * 60)
    print("🔍 EXPLORATORY DATA ANALYSIS — SkinAI Dataset")
    print("=" * 60)

    if not DATA_DIR.exists():
        print(f"❌ Dataset not found at: {DATA_DIR}")
        sys.exit(1)

    # 1. Đếm tất cả các folder
    print("\n📂 ALL FOLDERS IN DATASET:")
    all_folders = sorted([d for d in DATA_DIR.iterdir() if d.is_dir()])
    all_counts = {}
    for folder in all_folders:
        count = count_images(folder)
        all_counts[folder.name] = count
        print(f"  {folder.name:55s} : {count:5d} images")
    total = sum(all_counts.values())
    print(f"\n  TOTAL: {total} images in {len(all_folders)} folders")

    # Vẽ biểu đồ tổng quan
    plot_distribution(all_counts, "All Classes Distribution", "all_classes_distribution.png")

    # 2. Phân tích SKIN TYPE classes
    print("\n" + "=" * 60)
    print("🧴 SKIN TYPE CLASSES (for Model 1):")
    skin_type_counts = {}
    for folder_name, label in SKIN_TYPE_CLASSES.items():
        folder = DATA_DIR / folder_name
        if folder.exists():
            count = count_images(folder)
            skin_type_counts[label] = count
            print(f"  {label:15s} : {count:5d} images")
        else:
            print(f"  {label:15s} : ❌ NOT FOUND")

    if skin_type_counts:
        total_st = sum(skin_type_counts.values())
        print(f"  TOTAL: {total_st} images")
        plot_distribution(skin_type_counts, "Skin Type Distribution", "skin_type_distribution.png")

        # Check class imbalance
        min_class = min(skin_type_counts.values())
        max_class = max(skin_type_counts.values())
        ratio = max_class / min_class if min_class > 0 else 0
        print(f"\n  ⚠️  Class imbalance ratio: {ratio:.1f}x (max/min)")
        if ratio > 3:
            print("  → Cần augmentation hoặc oversampling cho class ít ảnh!")

    # 3. Phân tích SKIN ISSUE classes
    print("\n" + "=" * 60)
    print("🔬 SKIN ISSUE CLASSES (for Model 2):")
    skin_issue_counts = {}
    for folder_name, label in SKIN_ISSUE_CLASSES.items():
        folder = DATA_DIR / folder_name
        if folder.exists():
            count = count_images(folder)
            skin_issue_counts[label] = count
            print(f"  {label:15s} : {count:5d} images")
        else:
            print(f"  {label:15s} : ❌ NOT FOUND")

    if skin_issue_counts:
        total_si = sum(skin_issue_counts.values())
        print(f"  TOTAL: {total_si} images")
        plot_distribution(skin_issue_counts, "Skin Issue Distribution", "skin_issue_distribution.png")

    # 4. Thống kê kích thước ảnh
    print("\n" + "=" * 60)
    print("📐 IMAGE SIZE STATISTICS (sampled):")
    stats = get_image_stats(DATA_DIR, sample_size=200)
    if stats:
        print(f"  Width  : min={stats['min_w']}, max={stats['max_w']}, avg={stats['avg_w']}")
        print(f"  Height : min={stats['min_h']}, max={stats['max_h']}, avg={stats['avg_h']}")
        print(f"  Sampled: {stats['samples']} images")
        print(f"  → Cần resize về 224x224 cho EfficientNet")

    # 5. Kiểm tra ảnh lỗi
    print("\n" + "=" * 60)
    print("🔧 CHECKING FOR CORRUPTED IMAGES (sample 500):")
    corrupted = check_corrupted_images(DATA_DIR, max_check=500)
    if corrupted:
        print(f"  ⚠️ Found {len(corrupted)} corrupted images!")
        for c in corrupted[:5]:
            print(f"    - {c}")
    else:
        print("  ✅ No corrupted images found in sample!")

    print("\n" + "=" * 60)
    print("✅ EDA COMPLETE! Charts saved to:", OUTPUT_DIR)
    print("=" * 60)


if __name__ == "__main__":
    main()
