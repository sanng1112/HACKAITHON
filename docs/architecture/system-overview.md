# System Overview — Tổng quan Hệ thống

## Mục tiêu hệ thống

GovOne là nền tảng quản lý hành chính công thông minh, tích hợp AI để tự động hóa toàn bộ quy trình từ tiếp nhận đến trả kết quả thủ tục hành chính, phục vụ đồng thời **người dân** và **cán bộ**.

## Phạm vi

### Trong phạm vi
- Tiếp nhận hồ sơ hành chính qua voice-first (Kiosk) và web form
- OCR & số hóa hồ sơ giấy tờ (CCCD, sổ hộ khẩu, giấy khai sinh...)
- Xác thực danh tính qua eKYC (face compare + liveness detection)
- Quy trình xử lý hồ sơ (state machine: tiếp nhận → xử lý → duyệt/từ chối/bổ sung)
- Đo lường mức độ hài lòng qua Sentiment AI (camera)
- Dashboard thống kê & báo cáo cho cán bộ

### Ngoài phạm vi
- Ký số điện tử (tích hợp sau)
- Thanh toán phí/lệ phí trực tuyến (tích hợp sau)
- Liên thông dữ liệu giữa các cấp chính quyền (phase 2)
- Ứng dụng di động native (React Native — phase 2)

## Người dùng & Vai trò

### Citizen (Công dân)
- **Kênh:** Kiosk (chính), Web App, Mobile App
- **Tương tác:** Voice-first — nói thay vì gõ
- **Tác vụ:** Tra cứu thủ tục, nộp hồ sơ, upload giấy tờ, đặt lịch hẹn, nhận thông báo kết quả

### Officer (Cán bộ)
- **Kênh:** Web Dashboard
- **Tương tác:** Form-based + scan
- **Tác vụ:** Tiếp nhận hồ sơ, kiểm tra & đối chiếu, phê duyệt/từ chối/yêu cầu bổ sung, tạo thông báo, xem báo cáo

### Admin (Quản trị viên)
- **Kênh:** Web Admin
- **Tương tác:** Form-based
- **Tác vụ:** Quản lý users, phân quyền, cấu hình loại thủ tục, xem audit log

### AI System (Hệ thống AI)
- **Kênh:** Internal REST APIs
- **Tương tác:** Programmatic
- **Tác vụ:** OCR, STT, NLP, eKYC, Sentiment analysis

## Ranh giới hệ thống

```
┌──────────────────────────────────────────────────────────────────────┐
│                          GOVONE SYSTEM                                │
│                                                                       │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌───────┐  │
│  │  Kiosk  │   │Web App  │   │ Mobile  │   │  Admin  │   │  API  │  │
│  └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘   └───┬───┘  │
│       │             │             │             │            │       │
│       └─────────────┴─────────────┴─────────────┴────────────┘       │
│                                 │                                     │
│                          ┌──────┴──────┐                              │
│                          │  API Gateway │                             │
│                          └──────┬──────┘                              │
│                 ┌───────────────┼───────────────┐                     │
│          ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐             │
│          │  Auth Svc   │ │  HoSo Svc  │ │  AI Svc    │             │
│          └──────┬──────┘ └──────┬──────┘ └──────┬──────┘             │
│                 │               │               │                     │
│          ┌──────┴───────────────┴───────────────┴──────┐             │
│          │              DATA LAYER                      │             │
│          │  PostgreSQL │ Redis │ MinIO │ Knowledge Base │             │
│          └──────────────────────────────────────────────┘             │
└──────────────────────────────────────────────────────────────────────┘
      │                                  │                              │
      ▼                                  ▼                              │
┌──────────────┐              ┌──────────────────┐                     │
│  VNPT APIs   │              │  Fallback Models  │                    │
│ SmartVoice   │              │  EasyOCR / Whisper │                   │
│ Smartbot     │              │  PhoBERT           │                    │
│ SmartReader  │              └──────────────────┘                     │
│ eKYC         │                                                       │
│ SmartVision  │                                                       │
└──────────────┘                                                       │
```

## Yêu cầu phi chức năng

| Yêu cầu | Chỉ tiêu |
|---|---|
| **Độ sẵn sàng** | 99.5% (downtime < 3.6 giờ/tháng) |
| **Thời gian phản hồi API** | p95 < 200ms (CRUD), p95 < 5s (AI tasks) |
| **Bảo mật** | JWT + RBAC, HTTPS, mã hóa dữ liệu nhạy cảm |
| **Tuân thủ** | Nghị định 130/2018/NĐ-CP (chữ ký số), Nghị định 13/2023/NĐ-CP (dữ liệu cá nhân) |
| **Khả năng mở rộng** | 10.000 concurrent users, 50.000 hồ sơ/ngày |
| **Khả năng khôi phục** | RPO < 1 giờ, RTO < 4 giờ |
