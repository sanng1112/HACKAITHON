# API Design — Thiết kế REST API

## Base URL

```
Development: http://localhost:8000/api
Production:  https://govone.vn/api
```

## Response Format

Mọi response tuân theo format chuẩn:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "pagination": null
}
```

### Thành công

```json
{
  "success": true,
  "data": { "id": "uuid", "ho_ten": "Nguyễn Văn A" },
  "error": null,
  "pagination": null
}
```

### Lỗi

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "HO_SO_NOT_FOUND",
    "message": "Không tìm thấy hồ sơ với mã HS-2026-0001"
  },
  "pagination": null
}
```

### Danh sách (có phân trang)

```json
{
  "success": true,
  "data": [ ... ],
  "error": null,
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 156,
    "total_pages": 8
  }
}
```

## Authentication

### Login
```
POST /api/auth/login
Content-Type: application/json

Request:
{
  "email": "user@govone.vn",
  "password": "password123"
}

Response 200:
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
      "id": "uuid",
      "email": "user@govone.vn",
      "ho_ten": "Nguyễn Văn A",
      "role": "citizen"
    }
  }
}

Response 401:
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Email hoặc mật khẩu không đúng"
  }
}
```

### Register
```
POST /api/auth/register

Request:
{
  "email": "new@govone.vn",
  "password": "password123",
  "ho_ten": "Nguyễn Văn A",
  "so_cccd": "079201000123",
  "so_dien_thoai": "0912345678"
}

Response 201:
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "new@govone.vn",
    "ho_ten": "Nguyễn Văn A",
    "role": "citizen",
    "created_at": "2026-06-12T00:00:00Z"
  }
}

Response 409:
{
  "success": false,
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "Email đã được đăng ký"
  }
}
```

### Token Management
```
POST /api/auth/refresh
Authorization: Bearer <refresh_token>

Response 200:
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "expires_in": 1800
  }
}
```

```
GET /api/auth/me
Authorization: Bearer <access_token>

Response 200:
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@govone.vn",
    "ho_ten": "Nguyễn Văn A",
    "role": "citizen",
    "so_cccd": "079201000123",
    "trang_thai": "active"
  }
}
```

```
POST /api/auth/change-password
Authorization: Bearer <access_token>

Request:
{
  "current_password": "old123",
  "new_password": "new456"
}

Response 200:
{ "success": true, "data": { "message": "Đổi mật khẩu thành công" } }
```

### Authorization Header
Tất cả request cần xác thực phải gửi:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

## API Endpoints

### Hồ sơ (HoSo)

#### GET /api/ho-so — Danh sách hồ sơ
```
Query: ?page=1&limit=20&trang_thai=DANG_XU_LY&loai_thu_tuc=cap-giay-phep&sort_by=ngay_nop&sort_order=desc
Authorization: Bearer <token>

Response 200:
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "ma_ho_so": "HS-2026-0001",
      "loai_thu_tuc": "cap-giay-phep",
      "trang_thai": "DANG_XU_LY",
      "ngay_nop": "2026-06-12T00:00:00Z",
      "nguoi_nop": { "id": "uuid", "ho_ten": "Nguyễn Văn A" }
    }
  ],
  "pagination": { "page": 1, "limit": 20, "total": 156, "total_pages": 8 }
}
```

#### POST /api/ho-so — Tạo hồ sơ mới
```
Authorization: Bearer <token> (role: citizen)

Request:
{
  "loai_thu_tuc": "cap-giay-phep",
  "noi_dung": "Xin cấp giấy phép xây dựng cho nhà ở tại 123 Lê Lợi"
}

Response 201:
{
  "success": true,
  "data": {
    "id": "uuid",
    "ma_ho_so": "HS-2026-0042",
    "loai_thu_tuc": "cap-giay-phep",
    "trang_thai": "CHO_TIEP_NHAN",
    "ngay_nop": "2026-06-12T10:30:00Z"
  }
}
```

#### GET /api/ho-so/:id — Chi tiết hồ sơ
```
Authorization: Bearer <token>

Response 200:
{
  "success": true,
  "data": {
    "id": "uuid",
    "ma_ho_so": "HS-2026-0042",
    "loai_thu_tuc": "cap-giay-phep",
    "noi_dung": "Xin cấp giấy phép xây dựng...",
    "trang_thai": "CHO_TIEP_NHAN",
    "nguoi_nop": { "id": "uuid", "ho_ten": "Nguyễn Văn A" },
    "nguoi_xu_ly": null,
    "tai_lieu": [
      { "id": "uuid", "ten_file": "cccd.pdf", "loai_file": "application/pdf" }
    ],
    "lich_su": [
      { "hanh_dong": "TAO_MOI", "trang_thai_moi": "CHO_TIEP_NHAN", "created_at": "..." }
    ]
  }
}
```

