"""Standard API response helpers.

All API responses follow this format:
{
    "success": bool,
    "data": Any | None,
    "error": {"code": str, "message": str} | None,
    "pagination": {"page": int, "limit": int, "total": int, "total_pages": int} | None
}
"""
from typing import Any, Optional


def success_response(data: Any = None, pagination: Optional[dict] = None) -> dict:
    """Build a success response."""
    return {
        "success": True,
        "data": data,
        "error": None,
        "pagination": pagination,
    }


def error_response(code: str, message: str) -> dict:
    """Build an error response."""
    return {
        "success": False,
        "data": None,
        "error": {"code": code, "message": message},
        "pagination": None,
    }


def build_pagination(page: int, limit: int, total: int) -> dict:
    """Build pagination metadata dict."""
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": max(1, (total + limit - 1) // limit) if total > 0 else 1,
    }
