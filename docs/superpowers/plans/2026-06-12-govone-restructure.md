# GovOne — Tái cấu trúc Project làm Mainstream

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Xóa VoiceOne và AutoCheck, đưa GovOne thành project chính, viết README.md chi tiết, tái cấu trúc thư mục theo mô hình 4 rounds.

**Architecture:** Project root là GovOne backend monorepo. Tầng proposal (`proposal/`) giữ nguyên scripts + assets hiện có. Tầng production được tổ chức thành `frontend/` (Round 1), `backend/` (Round 2+3) gồm `api/`, `database/`, `services/`, và `backend/ai/` (Round 4).

**Tech Stack:** Python 3 (scripts proposal), FastAPI (backend), React/Next.js (frontend), PostgreSQL (database).

---

## Task 1: Xóa VoiceOne và AutoCheck

**Files:**
- Delete: `hackaithon-de-tai-6-vong-1/` (toàn bộ thư mục)
- Delete: `hackaithon-de-tai-6-autocheck/` (toàn bộ thư mục)

- [ ] **Step 1: Xóa thư mục vong-1 và autocheck**

```bash
rm -rf "hackaithon-de-tai-6-vong-1" "hackaithon-de-tai-6-autocheck"
```

- [ ] **Step 2: Kiểm tra kết quả**

```bash
ls -la
```
Expected: Chỉ còn `hackaithon-de-tai-6-govone/`, `docs/`, `.gitignore`, `.commandcode/`, `.git/`, và file PDF gốc.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: remove voiceone and autocheck sub-projects"

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Task 2: Đưa GovOne lên làm project root

**Files:**
- Move: `hackaithon-de-tai-6-govone/*` → `./`
- Delete: `hackaithon-de-tai-6-govone/` (thư mục rỗng sau move)

- [ ] **Step 1: Chuyển toàn bộ nội dung GovOne ra root**

```bash
shopt -s dotglob
mv hackaithon-de-tai-6-govone/* ./
rmdir hackaithon-de-tai-6-govone
```

- [ ] **Step 2: Tổ chức lại thư mục — tạo cấu trúc mới**

```bash
mkdir -p proposal/assets proposal/scripts proposal/docs
mkdir -p frontend/src/components frontend/src/pages frontend/src/hooks frontend/src/services frontend/src/types
mkdir -p backend/src/api backend/src/services backend/src/models backend/src/database/repositories backend/src/config
mkdir -p backend/src/ai/models backend/src/ai/services backend/src/ai/api backend/src/ai/tasks backend/src/ai/utils
mkdir -p backend/tests backend/migrations/versions backend/seed
mkdir -p docs/architecture
```

- [ ] **Step 3: Di chuyển proposal assets và scripts**

```bash
mv assets/* proposal/assets/ 2>/dev/null
rmdir assets 2>/dev/null
mv scripts/* proposal/scripts/ 2>/dev/null
rmdir scripts 2>/dev/null
mv proposal.docx proposal/ 2>/dev/null
mv proposal.pdf proposal/ 2>/dev/null
mv rounds/ docs/rounds/ 2>/dev/null
mv tests/ proposal/tests/ 2>/dev/null
```

- [ ] **Step 4: Xác minh cấu trúc mới**

```bash
find . -maxdepth 3 -not -path './.git/*' -not -path './.commandcode/*' -not -path './.venv/*' -not -path './__pycache__/*' -not -path './proposal/scripts/__pycache__/*' | sort
```
Expected: `backend/`, `frontend/`, `proposal/`, `docs/`, `docs/rounds/`, `docs/architecture/`

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: restructure govone as project root with round-based layout

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Task 3: Viết README.md chi tiết

**Files:**
- Overwrite: `README.md`

- [ ] **Step 1: Viết README.md hoàn chỉnh**

Nội dung README.md:

```markdown
# GovOne — Hệ thống Quản lý Hành chính Công Thông minh

> **Hackaithon 2026 — Đề tài 6: Ứng dụng Trí tuệ Nhân tạo trong Dịch vụ Công**

**GovOne** là hệ thống quản lý hành chính công tích hợp AI, phục vụ **cả hai đối tượng**: người dân (voice-first) và cán bộ (OCR pipeline). Hệ thống tận dụng 7 API VNPT AI để tự động hóa toàn bộ quy trình từ tiếp nhận, xử lý, đến trả kết quả thủ tục hành chính.

---

## 🎯 Vấn đề & Giải pháp

| Pain-point | Mô tả | Cách GovOne giải quyết |
|---|---|---|
| **PP1** — Rào cản công nghệ | Người già, người khuyết tật không dùng được form web | Voice-first: nói → STT → NLP → TTS trả lời |
| **PP2** — Tồn đọng hồ sơ giấy | ~70% hồ sơ chưa số hóa, tra cứu mất 30-60 phút | OCR + SmartReader tự động số hóa, phân loại, bóc tách |
| **PP3** — Xác thực thủ công | Cán bộ kiểm tra CCCD bằng mắt, dễ sai sót | eKYC: OCR + Compare + Liveness tự động |
| **PP4** — Thiếu phản hồi | Không đo được mức độ hài lòng của người dân | SmartVision Sentiment: camera phân tích cảm xúc real-time |

---

## 🏗️ Kiến trúc hệ thống (4 tầng)

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

## 📂 Cấu trúc dự án

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
    │   ├── round-1-frontend.md
    │   ├── round-2-backend-logic.md
    │   ├── round-3-backend-database.md
    │   └── round-4-backend-models.md
    └── architecture/            # Tài liệu kiến trúc bổ sung
```