#### PUT /api/ho-so/:id — Cập nhật hồ sơ
```
Authorization: Bearer <token> (chủ hồ sơ, chỉ khi CHO_TIEP_NHAN)

Request:
{
  "noi_dung": "Nội dung đã chỉnh sửa"
}

Response 200:
{ "success": true, "data": { "message": "Cập nhật thành công" } }
```

#### POST /api/ho-so/:id/upload — Upload tài liệu
```
Authorization: Bearer <token> (chủ hồ sơ)
Content-Type: multipart/form-data

Form fields: file=<binary>, loai="cccd"

Response 201:
{
  "success": true,
  "data": {
    "id": "uuid",
    "ten_file": "cccd_mat_truoc.jpg",
    "loai_file": "image/jpeg",
    "kich_thuoc": 245760,
    "duong_dan": "/uploads/2026/06/cccd_mat_truoc.jpg"
  }
}
```

#### POST /api/ho-so/:id/submit — Nộp hồ sơ
```
Authorization: Bearer <token> (chủ hồ sơ)

Response 200:
{
  "success": true,
  "data": {
    "id": "uuid",
    "trang_thai": "CHO_XU_LY",
    "message": "Hồ sơ đã được nộp, chờ cán bộ tiếp nhận"
  }
}
```

### Xử lý hồ sơ (Officer Actions)

#### PUT /api/ho-so/:id/tiep-nhan
```
Authorization: Bearer <token> (role: officer)

Request: {} (optional body for notes)

Response 200:
{
  "success": true,
  "data": {
    "id": "uuid",
    "trang_thai": "DANG_XU_LY",
    "nguoi_xu_ly": { "id": "uuid", "ho_ten": "Trần Văn B" }
  }
}
```

#### PUT /api/ho-so/:id/phe-duyet
```
Authorization: Bearer <token> (role: officer, người đang xử lý)

Request:
{
  "ghi_chu": "Đã kiểm tra đầy đủ, hợp lệ"
}

Response 200:
{
  "success": true,
  "data": {
    "id": "uuid",
    "trang_thai": "DA_XU_LY",
    "message": "Hồ sơ đã được phê duyệt"
  }
}
```

#### PUT /api/ho-so/:id/tu-choi
```
Authorization: Bearer <token> (role: officer)

Request:
{
  "ly_do": "Thiếu giấy xác nhận quyền sử dụng đất"
}

Response 200:
{
  "success": true,
  "data": {
    "id": "uuid",
    "trang_thai": "TU_CHOI",
    "message": "Hồ sơ đã bị từ chối"
  }
}
```

#### PUT /api/ho-so/:id/yeu-cau-bo-sung
```
Authorization: Bearer <token> (role: officer)

Request:
{
  "yeu_cau": [
    { "ten_tai_lieu": "Giấy xác nhận quyền sử dụng đất", "ghi_chu": "Bản sao công chứng" },
    { "ten_tai_lieu": "CMND/CCCD photo", "ghi_chu": "Cả 2 mặt" }
  ]
}

Response 200:
{
  "success": true,
  "data": {
    "id": "uuid",
    "trang_thai": "CHO_BO_SUNG",
    "message": "Đã gửi yêu cầu bổ sung"
  }
}
```

#### GET /api/ho-so/:id/lich-su
```
Authorization: Bearer <token> (role: officer/admin)

Response 200:
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "hanh_dong": "TIEP_NHAN",
      "trang_thai_cu": "CHO_XU_LY",
      "trang_thai_moi": "DANG_XU_LY",
      "nguoi_thuc_hien": { "ho_ten": "Trần Văn B" },
      "ghi_chu": "",
      "created_at": "2026-06-12T10:35:00Z"
    }
  ]
}
```

### Lịch hẹn (LichHen)

#### GET /api/lich-hen — Danh sách lịch hẹn
```
Query: ?page=1&limit=20&trang_thai=CHO_XAC_NHAN&from_date=2026-06-01&to_date=2026-06-30
Authorization: Bearer <token>

Response 200:
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "tieu_de": "Nộp hồ sơ cấp giấy phép",
      "ngay_hen": "2026-06-15",
      "gio_hen": "09:00",
      "trang_thai": "CHO_XAC_NHAN",
      "can_bo": { "ho_ten": "Trần Văn B" }
    }
  ],
  "pagination": { "page": 1, "limit": 20, "total": 5, "total_pages": 1 }
}
```

