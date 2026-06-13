"""
Tiện ích xử lý audio — chuẩn bị file âm thanh trước khi đưa vào STT.
"""
import io
import logging
import os
import subprocess
import tempfile

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {".wav", ".mp3", ".m4a", ".ogg", ".flac", ".webm"}


def get_audio_format(audio_bytes: bytes) -> str:
    """Đoán format audio từ magic bytes."""
    if audio_bytes[:4] == b"RIFF":
        return "wav"
    if audio_bytes[:3] == b"ID3" or audio_bytes[:2] == b"\xff\xfb":
        return "mp3"
    if audio_bytes[4:8] == b"ftyp":
        return "m4a"
    if audio_bytes[:4] == b"OggS":
        return "ogg"
    return "wav"  # default


def convert_to_wav(audio_bytes: bytes, source_format: str = "mp3") -> bytes:
    """
    Convert audio sang WAV 16kHz mono — định dạng Whisper thích nhất.
    Cần ffmpeg cài trên hệ thống.
    """
    with tempfile.NamedTemporaryFile(
        suffix=f".{source_format}", delete=False
    ) as src:
        src.write(audio_bytes)
        src_path = src.name

    dst_path = src_path.replace(f".{source_format}", "_converted.wav")

    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", src_path,
            "-ar", "16000",       # 16kHz sample rate
            "-ac", "1",           # mono
            "-c:a", "pcm_s16le",  # 16-bit PCM
            dst_path,
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg lỗi: {result.stderr}")

        with open(dst_path, "rb") as f:
            return f.read()

    except FileNotFoundError:
        logger.warning("ffmpeg chưa cài — dùng pydub để convert.")
        return _convert_with_pydub(audio_bytes, source_format)

    finally:
        for p in [src_path, dst_path]:
            if os.path.exists(p):
                os.unlink(p)


def _convert_with_pydub(audio_bytes: bytes, source_format: str) -> bytes:
    """Fallback convert bằng pydub (không cần ffmpeg riêng)."""
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(
            io.BytesIO(audio_bytes), format=source_format
        )
        audio = audio.set_frame_rate(16000).set_channels(1)
        buf = io.BytesIO()
        audio.export(buf, format="wav")
        return buf.getvalue()
    except Exception as e:
        logger.error(f"pydub convert thất bại: {e}")
        return audio_bytes  # Trả về raw, để Whisper tự xử lý


def prepare_audio(audio_bytes: bytes) -> bytes:
    """
    Pipeline chuẩn bị audio:
    1. Detect format
    2. Convert sang WAV 16kHz mono nếu cần
    """
    fmt = get_audio_format(audio_bytes)
    if fmt == "wav":
        return audio_bytes  # WAV đã đúng định dạng
    logger.info(f"Convert audio từ {fmt} → wav")
    return convert_to_wav(audio_bytes, source_format=fmt)


def validate_audio_size(audio_bytes: bytes, max_mb: int = 25) -> None:
    """Kiểm tra kích thước file audio."""
    size_mb = len(audio_bytes) / (1024 * 1024)
    if size_mb > max_mb:
        raise ValueError(
            f"File audio quá lớn: {size_mb:.1f}MB (tối đa {max_mb}MB)"
        )
