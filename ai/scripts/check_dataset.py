"""
Script kiểm tra dataset đã tải về.
Chạy: python ai/scripts/check_dataset.py
"""

import os
from pathlib import Path
from collections import Counter

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"

def check_dataset(name, path):
    """Kiểm tra 1 dataset: đếm ảnh, liệt kê class."""
    full_path = DATA_DIR / path
    print(f"\n{'='*50}")
    print(f"📂 Dataset: {name}")
    print(f"   Path: {full_path}")
    
    if not full_path.exists():
        print(f"   ❌ Chưa tải! Folder không tồn tại.")
        return
    
    # Đếm ảnh theo extension
    img_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'}
    all_images = []
    
    for root, dirs, files in os.walk(full_path):
        for f in files:
            if Path(f).suffix.lower() in img_extensions:
                # Class = tên folder chứa ảnh
                rel = os.path.relpath(root, full_path)
                all_images.append(rel)
    
    if not all_images:
        print(f"   ⚠️ Không tìm thấy ảnh nào!")
        return
    
    print(f"   ✅ Tổng số ảnh: {len(all_images)}")
    
    # Đếm theo class (folder)
    class_counts = Counter(all_images)
    print(f"   📊 Phân phối theo class:")
    for cls, count in sorted(class_counts.items()):
        bar = '█' * (count // 20)
        print(f"      {cls:30s} : {count:5d} ảnh  {bar}")


def main():
    print("🔍 KIỂM TRA DATASET")
    print(f"   Data directory: {DATA_DIR}")
    
    datasets = [
        ("ACNE04 (Phân loại mụn)", "acne04"),
        ("HAM10000 (Bệnh da liễu)", "ham10000"),
        ("Skin Type (Loại da)", "skin_type"),
    ]
    
    for name, path in datasets:
        check_dataset(name, path)
    
    print(f"\n{'='*50}")
    print("✅ Kiểm tra hoàn tất!")
    print("Tip: Nếu dataset chưa tải, xem hướng dẫn tại ai/data/DATASETS.md")


if __name__ == "__main__":
    main()
