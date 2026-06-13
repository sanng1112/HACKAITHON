"""
Celery tasks cho OCR — xử lý bất đồng bộ, không block API.
"""
import asyncio
import logging

from backend.src.ai.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


def _run_async(coro):
    """Helper chạy async function trong Celery (sync) context."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(
    bind=True,
    name="ocr.process_image",
    max_retries=3,
    default_retry_delay=10,
)
def task_ocr_image(self, image_b64: str, aggressive: bool = False) -> dict:
    """
    Task OCR một ảnh đơn.

    Args:
        image_b64: ảnh encode base64
        aggressive: có dùng tiền xử lý mạnh không

    Returns: dict kết quả OCR
    """
    import base64
    try:
        image_bytes = base64.b64decode(image_b64)
        from backend.src.ai.services.ocr_service import process_image
        return _run_async(process_image(image_bytes, aggressive_preprocess=aggressive))
    except Exception as exc:
        logger.error(f"OCR task lỗi: {exc}")
        raise self.retry(exc=exc)


@celery_app.task(
    bind=True,
    name="ocr.process_batch",
    max_retries=2,
    default_retry_delay=15,
)
def task_ocr_batch(self, images_b64: list[str]) -> list[dict]:
    """
    Task OCR batch nhiều ảnh.

    Args:
        images_b64: list ảnh encode base64

    Returns: list kết quả OCR
    """
    import base64
    try:
        images = [base64.b64decode(b64) for b64 in images_b64]
        from backend.src.ai.services.ocr_service import process_batch
        return _run_async(process_batch(images))
    except Exception as exc:
        logger.error(f"OCR batch task lỗi: {exc}")
        raise self.retry(exc=exc)


@celery_app.task(
    bind=True,
    name="ocr.auto_fill",
    max_retries=3,
    default_retry_delay=10,
)
def task_auto_fill(self, image_b64: str, target_form: str = None) -> dict:
    """Task auto-fill form từ ảnh CCCD/CMND."""
    import base64
    try:
        image_bytes = base64.b64decode(image_b64)
        from backend.src.ai.services.auto_fill_service import auto_fill_from_image
        return _run_async(auto_fill_from_image(image_bytes, target_form=target_form))
    except Exception as exc:
        logger.error(f"Auto-fill task lỗi: {exc}")
        raise self.retry(exc=exc)
