"""
NLP API Router.
"""
import logging

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field

from src.ai.services.nlp_service import analyze_text, classify_procedure, extract_priority

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai/nlp", tags=["NLP"])


class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Văn bản tiếng Việt")


@router.post("/analyze", summary="Phân tích đầy đủ: NER + phân loại thủ tục")
async def nlp_analyze(body: TextInput):
    """
    Phân tích văn bản:
    - Trích xuất thực thể (NER): họ tên, ngày tháng, số điện thoại...
    - Phân loại loại thủ tục hành chính
    """
    try:
        result = await analyze_text(body.text)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"NLP analyze API lỗi: {e}")
        raise HTTPException(500, str(e))


@router.post("/classify", summary="Phân loại loại thủ tục hành chính")
async def nlp_classify(body: TextInput):
    """Chỉ trả về phân loại thủ tục, nhanh hơn /analyze."""
    try:
        result = await classify_procedure(body.text)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"NLP classify API lỗi: {e}")
        raise HTTPException(500, str(e))


@router.post("/priority", summary="Đánh giá mức độ ưu tiên hồ sơ")
async def nlp_priority(body: TextInput):
    """Trả về mức ưu tiên: high / medium / low."""
    try:
        priority = await extract_priority(body.text)
        return {"success": True, "data": {"priority": priority}}
    except Exception as e:
        raise HTTPException(500, str(e))
