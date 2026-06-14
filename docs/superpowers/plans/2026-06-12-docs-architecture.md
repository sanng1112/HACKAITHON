# Docs Architecture — Khung kiến trúc tổng quan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hoàn thiện thư mục `docs/architecture/` với 6 file tài liệu kiến trúc: index tổng quan, system overview, kiến trúc 4 tầng, luồng dữ liệu, thiết kế API, kiến trúc triển khai.

**Architecture:** Mỗi file là một tài liệu markdown độc lập, liên kết chéo qua mục lục. `README.md` là hub chính liệt kê tất cả. Các file còn lại đi sâu từng khía cạnh kiến trúc GovOne.

**Tech Stack:** Markdown — không code, thuần tài liệu.

---

## Task 1: Tạo docs/architecture/README.md — Index & tổng quan

**Files:**
- Create: `docs/architecture/README.md`

- [ ] **Step 1: Tạo README.md**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add docs/architecture/README.md
git commit -m "docs: architecture index and overview

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Task 2: Tạo docs/architecture/system-overview.md — Tổng quan hệ thống

**Files:**
- Create: `docs/architecture/system-overview.md`

- [ ] **Step 1: Tạo system-overview.md**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add docs/architecture/system-overview.md
git commit -m "docs: system overview with scope, users, and boundaries

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Task 3: Tạo docs/architecture/4-layer-architecture.md — Kiến trúc 4 tầng

**Files:**
- Create: `docs/architecture/4-layer-architecture.md`

- [ ] **Step 1: Tạo 4-layer-architecture.md**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add docs/architecture/4-layer-architecture.md
git commit -m "docs: 4-layer architecture with component details and communication rules

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Task 4: Tạo docs/architecture/data-flow.md — Luồng dữ liệu

**Files:**
- Create: `docs/architecture/data-flow.md`

- [ ] **Step 1: Tạo data-flow.md**

```markdown
# Data Flow — Luồng Dữ liệu

GovOne có **2 luồng dữ liệu chính** hoạt động song song: Voice-first cho người dân và OCR pipeline cho cán bộ.

## Luồng 1: Citizen Voice-First

```
CÔNG DÂN
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 1: TIẾP NHẬN                                               │
│ Camera phát hiện người → SmartVoice TTS: "Xin chào! Bác cần gì?"│
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 2: VOICE INPUT                                             │
│ Người dân nói → Micro → SmartVoice STT → text (độ chính xác>95%)│
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 3: INTENT PROCESSING                                       │
│ Smartbot NLP: phân tích ý định → xác định thủ tục cần làm        │
│ Intent Engine: route đến đúng workflow xử lý                     │
└───────┬─────────────────────┬───────────────────────────────────┘
        │                     │
        ▼                     ▼
  ┌──────────┐        ┌──────────────┐
  │ Cần giấy │        │ Không cần    │
  │ tờ?      │        │ giấy tờ      │
  └────┬─────┘        └──────┬───────┘
       │                     │
       ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│ BƯỚC 4: eKYC     │  │ BƯỚC 5: TTS     │
