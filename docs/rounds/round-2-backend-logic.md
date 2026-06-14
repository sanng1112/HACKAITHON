# Round 2: Backend — Xử lý Logic nghiệp vụ (Business Logic Layer)

**Người phụ trách:** Backend Developer 1 (Người B)

> **Tài liệu tham khảo kiến trúc:**
> - [Tổng quan hệ thống](../architecture/system-overview.md) — actors, scope, non-functional
> - [Kiến trúc 4 tầng](../architecture/4-layer-architecture.md) — Tầng 3: Processing Layer
> - [Thiết kế API](../architecture/api-design.md) — request/response chi tiết từng endpoint
> - [Luồng dữ liệu](../architecture/data-flow.md) — state machine, workflow rules
> - [Triển khai](../architecture/deployment.md) — Docker, services, CI/CD

---

## Mục tiêu tổng quan

Xây dựng **Tầng 3 — Processing Layer** của kiến trúc GovOne 4 tầng. Tầng này chịu trách nhiệm toàn bộ logic nghiệp vụ: xác thực & phân quyền, quản lý hồ sơ hành chính (state machine), quản lý lịch hẹn, thông báo — tất cả giao tiếp với frontend qua REST API và với database qua repository layer đã xây dựng ở Round 3.

### Vị trí trong kiến trúc 4 tầng

```
┌──────────────────────────────────────────────────────────────────┐
│  TẦNG 1: USER LAYER     Kiosk · Web App · Mobile App            │  ← Frontend (đã xong)
├──────────────────────────────────────────────────────────────────┤
│  TẦNG 2: AI CORE        7 VNPT APIs · Fallback Models           │  ← Round 4 (đã xong)
├──────────────────────────────────────────────────────────────────┤
│  TẦNG 3: PROCESSING LAYER  ← BẠN ĐANG Ở ĐÂY — Round 2            │
│  ┌───────────────────────────────────────────────────────────────┐│
│  │  Auth Service · HoSo Service · LichHen Service · Notify Svc  ││
│  │  Middleware: JWT · RBAC · Error Handler · Logging · Rate Limit││
│  └───────────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────────┤
│  TẦNG 4: DATA LAYER     PostgreSQL · Redis · MinIO · KB         │  ← Round 3 (đã xong)
└──────────────────────────────────────────────────────────────────┘
```

### Phụ thuộc

| Round | Trạng thái | Ghi chú |
|---|---|---|
| **Round 3 (Database)** | ✅ Đã xong | Models, repositories, migrations, seed data |
| **Round 4 (AI Models)** | ✅ Đã xong | AI routers, services, tasks (có thể dùng chung `main.py`) |
| **Round 2 (này)** | 🔄 Đang xây | Services, API routers, middleware |

---

## 📋 Trạng thái dự án hiện tại

### ✅ Đã có sẵn (thừa hưởng từ Round 3 & 4)

```
backend/
├── src/
│   ├── ai/                   # Round 4 — AI routers + services (giữ nguyên)
│   ├── config/settings.py    # Cấu hình chung
│   ├── database/
│   │   ├── connection.py     # Kết nối DB (SQLAlchemy async session)
│   │   ├── base.py           # Declarative base
│   │   └── repositories/     # 6 repositories (user, ho_so, ho_so_tai_lieu,
│   │                           ho_so_lich_su, lich_hen, thong_bao)
│   ├── models/               # 6 SQLAlchemy models
│   └── main.py               # FastAPI app — đã register AI routers + CORS
├── migrations/               # Alembic — 7 migration files
├── seed/                     # Seed data
├── tests/                    # Repository tests + AI tests
└── requirements.txt
```

### ❌ Cần xây dựng trong Round 2

