"""
OCR API Router — endpoints nhận ảnh và trả kết quả OCR.
"""
import base64
import logging
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.src.ai.config.settings import ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE_MB
from backend.src.ai.services.ocr_service import process_batch, process_image

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai/ocr", tags=["OCR"])


def _validate_image(file: UploadFile) -> None:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            400,
            f"Định dạng ảnh không hợp lệ: {file.content_type}. "
            f"Chấp nhận: {', '.join(ALLOWED_IMAGE_TYPES)}",
        )


@router.post(
    "",
    summary="OCR một ảnh giấy tờ",
    response_description="Text và thông tin có cấu trúc từ ảnh",
)
async def ocr_single(
    file: UploadFile = File(..., description="Ảnh giấy tờ (CCCD, CMND, ...)"),
    aggressive: bool = Form(False, description="Dùng tiền xử lý mạnh hơn cho ảnh cũ/mờ"),
):
    """
    Nhận dạng văn bản từ ảnh giấy tờ tiếng Việt.

    - Hỗ trợ: CCCD, CMND, bằng lái, giấy khai sinh, hộ chiếu
    - Tự động phân loại loại giấy tờ
    - Trích xuất thông tin có cấu trúc (họ tên, ngày sinh, số CCCD...)
    """
    _validate_image(file)
    image_bytes = await file.read()

    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        raise HTTPException(
            400,
            f"Ảnh quá lớn: {size_mb:.1f}MB (tối đa {MAX_IMAGE_SIZE_MB}MB)",
        )

    try:
        result = await process_image(image_bytes, aggressive_preprocess=aggressive)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"OCR API lỗi: {e}")
        raise HTTPException(500, f"Lỗi xử lý OCR: {str(e)}")


@router.post(
    "/batch",
    summary="OCR nhiều ảnh cùng lúc",
)
async def ocr_batch(
    files: list[UploadFile] = File(..., description="Danh sách ảnh (tối đa 10)"),
):
    """OCR batch — xử lý nhiều ảnh trong một request."""
    if len(files) > 10:
        raise HTTPException(400, "Tối đa 10 ảnh mỗi lần.")

    images = []
    for f in files:
        _validate_image(f)
        images.append(await f.read())

    try:
        results = await process_batch(images)
        return {"success": True, "data": results, "total": len(results)}
    except Exception as e:
        logger.error(f"OCR batch API lỗi: {e}")
        raise HTTPException(500, f"Lỗi xử lý batch OCR: {str(e)}")


@router.post(
    "/async",
    summary="OCR bất đồng bộ (trả về task ID)",
)
async def ocr_async(
    file: UploadFile = File(...),
    aggressive: bool = Form(False),
):
    """
    Submit task OCR vào Celery queue.
    Client dùng GET /api/ai/task/{task_id} để kiểm tra kết quả.
    """
    _validate_image(file)
    image_bytes = await file.read()
    image_b64 = base64.b64encode(image_bytes).decode()

    from backend.src.ai.tasks.ocr_tasks import task_ocr_image
    task = task_ocr_image.delay(image_b64, aggressive)

    return {
        "success": True,
        "task_id": task.id,
        "status": "queued",
        "poll_url": f"/api/ai/task/{task.id}",
    }
