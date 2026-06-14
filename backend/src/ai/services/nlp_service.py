"""
NLP Service — phân tích văn bản tiếng Việt cho hồ sơ hành chính.
"""
import logging

from src.ai.models.nlp_model import NLPModel

logger = logging.getLogger(__name__)

_nlp_model: NLPModel = None


def get_nlp_model() -> NLPModel:
    global _nlp_model
    if _nlp_model is None:
        _nlp_model = NLPModel()
    return _nlp_model


async def analyze_text(text: str) -> dict:
    """
    Phân tích văn bản: NER + phân loại thủ tục.

    Returns:
        {
            "entities": list,
            "procedure_class": str,
            "procedure_score": float,
            "source": str
        }
    """
    if not text or not text.strip():
        return {
            "entities": [],
            "procedure_class": "khác",
            "procedure_score": 0.0,
            "source": "empty_input",
        }
    model = get_nlp_model()
    return model.predict(text)


async def classify_procedure(text: str) -> dict:
    """Chỉ trả về phân loại thủ tục, không kèm entities."""
    result = await analyze_text(text)
    return {
        "procedure_class": result["procedure_class"],
        "procedure_score": result["procedure_score"],
        "source": result["source"],
    }


async def extract_priority(text: str) -> str:
    """
    Đánh giá mức độ ưu tiên của hồ sơ dựa trên nội dung.
    Returns: "high" | "medium" | "low"
    """
    text_lower = text.lower()
    high_keywords = ["khẩn", "gấp", "cấp cứu", "tai nạn", "khiếu nại", "tố cáo"]
    low_keywords = ["thông tin", "hỏi", "tra cứu"]

    if any(k in text_lower for k in high_keywords):
        return "high"
    if any(k in text_lower for k in low_keywords):
        return "low"
    return "medium"


def get_health() -> dict:
    return get_nlp_model().health()
