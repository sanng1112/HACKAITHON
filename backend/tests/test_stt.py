"""
Unit tests cho STT pipeline.
"""
from unittest.mock import MagicMock, patch

import pytest


class TestSTTModel:
    @patch("backend.src.ai.models.stt_model.VNPT_API_KEY", "")
    @patch("whisper.load_model")
    def test_load_whisper(self, mock_load):
        mock_load.return_value = MagicMock()
        from backend.src.ai.models.stt_model import STTModel
        model = STTModel()
        model.load()
        assert model._is_loaded

    @patch("backend.src.ai.models.stt_model.VNPT_API_KEY", "")
    @patch("whisper.load_model")
    def test_predict_returns_text(self, mock_load):
        mock_whisper = MagicMock()
        mock_whisper.transcribe.return_value = {
            "text": "Tôi muốn đăng ký hộ khẩu",
            "language": "vi",
        }
        mock_load.return_value = mock_whisper

        from backend.src.ai.models.stt_model import STTModel
        import tempfile, os
        model = STTModel()
        model.load()

        # Tạo file wav tạm rỗng để test
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(b"\x00" * 100)
            tmp_path = f.name

        try:
            result = model.predict(tmp_path)
            assert result["text"] == "Tôi muốn đăng ký hộ khẩu"
            assert result["source"] == "whisper"
        finally:
            os.unlink(tmp_path)


class TestAudioUtils:
    def test_validate_audio_size_ok(self):
        from backend.src.ai.utils.audio_utils import validate_audio_size
        # 1MB — OK
        validate_audio_size(b"\x00" * 1024 * 1024, max_mb=25)

    def test_validate_audio_size_too_large(self):
        from backend.src.ai.utils.audio_utils import validate_audio_size
        with pytest.raises(ValueError, match="quá lớn"):
            validate_audio_size(b"\x00" * 30 * 1024 * 1024, max_mb=25)

    def test_get_audio_format_wav(self):
        from backend.src.ai.utils.audio_utils import get_audio_format
        # WAV magic bytes
        assert get_audio_format(b"RIFF....WAVE") == "wav"

    def test_get_audio_format_mp3(self):
        from backend.src.ai.utils.audio_utils import get_audio_format
        assert get_audio_format(b"ID3\x03\x00") == "mp3"