│ Scan CCCD → OCR  │  │ TTS đọc kết quả  │
│ Face compare     │  │ tra cứu          │
│ Liveness check   │  └──────────────────┘
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 5: AUTO-FILL                                               │
│ OCR data → map vào form → hiển thị để công dân xác nhận          │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 6: SUBMIT                                                 │
│ Công dân xác nhận → Submit form → Lưu HoSo (DB)                 │
│ → Sinh mã hồ sơ → Gửi thông báo đến cán bộ                      │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 7: SENTIMENT                                               │
│ SmartVision: phân tích biểu cảm khuôn mặt → ghi nhận hài lòng   │
│ → Lưu vào DB → Dashboard cán bộ cập nhật real-time              │
└──────────────────────────────────────────────────────────────────┘
```

### Dữ liệu đầu vào/ra — Citizen Flow

| Bước | Input | Output | Công nghệ |
|---|---|---|---|
| 1 | Camera frame | Người detected + TTS greeting | SmartVision Face, SmartVoice TTS |
| 2 | Audio stream (16kHz mono) | Text tiếng Việt | SmartVoice STT |
| 3 | Text query | Intent + parameters | Smartbot NLP |
| 4 | Ảnh CCCD + face | OCR data + match score | eKYC OCR, Compare, Liveness |
| 5 | OCR fields + form template | Pre-filled form JSON | Field mapping engine |
| 6 | Form JSON | HoSo record (DB) | HoSo Service |
| 7 | Camera frame | Sentiment score (0-100) | SmartVision Sentiment |

---

## Luồng 2: Officer OCR Pipeline

```
CÁN BỘ
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 1: NẠP HỒ SƠ                                              │
│ Scan từ máy scanner / Upload file PDF, JPG, PNG                 │
│ → Lưu raw file vào MinIO → Tạo HoSoTaiLieu record               │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 2: PHÂN LOẠI                                              │
│ SmartVision Classification: nhận diện loại giấy tờ               │
│ → CCCD, CMND, sổ hộ khẩu, giấy khai sinh, bằng cấp, hóa đơn... │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 3: OCR & BÓC TÁCH                                         │
│ SmartReader OCR: nhận dạng text (>95%)                          │
│ SmartReader Doc AI: bóc tách thông tin có cấu trúc              │
│ → JSON fields: {hoten, ngaysinh, cccd, diachi...}              │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 4: ĐỐI CHIẾU                                              │
│ eKYC OCR: extract CCCD từ ảnh → so sánh với DB dân cư           │
│ Rules Engine: kiểm tra logic (họ tên khớp? ngày sinh hợp lệ?)   │
│ → Kết quả: KHOP / CANH_BAO / LOI                                │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
              ┌──────────┐    ┌──────────────┐
              │ KHOP     │    │ CANH BAO/LOI │
              └────┬─────┘    └──────┬───────┘
                   │                 │
                   ▼                 ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│ BƯỚC 5a: DUYỆT          │  │ BƯỚC 5b: SỬA / BỔ SUNG  │
│ Cán bộ kiểm tra → Duyệt │  │ Dashboard hiện cảnh báo  │
│ → HoSo status: DA_XU_LY │  │ → Sửa thủ công hoặc     │
└──────────────────────────┘  │ yêu cầu bổ sung         │
                              └──────────────────────────┘
```

### Dữ liệu đầu vào/ra — Officer Flow

| Bước | Input | Output | Công nghệ |
|---|---|---|---|
| 1 | File scan (PDF/JPG/PNG) | Raw file path (MinIO) + HoSoTaiLieu record | File upload, MinIO |
| 2 | Image byte stream | Document type label | SmartVision Classification |
| 3 | Image byte stream | Structured fields JSON | SmartReader OCR + Doc AI |
| 4 | OCR JSON + CCCD data | Match result (KHOP/CANH_BAO/LOI) | Rules Engine, eKYC |
| 5 | Match result + officer decision | Updated HoSo status (DB) | HoSo Service |

---

## Luồng 3: State Machine Hồ sơ

```
                    ┌──────────────┐
                    │ CHO_TIEP_NHAN│ ← Tạo mới
                    └──────┬───────┘
                           │ Cán bộ nhận
                           ▼
                    ┌──────────────┐
                    │  CHO_XU_LY   │
                    └──────┬───────┘
                           │ Cán bộ bắt đầu xử lý
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
              │              ┌──────────────┐
              │              │ CHO_BO_SUNG  │
              │              │ (Y/c bổ sung)│
              │              └──────┬───────┘
              │                     │ Công dân bổ sung
              │                     ▼
              │              ┌──────────────┐
              │              │ DA_BO_SUNG   │
              │              └──────┬───────┘
              │                     │ Trở lại xử lý
              │                     └─────────┐
              │                               │
              └───────────────────────────────┘
                                   │
                                   ▼
                            ┌──────────────┐
                            │   ĐÓNG HS    │
                            └──────────────┘