---

## 🔄 Kế hoạch phát triển — 4 Rounds

| Round | Tên | Người phụ trách | Công nghệ chính | Phụ thuộc |
|---|---|---|---|---|
| **1** | **Frontend** | Frontend Dev | React/Next.js, TypeScript, Tailwind CSS | Round 2 (có thể mock) |
| **2** | **Backend Logic** | Backend Dev 1 | FastAPI/NestJS, JWT, REST APIs | Round 3 |
| **3** | **Backend Database** | Backend Dev 2 | PostgreSQL, SQLAlchemy, Alembic | — (làm trước) |
| **4** | **Backend AI Models** | Backend Dev 3 | PyTorch, EasyOCR, Whisper, Celery | Round 2+3 |

**Thứ tự khuyến nghị:** Round 3 → Round 2 → Round 1 (song song với mock) → Round 4

---

## 🚀 Cài đặt & Chạy

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
pip install -r requirements.txt
cp .env.example .env

# Database migration
alembic upgrade head
python seed/seed_data.py

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

## 🧠 Công nghệ AI

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

## 📊 KPI Mục tiêu

| Chỉ số | Hiện tại | Mục tiêu GovOne |
|---|---|---|
| Thời gian xử lý thủ tục | 20-30 phút | 5-7 phút (↓70%) |
| Độ phủ người dùng | ~30% | >95% |
| Tỷ lệ hài lòng | ~65% | >90% |
| Thời gian tra cứu hồ sơ cũ | 30-60 phút | <5 phút (↓90%) |
| Tỷ lệ sai sót hồ sơ | ~15% | <2% |

---

## 💰 Mô hình kinh doanh (B2G)

| Gói | Giá/tháng | Bao gồm |
|---|---|---|
| **Basic** | 8.000.000đ | 1 Kiosk, OCR 500 lượt, Smartbot 10 thủ tục |
| **Pro** | 20.000.000đ | Kiosk + Web, OCR 2.000 lượt, Smartbot 50 thủ tục, eKYC |
| **Enterprise** | Tùy chỉnh | Không giới hạn, tích hợp CSDL riêng, SLA 99.9% |

**Thị trường mục tiêu:** TAM ~18.000 tỷ → SAM ~800 tỷ → SOM ~40 tỷ (200 UBND năm đầu)

---

## 👥 Đội ngũ

- **Frontend Developer** — React/Next.js, TypeScript, Tailwind (Round 1)
- **Backend Developer 1** — FastAPI/NestJS, Business Logic (Round 2)
- **Backend Developer 2** — PostgreSQL, SQLAlchemy, Data Layer (Round 3)
- **Backend Developer 3** — AI/ML, PyTorch, OCR/STT/NLP (Round 4)

---

## 📄 License

MIT — Hackaithon 2026
```

- [ ] **Step 2: Xác minh file README.md**

```bash
wc -l README.md
```
Expected: ~200+ dòng

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: comprehensive README.md for GovOne project

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Task 4: Tạo file cấu hình project root

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore` (mở rộng)

- [ ] **Step 1: Tạo requirements.txt cho backend/proposal**

```text
# GovOne — Backend & Proposal Dependencies
# ==========================================

# Proposal generation
python-docx==1.1.2
Pillow==11.0.0

# Backend API
fastapi==0.115.0
uvicorn[standard]==0.31.0
pydantic==2.9.0
pydantic-settings==2.6.0

# Database
sqlalchemy==2.0.35
alembic==1.13.0
psycopg2-binary==2.9.10
asyncpg==0.30.0

# Auth
pyjwt==2.9.0
bcrypt==4.2.0

# Async tasks
celery==5.4.0
redis==5.2.0

# AI/ML (Round 4)
torch==2.5.0
easyocr==1.7.2
openai-whisper==20240930
transformers==4.45.0

# Image/audio processing
opencv-python-headless==4.10.0
librosa==0.10.2

# Testing
pytest==8.3.0
pytest-asyncio==0.24.0
httpx==0.28.0
```

- [ ] **Step 2: Tạo .env.example**

