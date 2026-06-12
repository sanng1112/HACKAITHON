# GovOne - Phân chia Rounds phát triển

## Tổng quan 4 Rounds

Hệ thống GovOne được chia thành **4 rounds phát triển độc lập**, mỗi round do một người phụ trách. Mỗi round là một phần riêng biệt, khi hoàn thành là hoàn thiện được chức năng đó.

| Round | Tên | Người phụ trách | Công nghệ chính |
|-------|-----|----------------|-----------------|
| 1 | **Frontend** - Giao diện người dùng | Người A (Frontend Developer) | React/Next.js, TypeScript, Tailwind CSS |
| 2 | **Backend Logic** - Xử lý nghiệp vụ | Người B (Backend Developer 1) | FastAPI/NestJS, JWT, REST APIs |
| 3 | **Backend Database** - Quản lý dữ liệu | Người C (Backend Developer 2) | PostgreSQL, SQLAlchemy, Alembic |
| 4 | **Backend Models** - Gọi models AI | Người D (Backend Developer 3) | PyTorch, EasyOCR, Whisper, Celery |

## Kiến trúc tổng thể

```
┌─────────────────────────────────────────────────┐
│                   Frontend                       │
│              (Round 1 - Người A)                 │
│     React/Next.js + TypeScript + Tailwind        │
└──────────────────┬──────────────────────────────┘
                   │  HTTP/REST APIs
┌──────────────────▼──────────────────────────────┐
│              Backend Logic                        │
│             (Round 2 - Người B)                   │
│      FastAPI/NestJS + JWT + Services              │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌───────▼────────┐
│   Database     │   │   AI Models    │
│ (Round 3 - C)  │   │ (Round 4 - D)  │
│  PostgreSQL    │   │ OCR/STT/NLP    │
│  SQLAlchemy    │   │ PyTorch/Celery │
└────────────────┘   └────────────────┘
```

## Mối quan hệ giữa các rounds

- **Round 1 (Frontend)** ← gọi API → **Round 2 (Backend Logic)**
- **Round 2 (Backend Logic)** ← đọc/ghi → **Round 3 (Database)**
- **Round 2 (Backend Logic)** ← gọi AI → **Round 4 (Models)**
- **Round 3 (Database)** ← lưu kết quả ← **Round 4 (Models)**

## Thứ tự ưu tiên

1. **Luồng chính:** Round 3 → Round 2 → Round 1 (có thể làm song song với mock)
2. **Luồng AI:** Round 4 có thể làm độc lập, tích hợp sau
3. **Khuyến nghị:** Round 3 và Round 4 làm trước, Round 2 và Round 1 làm sau hoặc song song
