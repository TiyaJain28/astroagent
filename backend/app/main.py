from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.birth import router as birth_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="AstroAgent API",
    description="AI-powered astrology assistant built with LangGraph, Gemini, Swiss Ephemeris, and RAG.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(birth_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "AstroAgent",
        "version": "1.0.0"
    }