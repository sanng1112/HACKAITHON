# Round 1: Frontend - Giao diện người dùng

**Người phụ trách:** Frontend Developer (Người A)

---

## Mục tiêu tổng quan

Xây dựng toàn bộ giao diện người dùng (User Interface) cho hệ thống GovOne - Hệ thống quản lý hành chính công thông minh. Round này bao gồm tất cả các trang, components, và trải nghiệm người dùng cho cả **công dân** và **cán bộ**.

Hoàn thành Round 1 đồng nghĩa với việc **toàn bộ giao diện hoạt động hoàn chỉnh**, có thể tương tác, kết nối được với API backend.

---

## 📋 Danh sách công việc chi tiết

### 1.1 Thiết lập dự án Frontend

- [ ] Khởi tạo project với framework **React** (Next.js hoặc Vite + React)
- [ ] Cấu hình TypeScript
- [ ] Thiết lập Tailwind CSS hoặc thư viện UI components
- [ ] Cấu hình routing (React Router / Next.js Router)
- [ ] Thiết lập cấu trúc thư mục

### 1.2 Xác thực & Phân quyền (Authentication & Authorization)

- [ ] Trang **Đăng nhập** (Login) - cả công dân và cán bộ
- [ ] Trang **Đăng ký** (Register) - cho công dân mới
- [ ] Trang **Quên mật khẩu** / Đặt lại mật khẩu
- [ ] Bảo vệ routes dựa trên role (citizen / officer / admin)
- [ ] Lưu & quản lý JWT token (localStorage / httpOnly cookie)
- [ ] Tự động redirect khi token hết hạn

### 1.3 Giao diện dành cho Công dân (Citizen Portal)

- [ ] **Dashboard công dân**: hiển thị thông báo, trạng thái hồ sơ, lịch hẹn
- [ ] **Trang nộp hồ sơ hành chính**: form động nhiều bước (wizard)
  - Chọn loại thủ tục (cấp giấy phép, đăng ký hộ khẩu, xác nhận...)
  - Điền thông tin form
  - Tải lên tài liệu / giấy tờ (upload file)
  - Xác nhận và gửi
- [ ] **Trang tra cứu hồ sơ**: tìm kiếm, xem trạng thái, lịch sử
- [ ] **Trang lịch hẹn làm việc**: đặt lịch, xem lịch, huỷ lịch
- [ ] **Trang thông báo**: danh sách thông báo từ cơ quan
- [ ] **Trang hồ sơ cá nhân**: xem/sửa thông tin cá nhân
- [ ] **Giao diện Kiosk (tra cứu công cộng)**:
  - Màn hình cảm ứng thân thiện
  - Tra cứu hồ sơ bằng mã số
  - In phiếu/số thứ tự

### 1.4 Giao diện dành cho Cán bộ (Officer Dashboard)

- [ ] **Dashboard cán bộ**: thống kê tổng quan (số hồ sơ mới, đang xử lý, đã xong)
- [ ] **Trang quản lý hồ sơ đến**: danh sách hồ sơ cần xử lý
  - Filter theo trạng thái, loại thủ tục, ngày
  - Tìm kiếm nâng cao
- [ ] **Trang xử lý hồ sơ chi tiết**:
  - Xem thông tin hồ sơ, tài liệu đính kèm
  - Phê duyệt / Từ chối (kèm lý do)
  - Yêu cầu bổ sung giấy tờ
  - Ghi chú nội bộ
- [ ] **Trang lịch sử xử lý**: audit trail các thao tác
- [ ] **Trang quản lý lịch hẹn**: xem và xác nhận lịch hẹn công dân
- [ ] **Trang quản lý thông báo**: tạo và gửi thông báo đến công dân

### 1.5 Components dùng chung (Shared Components)

- [ ] **Header/Navbar** responsive (với thông tin người dùng)
- [ ] **Sidebar menu** dành cho cán bộ
- [ ] **Footer**
- [ ] **Loading spinner / skeleton loading**
- [ ] **Modal / Dialog** xác nhận
- [ ] **Toast notification** hiển thị thông báo
- [ ] **Breadcrumb** điều hướng
- [ ] **DataTable / Pagination** với sort, filter
- [ ] **File upload component** với drag & drop, preview
- [ ] **Form components** (Input, Select, DatePicker, TextArea, Checkbox...)
- [ ] **Status badge** hiển thị trạng thái hồ sơ (màu sắc theo từng trạng thái)
- [ ] **Empty state** khi không có dữ liệu
- [ ] **Error boundary** component

