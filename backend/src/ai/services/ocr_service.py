"""
OCR Service — pipeline hoàn chỉnh từ ảnh → text → thông tin có cấu trúc.
"""
import hashlib
import logging

from src.ai.models.ocr_model import OCRModel
from src.ai.utils.image_utils import (
    classify_document_type,
    preprocess_for_ocr,
)
from src.ai.utils.text_utils import (
    calculate_confidence_score,
    extract_structured_fields,
)

logger = logging.getLogger(__name__)

# Singleton model — load một lần, dùng nhiều lần
_ocr_model: OCRModel = None

# Cache đơn giản in-memory (production nên dùng Redis)
_result_cache: dict = {}


def get_ocr_model() -> OCRModel:
    global _ocr_model
    if _ocr_model is None:
        _ocr_model = OCRModel()
    return _ocr_model


def _cache_key(image_bytes: bytes) -> str:
    return hashlib.md5(image_bytes).hexdigest()


async def process_image(image_bytes: bytes, aggressive_preprocess: bool = False) -> dict:
    """
    Pipeline OCR đầy đủ:
    1. Kiểm tra cache
    2. Tiền xử lý ảnh
    3. OCR
    4. Trích xuất thông tin có cấu trúc
    5. Phân loại loại giấy tờ

    Returns:
        {
            "raw_text": str,
            "document_type": str,
            "fields": dict,
            "confidence": float,
            "blocks": list,
            "source": str,
            "cached": bool
        }
    """
    cache_key = _cache_key(image_bytes)
    if cache_key in _result_cache:
        logger.info(f"OCR cache hit: {cache_key[:8]}...")
        return {**_result_cache[cache_key], "cached": True}

    # Tiền xử lý
    processed = preprocess_for_ocr(image_bytes, aggressive=aggressive_preprocess)

    # Chạy OCR
    model = get_ocr_model()
    ocr_result = model.predict(processed)

    raw_text = ocr_result.get("raw_text", "")

    # Trích xuất fields có cấu trúc
    fields = extract_structured_fields(raw_text)
    confidence = calculate_confidence_score(fields)
    doc_type = classify_document_type(raw_text)

    result = {
        "raw_text": raw_text,
        "document_type": doc_type,
        "fields": fields,
        "confidence": confidence,
        "blocks": ocr_result.get("blocks", []),
        "source": ocr_result.get("source", "unknown"),
        "cached": False,
    }

    # Lưu cache nếu confidence đủ cao
    if confidence >= 0.3:
        _result_cache[cache_key] = {k: v for k, v in result.items() if k != "cached"}

    return result


async def process_batch(images: list[bytes]) -> list[dict]:
    """OCR nhiều ảnh cùng lúc."""
    results = []
    for i, img_bytes in enumerate(images):
        try:
            result = await process_image(img_bytes)
            result["index"] = i
            results.append(result)
        except Exception as e:
            logger.error(f"OCR batch lỗi ảnh {i}: {e}")
            results.append({"index": i, "error": str(e)})
    return results


def get_health() -> dict:
    model = get_ocr_model()
    return model.health()
