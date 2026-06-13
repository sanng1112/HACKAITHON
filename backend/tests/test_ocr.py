"""
Unit tests cho OCR pipeline.
"""
import base64
from unittest.mock import MagicMock, patch

import pytest


# ─── Test utils ──────────────────────────────────────────────


class TestTextUtils:
    def test_extract_id_number_cccd(self):
        from backend.src.ai.utils.text_utils import extract_id_number
        assert extract_id_number("Số CCCD: 001099012345") == "001099012345"

    def test_extract_id_number_cmnd(self):
        from backend.src.ai.utils.text_utils import extract_id_number
        assert extract_id_number("CMND: 012345678") == "012345678"

    def test_extract_id_number_not_found(self):
        from backend.src.ai.utils.text_utils import extract_id_number
        assert extract_id_number("Không có số nào") is None

    def test_extract_date_of_birth(self):
        from backend.src.ai.utils.text_utils import extract_date_of_birth
        result = extract_date_of_birth("Ngày sinh: 15/08/1990")
        assert result == "15/08/1990"

    def test_extract_full_name(self):
        from backend.src.ai.utils.text_utils import extract_full_name
        result = extract_full_name("Họ và tên: NGUYỄN VĂN AN")
        assert result == "NGUYỄN VĂN AN"

    def test_extract_structured_fields_complete(self):
        from backend.src.ai.utils.text_utils import extract_structured_fields
        text = """
        Họ và tên: TRẦN THỊ BÌNH
        Ngày sinh: 20/03/1985
        Số CCCD: 001085012345
        Quê quán: Hà Nội
        Ngày cấp: 10/01/2022
        Nơi cấp: Cục Cảnh sát QLHC về TTXH
        """
        fields = extract_structured_fields(text)
        assert fields["full_name"] == "TRẦN THỊ BÌNH"
        assert fields["date_of_birth"] == "20/03/1985"
        assert fields["id_number"] == "001085012345"

    def test_confidence_score_full(self):
        from backend.src.ai.utils.text_utils import calculate_confidence_score
        fields = {
            "id_number": "001099012345",
            "full_name": "NGUYỄN VĂN A",
            "date_of_birth": "01/01/1990",
            "hometown": "Hà Nội",
            "issue_date": "01/01/2022",
            "issue_place": "Cục CSQLHC",
            "phone": None,
        }
        score = calculate_confidence_score(fields)
        assert score == pytest.approx(6 / 7, rel=0.01)

    def test_confidence_score_empty(self):
        from backend.src.ai.utils.text_utils import calculate_confidence_score
        fields = {k: None for k in ["id_number", "full_name", "date_of_birth"]}
        assert calculate_confidence_score(fields) == 0.0


# ─── Test image utils ─────────────────────────────────────────


class TestImageUtils:
    def test_classify_document_type_cccd(self):
        from backend.src.ai.utils.image_utils import classify_document_type
        assert classify_document_type("CĂN CƯỚC CÔNG DÂN 001099012345") == "CCCD"

    def test_classify_document_type_cmnd(self):
        from backend.src.ai.utils.image_utils import classify_document_type
        assert classify_document_type("CHỨNG MINH NHÂN DÂN") == "CMND"

    def test_classify_document_type_unknown(self):
        from backend.src.ai.utils.image_utils import classify_document_type
        assert classify_document_type("văn bản ngẫu nhiên") == "UNKNOWN"


# ─── Test OCR model (mock) ────────────────────────────────────


class TestOCRModel:
    @patch("backend.src.ai.models.ocr_model.VNPT_API_KEY", "")
    @patch("easyocr.Reader")
    def test_load_easyocr(self, mock_reader):
        from backend.src.ai.models.ocr_model import OCRModel
        model = OCRModel()
        mock_reader.return_value = MagicMock()
        model.load()
        assert model._is_loaded

    def test_health_before_load(self):
        from backend.src.ai.models.ocr_model import OCRModel
        model = OCRModel()
        h = model.health()
        assert h["status"] == "not_loaded"

    @patch("backend.src.ai.models.ocr_model.VNPT_API_KEY", "")
    @patch("easyocr.Reader")
    def test_predict_returns_expected_keys(self, mock_reader):
        mock_instance = MagicMock()
        mock_instance.readtext.return_value = [
            ([[0, 0], [100, 0], [100, 30], [0, 30]], "NGUYỄN VĂN A", 0.95)
        ]
        mock_reader.return_value = mock_instance

        from backend.src.ai.models.ocr_model import OCRModel
        import numpy as np
        model = OCRModel()
        model.load()

        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        result = model.predict(dummy_image)

        assert "raw_text" in result
        assert "blocks" in result
        assert "source" in result
        assert result["source"] == "easyocr"


# ─── Test auto-fill service ───────────────────────────────────


class TestAutoFillService:
    @pytest.mark.asyncio
    async def test_validate_form_data_valid(self):
        from backend.src.ai.services.auto_fill_service import validate_form_data
        form = {
            "so_cmnd_cccd": "001099012345",
            "ngay_sinh": "15/08/1990",
            "so_dien_thoai": "0912345678",
        }
        result = await validate_form_data(form)
        assert result["valid"] is True
        assert result["errors"] == {}

    @pytest.mark.asyncio
    async def test_validate_form_data_invalid_cccd(self):
        from backend.src.ai.services.auto_fill_service import validate_form_data
        form = {"so_cmnd_cccd": "123"}  # Sai — không đủ 9 hoặc 12 số
        result = await validate_form_data(form)
        assert result["valid"] is False
        assert "so_cmnd_cccd" in result["errors"]

    @pytest.mark.asyncio
    async def test_validate_form_data_invalid_phone(self):
        from backend.src.ai.services.auto_fill_service import validate_form_data
        form = {"so_dien_thoai": "1234567890"}  # Không bắt đầu bằng 0[3-9]
        result = await validate_form_data(form)
        assert result["valid"] is False
