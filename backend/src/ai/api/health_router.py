"""
Health Router — kiểm tra trạng thái models và polling task.
"""
import logging

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["Health & Tasks"])


@router.get("/health", summary="Kiểm tra trạng thái tất cả AI models")
async def health_check():
    """
    Trả về trạng thái load + metrics của OCR, STT, NLP models.
    Dùng cho monitoring và readiness probe của k8s/Docker.
    """
    from backend.src.ai.services.ocr_service import get_health as ocr_health
    from backend.src.ai.services.stt_service import get_health as stt_health
    from backend.src.ai.services.nlp_service import get_health as nlp_health

    statuses = {
        "ocr": ocr_health(),
        "stt": stt_health(),
        "nlp": nlp_health(),
    }

    # Overall status: ready nếu ít nhất 1 model loaded
    any_ready = any(s.get("status") == "ready" for s in statuses.values())

    return {
        "status": "ok" if any_ready else "degraded",
        "models": statuses,
    }


@router.post("/reload", summary="Reload tất cả models (khi cập nhật weights)")
async def reload_models(model: str = "all"):
    """
    Reload model theo tên: 'ocr', 'stt', 'nlp', hoặc 'all'.
    """
    reloaded = []
    errors = []

    def try_reload(name: str, get_model_fn):
        try:
            m = get_model_fn()
            if m._is_loaded:
                m.reload()
                reloaded.append(name)
            else:
                reloaded.append(f"{name} (skipped — not loaded yet)")
        except Exception as e:
            errors.append(f"{name}: {str(e)}")

    if model in ("all", "ocr"):
        from backend.src.ai.services.ocr_service import get_ocr_model
        try_reload("ocr", get_ocr_model)

    if model in ("all", "stt"):
        from backend.src.ai.services.stt_service import get_stt_model
        try_reload("stt", get_stt_model)

    if model in ("all", "nlp"):
        from backend.src.ai.services.nlp_service import get_nlp_model
        try_reload("nlp", get_nlp_model)

    return {
        "reloaded": reloaded,
        "errors": errors,
    }


@router.get("/task/{task_id}", summary="Kiểm tra trạng thái Celery task")
async def get_task_status(task_id: str):
    """
    Polling endpoint cho async tasks (OCR/STT/NLP).

    Trả về:
    - `status`: PENDING | STARTED | SUCCESS | FAILURE | RETRY
    - `result`: kết quả nếu SUCCESS
    - `error`: thông báo lỗi nếu FAILURE
    - `progress`: 0-100 nếu task hỗ trợ progress tracking
    """
    try:
        from celery.result import AsyncResult
        from backend.src.ai.tasks.celery_app import celery_app

        result = AsyncResult(task_id, app=celery_app)
        status = result.status

        response = {
            "task_id": task_id,
            "status": status,
            "result": None,
            "error": None,
            "progress": None,
        }

        if status == "SUCCESS":
            response["result"] = result.result
            response["progress"] = 100
        elif status == "FAILURE":
            response["error"] = str(result.result)
        elif status == "STARTED":
            # Nếu task có cập nhật progress qua update_state
            meta = result.info or {}
            response["progress"] = meta.get("progress", 0)

        return {"success": True, "data": response}

    except Exception as e:
        logger.error(f"Task status API lỗi: {e}")
        raise HTTPException(500, f"Không lấy được task status: {str(e)}")