```
backend/src/
├── api/                      # API routers (xử lý HTTP request/response)
│   ├── __init__.py           #   (đã có — file rỗng)
│   ├── auth.py               # 🔴 Đăng ký, đăng nhập, refresh, me, logout
│   ├── ho_so.py              # 🔴 CRUD hồ sơ + workflow actions
│   ├── lich_hen.py           # 🔴 CRUD lịch hẹn
│   ├── thong_bao.py          # 🔴 CRUD thông báo
│   └── deps.py               # 🔴 Dependency injection (get_db, get_current_user, ...)
├── services/                 # Business logic layer
│   ├── __init__.py           #   (đã có — file rỗng)
│   ├── auth_service.py       # 🔴 Xử lý auth: hash, JWT, roles
│   ├── ho_so_service.py      # 🔴 State machine, workflow, CRUD
│   ├── lich_hen_service.py   # 🔴 Lịch hẹn logic, conflict detection
│   └── thong_bao_service.py  # 🔴 Tạo & gửi thông báo
├── middleware/
│   ├── __init__.py           # 🔴
│   ├── auth_middleware.py    # 🔴 JWT verification, role-based access
│   ├── error_handler.py      # 🔴 Global exception → response format chuẩn
│   └── logging_middleware.py # 🔴 Log mọi request
└── utils/
    ├── __init__.py           # 🔴
    ├── security.py           # 🔴 Bcrypt hash, JWT encode/decode
    ├── pagination.py         # 🔴 Pagination helper
    └── response.py           # 🔴 Standard response builder
```

---

## 2.1 Thiết lập dự án Backend

- [x] Framework backend: **FastAPI** (Python 3.12)
- [x] Cấu hình project structure — đã có sẵn từ Round 3
- [ ] Tích hợp các router Round 2 vào `main.py` (auth, ho_so, lich_hen, thong_bao)
- [ ] Đăng ký middleware: CORS (đã có), error handler, logging, rate limiting

### Cập nhật `main.py`

```python
# Thêm vào src/main.py trong hàm create_app()

# ─── Middleware ────────────────────────────────────────────
from src.middleware.logging_middleware import LoggingMiddleware
from src.middleware.error_handler import setup_error_handlers

setup_error_handlers(app)              # Global exception handler
app.add_middleware(LoggingMiddleware)   # Request logging

# ─── Business routers (Round 2) ────────────────────────────
from src.api.auth import router as auth_router
from src.api.ho_so import router as ho_so_router
from src.api.lich_hen import router as lich_hen_router
from src.api.thong_bao import router as thong_bao_router

app.include_router(auth_router, prefix="/api")
app.include_router(ho_so_router, prefix="/api")
app.include_router(lich_hen_router, prefix="/api")
app.include_router(thong_bao_router, prefix="/api")
```

---

## 2.2 Hệ thống Xác thực & Phân quyền

### Chi tiết triển khai

**File:** `src/utils/security.py` + `src/services/auth_service.py` + `src/api/auth.py` + `src/middleware/auth_middleware.py`

### API Endpoints

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| POST | `/api/auth/register` | Đăng ký tài khoản mới | None |
| POST | `/api/auth/login` | Đăng nhập → JWT | None |
| POST | `/api/auth/refresh` | Refresh token | Refresh token |
| GET | `/api/auth/me` | Thông tin user hiện tại | Bearer token |
| POST | `/api/auth/change-password` | Đổi mật khẩu | Bearer token |
| POST | `/api/auth/logout` | Đăng xuất (vô hiệu hoá token) | Bearer token |

### Flow xác thực

```
Request → auth_middleware.py
  ├── Token missing?       → 401 UNAUTHORIZED
  ├── Token expired?       → 401 TOKEN_EXPIRED
  ├── Token invalid?       → 401 UNAUTHORIZED
  └── Token valid          → Inject user vào request → next()
```

### Chi tiết các module

#### `src/utils/security.py`
- `hash_password(plain: str) -> str` — bcrypt hash
- `verify_password(plain: str, hashed: str) -> bool` — check hash
- `create_access_token(data: dict) -> str` — JWT encode (HS256, 30 phút)
- `create_refresh_token(data: dict) -> str` — JWT encode (7 ngày)
- `decode_token(token: str) -> dict` — JWT decode, raise exception nếu hết hạn
- Token payload: `{"sub": user_id, "role": "citizen", "exp": timestamp}`

#### `src/services/auth_service.py`
- `register(db, data: RegisterInput) -> User` — validate unique email/CCCD → hash pass → create user
- `login(db, email, password) -> dict` — verify credentials → return access_token + refresh_token + user
- `refresh_token(db, token: str) -> dict` — decode refresh → issue new pair (old refresh vô hiệu)
- `get_current_user(db, user_id: UUID) -> User` — lấy user info (cho GET /auth/me)
- `change_password(db, user, current_pw, new_pw) -> None` — verify current → hash new → save

