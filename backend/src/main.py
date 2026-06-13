"""GovOne — Main application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Hệ thống Quản lý Hành chính Công Thông minh — Hackaithon 2026",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # ─── Register AI routers (Round 4) ────────────────────────────────
    from src.ai.api.ocr_router import router as ocr_router
    from src.ai.api.stt_router import router as stt_router
    from src.ai.api.nlp_router import router as nlp_router
    from src.ai.api.auto_fill_router import router as auto_fill_router
    from src.ai.api.health_router import router as health_router
    
    app.include_router(ocr_router)
    app.include_router(stt_router)
    app.include_router(nlp_router)
    app.include_router(auto_fill_router)
    app.include_router(health_router)
    
    return app


app = create_app()


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
