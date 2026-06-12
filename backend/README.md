# GovOne Backend Database (Round 3)

Đây là thư mục chứa tầng Database & Data Layer cho hệ thống GovOne, hoàn thành Round 3 với đầy đủ chức năng và cấu trúc chuẩn.

## Tính năng đã hoàn thành (Round 3)

1. **Thiết lập Database**: Cấu hình PostgreSQL, kết nối bằng asyncpg với SQLAlchemy 2.0. Có config connection pool đầy đủ.
2. **Thiết kế Schema**: 
    - `users`: Quản lý người dùng, đánh index các trường quan trọng (email, so_cccd, role).
    - `ho_so`: Quản lý hồ sơ hành chính, liên kết foreign key với users.
    - `ho_so_tai_lieu`: Lưu trữ tài liệu đính kèm của hồ sơ.
    - `ho_so_lich_su`: Ghi nhận lịch sử (Audit trail) với các thay đổi của hồ sơ.
    - `lich_hen`: Quản lý lịch hẹn giữa công dân và cán bộ.
    - `thong_bao`: Hệ thống thông báo.
3. **Repository Pattern**: Xây dựng kiến trúc `BaseRepository` chuẩn xác, cùng với các Repositories chuyên biệt (`UserRepository`, `HoSoRepository`, `LichHenRepository`, `ThongBaoRepository`) dùng chung AsyncSession.
4. **Seed Data**: Đã chuẩn bị script seed database (`seed/seed_data.py`) mặc định (admin), sẵn sàng để seed nhiều data giả lập hơn.
5. **Migrations**: Tích hợp Alembic sẵn sàng để thực thi (upgrade/downgrade schema).

## Tech Stack

- **Python** (FastAPI)
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0 (asyncio)
- **Migration**: Alembic
- **Driver**: asyncpg

## Cấu trúc thư mục

```
backend/
├── src/
│   ├── database/
│   │   ├── connection.py        # Database connection & session
│   │   ├── base.py              # Base model declarative
│   │   └── repositories/        # Các Class quản lý Query Database 
│   ├── models/                  # Các Models (Schema)
│   └── config/
│       └── settings.py          # Configuration env
├── migrations/                  # Thư mục Alembic cấu hình version control DB
├── seed/                        # Script seed dữ liệu giả
├── tests/                       # Unit test (Repositories, migrations)
├── requirements.txt             # Các package cần thiết
└── README.md                    # Hướng dẫn này
```

## Hướng dẫn cài đặt và sử dụng

### 1. Cài đặt thư viện

Sử dụng môi trường ảo (virtualenv) hoặc trực tiếp để cài đặt các packages yêu cầu:

```bash
pip install -r requirements.txt
```

### 2. Thiết lập Database (PostgreSQL)

Hãy đảm bảo bạn đã có PostgreSQL đang chạy.
Sửa `DATABASE_URL` trong file `.env` hoặc cấu hình `src/config/settings.py` cho khớp với database cục bộ của bạn.

Mặc định: `postgresql+asyncpg://postgres:postgres@localhost:5432/govone`

*(Tạo database `govone` trước khi chạy migrations)*.

### 3. Khởi tạo Migrations

Nếu đây là lần chạy đầu tiên, bạn có thể sinh ra file migration và chạy migration:

```bash
# Tạo một migration mới (tự động phát hiện thay đổi trong models)
alembic revision --autogenerate -m "Initial schema"

# Chạy migrate để áp dụng lên Database
alembic upgrade head
```

### 4. Chạy Seed Data

Script sau sẽ nạp dữ liệu mẫu ban đầu (như admin user):

```bash
python -m seed.seed_data
```

## Lưu ý

- **Mô hình Repository**: Khi lấy thông tin DB ở tầng Business logic, chỉ cần gọi `user_repo.get(...)`, `ho_so_repo.get(...)`, truyền `AsyncSession` vào là có thể tái sử dụng dễ dàng.
- **Migrations**: Mọi thay đổi về class model trong `src/models/*.py` cần được chạy tự động lệnh `alembic revision --autogenerate -m "Mô tả"` để tạo scripts trước khi đẩy code.
