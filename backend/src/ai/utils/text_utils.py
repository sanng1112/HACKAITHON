"""
Tiện ích xử lý văn bản — trích xuất thông tin có cấu trúc từ OCR output.
"""
import re
import unicodedata
from typing import Optional


def normalize_text(text: str) -> str:
    """Chuẩn hóa unicode, xoá khoảng trắng thừa."""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_ocr_output(raw_text: str) -> str:
    """Làm sạch text từ OCR — xoá ký tự rác thường gặp."""
    # Xoá ký tự không in được (trừ newline/tab)
    text = re.sub(r"[^\x20-\x7E\u00C0-\u024F\u1E00-\u1EFF\n\t]", "", raw_text)
    text = re.sub(r"[|\\]{2,}", " ", text)  # || hoặc \\ hay xuất hiện trong OCR
    return normalize_text(text)


# ─── Trích xuất thông tin CCCD/CMND ──────────────────────────

def extract_id_number(text: str) -> Optional[str]:
    """Trích xuất số CCCD (12 số) hoặc CMND (9 số)."""
    # CCCD: 12 chữ số
    m = re.search(r"\b(\d{12})\b", text)
    if m:
        return m.group(1)
    # CMND: 9 chữ số
    m = re.search(r"\b(\d{9})\b", text)
    return m.group(1) if m else None


def extract_full_name(text: str) -> Optional[str]:
    """
    Trích xuất họ tên sau nhãn 'Họ và tên' hoặc 'Full name'.
    Ví dụ: 'Họ và tên: NGUYỄN VĂN A' → 'NGUYỄN VĂN A'
    """
    patterns = [
        r"(?:Họ và tên|Họ tên|Full name)\s*[:/]?\s*([A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯẠẮẶẴẨẮẶ\s]{5,50})",
        r"(?:Name)\s*[:/]?\s*([A-Z][a-zA-ZÀ-ỹ\s]{4,49})",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def extract_date_of_birth(text: str) -> Optional[str]:
    """Trích xuất ngày sinh. Trả về chuỗi raw như tìm thấy."""
    patterns = [
        r"(?:Ngày sinh|Date of birth|DOB)\s*[:/]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
        r"(?:Sinh ngày)\s*[:/]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
        r"\b(\d{2}/\d{2}/\d{4})\b",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def extract_hometown(text: str) -> Optional[str]:
    """Trích xuất quê quán / nơi thường trú."""
    patterns = [
        r"(?:Quê quán|Hometown|Place of origin)\s*[:/]?\s*(.{5,100}?)(?:\n|$)",
        r"(?:Nơi thường trú|Permanent residence)\s*[:/]?\s*(.{5,150}?)(?:\n|$)",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip().rstrip(".")
    return None


def extract_issue_date(text: str) -> Optional[str]:
    """Trích xuất ngày cấp."""
    m = re.search(
        r"(?:Ngày cấp|Date of issue|Cấp ngày)\s*[:/]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
        text, re.IGNORECASE
    )
    return m.group(1) if m else None


def extract_issue_place(text: str) -> Optional[str]:
    """Trích xuất nơi cấp."""
    m = re.search(
        r"(?:Nơi cấp|Place of issue)\s*[:/]?\s*(.{3,80}?)(?:\n|$)",
        text, re.IGNORECASE
    )
    return m.group(1).strip() if m else None


def extract_phone(text: str) -> Optional[str]:
    """Trích xuất số điện thoại Việt Nam."""
    m = re.search(r"\b(0[3-9]\d{8})\b", text)
    return m.group(1) if m else None


# ─── Wrapper tổng hợp ─────────────────────────────────────────

def extract_structured_fields(raw_text: str) -> dict:
    """
    Trích xuất toàn bộ trường thông tin từ OCR text của giấy tờ.
    Trả về dict với các field None nếu không tìm thấy.
    """
    text = clean_ocr_output(raw_text)
    return {
        "id_number": extract_id_number(text),
        "full_name": extract_full_name(text),
        "date_of_birth": extract_date_of_birth(text),
        "hometown": extract_hometown(text),
        "issue_date": extract_issue_date(text),
        "issue_place": extract_issue_place(text),
        "phone": extract_phone(text),
    }


def calculate_confidence_score(fields: dict) -> float:
    """
    Tính điểm confidence tổng thể của kết quả trích xuất.
    Dựa trên tỉ lệ field có giá trị / tổng số field.
    """
    total = len(fields)
    filled = sum(1 for v in fields.values() if v is not None)
    return round(filled / total, 2) if total > 0 else 0.0
