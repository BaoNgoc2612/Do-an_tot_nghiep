# Kiến trúc Hệ thống SkinAI

## Sơ đồ tổng quan

```
┌─────────────────────────────────────────────────────────────────────┐
│                         NGƯỜI DÙNG (Browser)                        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTPS
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vercel)                                 │
│  ┌───────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ ┌───────────┐ │
│  │  ReactJS  │ │ Tailwind │ │ Chart.js │ │ Axios  │ │React Query│ │
│  └───────────┘ └──────────┘ └──────────┘ └────────┘ └───────────┘ │
│                                                                     │
│  Pages: Login | Dashboard | Upload | Result | Routine | History     │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ REST API (JSON)
                               │ JWT Token Authentication
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND (Render)                                  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    FastAPI Server                             │   │
│  ├──────────────────────────────────────────────────────────────┤   │
│  │                                                              │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐    │   │
│  │  │ Auth Module │  │ Analysis    │  │ Routine Module   │    │   │
│  │  │             │  │ Module      │  │                  │    │   │
│  │  │ • Register  │  │ • Upload    │  │ • Generate AM/PM │    │   │
│  │  │ • Login     │  │ • Predict   │  │ • Get history    │    │   │
│  │  │ • JWT       │  │ • History   │  │ • Compare        │    │   │
│  │  └─────────────┘  └──────┬──────┘  └────────┬─────────┘    │   │
│  │                          │                   │              │   │
│  │                          ▼                   ▼              │   │
│  │              ┌──────────────────┐  ┌────────────────────┐   │   │
│  │              │   AI Engine      │  │  Gemini API Client │   │   │
│  │              │                  │  │                    │   │   │
│  │              │ • EfficientNetB0 │  │ • Skincare advice  │   │   │
│  │              │ • Skin type      │  │ • Explain why      │   │   │
│  │              │ • Issue detect   │  │ • Chat Q&A         │   │   │
│  │              │ • TensorFlow     │  │                    │   │   │
│  │              └──────────────────┘  └────────────────────┘   │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │              SQLAlchemy ORM + Alembic                 │   │   │
│  │  └──────────────────────────┬───────────────────────────┘   │   │
│  └─────────────────────────────┼────────────────────────────────┘   │
└────────────────────────────────┼────────────────────────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│   PostgreSQL     │ │   Cloudinary     │ │  Google Gemini   │
│   (Neon.tech)    │ │   (Free tier)    │ │  1.5 Flash API   │
│                  │ │                  │ │                  │
│ • users          │ │ • Skin images    │ │ • Skincare advice│
│ • skin_analyses  │ │ • Avatars        │ │ • Explain AI     │
│ • routines       │ │ • Product imgs   │ │ • Chat support   │
│ • products       │ │                  │ │                  │
│ • notifications  │ │                  │ │                  │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

## Luồng xử lý chính (Flow)

### Luồng 1: Phân tích da
```
User upload ảnh → Frontend gửi ảnh → Backend nhận ảnh
  → Upload ảnh lên Cloudinary (lấy URL)
  → AI Engine predict:
      • Model 1: Phân loại loại da (oily/dry/normal)
      • Model 2: Phát hiện vấn đề (acne/dark_spots/...)
  → Gửi kết quả AI cho Gemini API → nhận tư vấn skincare
  → Lưu tất cả vào PostgreSQL
  → Trả về JSON cho Frontend hiển thị
```

### Luồng 2: Tạo Skincare Routine
```
Kết quả phân tích → Recommendation Engine (rule-based):
  • Da dầu + mụn → BHA, Niacinamide, Oil-free moisturizer
  • Da khô → Hyaluronic Acid, Ceramide, Rich cream
  • ...
  → Gemini API bổ sung giải thích chi tiết
  → Tạo routine AM (5 bước) + PM (5 bước)
  → Lưu vào database → Trả về Frontend
```

### Luồng 3: Theo dõi tiến trình
```
User có nhiều lần phân tích → Backend query lịch sử
  → Tính delta scores giữa các lần
  → Trả về data dạng time-series cho Chart.js
  → Frontend vẽ Line chart: cải thiện theo tuần
```

## API Endpoints

| Method | Endpoint | Mô tả |
|---|---|---|
| POST | `/auth/register` | Đăng ký |
| POST | `/auth/login` | Đăng nhập → JWT token |
| GET | `/auth/me` | Thông tin user hiện tại |
| POST | `/api/analyze` | Upload ảnh + phân tích da |
| GET | `/api/analyses/history` | Lịch sử phân tích |
| GET | `/api/analyses/{id}` | Chi tiết 1 lần phân tích |
| GET | `/api/analyses/compare/{id1}/{id2}` | So sánh 2 lần |
| GET | `/api/analyses/progress` | Data tiến trình (chart) |
| POST | `/api/routine/generate` | Tạo routine AM/PM |
| GET | `/api/routine/{analysis_id}` | Lấy routine của 1 phân tích |
| POST | `/api/chat` | Chat với Gemini AI |
| GET | `/api/notifications` | Danh sách thông báo |
| PUT | `/api/notifications/{id}/read` | Đánh dấu đã đọc |
| GET | `/api/products` | Danh sách sản phẩm |
| PUT | `/api/user/profile` | Cập nhật profile |
| DELETE | `/api/user/account` | Xóa tài khoản |