### 1.6 Xử lý trạng thái & API Integration

- [ ] Thiết lập **HTTP client** (Axios) với interceptor
- [ ] Xử lý **loading state** cho mỗi trang/component
- [ ] Xử lý **error state** với thông báo thân thiện
- [ ] Xử lý **empty state** khi không có dữ liệu
- [ ] Xử lý **pagination** trên danh sách
- [ ] **Optimistic updates** cho các thao tác nhanh
- [ ] **Polling / WebSocket** cho cập nhật trạng thái real-time

### 1.7 Responsive & Accessibility

- [ ] Giao diện **responsive** (mobile, tablet, desktop)
- [ ] Hỗ trợ **Vietnamese** (i18n nếu cần)
- [ ] Tối ưu **SEO** (nếu là Next.js)
- [ ] **Accessibility** (ARIA labels, keyboard navigation)
- [ ] Tối ưu **performance** (lazy loading, code splitting)

### 1.8 API Contract (đầu vào/đầu ra)

Frontend sẽ gọi các API sau (do Backend cung cấp):

**Auth APIs**
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/auth/login` | Đăng nhập |
| POST | `/api/auth/register` | Đăng ký |
| POST | `/api/auth/refresh` | Refresh token |
| GET  | `/api/auth/me` | Lấy thông tin user hiện tại |

**Hồ sơ APIs**
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET  | `/api/ho-so` | Danh sách hồ sơ |
| POST | `/api/ho-so` | Tạo hồ sơ mới |
| GET  | `/api/ho-so/:id` | Chi tiết hồ sơ |
| PUT  | `/api/ho-so/:id` | Cập nhật hồ sơ |
| POST | `/api/ho-so/:id/upload` | Upload tài liệu |
| POST | `/api/ho-so/:id/dong` | Đóng/hoàn tất hồ sơ |

**Xử lý APIs**
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| PUT  | `/api/ho-so/:id/phe-duyet` | Phê duyệt hồ sơ |
| PUT  | `/api/ho-so/:id/tu-choi` | Từ chối hồ sơ |
| PUT  | `/api/ho-so/:id/yeu-cau-bo-sung` | Yêu cầu bổ sung |

**Lịch hẹn APIs**
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET  | `/api/lich-hen` | Danh sách lịch hẹn |
| POST | `/api/lich-hen` | Tạo lịch hẹn |
| PUT  | `/api/lich-hen/:id` | Cập nhật lịch hẹn |
| DELETE | `/api/lich-hen/:id` | Huỷ lịch hẹn |

**Thông báo APIs**
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET  | `/api/thong-bao` | Danh sách thông báo |
| POST | `/api/thong-bao` | Tạo thông báo |
| PUT  | `/api/thong-bao/:id/da-doc` | Đánh dấu đã đọc |

---

## 🧪 Tiêu chí hoàn thành (Definition of Done)

1. ✅ Tất cả các trang có thể render được với dữ liệu mẫu (mock data)
2. ✅ Kết nối thành công tới API backend (khi backend đã sẵn sàng)
3. ✅ Xử lý đúng 3 trạng thái: loading, error, empty
4. ✅ Responsive trên mobile (>= 375px), tablet, desktop
5. ✅ Form validation hoạt động (required fields, định dạng)
6. ✅ Authentication flow: login -> lưu token -> redirect -> logout
7. ✅ Authorization: công dân chỉ thấy trang công dân, cán bộ chỉ thấy trang cán bộ
8. ✅ Có ít nhất 1 unit test cho component quan trọng
9. ✅ Code được format, không có lỗi ESLint/TypeScript

---

## 🚀 Tech Stack đề xuất

- **Framework:** Next.js 14+ (App Router) hoặc Vite + React
- **Ngôn ngữ:** TypeScript
- **UI:** Tailwind CSS + Shadcn/ui hoặc Ant Design
- **State:** Zustand hoặc Redux Toolkit
- **HTTP Client:** Axios
- **Form:** React Hook Form + Zod
- **Testing:** Vitest + React Testing Library

---

## 🔗 Phụ thuộc (Dependencies)

- Round 2 (Backend Logic) phải hoàn thành API endpoints để tích hợp
- Có thể làm việc song song với Round 2 nếu dùng mock data trước
