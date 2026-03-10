"""
Tuần 3 - Bước 2: Tiền xử lý & Chia dữ liệu
Chạy: python ai/scripts/02_preprocess_data.py

Script này sẽ:
1. Copy ảnh từ dataset gốc theo class đã chọn
2. Resize về 224x224
3. Chia train/val/test (70/15/15) stratified
4. Lưu CSV danh sách file
5. Áp dụng augmentation cho class ít ảnh
"""

import os
import shutil
import csv
from pathlib import Path
from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split

# === CẤU HÌNH ===
BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data" / "raw" / "skin_disease" / "Image_Dataset_for_Skin_Disease"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
IMG_SIZE = (224, 224)

# Task 1: Phân loại loại da
SKIN_TYPE_MAP = {
    "Oily_Skin": "oily",
    "Dry_Skin": "dry",
    "Normal_Skin": "normal",
}

# Task 2: Phân loại vấn đề da (chọn 6 class phổ biến để bắt đầu)
SKIN_ISSUE_MAP = {
    "Acne": "acne",
    "Eczema": "eczema",
    "Psoriasis_Pictures_Lichen_Planus_And_Related_Diseases": "psoriasis",
    "Rashes": "rashes",
    "Rosacea": "rosacea",
    "Dermatitis": "dermatitis",
    "Normal_Skin": "healthy",
}

IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}


def collect_images(class_map: dict, task_name: str) -> tuple:
    """Thu thập danh sách ảnh + label từ class map."""
    file_paths = []
    labels = []
    for folder_name, label in class_map.items():
        folder = RAW_DIR / folder_name
        if not folder.exists():
            print(f"  ⚠️ Folder not found: {folder_name}")
            continue
        count = 0
        for f in folder.rglob("*"):
            if f.suffix.lower() in IMG_EXTENSIONS:
                file_paths.append(str(f))
                labels.append(label)
                count += 1
        print(f"  {label:15s} : {count:5d} images from {folder_name}")
    print(f"  Total: {len(file_paths)} images")
    return file_paths, labels


def resize_and_copy(src_path: str, dst_path: str):
    """Resize ảnh về IMG_SIZE và lưu."""
    try:
        img = Image.open(src_path).convert("RGB")
        img = img.resize(IMG_SIZE, Image.LANCZOS)
        img.save(dst_path, "JPEG", quality=95)
        return True
    except Exception as e:
        print(f"  ❌ Error processing {src_path}: {e}")
        return False


def augment_image(img: Image.Image, aug_type: int) -> Image.Image:
    """Áp dụng augmentation đơn giản."""
    if aug_type == 0:
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    elif aug_type == 1:
        return img.rotate(15, fillcolor=(0, 0, 0))
    elif aug_type == 2:
        return img.rotate(-15, fillcolor=(0, 0, 0))
    elif aug_type == 3:
        arr = np.array(img, dtype=np.float32)
        arr = np.clip(arr * 1.2, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)
    elif aug_type == 4:
        arr = np.array(img, dtype=np.float32)
        arr = np.clip(arr * 0.8, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)
    return img


def process_task(class_map: dict, task_name: str):
    """Xử lý 1 task: thu thập, resize, chia, augment."""
    print(f"\n{'='*60}")
    print(f"📦 PROCESSING: {task_name}")
    print(f"{'='*60}")

    # 1. Thu thập ảnh
    file_paths, labels = collect_images(class_map, task_name)
    if not file_paths:
        print("❌ No images found!")
        return

    # 2. Chia train/val/test (70/15/15) stratified
    print(f"\n📊 Splitting data (70/15/15)...")
    X_train, X_temp, y_train, y_temp = train_test_split(
        file_paths, labels, test_size=0.3, random_state=42, stratify=labels
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    print(f"  Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")

    # 3. Resize và copy vào thư mục processed
    task_dir = PROCESSED_DIR / task_name
    csv_rows = []

    for split_name, X_split, y_split in [
        ("train", X_train, y_train),
        ("val", X_val, y_val),
        ("test", X_test, y_test),
    ]:
        print(f"\n  Processing {split_name}...")
        split_dir = task_dir / split_name
        success = 0

        for i, (src, label) in enumerate(zip(X_split, y_split)):
            label_dir = split_dir / label
            label_dir.mkdir(parents=True, exist_ok=True)
            dst = label_dir / f"{label}_{split_name}_{i:05d}.jpg"
            if resize_and_copy(src, str(dst)):
                csv_rows.append([str(dst), label, split_name])
                success += 1

        print(f"  ✅ {split_name}: {success} images processed")

    # 4. Augmentation cho class ít ảnh (chỉ train set)
    print(f"\n🔄 Augmenting underrepresented classes in train set...")
    from collections import Counter
    train_counts = Counter(y_train)
    max_count = max(train_counts.values())
    target_count = int(max_count * 0.7)  # Target: 70% class lớn nhất

    for label, count in train_counts.items():
        if count < target_count:
            need = target_count - count
            print(f"  {label}: {count} → augmenting {need} more to reach {target_count}")
            label_dir = task_dir / "train" / label
            existing = list(label_dir.glob("*.jpg"))
            aug_idx = 0
            for j in range(need):
                src_img_path = existing[j % len(existing)]
                try:
                    img = Image.open(src_img_path)
                    aug_img = augment_image(img, j % 5)
                    dst = label_dir / f"{label}_aug_{aug_idx:05d}.jpg"
                    aug_img.save(str(dst), "JPEG", quality=95)
                    csv_rows.append([str(dst), label, "train_aug"])
                    aug_idx += 1
                except Exception as e:
                    print(f"    ❌ Aug error: {e}")

    # 5. Lưu CSV
    csv_path = task_dir / "dataset_split.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file_path", "label", "split"])
        writer.writerows(csv_rows)
    print(f"\n📄 CSV saved: {csv_path}")

    # 6. Tóm tắt
    print(f"\n📊 FINAL SUMMARY for {task_name}:")
    final_counts = {}
    for split in ["train", "val", "test"]:
        split_dir = task_dir / split
        if split_dir.exists():
            for label_dir in sorted(split_dir.iterdir()):
                if label_dir.is_dir():
                    count = len(list(label_dir.glob("*.jpg")))
                    key = f"{split}/{label_dir.name}"
                    final_counts[key] = count
                    print(f"  {key:30s} : {count:5d}")


def main():
    print("🚀 DATA PREPROCESSING — SkinAI")
    print(f"  Input: {RAW_DIR}")
    print(f"  Output: {PROCESSED_DIR}")
    print(f"  Image size: {IMG_SIZE}")

    # Task 1: Skin Type
    process_task(SKIN_TYPE_MAP, "skin_type")

    # Task 2: Skin Issues
    process_task(SKIN_ISSUE_MAP, "skin_issues")

    print(f"\n{'='*60}")
    print("✅ ALL PREPROCESSING COMPLETE!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