#### `src/api/auth.py`
- Router FastAPI với 6 endpoints
- Input validation qua Pydantic schemas (inline hoặc trong schema riêng)
- Response theo format chuẩn từ `utils/response.py`

#### `src/middleware/auth_middleware.py`
- `AuthMiddleware` class kiểm tra `Authorization: Bearer <token>` header
- Skip list: `/api/auth/login`, `/api/auth/register`, `/api/health`, `/docs`, `/openapi.json`
- Trên mọi request: decode token → attach `request.user` = User object
- `require_roles("officer", "admin")` — decorator/dependency kiểm tra role

### Response format (xem chi tiết [api-design.md](../architecture/api-design.md))

```
POST /api/auth/register → 201
{
  "success": true,
  "data": { "id": "uuid", "email": "...", "ho_ten": "...", "role": "citizen" },
  "error": null
}

POST /api/auth/login → 200
{
  "success": true,
  "data": {
    "access_token": "eyJ...", "refresh_token": "eyJ...",
    "token_type": "bearer", "expires_in": 1800,
    "user": { "id": "uuid", "email": "...", "role": "citizen" }
  },
  "error": null
}

POST /api/auth/login (sai mật khẩu) → 401
{
  "success": false,
  "error": { "code": "INVALID_CREDENTIALS", "message": "Email hoặc mật khẩu không đúng" }
}
```

### Mã lỗi auth

| HTTP | Error Code | Điều kiện |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Email không hợp lệ, thiếu field |
| 401 | `UNAUTHORIZED` | Không gửi token |
| 401 | `TOKEN_EXPIRED` | Token hết hạn |
| 401 | `INVALID_CREDENTIALS` | Sai email/password |
| 403 | `FORBIDDEN` | Không đủ quyền (role check fail) |
| 409 | `EMAIL_EXISTS` | Email đã đăng ký |
| 409 | `CCCD_EXISTS` | CCCD đã đăng ký |

---

## 2.3 Quản lý Hồ sơ Hành chính

### Chi tiết triển khai

**File:** `src/services/ho_so_service.py` + `src/api/ho_so.py`

### API Endpoints

| Method | Endpoint | Mô tả | Role |
|--------|----------|-------|------|
| POST | `/api/ho-so` | Tạo hồ sơ mới | citizen |
| GET | `/api/ho-so` | Danh sách hồ sơ (phân trang, filter) | citizen/officer/admin |
| GET | `/api/ho-so/:id` | Chi tiết hồ sơ | citizen/officer/admin |
| PUT | `/api/ho-so/:id` | Cập nhật hồ sơ (khi `CHO_TIEP_NHAN`) | citizen (chủ hồ sơ) |
| POST | `/api/ho-so/:id/upload` | Upload tài liệu | citizen (chủ hồ sơ) |
| POST | `/api/ho-so/:id/submit` | Nộp hồ sơ → `CHO_XU_LY` | citizen (chủ hồ sơ) |
| PUT | `/api/ho-so/:id/tiep-nhan` | Tiếp nhận → `DANG_XU_LY` | officer |
| PUT | `/api/ho-so/:id/phe-duyet` | Phê duyệt → `DA_XU_LY` | officer |
| PUT | `/api/ho-so/:id/tu-choi` | Từ chối → `TU_CHOI` + lý do | officer |
| PUT | `/api/ho-so/:id/yeu-cau-bo-sung` | Yêu cầu bổ sung → `CHO_BO_SUNG` | officer |
| POST | `/api/ho-so/:id/bo-sung` | Công dân gửi bổ sung → `DA_BO_SUNG` | citizen |
| GET | `/api/ho-so/:id/lich-su` | Lịch sử thay đổi trạng thái | citizen/officer |
| DELETE | `/api/ho-so/:id` | Xoá hồ sơ (chỉ khi `CHO_TIEP_NHAN`) | citizen (chủ hồ sơ) |

### Sinh mã hồ sơ tự động

Format: `HS-{YYYY}-{XXXX}` (vd: `HS-2026-0042`)

```
1. Query DB đếm số hồ sơ trong năm hiện tại: count = repo.count_by_year(2026)
2. next_number = count + 1
3. ma_ho_so = f"HS-{year}-{next_number:04d}"
```

### Query parameters cho GET /api/ho-so

