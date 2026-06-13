"""
Cấu hình toàn bộ AI layer.
Đọc từ biến môi trường hoặc dùng giá trị mặc định.
"""
import os
from pathlib import Path

# Thư mục gốc của project
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# ─── Model Cache ──────────────────────────────────────────────
MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", str(BASE_DIR / ".model_cache"))
Path(MODEL_CACHE_DIR).mkdir(parents=True, exist_ok=True)

# ─── OCR ──────────────────────────────────────────────────────
OCR_LANGUAGES = ["vi", "en"]          # Tiếng Việt ưu tiên
OCR_GPU = os.getenv("OCR_GPU", "false").lower() == "true"
OCR_CONFIDENCE_THRESHOLD = float(os.getenv("OCR_CONFIDENCE_THRESHOLD", "0.5"))

# ─── STT (Whisper) ────────────────────────────────────────────
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "small")   # tiny/base/small/medium
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "vi")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")             # cpu / cuda

# ─── NLP (PhoBERT / Underthesea) ──────────────────────────────
NLP_MODEL_NAME = os.getenv("NLP_MODEL_NAME", "vinai/phobert-base")
NLP_DEVICE = os.getenv("NLP_DEVICE", "cpu")
NLP_MAX_LENGTH = int(os.getenv("NLP_MAX_LENGTH", "256"))

# ─── Redis / Celery ───────────────────────────────────────────
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
CELERY_TASK_TIMEOUT = int(os.getenv("CELERY_TASK_TIMEOUT", "300"))  # giây

# ─── VNPT API (ưu tiên dùng nếu có key) ──────────────────────
VNPT_API_KEY = os.getenv("VNPT_API_KEY", "")
VNPT_OCR_URL = os.getenv("VNPT_OCR_URL", "https://api.vnpt.vn/ai/ocr")
VNPT_STT_URL = os.getenv("VNPT_STT_URL", "https://api.vnpt.vn/ai/stt")
VNPT_NLP_URL = os.getenv("VNPT_NLP_URL", "https://api.vnpt.vn/ai/nlp")
VNPT_EKYC_URL = os.getenv("VNPT_EKYC_URL", "https://api.vnpt.vn/ai/ekyc")

# ─── Upload / Temp files ──────────────────────────────────────
UPLOAD_DIR = os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads"))
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
MAX_IMAGE_SIZE_MB = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
MAX_AUDIO_SIZE_MB = int(os.getenv("MAX_AUDIO_SIZE_MB", "25"))
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/tiff"}
ALLOWED_AUDIO_TYPES = {"audio/wav", "audio/mpeg", "audio/mp4", "audio/x-m4a"}

# ─── Cache kết quả (Redis TTL) ────────────────────────────────
RESULT_CACHE_TTL = int(os.getenv("RESULT_CACHE_TTL", "3600"))   # 1 giờ

# ─── Misc ─────────────────────────────────────────────────────
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
