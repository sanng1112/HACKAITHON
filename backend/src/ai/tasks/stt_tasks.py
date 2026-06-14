"""
Celery tasks cho STT.
"""
import asyncio
import logging

from src.ai.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


def _run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(
    bind=True,
    name="stt.transcribe",
    max_retries=3,
    default_retry_delay=10,
)
def task_transcribe(self, audio_b64: str) -> dict:
    """
    Task STT — transcribe file audio.

    Args:
        audio_b64: file audio encode base64

    Returns: {"text": str, "language": str, "confidence": float, "source": str}
    """
    import base64
    try:
        audio_bytes = base64.b64decode(audio_b64)
        from src.ai.services.stt_service import transcribe_audio
        return _run_async(transcribe_audio(audio_bytes))
    except Exception as exc:
        logger.error(f"STT task lỗi: {exc}")
        raise self.retry(exc=exc)


@celery_app.task(
    bind=True,
    name="stt.transcribe_and_map",
    max_retries=3,
    default_retry_delay=10,
)
def task_transcribe_and_map(self, audio_b64: str, form_fields: list) -> dict:
    """Task STT + map vào form fields."""
    import base64
    try:
        audio_bytes = base64.b64decode(audio_b64)
        from src.ai.services.stt_service import transcribe_and_map_to_form
        return _run_async(transcribe_and_map_to_form(audio_bytes, form_fields))
    except Exception as exc:
        logger.error(f"STT map task lỗi: {exc}")
        raise self.retry(exc=exc)
