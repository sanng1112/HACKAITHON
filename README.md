# GovOne — Hệ thống Quản lý Hành chính Công Thông minh

> **Hackaithon 2026 — Đề tài 6: Ứng dụng Trí tuệ Nhân tạo trong Dịch vụ Công**

**GovOne** là hệ thống quản lý hành chính công tích hợp AI, phục vụ **cả hai đối tượng**: người dân (voice-first) và cán bộ (OCR pipeline). Hệ thống tận dụng 7 API VNPT AI để tự động hóa toàn bộ quy trình từ tiếp nhận, xử lý, đến trả kết quả thủ tục hành chính.

---

## Vấn đề & Giải pháp

| Pain-point | Mô tả | Cách GovOne giải quyết |
|---|---|---|
| **PP1** — Rào cản công nghệ | Người già, người khuyết tật không dùng được form web | Voice-first: nói → STT → NLP → TTS trả lời |
| **PP2** — Tồn đọng hồ sơ giấy | ~70% hồ sơ chưa số hóa, tra cứu mất 30-60 phút | OCR + SmartReader tự động số hóa, phân loại, bóc tách |
| **PP3** — Xác thực thủ công | Cán bộ kiểm tra CCCD bằng mắt, dễ sai sót | eKYC: OCR + Compare + Liveness tự động |
| **PP4** — Thiếu phản hồi | Không đo được mức độ hài lòng của người dân | SmartVision Sentiment: camera phân tích cảm xúc real-time |

---

## Kiến trúc hệ thống (4 tầng)

```
┌─────────────────────────────────────────────────────────────────┐
│  TẦNG 1 — USER LAYER                                            │
│  Kiosk (Voice-first)  │  Web App (React)  │  Mobile (React Nat.)│
├─────────────────────────────────────────────────────────────────┤
│  TẦNG 2 — AI CORE (7 VNPT APIs)                                 │
│  SmartVoice STT/TTS │ Smartbot NLP │ SmartReader OCR/Doc AI     │
│  eKYC OCR/Compare/Liveness │ SmartVision Classification/Sentiment│
├─────────────────────────────────────────────────────────────────┤
│  TẦNG 3 — PROCESSING LAYER                                      │
│  Voice Gateway │ Intent Engine │ Doc Processor │ Sentiment AI   │
├─────────────────────────────────────────────────────────────────┤
│  TẦNG 4 — DATA LAYER                                            │
│  PostgreSQL │ Redis │ MinIO/S3 │ Knowledge Base                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Cấu trúc dự án

```
govone/
├── README.md                    # ← Bạn đang ở đây
├── proposal/                    # Tài liệu & scripts tạo proposal
│   ├── proposal.docx            # Proposal đầy đủ (7 sections)
│   ├── proposal.pdf
│   ├── assets/                  # Logo, sơ đồ kiến trúc, wireframes
│   ├── scripts/                 # Python scripts sinh proposal
│   └── tests/                   # Unit test nội dung proposal
├── frontend/                    # Round 1 — Giao diện người dùng
│   └── src/
│       ├── components/          # Shared UI components
│       ├── pages/               # Các trang: citizen, officer, auth
│       ├── hooks/               # Custom React hooks
│       ├── services/            # API client (Axios)
│       └── types/               # TypeScript type definitions
├── backend/                     # Round 2+3+4 — Backend services
│   ├── src/
│   │   ├── api/                 # REST API routers (auth, ho-so, lich-hen, thong-bao)
│   │   ├── services/            # Business logic layer
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── database/            # Connection, repositories
│   │   ├── config/              # App configuration
│   │   └── ai/                  # Round 4 — AI/ML integration
│   │       ├── models/          # OCR, STT, NLP model wrappers
│   │       ├── services/        # AI pipeline services
│   │       ├── api/             # AI API endpoints
│   │       ├── tasks/           # Celery async task definitions
│   │       └── utils/           # Image, audio, text utilities
│   ├── tests/
│   ├── migrations/              # Alembic migration scripts
│   │   └── versions/
│   └── seed/                    # Database seed data
└── docs/
    ├── rounds/                  # Kế hoạch phát triển 4 rounds
    │   ├── README.md
    │   ├── round-1-frontend.md
    │   ├── round-2-backend-logic.md
    │   ├── round-3-backend-database.md
    │   └── round-4-backend-models.md
    └── architecture/            # Tài liệu kiến trúc bổ sung
