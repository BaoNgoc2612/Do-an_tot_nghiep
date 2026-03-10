# Dataset Notes

## Danh sách Dataset cần tải

### 1. ACNE04
- **Nguồn:** Kaggle
- **Tìm kiếm:** "ACNE04" hoặc "acne grading classification"
- **Mô tả:** ~1.400 ảnh phân loại mụn theo 4 mức độ (nhẹ/vừa/nặng/rất nặng)
- **Lưu tại:** `ai/data/raw/acne04/`
- **Dùng cho:** Train model phát hiện mụn (Tuần 5)
- [ ] Đã tải

### 2. HAM10000
- **Nguồn:** Kaggle
- **Tìm kiếm:** "HAM10000" hoặc "skin cancer mnist ham10000"
- **Mô tả:** >10.000 ảnh bệnh da liễu có nhãn bác sĩ (7 loại tổn thương)
- **Lưu tại:** `ai/data/raw/ham10000/`
- **Dùng cho:** Train model phân loại tổn thương da (Tuần 5, mở rộng)
- [ ] Đã tải

### 3. Skin Type Classification
- **Nguồn:** Kaggle
- **Tìm kiếm:** "oily dry skin type" hoặc "skin type classification"
- **Mô tả:** Ảnh phân loại loại da (dầu/khô/hỗn hợp/thường)
- **Lưu tại:** `ai/data/raw/skin_type/`
- **Dùng cho:** Train model phân loại loại da (Tuần 4)
- [ ] Đã tải

## Ghi chú
- Tổng dung lượng ước tính: ~2-4 GB
- Không push data lên GitHub (đã có trong .gitignore)
- Sau khi tải, chạy script kiểm tra ở `ai/scripts/check_dataset.py`
