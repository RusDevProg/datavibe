from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, analyze, chat
from app.services.ai_service import AIService
import os

app = FastAPI(
    title="DataVibe API",
    description="AI-Powered Data Dashboard",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(analyze.router, prefix="/api", tags=["Analyze"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": "DataVibe API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}