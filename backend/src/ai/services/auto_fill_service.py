"""
Auto-fill Service — pipeline kết hợp OCR + NLP để tự động điền form hành chính.

Flow:
  Upload ảnh CCCD/CMND
    → OCR trích xuất text
    → NLP phân tích thực thể
    → Map vào form fields
    → Trả kết quả + confidence để user xác nhận
"""
import logging
from typing import Optional

from backend.src.ai.services.nlp_service import analyze_text
from backend.src.ai.services.ocr_service import process_image
from backend.src.ai.utils.text_utils import calculate_confidence_score

logger = logging.getLogger(__name__)

# Mapping từ field nội bộ → tên field trong form hành chính
FORM_FIELD_MAP = {
    "id_number":     "so_cmnd_cccd",
    "full_name":     "ho_va_ten",
    "date_of_birth": "ngay_sinh",
    "hometown":      "que_quan",
    "issue_date":    "ngay_cap",
    "issue_place":   "noi_cap",
    "phone":         "so_dien_thoai",
}


async def auto_fill_from_image(
    image_bytes: bytes,
    target_form: Optional[str] = None,
) -> dict:
    """
    Pipeline auto-fill chính.

    Args:
        image_bytes: ảnh giấy tờ (CCCD, CMND, ...)
        target_form: tên form đích (ví dụ "khai_sinh", "dang_ky_ho_khau")
                     None → dùng mapping mặc định

    Returns:
        {
            "form_data": dict,          # các field đã điền
            "uncertain_fields": list,   # field cần user xác nhận
            "document_type": str,
            "raw_text": str,
            "confidence": float,
            "needs_review": bool        # True nếu confidence < 0.6
        }
    """
    # Bước 1: OCR
    ocr_result = await process_image(image_bytes)
    raw_text = ocr_result.get("raw_text", "")
    ocr_fields = ocr_result.get("fields", {})
    doc_type = ocr_result.get("document_type", "UNKNOWN")

    # Bước 2: NLP bổ sung (lấy thêm entities nếu OCR chưa đủ)
    nlp_result = await analyze_text(raw_text)
    nlp_entities = nlp_result.get("entities", [])

    # Bổ sung entities từ NLP vào ocr_fields nếu field còn None
    for entity in nlp_entities:
        label = entity.get("label", "")
        value = entity.get("text", "")
        if label == "PER" and ocr_fields.get("full_name") is None:
            ocr_fields["full_name"] = value
        elif label == "DATE" and ocr_fields.get("date_of_birth") is None:
            ocr_fields["date_of_birth"] = value
        elif label == "LOC" and ocr_fields.get("hometown") is None:
            ocr_fields["hometown"] = value

    # Bước 3: Map vào form fields
    form_data = {}
    uncertain_fields = []

    for internal_key, form_key in FORM_FIELD_MAP.items():
        value = ocr_fields.get(internal_key)
        if value:
            form_data[form_key] = value
        else:
            uncertain_fields.append(form_key)

    # Bước 4: Tính confidence tổng thể
    overall_confidence = calculate_confidence_score(ocr_fields)

    return {
        "form_data": form_data,
        "uncertain_fields": uncertain_fields,
        "document_type": doc_type,
        "raw_text": raw_text,
        "confidence": overall_confidence,
        "needs_review": overall_confidence < 0.6 or len(uncertain_fields) > 2,
        "procedure_suggestion": nlp_result.get("procedure_class"),
    }


async def validate_form_data(form_data: dict) -> dict:
    """
    Kiểm tra tính hợp lệ của form data trước khi submit.

    Returns:
        {
            "valid": bool,
            "errors": dict  # {field_name: error_message}
        }
    """
    import re
    errors = {}

    cccd = form_data.get("so_cmnd_cccd", "")
    if cccd and not re.match(r"^\d{9}$|^\d{12}$", cccd):
        errors["so_cmnd_cccd"] = "Số CMND/CCCD phải có 9 hoặc 12 chữ số"

    ngay_sinh = form_data.get("ngay_sinh", "")
    if ngay_sinh and not re.match(r"\d{1,2}[/-]\d{1,2}[/-]\d{4}", ngay_sinh):
        errors["ngay_sinh"] = "Ngày sinh không đúng định dạng (dd/mm/yyyy)"

    sdt = form_data.get("so_dien_thoai", "")
    if sdt and not re.match(r"^0[3-9]\d{8}$", sdt):
        errors["so_dien_thoai"] = "Số điện thoại không hợp lệ"

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }
