"""
Tiện ích xử lý ảnh — tiền xử lý trước khi đưa vào OCR.
"""
import io
import logging

import cv2
import numpy as np
from PIL import Image, ImageEnhance

logger = logging.getLogger(__name__)

# Kích thước tối đa (pixel) để tránh OOM
MAX_DIMENSION = 4096


def bytes_to_cv2(image_bytes: bytes) -> np.ndarray:
    """Chuyển raw bytes → numpy array (BGR)."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Không decode được ảnh — định dạng không hợp lệ.")
    return img


def cv2_to_bytes(img: np.ndarray, ext: str = ".jpg") -> bytes:
    """Chuyển numpy array → bytes."""
    ok, buf = cv2.imencode(ext, img)
    if not ok:
        raise RuntimeError("Không encode được ảnh.")
    return buf.tobytes()


def resize_if_needed(img: np.ndarray) -> np.ndarray:
    """Thu nhỏ ảnh nếu quá lớn, giữ tỉ lệ."""
    h, w = img.shape[:2]
    if max(h, w) <= MAX_DIMENSION:
        return img
    scale = MAX_DIMENSION / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)


def to_grayscale(img: np.ndarray) -> np.ndarray:
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def denoise(img: np.ndarray) -> np.ndarray:
    """Khử nhiễu nhẹ — phù hợp với ảnh scan/chụp điện thoại."""
    if len(img.shape) == 2:
        return cv2.fastNlMeansDenoising(img, h=10)
    return cv2.fastNlMeansDenoisingColored(img, h=10)


def binarize(img: np.ndarray) -> np.ndarray:
    """Adaptive threshold — hiệu quả với ảnh bị đổ bóng."""
    gray = to_grayscale(img)
    return cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2,
    )


def deskew(img: np.ndarray) -> np.ndarray:
    """Tự động chỉnh nghiêng (deskew) cho ảnh bị lệch góc nhỏ."""
    gray = to_grayscale(img)
    coords = np.column_stack(np.where(gray < 128))
    if len(coords) == 0:
        return img
    angle = cv2.minAreaRect(coords)[-1]
    # minAreaRect trả góc từ -90 đến 0
    if angle < -45:
        angle = 90 + angle
    if abs(angle) < 0.5:
        return img  # Không cần xoay
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        img, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )
    return rotated


def enhance_contrast(image_bytes: bytes) -> bytes:
    """Tăng độ tương phản bằng PIL — hữu ích với ảnh mờ/cũ."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = ImageEnhance.Sharpness(img).enhance(1.3)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def preprocess_for_ocr(image_bytes: bytes, aggressive: bool = False) -> bytes:
    """
    Pipeline tiền xử lý chuẩn trước khi đưa vào OCR.

    aggressive=False: resize + denoise nhẹ (phù hợp ảnh chụp điện thoại)
    aggressive=True:  + deskew + binarize (phù hợp ảnh scan cũ)
    """
    try:
        img = bytes_to_cv2(image_bytes)
        img = resize_if_needed(img)
        img = denoise(img)

        if aggressive:
            img = deskew(img)
            img = binarize(img)

        return cv2_to_bytes(img)
    except Exception as e:
        logger.warning(f"Tiền xử lý ảnh thất bại, dùng ảnh gốc: {e}")
        return image_bytes


def classify_document_type(text: str) -> str:
    """
    Phân loại loại giấy tờ dựa trên từ khóa trong text OCR.
    Đơn giản nhưng đủ chính xác cho CCCD/CMND/bằng lái.
    """
    text_lower = text.lower()
    if any(k in text_lower for k in ["căn cước công dân", "cccd", "012"]):
        return "CCCD"
    if any(k in text_lower for k in ["chứng minh nhân dân", "cmnd"]):
        return "CMND"
    if any(k in text_lower for k in ["giấy phép lái xe", "bằng lái"]):
        return "BANG_LAI"
    if any(k in text_lower for k in ["hộ chiếu", "passport"]):
        return "HO_CHIEU"
    if any(k in text_lower for k in ["giấy khai sinh", "khai sinh"]):
        return "KHAI_SINH"
    if any(k in text_lower for k in ["giấy đăng ký", "đăng ký xe"]):
        return "DANG_KY_XE"
    return "UNKNOWN"