```

### Quy tắc chuyển trạng thái

| Từ | Đến | Điều kiện | Actor |
|---|---|---|---|
| CHO_TIEP_NHAN | CHO_XU_LY | Cán bộ tiếp nhận | Officer |
| CHO_XU_LY | DANG_XU_LY | Cán bộ bắt đầu xử lý | Officer |
| DANG_XU_LY | DA_XU_LY | Phê duyệt | Officer |
| DANG_XU_LY | TU_CHOI | Từ chối + lý do | Officer |
| DANG_XU_LY | CHO_BO_SUNG | Yêu cầu bổ sung | Officer |
| CHO_BO_SUNG | DA_BO_SUNG | Công dân nộp bổ sung | Citizen |
| DA_BO_SUNG | DANG_XU_LY | Cán bộ xử lý tiếp | Officer |
```

- [ ] **Step 2: Commit**

```bash
git add docs/architecture/data-flow.md
git commit -m "docs: data flow — citizen voice-first + officer OCR pipeline + state machine

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Task 5: Tạo docs/architecture/api-design.md — Thiết kế API

**Files:**
- Create: `docs/architecture/api-design.md`

- [ ] **Step 1: Tạo api-design.md**

```markdown
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

{
  "email": "user@govone.vn",
  "password": "password123"
}

→ 200: { "access_token": "eyJ...", "refresh_token": "eyJ...", "expires_in": 1800 }
→ 401: { "error": { "code": "INVALID_CREDENTIALS" } }
```

### Register
```
POST /api/auth/register

{
  "email": "new@govone.vn",
  "password": "password123",
  "ho_ten": "Nguyễn Văn A",
  "so_cccd": "079201000123",
  "so_dien_thoai": "0912345678"
}

→ 201: { "id": "uuid", "email": "new@govone.vn", "role": "citizen" }
→ 409: { "error": { "code": "EMAIL_EXISTS" } }
```

### Token Flow
```
POST /api/auth/refresh          → Refresh access token
GET  /api/auth/me               → Lấy thông tin user hiện tại
POST /api/auth/logout           → Vô hiệu hóa token
POST /api/auth/change-password  → Đổi mật khẩu
```

### Authorization Header
Tất cả request cần xác thực phải gửi:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

## API Endpoints

### Hồ sơ (HoSo)

| Method | Endpoint | Mô tả | Role |
|---|---|---|---|
| `GET` | `/api/ho-so` | Danh sách hồ sơ (phân trang, filter) | citizen/officer |
| `POST` | `/api/ho-so` | Tạo hồ sơ mới | citizen |
| `GET` | `/api/ho-so/:id` | Chi tiết hồ sơ | citizen/officer |
| `PUT` | `/api/ho-so/:id` | Cập nhật hồ sơ (chỉ CHO_TIEP_NHAN) | citizen |
| `POST` | `/api/ho-so/:id/upload` | Upload tài liệu đính kèm | citizen |
| `POST` | `/api/ho-so/:id/submit` | Nộp hồ sơ (CHO_TIEP_NHAN → CHO_XU_LY) | citizen |

### Xử lý hồ sơ (Officer Actions)

| Method | Endpoint | Mô tả | Role |
|---|---|---|---|
| `PUT` | `/api/ho-so/:id/tiep-nhan` | Tiếp nhận (CHO_XU_LY → DANG_XU_LY) | officer |
| `PUT` | `/api/ho-so/:id/phe-duyet` | Phê duyệt (DANG_XU_LY → DA_XU_LY) | officer |
| `PUT` | `/api/ho-so/:id/tu-choi` | Từ chối + lý do | officer |
| `PUT` | `/api/ho-so/:id/yeu-cau-bo-sung` | Yêu cầu bổ sung | officer |
| `GET` | `/api/ho-so/:id/lich-su` | Lịch sử xử lý | officer |

### Lịch hẹn (LichHen)

| Method | Endpoint | Mô tả | Role |
|---|---|---|---|
| `GET` | `/api/lich-hen` | Danh sách lịch hẹn | citizen/officer |
| `POST` | `/api/lich-hen` | Tạo lịch hẹn | citizen |
| `PUT` | `/api/lich-hen/:id` | Cập nhật lịch hẹn | citizen/officer |
| `DELETE` | `/api/lich-hen/:id` | Hủy lịch hẹn | citizen |

### Thông báo (ThongBao)

| Method | Endpoint | Mô tả | Role |
|---|---|---|---|
| `GET` | `/api/thong-bao` | Danh sách thông báo | citizen/officer |
| `POST` | `/api/thong-bao` | Tạo thông báo | officer |
| `PUT` | `/api/thong-bao/:id/da-doc` | Đánh dấu đã đọc | citizen/officer |

### AI Services (Internal)

| Method | Endpoint | Mô tả |
|---|---|---|
| `POST` | `/api/ai/ocr` | OCR ảnh giấy tờ → text + fields |
| `POST` | `/api/ai/ocr/batch` | OCR nhiều ảnh (async) |
| `POST` | `/api/ai/stt` | Speech-to-Text audio → text |
| `POST` | `/api/ai/tts` | Text-to-Speech text → audio |
| `POST` | `/api/ai/nlp/classify` | Phân loại nội dung → loại thủ tục |
| `POST` | `/api/ai/ekyc/verify` | Xác thực CCCD + face |
| `POST` | `/api/ai/auto-fill` | Upload ảnh → tự động điền form |
| `GET` | `/api/ai/task/:id` | Kiểm tra trạng thái async task |
| `GET` | `/api/ai/health` | Kiểm tra trạng thái AI models |

### System

| Method | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/health/db` | Database health check |
| `GET` | `/docs` | Swagger UI (auto-generated) |

