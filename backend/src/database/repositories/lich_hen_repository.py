from sqlalchemy.ext.asyncio import AsyncSession
from src.models.lich_hen import LichHen
from .base_repository import BaseRepository

class LichHenRepository(BaseRepository[LichHen]):
    def __init__(self):
        super().__init__(LichHen)

lich_hen_repo = LichHenRepository()
