# Database Schema — SkinAI

## Sơ đồ quan hệ (ERD)

```
┌──────────────┐       ┌─────────────────────┐       ┌──────────────────────┐
│    users     │       │   skin_analyses     │       │  skincare_routines   │
├──────────────┤       ├─────────────────────┤       ├──────────────────────┤
│ id (PK)      │──┐    │ id (PK)             │──┐    │ id (PK)              │
│ email        │  │    │ user_id (FK)        │  │    │ analysis_id (FK)     │
│ username     │  ├───>│ image_url           │  ├───>│ routine_type (AM/PM) │
│ hashed_pwd   │  │    │ skin_type           │  │    │ steps (JSON)         │
│ avatar_url   │  │    │ issues (JSON)       │  │    │ explanation          │
│ created_at   │  │    │ scores (JSON)       │  │    │ created_at           │
│ updated_at   │  │    │ ai_confidence       │  │    └──────────────────────┘
└──────────────┘  │    │ gemini_advice       │  │
                  │    │ created_at          │  │    ┌──────────────────────┐
                  │    └─────────────────────┘  │    │     products         │
                  │                             │    ├──────────────────────┤
                  │    ┌─────────────────────┐  │    │ id (PK)              │
                  │    │   notifications     │  │    │ name                 │
                  │    ├─────────────────────┤  │    │ brand                │
                  └───>│ id (PK)             │  │    │ category             │
                       │ user_id (FK)        │  │    │ ingredients (JSON)   │
                       │ type                │  │    │ skin_types (JSON)    │
                       │ message             │  │    │ image_url            │
                       │ is_read             │  │    │ description          │
                       │ created_at          │  │    └──────────────────────┘
                       └─────────────────────┘
```

## Chi tiết các bảng

### 1. users — Người dùng
| Cột | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | UUID | PK | ID người dùng |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email đăng nhập |
| username | VARCHAR(100) | UNIQUE, NOT NULL | Tên hiển thị |
| hashed_password | VARCHAR(255) | NOT NULL | Password đã hash (bcrypt) |
| avatar_url | TEXT | NULL | URL ảnh đại diện (Cloudinary) |
| created_at | TIMESTAMP | DEFAULT NOW() | Ngày tạo tài khoản |
| updated_at | TIMESTAMP | DEFAULT NOW() | Ngày cập nhật |

### 2. skin_analyses — Kết quả phân tích da
| Cột | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | UUID | PK | ID phân tích |
| user_id | UUID | FK → users.id | Người dùng |
| image_url | TEXT | NOT NULL | URL ảnh da (Cloudinary) |
| skin_type | VARCHAR(50) | NOT NULL | Loại da: oily/dry/normal/combination |
| issues | JSONB | DEFAULT '[]' | Danh sách vấn đề: [{name, severity, confidence}] |
| scores | JSONB | DEFAULT '{}' | Chỉ số: {oil: 80, moisture: 40, acne: 60, ...} |
| ai_confidence | FLOAT | NOT NULL | Độ tin cậy model (0-1) |
| gemini_advice | TEXT | NULL | Tư vấn từ Gemini API |
| created_at | TIMESTAMP | DEFAULT NOW() | Ngày phân tích |

### 3. skincare_routines — Chu trình skincare
| Cột | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | UUID | PK | ID routine |
| analysis_id | UUID | FK → skin_analyses.id | Liên kết kết quả phân tích |
| routine_type | VARCHAR(10) | NOT NULL | AM hoặc PM |
| steps | JSONB | NOT NULL | [{step: 1, product_type, product_name, reason}] |
| explanation | TEXT | NULL | Giải thích tổng quan từ Gemini |
| created_at | TIMESTAMP | DEFAULT NOW() | Ngày tạo |

### 4. products — Sản phẩm skincare (tham khảo)
| Cột | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | UUID | PK | ID sản phẩm |
| name | VARCHAR(255) | NOT NULL | Tên sản phẩm |
| brand | VARCHAR(100) | NULL | Thương hiệu |
| category | VARCHAR(50) | NOT NULL | cleanser/toner/serum/moisturizer/sunscreen |
| ingredients | JSONB | DEFAULT '[]' | Danh sách thành phần chính |
| skin_types | JSONB | DEFAULT '[]' | Phù hợp loại da nào |
| image_url | TEXT | NULL | Ảnh sản phẩm |
| description | TEXT | NULL | Mô tả |

### 5. notifications — Thông báo / Nhắc nhở
| Cột | Kiểu | Ràng buộc | Mô tả |
|---|---|---|---|
| id | UUID | PK | ID thông báo |
| user_id | UUID | FK → users.id | Người nhận |
| type | VARCHAR(50) | NOT NULL | routine_reminder / analysis_complete / tip |
| message | TEXT | NOT NULL | Nội dung thông báo |
| is_read | BOOLEAN | DEFAULT FALSE | Đã đọc chưa |
| created_at | TIMESTAMP | DEFAULT NOW() | Ngày tạo |

## Ví dụ dữ liệu JSON

### issues (skin_analyses)
```json
[
  {"name": "acne", "severity": "moderate", "confidence": 0.85},
  {"name": "dark_spots", "severity": "mild", "confidence": 0.72},
  {"name": "large_pores", "severity": "mild", "confidence": 0.65}
]
```

### scores (skin_analyses)
```json
{
  "oil": 75,
  "moisture": 35,
  "acne": 60,
  "dark_spots": 40,
  "wrinkles": 10,
  "pores": 55
}
```

### steps (skincare_routines)
```json
[
  {"step": 1, "type": "cleanser", "name": "Gel rửa mặt BHA", "ingredient": "Salicylic Acid 2%", "reason": "Làm sạch dầu thừa, thông thoáng lỗ chân lông"},
  {"step": 2, "type": "toner", "name": "Toner Niacinamide", "ingredient": "Niacinamide 5%", "reason": "Kiểm soát dầu, se khít lỗ chân lông"},
  {"step": 3, "type": "serum", "name": "Serum Vitamin C", "ingredient": "Ascorbic Acid 15%", "reason": "Làm sáng thâm mụn"},
  {"step": 4, "type": "moisturizer", "name": "Kem dưỡng ẩm nhẹ", "ingredient": "Hyaluronic Acid", "reason": "Cấp ẩm không gây bít tắc"},
  {"step": 5, "type": "sunscreen", "name": "Kem chống nắng SPF50", "ingredient": "SPF50 PA+++", "reason": "Bảo vệ da khỏi tia UV (chỉ AM)"}
]
```
