from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import upload, reports, chat, healthCheck

app = FastAPI(
    title="Project Plan Review API",
    description="Upload project plans, generate reports, and query them with natural language.",
    version="0.1.0"
)

# Allow local frontend (adjust origin if hosted separately)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(healthCheck.router, prefix="/health", tags=["Health Check"])
