# Round 3: Backend - Quản lý Database (Data Layer)

**Người phụ trách:** Backend Developer 2 (Người C)

---

## Mục tiêu tổng quan

Xây dựng tầng **Database & Data Layer** cho hệ thống GovOne - thiết kế schema, migrations, repository pattern, và tối ưu truy vấn. Round này đảm bảo tất cả dữ liệu được lưu trữ an toàn, truy vấn hiệu quả, và sẵn sàng cho tầng Business Logic.

Hoàn thành Round 3 đồng nghĩa với việc **toàn bộ hệ thống dữ liệu hoạt động hoàn chỉnh**, có schema chuẩn, migrations, seed data, và các repository/truy vấn tối ưu.

---

## 📋 Danh sách công việc chi tiết

### 3.1 Thiết lập Database

- [ ] Chọn database: **PostgreSQL** (khuyến nghị) hoặc MySQL
- [ ] Cấu hình kết nối database (connection pool, timeout, SSL)
- [ ] Thiết lập ORM: **SQLAlchemy** (Python) hoặc **Prisma** (Node.js/TypeScript)
- [ ] Cấu hình Alembic (Python) hoặc Prisma Migrate (Node.js) cho migrations
- [ ] Thiết lập môi trường: development, testing, production

### 3.2 Thiết kế Schema Database

#### Bảng `users` - Người dùng
| Column | Type | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| id | UUID | PK, NOT NULL | ID người dùng |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email đăng nhập |
| password_hash | VARCHAR(255) | NOT NULL | Mật khẩu đã hash |
| ho_ten | VARCHAR(255) | NOT NULL | Họ và tên |
| so_cccd | VARCHAR(20) | UNIQUE | Số căn cước công dân |
| so_dien_thoai | VARCHAR(20) | | Số điện thoại |
| dia_chi | TEXT | | Địa chỉ |
| role | ENUM('citizen','officer','admin') | NOT NULL, DEFAULT 'citizen' | Vai trò |
| trang_thai | ENUM('active','inactive','locked') | NOT NULL, DEFAULT 'active' | Trạng thái tài khoản |
| refresh_token | TEXT | | Refresh token hiện tại |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Ngày tạo |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Ngày cập nhật |

- [ ] Tạo model `User`
- [ ] Tạo migration cho bảng `users`
- [ ] Index trên `email`, `so_cccd`, `role`

#### Bảng `ho_so` - Hồ sơ hành chính
| Column | Type | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| id | UUID | PK, NOT NULL | ID hồ sơ |
| ma_ho_so | VARCHAR(30) | UNIQUE, NOT NULL | Mã hồ sơ |
| user_id | UUID | FK -> users.id, NOT NULL | Người tạo |
| loai_thu_tuc | VARCHAR(100) | NOT NULL | Loại thủ tục |
| noi_dung | TEXT | NOT NULL | Nội dung hồ sơ |
| trang_thai | ENUM('CHO_TIEP_NHAN','CHO_XU_LY','DANG_XU_LY','DA_XU_LY','TU_CHOI','CHO_BO_SUNG','DA_BO_SUNG') | NOT NULL, DEFAULT 'CHO_TIEP_NHAN' | |
| nguoi_xu_ly_id | UUID | FK -> users.id | Cán bộ xử lý |
| ghi_chu_xu_ly | TEXT | | Ghi chú xử lý |
| ly_do_tu_choi | TEXT | | Lý do từ chối |
| yeu_cau_bo_sung | TEXT | | Yêu cầu bổ sung |
| ngay_nop | TIMESTAMP | NOT NULL, DEFAULT NOW() | |
| ngay_xu_ly | TIMESTAMP | | |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | |

- [ ] Tạo model `HoSo`
- [ ] Tạo migration cho bảng `ho_so`
- [ ] Index trên `ma_ho_so`, `user_id`, `trang_thai`, `ngay_nop`

#### Bảng `ho_so_tai_lieu` - Tài liệu đính kèm
| Column | Type | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| id | UUID | PK, NOT NULL | |
| ho_so_id | UUID | FK → ho_so.id, NOT NULL | Hồ sơ |
| ten_file | VARCHAR(255) | NOT NULL | Tên file gốc |
| duong_dan | TEXT | NOT NULL | Đường dẫn lưu file |
| loai_file | VARCHAR(50) | NOT NULL | MIME type |
| kich_thuoc | BIGINT | NOT NULL | Dung lượng (bytes) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | |

- [ ] Tạo model `HoSoTaiLieu`
- [ ] Tạo migration

#### Bảng `ho_so_lich_su` - Lịch sử xử lý (Audit Trail)
| Column | Type | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| id | UUID | PK, NOT NULL | |
| ho_so_id | UUID | FK → ho_so.id, NOT NULL | Hồ sơ |
| nguoi_thuc_hien_id | UUID | FK → users.id, NOT NULL | Người thực hiện |
| hanh_dong | VARCHAR(50) | NOT NULL | Hành động |
| trang_thai_cu | VARCHAR(30) | | Trạng thái trước |
| trang_thai_moi | VARCHAR(30) | | Trạng thái sau |
| ghi_chu | TEXT | | Ghi chú |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | |

- [ ] Tạo model `HoSoLichSu`
- [ ] Tạo migration
- [ ] Index trên `ho_so_id`, `created_at`


#### Bảng `lich_hen` - Lịch hẹn
| Column | Type | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| id | UUID | PK, NOT NULL | |
| user_id | UUID | FK → users.id, NOT NULL | Công dân |
| can_bo_id | UUID | FK → users.id | Cán bộ tiếp nhận |
| tieu_de | VARCHAR(255) | NOT NULL | Tiêu đề |
| ngay_hen | DATE | NOT NULL | Ngày hẹn |
| gio_hen | TIME | NOT NULL | Giờ hẹn |
| ghi_chu | TEXT | | Ghi chú |
| trang_thai | ENUM('CHO_XAC_NHAN','DA_XAC_NHAN','DA_HUY','HOAN_THANH') | DEFAULT 'CHO_XAC_NHAN' | |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | |

- [ ] Tạo model `LichHen`
- [ ] Tạo migration
- [ ] Index trên `user_id`, `ngay_hen`, `trang_thai`

#### Bảng `thong_bao` - Thông báo
| Column | Type | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| id | UUID | PK, NOT NULL | |
| user_id | UUID | FK → users.id | Người nhận (NULL = tất cả) |
| tieu_de | VARCHAR(255) | NOT NULL | Tiêu đề |
| noi_dung | TEXT | NOT NULL | Nội dung |
| loai | ENUM('he_thong','ho_so','lich_hen') | NOT NULL | Loại |
| da_doc | BOOLEAN | NOT NULL, DEFAULT FALSE | Đã đọc? |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | |

- [ ] Tạo model `ThongBao`
- [ ] Tạo migration
- [ ] Index trên `user_id`, `da_doc`, `created_at`
### 3.4 Migrations Scripts

- [ ] Migration `001_create_users`
- [ ] Migration `002_create_ho_so`
- [ ] Migration `003_create_ho_so_tai_lieu`
- [ ] Migration `004_create_ho_so_lich_su`
- [ ] Migration `005_create_lich_hen`
- [ ] Migration `006_create_thong_bao`
- [ ] Migration `007_add_indexes`
- [ ] Script **upgrade** (apply all migrations)
- [ ] Script **downgrade** (rollback migrations)
- [ ] Script **reset_db** (drop all + re-migrate)

### 3.5 Seed Data

- [ ] Tạo script seed **admin** mặc định (admin@govone.vn / Admin@123)
- [ ] Seed **cán bộ** mẫu (3-5 cán bộ)
- [ ] Seed **công dân** mẫu (5-10 công dân)
- [ ] Seed **loại thủ tục hành chính** mẫu (10-15 loại)
- [ ] Seed **hồ sơ** mẫu (20-30 hồ sơ với các trạng thái khác nhau)
- [ ] Seed **lịch hẹn** mẫu
- [ ] Seed **thông báo** mẫu
- [ ] Script `seed.py` chạy một lần

### 3.6 Repository Layer

