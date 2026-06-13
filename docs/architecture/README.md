# GovOne — Kiến trúc Hệ thống

> Tài liệu kiến trúc kỹ thuật cho hệ thống GovOne — Hành chính công Thông minh

## Mục lục

| File | Nội dung |
|---|---|
| [system-overview.md](system-overview.md) | Tổng quan hệ thống: mục tiêu, phạm vi, người dùng, ranh giới |
| [4-layer-architecture.md](4-layer-architecture.md) | Kiến trúc 4 tầng: User → AI Core → Processing → Data |
| [data-flow.md](data-flow.md) | Luồng dữ liệu: Voice-first citizen + OCR pipeline officer |
| [api-design.md](api-design.md) | Thiết kế REST API: endpoints, auth, response format |
| [deployment.md](deployment.md) | Kiến trúc triển khai: Docker, services, scaling |

## Sơ đồ tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│                     GOVONE — KIẾN TRÚC TỔNG THỂ                  │
├─────────────────────────────────────────────────────────────────┤
│  TẦNG 1: USER LAYER           Kiosk • Web App • Mobile App      │
│  TẦNG 2: AI CORE             7 VNPT APIs • Fallback Models      │
│  TẦNG 3: PROCESSING LAYER    Gateway • Engine • Processor       │
│  TẦNG 4: DATA LAYER          PostgreSQL • Redis • MinIO • KB    │
└─────────────────────────────────────────────────────────────────┘
```

## Đối tượng người dùng

| Vai trò | Kênh truy cập | Tính năng chính |
|---|---|---|
| **Công dân** | Kiosk touch (voice-first), Web, Mobile | Tra cứu thủ tục, nộp hồ sơ, đặt lịch hẹn, nhận thông báo |
| **Cán bộ** | Web Dashboard | Tiếp nhận & xử lý hồ sơ, quản lý lịch hẹn, gửi thông báo, báo cáo |
| **Quản trị viên** | Web Admin | Quản lý người dùng, cấu hình hệ thống, audit log |
| **Hệ thống AI** | Internal APIs | OCR, STT, NLP, eKYC, Sentiment — tự động hóa xử lý |

## Tech Stack quyết định

| Tầng | Công nghệ | Lý do |
|---|---|---|
| **Frontend** | Next.js 14 + TypeScript + Tailwind | SSR/SSG cho performance, type safety, rapid UI |
| **Backend API** | FastAPI (Python 3) | Async native, auto OpenAPI, Pydantic validation |
| **Database** | PostgreSQL 15 + SQLAlchemy 2.0 | ACID, full-text search, JSONB, mature ORM |
| **Cache/Queue** | Redis | Session store, Celery broker, rate limiting |
| **Object Storage** | MinIO (S3-compatible) | Document scans, on-premise deployable |
| **AI/ML** | PyTorch + EasyOCR + Whisper + PhoBERT | Local fallback khi VNPT API unavailable |
| **Container** | Docker + Docker Compose | Reproducible dev/prod, service isolation |

## Nguyên tắc thiết kế

1. **Separation of Concerns** — mỗi tầng có trách nhiệm rõ ràng, giao tiếp qua interface
2. **API-first** — mọi tính năng được expose qua REST API trước khi build UI
3. **Graceful Degradation** — fallback từ VNPT APIs xuống local models khi cần
4. **Stateless Services** — backend không lưu session, scale ngang dễ dàng
5. **Audit Everything** — mọi thay đổi trạng thái hồ sơ được ghi log
