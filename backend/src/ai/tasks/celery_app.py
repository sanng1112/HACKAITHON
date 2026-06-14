"""
Celery app — cấu hình async task queue cho GovOne AI layer.
"""
from celery import Celery

from src.ai.config.settings import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
    CELERY_TASK_TIMEOUT,
)

celery_app = Celery(
    "govone_ai",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        "backend.src.ai.tasks.ocr_tasks",
        "backend.src.ai.tasks.stt_tasks",
        "backend.src.ai.tasks.nlp_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Ho_Chi_Minh",
    enable_utc=True,

    # Timeout mặc định cho mỗi task
    task_soft_time_limit=CELERY_TASK_TIMEOUT,
    task_time_limit=CELERY_TASK_TIMEOUT + 60,

    # Retry khi task thất bại
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_max_retries=3,
    task_default_retry_delay=10,  # giây

    # Routing: mỗi loại task vào queue riêng
    task_routes={
        "backend.src.ai.tasks.ocr_tasks.*": {"queue": "ocr"},
        "backend.src.ai.tasks.stt_tasks.*": {"queue": "stt"},
        "backend.src.ai.tasks.nlp_tasks.*": {"queue": "nlp"},
    },

    # Worker prefetch — quan trọng khi task nặng (GPU)
    worker_prefetch_multiplier=1,
    worker_concurrency=2,
)