---

## Mã lỗi chuẩn

| HTTP Code | Error Code | Mô tả |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Dữ liệu đầu vào không hợp lệ |
| 401 | `UNAUTHORIZED` | Thiếu hoặc token không hợp lệ |
| 401 | `TOKEN_EXPIRED` | Token hết hạn |
| 403 | `FORBIDDEN` | Không có quyền truy cập |
| 404 | `NOT_FOUND` | Resource không tồn tại |
| 409 | `CONFLICT` | Xung đột dữ liệu |
| 422 | `BUSINESS_RULE_VIOLATION` | Vi phạm quy tắc nghiệp vụ |
| 429 | `RATE_LIMITED` | Quá nhiều request |
| 500 | `INTERNAL_ERROR` | Lỗi hệ thống |

## Pagination

Query params cho tất cả `GET /api/*` endpoints:
```
?page=1&limit=20&sort_by=created_at&sort_order=desc
```

## Filtering

```
GET /api/ho-so?trang_thai=DANG_XU_LY&loai_thu_tuc=cap-giay-phep&from_date=2026-01-01&to_date=2026-06-12
```
```

- [ ] **Step 2: Commit**

```bash
git add docs/architecture/api-design.md
git commit -m "docs: REST API design — endpoints, auth, response format, error codes

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Task 6: Tạo docs/architecture/deployment.md — Kiến trúc triển khai

**Files:**
- Create: `docs/architecture/deployment.md`

- [ ] **Step 1: Tạo deployment.md**

```markdown
# Deployment — Kiến trúc Triển khai

## Tổng quan

GovOne được triển khai theo mô hình **monorepo + containerized services**, sử dụng Docker Compose cho development và có thể mở rộng lên Kubernetes cho production.

## Services

```
┌─────────────────────────────────────────────────────────────────┐
│                     DOCKER COMPOSE STACK                          │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ nginx    │  │ frontend │  │ backend  │  │  ai-svc  │        │
│  │ :80,443  │  │ :3000    │  │ :8000    │  │ :8001    │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │             │                │
│  ┌────┴─────────────┴─────────────┴─────────────┴────┐          │
│  │                    NETWORK: govone                  │          │
│  └────┬───────────────────────────────────────────────┘          │
│       │                                                           │
│  ┌────┴─────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │postgres  │  │  redis   │  │  minio   │  │ celery   │        │
│  │:5432     │  │ :6379    │  │ :9000    │  │ worker   │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## docker-compose.yml (khung)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: govone
      POSTGRES_USER: govone
      POSTGRES_PASSWORD: govone
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U govone"]
      interval: 5s

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: govone
      MINIO_ROOT_PASSWORD: govone123
    volumes:
      - miniodata:/data
    ports:
      - "9000:9000"
      - "9001:9001"

  backend:
    build: ./backend
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
      - ./uploads:/app/uploads
    environment:
      - DATABASE_URL=postgresql://govone:govone@postgres:5432/govone
      - REDIS_URL=redis://redis:6379/0
      - APP_ENV=development
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  celery-worker:
    build: ./backend
    command: celery -A src.ai.tasks.celery_app worker --loglevel=info
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://govone:govone@postgres:5432/govone
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
      - postgres

  frontend:
    build: ./frontend
    command: npm run dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on:
      - frontend
      - backend