```

---

## Kế hoạch phát triển — 4 Rounds

| Round | Tên | Người phụ trách | Công nghệ chính | Phụ thuộc |
|---|---|---|---|---|
| **1** | **Frontend** | Frontend Dev | React/Next.js, TypeScript, Tailwind CSS | Round 2 (có thể mock) |
| **2** | **Backend Logic** | Backend Dev 1 | FastAPI/NestJS, JWT, REST APIs | Round 3 |
| **3** | **Backend Database** | Backend Dev 2 | PostgreSQL, SQLAlchemy, Alembic | — (làm trước) |
| **4** | **Backend AI Models** | Backend Dev 3 | PyTorch, EasyOCR, Whisper, Celery | Round 2+3 |

**Thứ tự khuyến nghị:** Round 3 → Round 2 → Round 1 (song song với mock) → Round 4

Chi tiết từng round xem tại [docs/rounds/](docs/rounds/).

---

## Cài đặt & Chạy

### Yêu cầu

- **Python 3.10+** — scripts proposal & backend
- **Node.js 20+** — frontend
- **PostgreSQL 15+** — database
- **Redis** — cache & async queue

### Cài đặt môi trường dev

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
cp ../.env.example .env

# Run dev server
uvicorn src.main:app --reload

# Frontend
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### Tạo proposal (nếu cần cập nhật)

```bash
cd proposal
python scripts/create_proposal.py
python scripts/add_section1.py
python scripts/add_section2.py
python scripts/add_section3.py
python scripts/add_section4.py
python scripts/add_section5.py
python scripts/add_section6.py
python scripts/finalize_proposal.py
python scripts/verify_content.py
```

### Chạy tests

```bash
# Proposal tests
cd proposal && python -m pytest tests/ -v

# Backend tests
cd backend && python -m pytest tests/ -v

# Frontend tests
cd frontend && npm run test
```

---

## Công nghệ AI

| API VNPT | Chức năng | Độ chính xác |
|---|---|---|
| **SmartVoice STT** | Speech-to-Text tiếng Việt | >95% |
| **SmartVoice TTS** | Text-to-Speech giọng tự nhiên | — |
| **Smartbot NLP** | Nhận diện ý định, xử lý hội thoại | >90% |
| **SmartReader OCR** | Nhận dạng ký tự quang học | >95% |
| **SmartReader Doc AI** | Bóc tách thông tin có cấu trúc | >90% |
| **eKYC OCR** | Nhận dạng CCCD/CMND | >98% |
| **eKYC Compare** | So sánh khuôn mặt với ảnh thẻ | >99% |
| **eKYC Liveness** | Phát hiện người thật/giả | >99% |
| **SmartVision Classification** | Phân loại loại giấy tờ | >95% |
| **SmartVision Face/Sentiment** | Nhận diện cảm xúc khuôn mặt | >85% |

*Fallback models (khi không có VNPT API):* EasyOCR, Whisper, PhoBERT chạy local.

---

## KPI Mục tiêu

| Chỉ số | Hiện tại | Mục tiêu GovOne |
|---|---|---|
| Thời gian xử lý thủ tục | 20-30 phút | 5-7 phút (↓70%) |
| Độ phủ người dùng | ~30% | >95% |
| Tỷ lệ hài lòng | ~65% | >90% |
| Thời gian tra cứu hồ sơ cũ | 30-60 phút | <5 phút (↓90%) |
| Tỷ lệ sai sót hồ sơ | ~15% | <2% |

---

## Mô hình kinh doanh (B2G)

| Gói | Giá/tháng | Bao gồm |
|---|---|---|
| **Basic** | 8.000.000đ | 1 Kiosk, OCR 500 lượt, Smartbot 10 thủ tục |
| **Pro** | 20.000.000đ | Kiosk + Web, OCR 2.000 lượt, Smartbot 50 thủ tục, eKYC |
| **Enterprise** | Tùy chỉnh | Không giới hạn, tích hợp CSDL riêng, SLA 99.9% |

**Thị trường mục tiêu:** TAM ~18.000 tỷ → SAM ~800 tỷ → SOM ~40 tỷ (200 UBND năm đầu)

---

## Đội ngũ

- **Frontend Developer** — React/Next.js, TypeScript, Tailwind (Round 1)
- **Backend Developer 1** — FastAPI/NestJS, Business Logic (Round 2)
- **Backend Developer 2** — PostgreSQL, SQLAlchemy, Data Layer (Round 3)
- **Backend Developer 3** — AI/ML, PyTorch, OCR/STT/NLP (Round 4)

---

## License

MIT — Hackaithon 2026
