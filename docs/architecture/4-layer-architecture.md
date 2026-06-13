# 4-Layer Architecture — Kiến trúc 4 tầng

GovOne được thiết kế theo kiến trúc **4 tầng (Layered Architecture)**, mỗi tầng đóng gói một tập trách nhiệm riêng và chỉ giao tiếp với tầng liền kề.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      TẦNG 1 — USER LAYER                             │
│                                                                      │
│  ┌───────────────────┐  ┌───────────────────┐  ┌──────────────────┐ │
│  │  Kiosk Touch      │  │  Web App          │  │  Mobile App      │ │
│  │  Voice-first      │  │  React / Next.js  │  │  React Native    │ │
│  │  Camera + Mic     │  │  Citizen Portal   │  │  Citizen App     │ │
│  │  Scan tray        │  │  Officer Dashboard│  │                  │ │
│  └────────┬──────────┘  └────────┬──────────┘  └────────┬─────────┘ │
│           │                      │                      │           │
├───────────┼──────────────────────┼──────────────────────┼───────────┤
│           │              HTTP REST / WebSocket           │           │
│           └──────────────────────┼──────────────────────┘           │
│                                  │                                   │
├──────────────────────────────────┼───────────────────────────────────┤
│                      TẦNG 2 — AI CORE                                │
│                                                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │ SmartVoice  │ │  Smartbot   │ │ SmartReader │ │    eKYC     │   │
│  │ ─────────── │ │ ─────────── │ │ ─────────── │ │ ─────────── │   │
│  │ STT: >95%   │ │ Intent:>90% │ │ OCR: >95%   │ │ OCR: >98%   │   │
│  │ TTS: natural │ │ Dialog mgmt │ │ Doc AI:>90% │ │ Compare:>99%│   │
│  │ Multi-accent │ │ Multi-turn  │ │ Structured  │ │ Liveness    │   │
│  └──────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                      SmartVision                             │    │
│  │  ───────────────────────────────────────────────────────────│    │
│  │  Classification: >95% | Face Detection: >99% | Sentiment:>85%│   │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                   FALLBACK LAYER (local)                      │    │
│  │  EasyOCR (OCR) | Whisper (STT) | PhoBERT (NLP)              │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                      TẦNG 3 — PROCESSING LAYER                        │
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │  Voice Gateway   │  │  Intent Engine   │  │  Doc Processor   │   │
│  │ ──────────────── │  │ ──────────────── │  │ ──────────────── │   │
│  │ Load balancing   │  │ Intent routing   │  │ OCR orchestration│   │
│  │ Audio streaming  │  │ Dialog state     │  │ Rules engine     │   │
│  │ Session mgmt     │  │ Context tracking │  │ Auto-validation  │   │
│  │ Fallback TTS txt │  │ Multi-turn       │  │ Field extraction │   │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘   │
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │  Auth Service    │  │  HoSo Service    │  │  Sentiment Svc   │   │
│  │ ──────────────── │  │ ──────────────── │  │ ──────────────── │   │
│  │ JWT generation   │  │ State machine    │  │ Face detection   │   │
│  │ Role-based ACL   │  │ Workflow engine  │  │ Emotion classify │   │
│  │ Token refresh    │  │ Audit trail      │  │ Satisfaction log │   │
│  │ Password reset   │  │ Notification     │  │ Real-time report │   │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘   │
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐                         │
│  │  Schedule Svc    │  │  Notify Svc      │                         │
│  │ ──────────────── │  │ ──────────────── │                         │
│  │ Appointment CRUD │  │ Push notification│                         │
│  │ Conflict detect  │  │ Email/SMS        │                         │
│  │ Calendar view    │  │ Read tracking    │                         │
│  └──────────────────┘  └──────────────────┘                         │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                      TẦNG 4 — DATA LAYER                              │
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │  PostgreSQL 15   │  │     Redis        │  │  MinIO / S3      │   │
│  │ ──────────────── │  │ ──────────────── │  │ ──────────────── │   │
│  │ Users            │  │ Session cache    │  │ Document scans   │   │
│  │ HoSo + state     │  │ Celery broker    │  │ Uploaded files   │   │
│  │ LichHen          │  │ Rate limit       │  │ Archived PDF/A   │   │
│  │ ThongBao         │  │ Hot data cache   │  │ Thumbnails       │   │
│  │ Audit log        │  │ Real-time pub/sub│  │                  │   │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                    Knowledge Base                              │    │
│  │ ──────────────────────────────────────────────────────────────│    │
│  │ Thủ tục hành chính (4.000+ TTHC) | FAQs | Hướng dẫn          │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Quy tắc giao tiếp giữa các tầng

| Hướng | Giao thức | Mô tả |
|---|---|---|
| **User → API Gateway** | HTTPS REST + WebSocket | Frontend gọi API qua HTTP, voice streaming qua WebSocket |
| **API Gateway → Services** | Internal HTTP/gRPC | Gateway route request đến service xử lý |
| **Services → AI Core** | HTTPS REST | Service gọi VNPT API hoặc local fallback model |
| **Services → Data** | SQL (PostgreSQL), Redis protocol, S3 API | CRUD qua ORM, cache qua Redis client, file qua S3 SDK |
| **AI Tasks → Queue** | Redis (Celery broker) | Tác vụ nặng được đẩy vào queue, worker xử lý async |

## Mỗi tầng có thể thay thế độc lập

- **Tầng 1:** Có thể thay React bằng Vue/Svelte — miễn gọi đúng API contract
- **Tầng 2:** Có thể chuyển từ VNPT API sang Google Cloud AI/AWS AI — chỉ cần adapter
- **Tầng 3:** Có thể thay FastAPI bằng NestJS — miễn giữ nguyên API contract
- **Tầng 4:** Có thể thay PostgreSQL bằng MySQL, MinIO bằng AWS S3 — qua repository interface