```
?page=1&limit=20
&trang_thai=DANG_XU_LY
&loai_thu_tuc=cap-giay-phep
&sort_by=ngay_nop&sort_order=desc
&from_date=2026-01-01&to_date=2026-06-12
&q=Nguyễn Văn A
```

**Phân quyền danh sách:** `citizen` chỉ thấy hồ sơ của mình; `officer` thấy hồ sơ đang xử lý + chờ xử lý; `admin` thấy tất cả.

### Upload file

- File lưu qua MinIO/S3 client (hoặc local uploads/ nếu chưa có MinIO)
- Kiểm tra: dung lượng (`FILE_TOO_LARGE` > 10MB), loại file (`UNSUPPORTED_FILE_TYPE`)
- Sau upload → tạo `HoSoTaiLieu` record trong DB

### Response format (xem chi tiết [api-design.md](../architecture/api-design.md))

```
POST /api/ho-so → 201
{
  "success": true,
  "data": {
    "id": "uuid", "ma_ho_so": "HS-2026-0042",
    "trang_thai": "CHO_TIEP_NHAN", "ngay_nop": "2026-06-12T10:30:00Z"
  }
}

GET /api/ho-so?page=1&limit=20 → 200
{
  "success": true,
  "data": [ { "id": "uuid", "ma_ho_so": "...", "trang_thai": "..." } ],
  "pagination": { "page": 1, "limit": 20, "total": 156, "total_pages": 8 }
}

PUT /api/ho-so/:id/tu-choi → 200
{
  "success": true,
  "data": { "id": "uuid", "trang_thai": "TU_CHOI", "message": "Hồ sơ đã bị từ chối" }
}
```

---

## 2.4 Workflow Xử lý Hồ sơ (State Machine)

### Sơ đồ trạng thái (xem chi tiết [data-flow.md#luồng-3-state-machine](../architecture/data-flow.md))

```
                    ┌──────────────┐
                    │ CHO_TIEP_NHAN│ ← Tạo mới
                    └──────┬───────┘
                           │ Công dân submit
                           ▼
                    ┌──────────────┐
                    │  CHO_XU_LY   │
                    └──────┬───────┘
                           │ Cán bộ tiếp nhận
                           ▼
                    ┌──────────────┐
              ┌─────│ DANG_XU_LY  │─────┐
              │     └──────────────┘     │
              │                         │
              ▼                         ▼
       ┌──────────────┐          ┌──────────────┐
       │  DA_XU_LY    │          │   TU_CHOI    │
       │ (Phê duyệt)  │          │ (Từ chối)    │
       └──────────────┘          └──────────────┘
                                        │
                              ┌──────────────┐
                              │ CHO_BO_SUNG  │
                              │ (Y/c bổ sung)│
                              └──────┬───────┘
                                     │ Công dân bổ sung
                                     ▼
                              ┌──────────────┐
                              │ DA_BO_SUNG   │
                              └──────┬───────┘
                                     │ Trở lại xử lý
                                     ▼
                              ┌──────────────┐
                              │  DANG_XU_LY  │
                              └──────────────┘
```

### Ma trận chuyển trạng thái

| Từ | → Đến | Hành động | Điều kiện | Actor |
|---|---|---|---|---|
| `CHO_TIEP_NHAN` | `CHO_XU_LY` | `submit()` | — | Citizen (chủ hồ sơ) |
| `CHO_XU_LY` | `DANG_XU_LY` | `tiep_nhan()` | — | Officer (bất kỳ) |
| `DANG_XU_LY` | `DA_XU_LY` | `phe_duyet()` | ghi_chu (optional) | Officer (đang xử lý) |
| `DANG_XU_LY` | `TU_CHOI` | `tu_choi()` | ly_do (required) | Officer (đang xử lý) |
| `DANG_XU_LY` | `CHO_BO_SUNG` | `yeu_cau_bo_sung()` | yeu_cau list | Officer (đang xử lý) |
| `CHO_BO_SUNG` | `DA_BO_SUNG` | `bo_sung()` | — | Citizen (chủ hồ sơ) |
| `DA_BO_SUNG` | `DANG_XU_LY` | `nhan_bo_sung()` | — | Officer (đang xử lý) |

### Triển khai State Machine

