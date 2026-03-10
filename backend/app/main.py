from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SkinAI API",
    description="Hệ thống Chẩn đoán Da liễu & Skincare Cá nhân hóa bằng AI",
    version="1.0.0",
)

# CORS - cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "SkinAI API is running", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
