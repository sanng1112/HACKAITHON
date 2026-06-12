from sqlalchemy.ext.asyncio import AsyncSession
from src.models.thong_bao import ThongBao
from .base_repository import BaseRepository

class ThongBaoRepository(BaseRepository[ThongBao]):
    def __init__(self):
        super().__init__(ThongBao)

thong_bao_repo = ThongBaoRepository()
