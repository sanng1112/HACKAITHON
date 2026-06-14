"""
STT API Router — endpoints nhận audio và trả văn bản.
"""
import base64
import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from src.ai.config.settings import ALLOWED_AUDIO_TYPES, MAX_AUDIO_SIZE_MB
from src.ai.services.stt_service import transcribe_audio, transcribe_and_map_to_form

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai/stt", tags=["STT"])


def _validate_audio(file: UploadFile) -> None:
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            400,
            f"Định dạng audio không hợp lệ: {file.content_type}. "
            f"Chấp nhận: {', '.join(ALLOWED_AUDIO_TYPES)}",
        )


@router.post(
    "",
    summary="Chuyển giọng nói -> văn bản",
)
async def stt_transcribe(
    file: UploadFile = File(..., description="File audio (.wav, .mp3, .m4a)"),
):
    """
    Speech-to-Text tiếng Việt.

    - Hỗ trợ: WAV, MP3, M4A
    - Tối ưu cho tiếng Việt (Whisper small hoặc VNPT SmartVoice)
    - Tối đa 25MB
    """
    _validate_audio(file)
    audio_bytes = await file.read()

    size_mb = len(audio_bytes) / (1024 * 1024)
    if size_mb > MAX_AUDIO_SIZE_MB:
        raise HTTPException(400, f"File audio quá lớn: {size_mb:.1f}MB")

    try:
        result = await transcribe_audio(audio_bytes)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"STT API lỗi: {e}")
        raise HTTPException(500, f"Lỗi xử lý STT: {str(e)}")


@router.post(
    "/form-fill",
    summary="STT + tự động map vào form fields",
)
async def stt_form_fill(
    file: UploadFile = File(...),
    form_fields: str = Form(
        "full_name,date_of_birth,hometown,phone",
        description="Danh sách field cần điền, cách nhau bởi dấu phẩy",
    ),
):
    """
    STT rồi tự động trích xuất thông tin điền vào form.
    Phù hợp cho kiosk voice-first ở UBND.
    """
    _validate_audio(file)
    audio_bytes = await file.read()
    fields = [f.strip() for f in form_fields.split(",") if f.strip()]

    try:
        result = await transcribe_and_map_to_form(audio_bytes, fields)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"STT form-fill API lỗi: {e}")
        raise HTTPException(500, f"Lỗi xử lý: {str(e)}")


@router.post(
    "/async",
    summary="STT bất đồng bộ (trả về task ID)",
)
async def stt_async(file: UploadFile = File(...)):
    """Submit task STT vào Celery queue."""
    _validate_audio(file)
    audio_bytes = await file.read()
    audio_b64 = base64.b64encode(audio_bytes).decode()

    from src.ai.tasks.stt_tasks import task_transcribe
    task = task_transcribe.delay(audio_b64)

    return {
        "success": True,
        "task_id": task.id,
        "status": "queued",
        "poll_url": f"/api/ai/task/{task.id}",
    }