```python
# src/services/ho_so_service.py

class TrangThai(str, Enum):
    CHO_TIEP_NHAN = "CHO_TIEP_NHAN"
    CHO_XU_LY = "CHO_XU_LY"
    DANG_XU_LY = "DANG_XU_LY"
    DA_XU_LY = "DA_XU_LY"
    TU_CHOI = "TU_CHOI"
    CHO_BO_SUNG = "CHO_BO_SUNG"
    DA_BO_SUNG = "DA_BO_SUNG"

# Transition rules: {current_state: {action: next_state}}
TRANSITIONS = {
    TrangThai.CHO_TIEP_NHAN: {"submit": TrangThai.CHO_XU_LY},
    TrangThai.CHO_XU_LY:     {"tiep_nhan": TrangThai.DANG_XU_LY},
    TrangThai.DANG_XU_LY:    {
        "phe_duyet":       TrangThai.DA_XU_LY,
        "tu_choi":         TrangThai.TU_CHOI,
        "yeu_cau_bo_sung": TrangThai.CHO_BO_SUNG,
    },
    TrangThai.CHO_BO_SUNG:  {"bo_sung": TrangThai.DA_BO_SUNG},
    TrangThai.DA_BO_SUNG:   {"nhan_bo_sung": TrangThai.DANG_XU_LY},
}

def transition(ho_so: HoSo, action: str) -> HoSo:
    next_state = TRANSITIONS[ho_so.trang_thai][action]
    ho_so.trang_thai = next_state
    return ho_so
```

### Audit Trail — `HoSoLichSu`

Mỗi lần chuyển trạng thái → tự động ghi:

```python
def ghi_lich_su(db, ho_so_id, hanh_dong, trang_thai_cu, trang_thai_moi,
                nguoi_thuc_hien_id, ghi_chu="", noi_dung_them=None):
    record = HoSoLichSu(
        ho_so_id=ho_so_id,
        hanh_dong=hanh_dong,
        trang_thai_cu=trang_thai_cu,
        trang_thai_moi=trang_thai_moi,
        nguoi_thuc_hien_id=nguoi_thuc_hien_id,
        ghi_chu=ghi_chu,
        noi_dung_them=noi_dung_them,
    )
    db.add(record)
    db.commit()
```

### Thông báo tự động khi trạng thái thay đổi

Trong mỗi hàm transition, sau khi commit:

```python
# Tự động gửi thông báo cho chủ hồ sơ
thong_bao_service.create_notification(
    db=db,
    user_id=ho_so.nguoi_nop_id,
    tieu_de=f"Hồ sơ {ho_so.ma_ho_so} đã chuyển sang {ho_so.trang_thai}",
    noi_dung=f"Hồ sơ của bạn đã được cập nhật. Trạng thái hiện tại: {dict_trang_thai[ho_so.trang_thai]}",
    loai="ho_so",
)
```

---

## 2.5 Quản lý Lịch hẹn

### Chi tiết triển khai

**File:** `src/services/lich_hen_service.py` + `src/api/lich_hen.py`

### API Endpoints

| Method | Endpoint | Mô tả | Role |
|--------|----------|-------|------|
| POST | `/api/lich-hen` | Tạo lịch hẹn | citizen |
| GET | `/api/lich-hen` | Danh sách lịch hẹn (filter, phân trang) | citizen/officer |
| GET | `/api/lich-hen/:id` | Chi tiết lịch hẹn | citizen/officer |
| PUT | `/api/lich-hen/:id` | Xác nhận / cập nhật | citizen/officer |
| DELETE | `/api/lich-hen/:id` | Huỷ lịch hẹn | citizen (chủ) |

### Business Rules

- **Kiểm tra trùng lịch:** `service.check_conflict(ngay_hen, gio_hen)` → query DB xem khung giờ đã có chưa
- **Huỷ:** Chỉ cho phép huỷ nếu còn >= 24h trước giờ hẹn
- **Phân quyền danh sách:** Citizen chỉ thấy lịch của mình; Officer thấy tất cả

### Conflict detection

```python
async def check_conflict(db, ngay_hen: date, gio_hen: time, exclude_id=None) -> bool:
    """Kiểm tra xem khung giờ đã có lịch hẹn nào chưa."""
    query = select(LichHen).where(
        LichHen.ngay_hen == ngay_hen,
        LichHen.gio_hen == gio_hen,
        LichHen.trang_thai.in_(["CHO_XAC_NHAN", "DA_XAC_NHAN"]),
    )
    if exclude_id:
        query = query.where(LichHen.id != exclude_id)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None  # True nếu conflict
```

