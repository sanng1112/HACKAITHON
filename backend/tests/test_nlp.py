"""
Unit tests cho NLP pipeline.
"""
from unittest.mock import MagicMock, patch

import pytest


class TestNLPModel:
    @patch("backend.src.ai.models.nlp_model.VNPT_API_KEY", "")
    def test_load_without_transformers(self):
        """Nếu không có transformers, model vẫn load được (dùng underthesea/regex)."""
        with patch.dict("sys.modules", {"underthesea": MagicMock(), "transformers": None}):
            from importlib import reload
            import backend.src.ai.models.nlp_model as m
            reload(m)
            model = m.NLPModel()
            # Không raise exception

    @patch("backend.src.ai.models.nlp_model.VNPT_API_KEY", "")
    def test_classify_keyword_matching(self):
        """Phân loại bằng keyword khi không có model transformer."""
        from backend.src.ai.models.nlp_model import NLPModel
        model = NLPModel()
        # Gán _model rỗng để test keyword matching
        model._model = {}
        model._is_loaded = True

        label, score = model._classify_procedure("Tôi muốn làm thủ tục đăng ký khai sinh")
        assert label == "đăng ký khai sinh"
        assert score >= 0.8

    @patch("backend.src.ai.models.nlp_model.VNPT_API_KEY", "")
    def test_regex_ner_id_number(self):
        from backend.src.ai.models.nlp_model import NLPModel
        model = NLPModel()
        model._model = {}
        model._is_loaded = True

        entities = model._regex_ner("Số CCCD 001099012345 ngày cấp 01/01/2022")
        labels = [e["label"] for e in entities]
        assert "ID_NUMBER" in labels
        assert "DATE" in labels


class TestNLPService:
    @pytest.mark.asyncio
    async def test_analyze_empty_text(self):
        from backend.src.ai.services.nlp_service import analyze_text
        result = await analyze_text("")
        assert result["procedure_class"] == "khác"
        assert result["entities"] == []

    @pytest.mark.asyncio
    async def test_extract_priority_high(self):
        from backend.src.ai.services.nlp_service import extract_priority
        assert await extract_priority("Đây là vấn đề khẩn cần giải quyết") == "high"

    @pytest.mark.asyncio
    async def test_extract_priority_low(self):
        from backend.src.ai.services.nlp_service import extract_priority
        assert await extract_priority("Tôi muốn hỏi thông tin về thủ tục") == "low"

    @pytest.mark.asyncio
    async def test_extract_priority_medium(self):
        from backend.src.ai.services.nlp_service import extract_priority
        assert await extract_priority("Tôi cần đăng ký khai sinh cho con") == "medium"
