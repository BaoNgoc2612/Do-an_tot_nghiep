# 🌸 SkinAI — Hệ thống Chẩn đoán Da liễu & Skincare Cá nhân hóa bằng AI

## Mô tả

Hệ thống web sử dụng AI để phân tích tình trạng da từ ảnh chụp, nhận diện loại da và các vấn đề da liễu, từ đó đề xuất chu trình skincare AM/PM cá nhân hóa. Người dùng có thể theo dõi tiến trình cải thiện da theo thời gian.

## Chức năng chính

- **Phân tích da từ ảnh** — Nhận diện loại da (dầu/khô/hỗn hợp/nhạy cảm) và phát hiện vấn đề (mụn, thâm, lỗ chân lông, nếp nhăn)
- **Gợi ý Skincare AM/PM** — Chu trình skincare cá nhân hóa với giải thích thành phần (Explainable AI)
- **Theo dõi tiến trình** — Upload ảnh định kỳ, biểu đồ so sánh before/after
- **Tài khoản người dùng** — Đăng ký, đăng nhập, lưu lịch sử phân tích

## Tech Stack

| Tầng | Công nghệ |
|---|---|
| AI Model | Python + TensorFlow + EfficientNetB0 |
| AI Tư vấn | Google Gemini 1.5 Flash API |
| Backend | Python + FastAPI + SQLAlchemy |
| Frontend | ReactJS + TailwindCSS + Chart.js |
| Database | PostgreSQL |
| Lưu ảnh | Cloudinary |
| Auth | JWT Token |
| Deploy | Render (backend) + Vercel (frontend) |
| Testing | Pytest + React Testing Library |

## Cấu trúc thư mục

```
skin-ai-project/
├── ai/              # AI model training & inference
├── backend/         # FastAPI server
├── frontend/        # ReactJS web app
└── docs/            # Tài liệu, wireframes, diagrams
```

## Cài đặt & Chạy

*(Sẽ cập nhật khi setup xong)*

## Tác giả

- Đồ án tốt nghiệp — Chuyên ngành Công nghệ Thông tin