#### POST /api/lich-hen — Tạo lịch hẹn
```
Authorization: Bearer <token> (role: citizen)

Request:
{
  "tieu_de": "Nộp hồ sơ cấp giấy phép",
  "ngay_hen": "2026-06-15",
  "gio_hen": "09:00",
  "ghi_chu": "Mang theo CCCD và sổ hộ khẩu"
}

Response 201:
{
  "success": true,
  "data": {
    "id": "uuid",
    "tieu_de": "Nộp hồ sơ cấp giấy phép",
    "ngay_hen": "2026-06-15",
    "gio_hen": "09:00",
    "trang_thai": "CHO_XAC_NHAN"
  }
}

Response 409:
{
  "success": false,
  "error": {
    "code": "SCHEDULE_CONFLICT",
    "message": "Khung giờ này đã có lịch hẹn khác"
  }
}
```

#### PUT /api/lich-hen/:id — Cập nhật lịch hẹn
```
Authorization: Bearer <token> (chủ lịch hoặc officer)

Request:
{
  "trang_thai": "DA_XAC_NHAN",
  "can_bo_id": "uuid"
}

Response 200:
{ "success": true, "data": { "message": "Cập nhật thành công" } }
```

#### DELETE /api/lich-hen/:id — Hủy lịch hẹn
```
Authorization: Bearer <token> (chủ lịch)

Response 200:
{ "success": true, "data": { "message": "Đã hủy lịch hẹn" } }

Response 422:
{
  "success": false,
  "error": {
    "code": "BUSINESS_RULE_VIOLATION",
    "message": "Chỉ được hủy lịch trước 24 giờ"
  }
}
```

### Thông báo (ThongBao)

#### GET /api/thong-bao — Danh sách thông báo
```
Query: ?page=1&limit=20&da_doc=false&loai=ho_so
Authorization: Bearer <token>

Response 200:
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "tieu_de": "Hồ sơ HS-2026-0042 đã được phê duyệt",
      "noi_dung": "Hồ sơ của bạn đã được cán bộ Trần Văn B phê duyệt.",
      "loai": "ho_so",
      "da_doc": false,
      "created_at": "2026-06-12T14:00:00Z"
    }
  ],
  "pagination": { "page": 1, "limit": 20, "total": 12, "total_pages": 1 }
}
```

#### POST /api/thong-bao — Tạo thông báo
```
Authorization: Bearer <token> (role: officer)

Request:
{
  "user_id": "uuid",          // null = gửi tất cả
  "tieu_de": "Lịch nghỉ lễ",
  "noi_dung": "UBND phường nghỉ từ 30/4 đến 3/5",
  "loai": "he_thong"
}

Response 201:
{
  "success": true,
  "data": { "id": "uuid", "message": "Thông báo đã được gửi" }
}
```

#### PUT /api/thong-bao/:id/da-doc — Đánh dấu đã đọc
```
Authorization: Bearer <token>

Response 200:
{ "success": true, "data": { "message": "Đã đánh dấu đã đọc" } }
```

### AI Services (Internal)

#### POST /api/ai/ocr — OCR ảnh giấy tờ
```
Content-Type: multipart/form-data
Form: file=<binary>, loai_giay_to="cccd"

Response 200:
{
  "success": true,
  "data": {
    "text": "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n...",
    "fields": {
      "ho_ten": "Nguyễn Văn A",
      "ngay_sinh": "15/06/1961",
      "so_cccd": "079201000123",
      "ngay_cap": "01/07/2021",
      "noi_cap": "Cục Cảnh sát QLHC về TTXH"
    },
    "confidence": 0.97,
    "loai_giay_to": "cccd"
  }
}
```

#### POST /api/ai/stt — Speech-to-Text
```
Content-Type: multipart/form-data
Form: file=<audio.wav>

Response 200:
{
  "success": true,
  "data": {
    "text": "Tôi muốn làm giấy xác nhận tình trạng hôn nhân",
    "confidence": 0.96,
    "duration_seconds": 3.5
  }
}
```