### Response format

```
POST /api/lich-hen → 201
{
  "success": true,
  "data": {
    "id": "uuid", "tieu_de": "Nộp hồ sơ cấp giấy phép",
    "ngay_hen": "2026-06-15", "gio_hen": "09:00",
    "trang_thai": "CHO_XAC_NHAN"
  }
}

Trùng lịch → 409
{
  "success": false,
  "error": { "code": "SCHEDULE_CONFLICT", "message": "Khung giờ này đã có lịch hẹn khác" }
}
```

---

## 2.6 Quản lý Thông báo

### Chi tiết triển khai

**File:** `src/services/thong_bao_service.py` + `src/api/thong_bao.py`

### API Endpoints

| Method | Endpoint | Mô tả | Role |
|--------|----------|-------|------|
| POST | `/api/thong-bao` | Tạo thông báo (cá nhân / broadcast) | officer |
| GET | `/api/thong-bao` | Danh sách thông báo | citizen/officer |
| PUT | `/api/thong-bao/:id/da-doc` | Đánh dấu đã đọc | citizen/officer |

### Business Rules

- `user_id = null` → broadcast (gửi cho tất cả)
- `user_id = uuid` → gửi riêng
- **Phân quyền danh sách:** Citizen chỉ thấy thông báo của mình hoặc broadcast
- **Loại thông báo:** `ho_so` (tự động), `he_thong` (cán bộ tạo), `lich_hen`

### Response format

```
GET /api/thong-bao?da_doc=false → 200
{
  "success": true,
  "data": [
    {
      "id": "uuid", "tieu_de": "Hồ sơ HS-2026-0042 đã được phê duyệt",
      "loai": "ho_so", "da_doc": false, "created_at": "2026-06-12T14:00:00Z"
    }
  ],
  "pagination": { "page": 1, "limit": 20, "total": 12 }
}
```

---

## 2.7 Middleware & Xử lý lỗi

### Global Exception Handler — `src/middleware/error_handler.py`

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message

def setup_error_handlers(app):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "data": None,
                "error": {"code": exc.code, "message": exc.message},
                "pagination": None,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        # Log full traceback
        logger.exception("Unhandled exception")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": None,
                "error": {"code": "INTERNAL_ERROR", "message": "Lỗi hệ thống"},
                "pagination": None,
            },
        )
```

### Standard Response Builders — `src/utils/response.py`

```python
from typing import Any, Optional
from pydantic import BaseModel

class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int

def success_response(data: Any = None, pagination: Optional[PaginationMeta] = None) -> dict:
    return {"success": True, "data": data, "error": None, "pagination": pagination}

def error_response(code: str, message: str) -> dict:
    return {"success": False, "data": None, "error": {"code": code, "message": message}, "pagination": None}
```

### Logging Middleware — `src/middleware/logging_middleware.py`

```python
import time
import logging

logger = logging.getLogger("govone.api")

class LoggingMiddleware:
    async def __call__(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration:.3f}s)")
        return response
```

### Rate Limiting

Triển khai qua Redis (dùng `redis` client):

| Role | Limit |
|------|-------|
| **Anonymous** | 30 req/phút |
| **Citizen** | 60 req/phút |
| **Officer** | 120 req/phút |
| **Admin** | 300 req/phút |
| **AI endpoints** | 10 req/phút (ocr/stt), 30 req/phút (classify) |

### Dependency Injection — `src/api/deps.py`

```python
from src.database.connection import get_session
from src.services.auth_service import get_current_user

