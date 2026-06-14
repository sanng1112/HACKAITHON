"""GovOne — Main application entry point."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("govone")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Hệ thống Quản lý Hành chính Công Thông minh — Hackaithon 2026",
    )

    # ─── CORS middleware ────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ─── Custom middleware ──────────────────────────────────────────
    from src.middleware.logging_middleware import LoggingMiddleware
    from src.middleware.error_handler import setup_error_handlers

    setup_error_handlers(app)
    app.add_middleware(LoggingMiddleware)

    # ─── AI routers (Round 4) ──────────────────────────────────────
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

    # ─── Business routers (Round 2) ────────────────────────────────
    from src.api.auth import router as auth_router
    from src.api.ho_so import router as ho_so_router
    from src.api.lich_hen import router as lich_hen_router
    from src.api.thong_bao import router as thong_bao_router

    app.include_router(auth_router)
    app.include_router(ho_so_router)
    app.include_router(lich_hen_router)
    app.include_router(thong_bao_router)

    logger.info("GovOne app created — all routers registered")
    return app


app = create_app()


@app.get("/api/health")
async def health_check():
    """Simple health check."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