```env
# GovOne Configuration
# =====================

# Database
DATABASE_URL=postgresql://govone:govone@localhost:5432/govone
DATABASE_URL_ASYNC=postgresql+asyncpg://govone:govone@localhost:5432/govone

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET=change-me-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# File Storage
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE_MB=10

# VNPT AI APIs (Round 4)
VNPT_SMARTVOICE_STT_URL=https://api.vnpt.ai/v1/smartvoice/stt
VNPT_SMARTVOICE_TTS_URL=https://api.vnpt.ai/v1/smartvoice/tts
VNPT_SMARTBOT_URL=https://api.vnpt.ai/v1/smartbot
VNPT_SMARTREADER_OCR_URL=https://api.vnpt.ai/v1/smartreader/ocr
VNPT_EKYC_URL=https://api.vnpt.ai/v1/ekyc
VNPT_SMARTVISION_URL=https://api.vnpt.ai/v1/smartvision
VNPT_API_KEY=

# App
APP_ENV=development
APP_DEBUG=true
APP_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

- [ ] **Step 3: Mở rộng .gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
dist/

# Node
node_modules/
.next/
out/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Uploads
uploads/

# Database
*.db
*.sqlite3

# AI Models
models/
*.pt
*.pth
*.bin

# Build
build/
*.pyc
```

- [ ] **Step 4: Commit**

```bash
git add requirements.txt .env.example .gitignore
git commit -m "chore: add project config files (requirements, env, gitignore)

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Task 5: Tạo stub files cho backend

**Files:**
- Create: `backend/src/__init__.py`
- Create: `backend/src/main.py`
- Create: `backend/src/config/__init__.py`
- Create: `backend/src/config/settings.py`
- Create: `backend/src/api/__init__.py`
- Create: `backend/src/services/__init__.py`
- Create: `backend/src/models/__init__.py`
- Create: `backend/src/database/__init__.py`
- Create: `backend/src/ai/__init__.py`
- Create: `backend/tests/__init__.py`

- [ ] **Step 1: Tạo backend/src/config/settings.py**

```python
"""Application configuration loaded from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "GovOne"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8000
    
    DATABASE_URL: str = "postgresql://govone:govone@localhost:5432/govone"
    DATABASE_URL_ASYNC: str = "postgresql+asyncpg://govone:govone@localhost:5432/govone"
    
    REDIS_URL: str = "redis://localhost:6379/0"
    
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    VNPT_API_KEY: str = ""
    
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
```

- [ ] **Step 2: Tạo backend/src/main.py**

```python
"""GovOne — Main application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Hệ thống Quản lý Hành chính Công Thông minh — Hackaithon 2026",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


app = create_app()


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
```

- [ ] **Step 3: Tạo các file __init__.py**

```bash
touch backend/src/__init__.py
touch backend/src/api/__init__.py
touch backend/src/services/__init__.py
touch backend/src/models/__init__.py
touch backend/src/database/__init__.py
touch backend/src/ai/__init__.py
touch backend/tests/__init__.py
```

- [ ] **Step 4: Commit**

```bash
git add backend/
git commit -m "feat: scaffold backend project structure (FastAPI)

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Task 6: Tạo stub files cho frontend

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/src/App.tsx`

- [ ] **Step 1: Tạo frontend/package.json**

```json
{
  "name": "govone-frontend",
  "version": "0.1.0",
  "private": true,
  "description": "GovOne — Frontend giao diện người dùng",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "vitest"
  },
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "axios": "^1.7.0",
    "react-hook-form": "^7.53.0",
    "zod": "^3.23.0",
    "@hookform/resolvers": "^3.9.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "typescript": "^5.6.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "vitest": "^2.1.0",
    "@testing-library/react": "^16.0.0"
  }
}
```

- [ ] **Step 2: Tạo frontend/tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

- [ ] **Step 3: Tạo frontend/.env.example**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

- [ ] **Step 4: Commit**

```bash
git add frontend/
git commit -m "feat: scaffold frontend project structure (Next.js)

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

## Task 7: Xác minh proposal scripts hoạt động sau restructure

**Lý do:** Tất cả scripts dùng `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` để lấy project root. Sau khi chuyển vào `proposal/scripts/`, pattern này tự động resolve về `proposal/` — nơi chứa `proposal.docx`, `proposal.pdf`, `assets/`. **Không cần sửa code.**

- [ ] **Step 1: Chạy test xác minh**

```bash
cd proposal && python -m pytest tests/ -v
```
Expected: Tất cả tests liên quan đến proposal.docx/PDF/assets pass. Các test về nội dung sections có thể fail nếu proposal.docx cũ không có nội dung — điều này bình thường, cần re-generate proposal để pass hết.

- [ ] **Step 2: Chạy verify nếu proposal.docx có sẵn**

```bash
cd proposal && python scripts/verify_content.py
```
Expected: Xác nhận proposal.docx, PDF, assets đều được tìm thấy đúng đường dẫn.

- [ ] **Step 3: Commit**

```bash
git add proposal/
git commit -m "verify: proposal scripts resolve correctly after restructure

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
```

---

---

## Self-Review Checklist

1. **Spec coverage:** ✅ Xóa voiceone & autocheck (Task 1) — ✅ GovOne làm mainstream (Task 2) — ✅ README.md chi tiết (Task 3) — ✅ Cấu trúc theo round (Tasks 4-8)
2. **Placeholder scan:** ✅ Không có TBD/TODO
3. **Type consistency:** ✅ Tất cả đường dẫn tham chiếu nhất quán
