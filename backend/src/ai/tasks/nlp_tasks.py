"""
Celery tasks cho NLP.
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
    name="nlp.analyze",
    max_retries=3,
    default_retry_delay=5,
)
def task_analyze_text(self, text: str) -> dict:
    """Task NLP phân tích text."""
    try:
        from src.ai.services.nlp_service import analyze_text
        return _run_async(analyze_text(text))
    except Exception as exc:
        logger.error(f"NLP analyze task lỗi: {exc}")
        raise self.retry(exc=exc)


@celery_app.task(
    bind=True,
    name="nlp.classify",
    max_retries=3,
    default_retry_delay=5,
)
def task_classify_procedure(self, text: str) -> dict:
    """Task NLP phân loại thủ tục."""
    try:
        from src.ai.services.nlp_service import classify_procedure
        return _run_async(classify_procedure(text))
    except Exception as exc:
        logger.error(f"NLP classify task lỗi: {exc}")
        raise self.retry(exc=exc)