volumes:
  pgdata:
  miniodata:
```

## Production Deployment

### Yêu cầu hạ tầng (mỗi UBND)

| Tài nguyên | Minimum | Khuyến nghị |
|---|---|---|
| **CPU** | 4 cores | 8 cores |
| **RAM** | 8 GB | 16 GB |
| **Disk** | 100 GB SSD | 500 GB SSD |
| **GPU** (AI) | Optional | NVIDIA T4 / A10 |
| **Network** | 100 Mbps | 1 Gbps |

### Kubernetes (khi scale >10 UBND)

```
┌──────────────────────────────────────────────────────┐
│                    INGRESS (nginx/traefik)            │
│                         :80/:443                      │
├──────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ frontend │  │ backend  │  │ ai-svc   │           │
│  │ (2 pods) │  │ (3 pods) │  │ (2 pods) │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ postgres │  │  redis   │  │  minio   │           │
│  │ (primary │  │(sentinel)│  │(distrib.)│           │
│  │ +replica)│  │          │  │          │           │
│  └──────────┘  └──────────┘  └──────────┘           │
├──────────────────────────────────────────────────────┤
│              PERSISTENT VOLUMES (SSD)                 │
└──────────────────────────────────────────────────────┘
```

## CI/CD Pipeline

```
Git Push → GitHub Actions
  ├── Lint (ESLint + Ruff)
  ├── Test (Vitest + Pytest)
  ├── Build Docker Images
  ├── Push to Registry (ghcr.io)
  └── Deploy
       ├── Dev: auto-deploy on push to master
       ├── Staging: auto-deploy on tag v*
       └── Prod: manual approval → deploy
```

## Monitoring

| Công cụ | Mục đích |
|---|---|
| **Prometheus + Grafana** | Metrics: requests/sec, latency, error rate, CPU, RAM |
| **Sentry** | Error tracking & alerting |
| **pg_stat_statements** | Slow query monitoring |
| **Celery Flower** | Task queue monitoring |
| **Healthcheck endpoints** | `/api/health`, `/api/health/db`, `/api/ai/health` |

## Backup Strategy

| Dữ liệu | Tần suất | Phương pháp |
|---|---|---|
| **PostgreSQL** | Hàng giờ (incremental) + Hàng ngày (full) | `pg_dump` + WAL archiving |
| **MinIO (scans)** | Hàng ngày | `mc mirror` đến secondary MinIO/S3 |
| **Configs** | Mỗi lần deploy | Git versioned |

## Bảo mật triển khai

- **HTTPS:** TLS 1.3 qua Let's Encrypt / chứng chỉ nội bộ
- **Network:** Internal services không expose port ra ngoài (chỉ qua nginx)
- **Secrets:** Không hardcode — dùng Docker secrets / Kubernetes secrets
- **Firewall:** Chỉ mở port 80/443, whitelist IP quản trị
- **Audit:** Log tất cả request admin, thay đổi cấu hình
```

- [ ] **Step 2: Commit**

```bash
git add docs/architecture/deployment.md
git commit -m "docs: deployment architecture — Docker Compose, Kubernetes, CI/CD, monitoring

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Self-Review Checklist

1. **Spec coverage:** ✅ README index (Task 1), system overview phạm vi/người dùng (Task 2), kiến trúc 4 tầng chi tiết (Task 3), 2 luồng dữ liệu + state machine (Task 4), REST API đầy đủ endpoints + auth + errors (Task 5), deployment Docker/K8s/CI/CD (Task 6)
2. **Placeholder scan:** ✅ Không có TBD/TODO
3. **Type consistency:** ✅ Service names, endpoint paths, error codes nhất quán giữa các file