#### POST /api/ai/nlp/classify — Phân loại nội dung
```
Content-Type: application/json

Request:
{ "text": "Tôi muốn làm giấy xác nhận tình trạng hôn nhân" }

Response 200:
{
  "success": true,
  "data": {
    "loai_thu_tuc": "xac-nhan-tinh-trang-hon-nhan",
    "confidence": 0.94,
    "intents": [
      { "label": "xac_nhan_hon_nhan", "score": 0.94 },
      { "label": "khai_sinh", "score": 0.02 }
    ]
  }
}
```

#### POST /api/ai/ekyc/verify — Xác thực CCCD + khuôn mặt
```
Content-Type: multipart/form-data
Form: cccd_image=<file>, face_image=<file>

Response 200:
{
  "success": true,
  "data": {
    "cccd_ocr": { "ho_ten": "Nguyễn Văn A", "so_cccd": "079201000123" },
    "face_match": { "is_match": true, "score": 0.99 },
    "liveness": { "is_live": true, "score": 0.98 },
    "verified": true
  }
}
```

#### POST /api/ai/auto-fill — Tự động điền form
```
Content-Type: multipart/form-data
Form: file=<cccd.jpg>

Response 200:
{
  "success": true,
  "data": {
    "form_fields": {
      "ho_ten": "Nguyễn Văn A",
      "ngay_sinh": "15/06/1961",
      "so_cccd": "079201000123",
      "gioi_tinh": "Nam",
      "quoc_tich": "Việt Nam",
      "que_quan": "Hà Nội"
    },
    "auto_filled_count": 6,
    "needs_manual_count": 1,
    "warnings": [
      { "field": "dia_chi_thuong_tru", "reason": "Không có trong ảnh CCCD" }
    ]
  }
}
```

#### GET /api/ai/task/:id — Kiểm tra async task
```
Response 200:
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "status": "PROCESSING",     // PENDING | PROCESSING | COMPLETED | FAILED
    "progress": 65,
    "result": null,
    "error": null
  }
}
```

#### GET /api/ai/health — AI models health
```
Response 200:
{
  "success": true,
  "data": {
    "ocr": { "loaded": true, "model": "EasyOCR", "version": "1.7.2" },
    "stt": { "loaded": true, "model": "Whisper", "version": "small" },
    "nlp": { "loaded": true, "model": "PhoBERT", "version": "base" },
    "vnpt_api": { "connected": true }
  }
}
```

### System

#### GET /api/health — Health check
```
Response 200:
{
  "success": true,
  "data": {
    "app": "GovOne",
    "version": "0.1.0",
    "uptime": 86400,
    "timestamp": "2026-06-12T10:00:00Z"
  }
}
```

#### GET /api/health/db — Database health
```
Response 200:
{ "success": true, "data": { "status": "connected", "latency_ms": 2 } }
```

---

## Mã lỗi chuẩn

| HTTP | Error Code | Mô tả |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Dữ liệu đầu vào không hợp lệ |
| 401 | `UNAUTHORIZED` | Thiếu hoặc token không hợp lệ |
| 401 | `TOKEN_EXPIRED` | Token hết hạn |
| 403 | `FORBIDDEN` | Không có quyền truy cập |
| 404 | `NOT_FOUND` | Resource không tồn tại |
| 409 | `CONFLICT` | Xung đột dữ liệu |
| 413 | `FILE_TOO_LARGE` | File vượt quá kích thước cho phép |
| 415 | `UNSUPPORTED_FILE_TYPE` | Loại file không được hỗ trợ |
| 422 | `BUSINESS_RULE_VIOLATION` | Vi phạm quy tắc nghiệp vụ |
| 429 | `RATE_LIMITED` | Quá nhiều request |
| 500 | `INTERNAL_ERROR` | Lỗi hệ thống |
| 503 | `SERVICE_UNAVAILABLE` | Service tạm thời không khả dụng |

## Pagination & Filtering

Tất cả `GET /api/*` list endpoint hỗ trợ:

```
Pagination:  ?page=1&limit=20
Sorting:     ?sort_by=created_at&sort_order=desc
Filtering:   ?trang_thai=DANG_XU_LY&from_date=2026-01-01&to_date=2026-06-12
Search:      ?q=Nguyễn Văn A
```

## Rate Limiting

| Role | Limit |
|---|---|
| **Anonymous** | 30 req/phút |
| **Citizen** | 60 req/phút |
| **Officer** | 120 req/phút |
| **Admin** | 300 req/phút |
| **AI endpoints** | 10 req/phút (ocr/stt), 30 req/phút (classify/auto-fill) |
