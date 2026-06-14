"""Pagination utilities for list endpoints."""
import math
from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    """A page of results with pagination metadata."""

    items: Sequence[T]
    total: int
    page: int
    limit: int

    @property
    def total_pages(self) -> int:
        return max(1, math.ceil(self.total / self.limit)) if self.total > 0 else 1

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    def to_dict(self) -> dict:
        return {
            "page": self.page,
            "limit": self.limit,
            "total": self.total,
            "total_pages": self.total_pages,
        }
