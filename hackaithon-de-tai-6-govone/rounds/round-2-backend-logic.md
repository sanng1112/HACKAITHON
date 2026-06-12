# Round 2: Backend - Xử lý Logic nghiệp vụ (Business Logic Layer)

**Người phụ trách:** Backend Developer 1 (Người B)

---

## Mục tiêu tổng quan

Xây dựng tầng **Business Logic** cho hệ thống GovOne - xử lý tất cả các nghiệp vụ hành chính công. Round này bao gồm các API endpoints, service layer, validation, workflow xử lý hồ sơ, và tích hợp giữa Frontend và Database.

Hoàn thành Round 2 đồng nghĩa với việc **toàn bộ logic nghiệp vụ hoạt động hoàn chỉnh**, các API có thể phục vụ Frontend, và dữ liệu được xử lý đúng quy trình.

---

## 📋 Danh sách công việc chi tiết

### 2.1 Thiết lập dự án Backend

- [ ] Chọn framework backend (khuyến nghị: **FastAPI** cho Python, hoặc **NestJS** cho Node.js)
- [ ] Cấu hình project structure theo mô hình layered architecture

### 2.2 Hệ thống Xác thực & Phân quyền

- [ ] **Đăng ký người dùng**: API `POST /api/auth/register`
  - Validate thông tin (email, số CMND/CCCD, số điện thoại)
  - Hash mật khẩu (bcrypt), gán role mặc định (citizen)
- [ ] **Đăng nhập**: API `POST /api/auth/login`
  - Xác thực thông tin, tạo JWT access token + refresh token
- [ ] **Refresh token**: API `POST /api/auth/refresh`
- [ ] **Lấy thông tin user hiện tại**: API `GET /api/auth/me`
- [ ] **Xác thực JWT middleware**: kiểm tra token trên mọi request cần bảo vệ
- [ ] **Phân quyền (Role-based)**: middleware kiểm tra role (citizen/officer/admin)
- [ ] **Logout**: vô hiệu hoá token

### 2.3 Quản lý Hồ sơ Hành chính

- [ ] **Tạo hồ sơ mới**: API `POST /api/ho-so`
  - Validate các trường bắt buộc, sinh mã hồ sơ tự động, gán trạng thái `CHO_TIEP_NHAN`
- [ ] **Danh sách hồ sơ**: API `GET /api/ho-so` (phân trang, filter, phân quyền)
- [ ] **Chi tiết hồ sơ**: API `GET /api/ho-so/:id`
- [ ] **Cập nhật hồ sơ**: API `PUT /api/ho-so/:id` (chỉ khi trạng thái `CHO_TIEP_NHAN`)
- [ ] **Upload tài liệu**: API `POST /api/ho-so/:id/upload` (kiểm tra file, lưu file)
- [ ] **Đóng/hoàn tất hồ sơ**: API `POST /api/ho-so/:id/dong` -> `CHO_XU_LY`

### 2.4 Workflow Xử lý Hồ sơ (State Machine)

Quy trình trạng thái: `CHO_TIEP_NHAN -> CHO_XU_LY -> DANG_XU_LY -> (DA_XU_LY / TU_CHOI / CHO_BO_SUNG) -> DA_BO_SUNG -> DANG_XU_LY`

- [ ] **Tiếp nhận hồ sơ**: cán bộ nhận hồ sơ, chuyển `CHO_XU_LY` -> `DANG_XU_LY`
- [ ] **Phê duyệt**: API `PUT /api/ho-so/:id/phe-duyet` -> `DA_XU_LY`
- [ ] **Từ chối**: API `PUT /api/ho-so/:id/tu-choi` -> `TU_CHOI`, kèm lý do
- [ ] **Yêu cầu bổ sung**: API `PUT /api/ho-so/:id/yeu-cau-bo-sung` -> `CHO_BO_SUNG`
- [ ] **Gửi thông báo tự động**: khi trạng thái thay đổi
- [ ] **Audit trail**: ghi lại lịch sử thay đổi trạng thái

### 2.5 Quản lý Lịch hẹn

- [ ] **Tạo lịch hẹn**: API `POST /api/lich-hen` (kiểm tra trùng lịch)
- [ ] **Danh sách lịch hẹn**: API `GET /api/lich-hen` (filter theo ngày, trạng thái)
- [ ] **Xác nhận lịch hẹn**: API `PUT /api/lich-hen/:id`
- [ ] **Huỷ lịch hẹn**: API `DELETE /api/lich-hen/:id` (chỉ trước 24h)

### 2.6 Quản lý Thông báo

- [ ] **Tạo thông báo**: API `POST /api/thong-bao` (gửi cá nhân hoặc tất cả)
- [ ] **Danh sách thông báo**: API `GET /api/thong-bao` (phân trang, filter)
- [ ] **Đánh dấu đã đọc**: API `PUT /api/thong-bao/:id/da-doc`

### 2.7 Middleware & Xử lý lỗi

- [ ] **Global exception handler**: bắt tất cả lỗi, trả về format chuẩn
- [ ] **Request validation**: validate input (Pydantic hoặc class-validator)
- [ ] **Logging middleware**: ghi log mọi request
- [ ] **CORS middleware**: cho phép frontend gọi API
- [ ] **Rate limiting**: giới hạn request để tránh spam

Response format chuẩn:
```json
{
  "success": true,
  "data": {},
  "error": { "code": "ERROR_CODE", "message": "Chi tiết lỗi" },
  "pagination": { "page": 1, "limit": 20, "total": 100 }
}
```

---

## 🧪 Tiêu chí hoàn thành (Definition of Done)

1. ✅ Tất cả API endpoints hoạt động và trả về đúng response format
2. ✅ Authentication & Authorization hoạt động đúng (JWT, roles)
3. ✅ Workflow trạng thái hồ sơ đúng quy trình (state machine)
4. ✅ CRUD đầy đủ cho: hồ sơ, lịch hẹn, thông báo, người dùng
5. ✅ Validation chặt chẽ ở tất cả đầu vào
6. ✅ Có ít nhất 80% unit test coverage cho services
7. ✅ Tài liệu API (Swagger/OpenAPI) tự động
8. ✅ Error handling xuyên suốt, không crash server

---

## 🚀 Tech Stack đề xuất

- **Framework:** FastAPI (Python) hoặc NestJS (Node.js/TypeScript)
- **Xác thực:** JWT (PyJWT / jsonwebtoken) + bcrypt
- **ORM:** SQLAlchemy + Alembic (Python) hoặc Prisma (Node.js)
- **Validation:** Pydantic (Python) / class-validator (Node.js)
- **Documentation:** Swagger/OpenAPI (tự động với FastAPI/NestJS)
- **Testing:** Pytest (Python) / Jest (Node.js)
- **File storage:** Local / MinIO / AWS S3

---

## 🔗 Phụ thuộc (Dependencies)

- **Round 3 (Database)** phải hoàn thành trước để có schema & migrations
- **Round 4 (Models)** cần API từ round này để tích hợp kết quả AI
- Có thể làm việc song song với Round 3 nếu define schema trước

---

## 📂 File cần tạo

```
backend/
├── src/
│   ├── api/             # auth.py, ho_so.py, lich_hen.py, thong_bao.py
│   ├── services/        # auth_service.py, ho_so_service.py, ...
│   ├── models/          # user.py, ho_so.py, lich_hen.py, thong_bao.py
│   ├── middleware/      # auth_middleware.py, error_handler.py
│   ├── config/          # settings.py
│   └── utils/           # helpers.py
├── tests/               # test_auth.py, test_ho_so.py, ...
├── main.py
└── requirements.txt
```
