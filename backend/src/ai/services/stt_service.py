"""
STT Service — pipeline chuyển audio → văn bản tiếng Việt.
"""
import logging

from backend.src.ai.models.stt_model import STTModel
from backend.src.ai.utils.audio_utils import prepare_audio, validate_audio_size
from backend.src.ai.config.settings import MAX_AUDIO_SIZE_MB

logger = logging.getLogger(__name__)

_stt_model: STTModel = None


def get_stt_model() -> STTModel:
    global _stt_model
    if _stt_model is None:
        _stt_model = STTModel()
    return _stt_model


async def transcribe_audio(audio_bytes: bytes) -> dict:
    """
    Pipeline STT đầy đủ:
    1. Validate kích thước
    2. Convert sang WAV 16kHz nếu cần
    3. Transcribe

    Returns:
        {
            "text": str,
            "language": str,
            "confidence": float | None,
            "source": str,
            "word_count": int
        }
    """
    validate_audio_size(audio_bytes, max_mb=MAX_AUDIO_SIZE_MB)

    # Chuẩn bị audio (convert nếu cần)
    prepared = prepare_audio(audio_bytes)

    model = get_stt_model()
    result = model.predict(prepared)

    text = result.get("text", "")
    result["word_count"] = len(text.split()) if text else 0

    return result


async def transcribe_and_map_to_form(audio_bytes: bytes, form_fields: list[str]) -> dict:
    """
    STT + tự động map text → form fields bằng keyword matching đơn giản.
    Dùng cho kiosk voice-first.

    Args:
        audio_bytes: file âm thanh
        form_fields: danh sách tên field cần điền, ví dụ ["full_name", "address"]

    Returns:
        {
            "text": str,
            "mapped_fields": dict  # {field_name: extracted_value}
        }
    """
    transcription = await transcribe_audio(audio_bytes)
    text = transcription.get("text", "")

    # Map đơn giản — thực tế nên dùng NLP service
    from backend.src.ai.utils.text_utils import extract_structured_fields
    all_fields = extract_structured_fields(text)

    mapped = {field: all_fields.get(field) for field in form_fields}

    return {
        "text": text,
        "mapped_fields": mapped,
        "source": transcription.get("source"),
    }


def get_health() -> dict:
    return get_stt_model().health()
