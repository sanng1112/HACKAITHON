import asyncio
import uuid
from datetime import datetime, timedelta
from src.database.connection import async_session_maker, engine
from src.models.user import User, RoleEnum, StatusEnum
from src.models.ho_so import HoSo, TrangThaiHoSoEnum
from src.models.lich_hen import LichHen, TrangThaiLichHenEnum
from src.models.thong_bao import ThongBao, LoaiThongBaoEnum
from src.database.base import Base

async def seed_data():
    async with async_session_maker() as db:
        # Seed Admin
        admin = User(
            email="admin@govone.vn", password_hash="hashed_admin_123", ho_ten="Admin",
            role=RoleEnum.admin, so_cccd="000000000000"
        )
        db.add(admin)
        
        # Seed Can Bo (3)
        can_bos = [
            User(email=f"canbo{i}@govone.vn", password_hash="hashed", ho_ten=f"Cán bộ {i}", role=RoleEnum.officer, so_cccd=f"10000000000{i}")
            for i in range(1, 4)
        ]
        db.add_all(can_bos)
        
        # Seed Cong Dan (5)
        cong_dans = [
            User(email=f"congdan{i}@govone.vn", password_hash="hashed", ho_ten=f"Công dân {i}", role=RoleEnum.citizen, so_cccd=f"20000000000{i}")
            for i in range(1, 6)
        ]
        db.add_all(cong_dans)
        
        await db.commit()
        await db.refresh(admin)
        for cb in can_bos:
            await db.refresh(cb)
        for cd in cong_dans:
            await db.refresh(cd)

        print("Users seeded successfully.")

        # Seed Ho So (20)
        ho_sos = []
        loai_thu_tuc = ["Cấp thẻ BHYT", "Đăng ký khai sinh", "Đăng ký kết hôn", "Cấp CCCD", "Đăng ký kinh doanh"]
        for i in range(1, 21):
            hs = HoSo(
                ma_ho_so=f"HS2026{i:04d}",
                user_id=cong_dans[i%5].id,
                loai_thu_tuc=loai_thu_tuc[i%5],
                noi_dung=f"Nội dung hồ sơ {i}",
                trang_thai=list(TrangThaiHoSoEnum)[i%7],
                nguoi_xu_ly_id=can_bos[i%3].id if i%7 > 0 else None
            )
            ho_sos.append(hs)
        db.add_all(ho_sos)
        
        # Seed Lich Hen (5)
        lich_hens = [
            LichHen(
                user_id=cong_dans[i].id,
                can_bo_id=can_bos[0].id,
                tieu_de=f"Lịch hẹn {i}",
                ngay_hen=(datetime.now() + timedelta(days=i)).date(),
                gio_hen=(datetime.now()).time(),
                trang_thai=TrangThaiLichHenEnum.CHO_XAC_NHAN
            ) for i in range(5)
        ]
        db.add_all(lich_hens)

        # Seed Thong Bao (5)
        thong_baos = [
            ThongBao(
                user_id=cong_dans[i].id,
                tieu_de=f"Thông báo {i}",
                noi_dung=f"Nội dung thông báo {i}",
                loai=LoaiThongBaoEnum.he_thong
            ) for i in range(5)
        ]
        db.add_all(thong_baos)

        await db.commit()
        print("All mock data seeded successfully.")

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_data()

if __name__ == "__main__":
    asyncio.run(main())