- [ ] **UserRepository**: CRUD users, tìm theo email/CCCD, phân trang
- [ ] **HoSoRepository**: CRUD hồ sơ, filter theo trạng thái/user/ngày, phân trang
- [ ] **HoSoTaiLieuRepository**: CRUD tài liệu theo hồ sơ
- [ ] **HoSoLichSuRepository**: Lấy lịch sử theo hồ sơ, ghi log
- [ ] **LichHenRepository**: CRUD lịch hẹn, kiểm tra trùng lịch
- [ ] **ThongBaoRepository**: CRUD thông báo, đánh dấu đã đọc
- [ ] **BaseRepository**: Abstract class với các method generic (get, create, update, delete, paginate)

### 3.7 Database Connection & Config

- [ ] Cấu hình `DATABASE_URL` cho các môi trường
- [ ] Connection pool (min=2, max=10)
- [ ] Retry connection khi mất kết nối
- [ ] Health check endpoint `/api/health/db`
- [ ] Session management (SQLAlchemy session per request)
- [ ] Transaction management (commit/rollback tự động)

### 3.8 Performance & Optimization

- [ ] **Indexes** cho tất cả cột thường xuyên query
- [ ] **Full-text search** cho nội dung hồ sơ (nếu cần)
- [ ] **Pagination** với cursor-based hoặc offset-based
- [ ] **N+1 query prevention** (eager loading relationships)
- [ ] **Caching** layer (Redis) cho dữ liệu ít thay đổi
- [ ] **Database monitoring** (slow query log)

---

## 🧪 Tiêu chí hoàn thành (Definition of Done)

1. ✅ Tất cả migrations chạy thành công trên môi trường dev
2. ✅ Có thể rollback migrations mà không mất dữ liệu
3. ✅ Seed data đầy đủ để demo (admin, cán bộ, công dân, hồ sơ, lịch hẹn)
4. ✅ Repository pattern hoạt động đúng (CRUD + pagination + filter)
5. ✅ Kết nối database ổn định, không rò rỉ kết nối
6. ✅ Health check `/health/db` trả về OK khi DB hoạt động
7. ✅ Tất cả relationships (foreign keys) hoạt động đúng
8. ✅ Query performance tối ưu (không có N+1, có index phù hợp)

---

## 🚀 Tech Stack đề xuất

- **Database:** PostgreSQL 15+
- **ORM:** SQLAlchemy 2.0 (Python) / Prisma (Node.js)
- **Migration:** Alembic (Python) / Prisma Migrate (Node.js)
- **Connection Pool:** psycopg2-binary / asyncpg (Python) / pg-pool (Node.js)
- **Caching:** Redis
- **Query Builder:** SQLAlchemy Core / Prisma Client
- **Testing:** Pytest + pytest-asyncio (Python) / Jest (Node.js)
- **Monitoring:** pg_stat_statements, slow query log

---

## 🔗 Phụ thuộc (Dependencies)

- **Round 2 (Backend Logic)** phụ thuộc vào schema từ round này
- Nên làm **Round 3 trước Round 2** hoặc làm song song với schema design agreement
- **Round 4 (Models)** có thể cần lưu kết quả AI vào database (cần migration mở rộng)

---

## 📂 File cần tạo

```
backend/
├── src/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py       # Database connection & session
│   │   ├── base.py             # Base model declarative
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── base_repository.py
│   │       ├── user_repository.py
│   │       ├── ho_so_repository.py
│   │       ├── lich_hen_repository.py
│   │       └── thong_bao_repository.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── ho_so.py
│   │   ├── ho_so_tai_lieu.py
│   │   ├── ho_so_lich_su.py
│   │   ├── lich_hen.py
│   │   └── thong_bao.py
│   └── config/
│       ├── __init__.py
│       └── settings.py
├── migrations/
│   ├── versions/
│   │   ├── 001_create_users.py
│   │   ├── 002_create_ho_so.py
│   │   ├── 003_create_ho_so_tai_lieu.py
│   │   ├── 004_create_ho_so_lich_su.py
│   │   ├── 005_create_lich_hen.py
│   │   ├── 006_create_thong_bao.py
│   │   └── 007_add_indexes.py
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
├── seed/
│   ├── __init__.py
│   ├── seed_data.py
│   └── seed_config.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_repositories/
│   │   ├── test_user_repository.py
│   │   ├── test_ho_so_repository.py
│   │   └── ...
│   └── test_migrations.py
└── requirements.txt
```

