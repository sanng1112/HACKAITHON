"""
Auto-fill API Router — upload ảnh CCCD/CMND -> điền form tự động.
"""
import base64
import logging
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from src.ai.config.settings import ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE_MB
from src.ai.services.auto_fill_service import auto_fill_from_image, validate_form_data

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai/auto-fill", tags=["Auto Fill"])


@router.post(
    "",
    summary="Upload ảnh CCCD/CMND -> tự động điền form",
)
async def auto_fill(
    file: UploadFile = File(..., description="Ảnh CCCD hoặc CMND"),
    target_form: Optional[str] = Form(None, description="Tên form đích"),
):
    """
    Pipeline đầy đủ:
    1. OCR ảnh giấy tờ
    2. NLP trích xuất thông tin
    3. Map vào các field form hành chính
    4. Trả kết quả + flag cần xác nhận nếu confidence thấp

    Trả về `needs_review: true` khi AI không chắc — user nên kiểm tra lại.
    """
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(400, f"Định dạng ảnh không hỗ trợ: {file.content_type}")

    image_bytes = await file.read()
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        raise HTTPException(400, f"Ảnh quá lớn: {size_mb:.1f}MB")

    try:
        result = await auto_fill_from_image(image_bytes, target_form=target_form)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Auto-fill API lỗi: {e}")
        raise HTTPException(500, f"Lỗi xử lý: {str(e)}")


class FormValidationRequest(BaseModel):
    form_data: dict


@router.post("/validate", summary="Kiểm tra tính hợp lệ của form data")
async def validate_form(body: FormValidationRequest):
    """Validate form data trước khi submit — số CCCD, ngày sinh, SĐT..."""
    try:
        result = await validate_form_data(body.form_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/async", summary="Auto-fill bất đồng bộ")
async def auto_fill_async(
    file: UploadFile = File(...),
    target_form: Optional[str] = Form(None),
):
    """Submit auto-fill vào Celery queue."""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(400, "Định dạng ảnh không hỗ trợ")

    image_bytes = await file.read()
    image_b64 = base64.b64encode(image_bytes).decode()

    from src.ai.tasks.ocr_tasks import task_auto_fill
    task = task_auto_fill.delay(image_b64, target_form)

    return {
        "success": True,
        "task_id": task.id,
        "status": "queued",
        "poll_url": f"/api/ai/task/{task.id}",
    }