# Sử dụng trong router:
# @router.get("/api/ho-so")
# async def list_ho_so(
#     db: AsyncSession = Depends(get_session),
#     current_user: User = Depends(get_current_user),
#     page: int = Query(1, ge=1),
#     limit: int = Query(20, ge=1, le=100),
# ):
```

---

## 📂 Cấu trúc file đầy đủ sau Round 2

```
backend/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py              # 6 endpoints auth
│   │   ├── ho_so.py             # 13 endpoints hồ sơ
│   │   ├── lich_hen.py          # 5 endpoints lịch hẹn
│   │   ├── thong_bao.py         # 3 endpoints thông báo
│   │   └── deps.py              # Dependency injection
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py      # Đăng ký, login, JWT
│   │   ├── ho_so_service.py     # CRUD + state machine
│   │   ├── lich_hen_service.py  # CRUD + conflict check
│   │   └── thong_bao_service.py # Notification logic
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py   # JWT verification
│   │   ├── error_handler.py     # Global exception handler
│   │   └── logging_middleware.py# Request logging
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py          # Hash, JWT helpers
│   │   ├── pagination.py        # Pagination helper
│   │   └── response.py          # Standard response builders
│   ├── models/                  # (Round 3 — giữ nguyên)
│   ├── database/                # (Round 3 — giữ nguyên)
│   ├── ai/                      # (Round 4 — giữ nguyên)
│   ├── config/settings.py
│   └── main.py                  # Cập nhật: thêm routers + middleware
├── migrations/                  # (Round 3 — giữ nguyên)
├── seed/                        # (Round 3 — giữ nguyên)
└── tests/
    ├── conftest.py              # (Round 3 — mở rộng)
    ├── test_auth.py             # Test auth APIs
    ├── test_ho_so.py            # Test ho so APIs + state machine
    ├── test_lich_hen.py         # Test lich hen APIs + conflict
    ├── test_thong_bao.py        # Test thong bao APIs
    └── test_repositories/       # (Round 3 — giữ nguyên)
```

---

## 🧪 Tiêu chí hoàn thành (Definition of Done)

1. ✅ Tất cả API endpoints (Auth: 6, HoSo: 13, LichHen: 5, ThongBao: 3) hoạt động và trả về đúng format chuẩn
2. ✅ Authentication & Authorization: JWT hoạt động, các endpoint bảo vệ đúng role
3. ✅ State machine hồ sơ: 7 trạng thái, 7 transitions — đúng quy tắc, audit trail tự động
4. ✅ Conflict detection cho lịch hẹn (không cho đặt trùng giờ)
5. ✅ Validation chặt chẽ: Pydantic schemas cho mọi input
6. ✅ Global exception handler: không crash server, trả về mã lỗi chuẩn
7. ✅ Logging: mọi request được ghi log
8. ✅ Rate limiting qua Redis
9. ✅ Có ít nhất **80% unit test coverage** cho services
10. ✅ Swagger/OpenAPI tự động (FastAPI built-in)
11. ✅ Tích hợp vào `main.py` — chạy cùng lúc với AI routers (Round 4)

---

## 🚀 Tech Stack

| Thành phần | Công nghệ | Ghi chú |
|---|---|---|
| **Framework** | FastAPI (Python 3.12) | Async native, auto OpenAPI |
| **Xác thực** | PyJWT + bcrypt | JWT HS256, 30p access + 7d refresh |
| **ORM** | SQLAlchemy 2.0 (async) | Đã có từ Round 3 |
| **Validation** | Pydantic v2 | Tích hợp sẵn trong FastAPI |
| **Queue** | Celery + Redis | Cho tác vụ nặng (AI async) |
| **File storage** | Local `uploads/` → MinIO (production) | Upload file hồ sơ |
| **Testing** | Pytest + httpx (async) | AsyncTestClient cho API tests |
| **Documentation** | Swagger UI tại `/docs` | FastAPI tự động sinh |

---

## 📦 Dependencies mới (thêm vào requirements.txt)

```
# Authentication & Security
pyjwt==2.8.0
bcrypt==4.1.3
python-multipart==0.0.9

# Async HTTP test
httpx==0.27.0
pytest-asyncio==0.23.0
aiosqlite==0.20.0       # Test với SQLite in-memory

# Rate limiting
slowapi==0.1.9           # FastAPI rate limiter (optional)
```

---

## 🔗 Quan hệ với các Round khác

| Round | Liên quan | Chi tiết |
|---|---|---|
| **Round 1 (Frontend)** | Gọi API từ Round 2 | Frontend gọi các endpoint này |
| **Round 3 (Database)** | Phụ thuộc | Models + Repositories đã có |
| **Round 4 (AI Models)** | Chạy song song | Chung `main.py`, AI routers đã register |
| **Round 5 (Upgrade)** | Mở rộng | Có thể thêm caching, WebSocket real-time |
