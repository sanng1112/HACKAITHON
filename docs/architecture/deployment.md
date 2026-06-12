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

## docker-compose.yml

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

## nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    server {
        listen 80;
        server_name govone.local;

        client_max_body_size 10M;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # Swagger docs
        location /docs {
            proxy_pass http://backend;
            proxy_set_header Host $host;
        }

        # Uploaded files
        location /uploads/ {
            alias /app/uploads/;
        }
    }
}
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
  ├── Lint
  │     ├── frontend: ESLint + Prettier
  │     └── backend: Ruff + mypy
  ├── Test
  │     ├── frontend: Vitest
  │     └── backend: Pytest + coverage (≥80%)
  ├── Build Docker Images
  │     ├── backend: python:3.12-slim base
  │     ├── frontend: node:20-alpine → next build
  │     └── ai-svc: pytorch/pytorch:2.5.0 base
  ├── Push to Registry (ghcr.io/govone)
  └── Deploy
       ├── Dev: auto-deploy on push to master
       ├── Staging: auto-deploy on tag v*-rc*
       └── Prod: manual approval → deploy
```

## GitHub Actions Workflow (khung)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Backend lint
        run: cd backend && pip install ruff && ruff check src/
      - name: Frontend lint
        run: cd frontend && npm ci && npm run lint

  test:
    needs: lint
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env: { POSTGRES_DB: govone_test, POSTGRES_USER: test, POSTGRES_PASSWORD: test }
        options: >-
          --health-cmd pg_isready --health-interval 10s --health-timeout 5s
    steps:
      - uses: actions/checkout@v4
      - name: Backend test
        run: cd backend && pip install -r ../requirements.txt && pytest tests/ -v --cov=src
      - name: Frontend test
        run: cd frontend && npm ci && npm run test

  build:
    needs: test
    if: github.ref == 'refs/heads/master' || startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build & push Docker images
        run: |
          docker build -t ghcr.io/govone/backend:latest ./backend
          docker build -t ghcr.io/govone/frontend:latest ./frontend
          docker push ghcr.io/govone/backend:latest
          docker push ghcr.io/govone/frontend:latest

  deploy-staging:
    needs: build
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: echo "Deploying to staging server via SSH..."

  deploy-prod:
    needs: build
    if: startsWith(github.ref, 'refs/tags/v') && github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        run: echo "Deploying to production server via SSH..."
```

## Docker Images

### Backend Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./
EXPOSE 3000
CMD ["npm", "start"]
```

### AI Service Dockerfile
```dockerfile
FROM pytorch/pytorch:2.5.0

WORKDIR /app
COPY requirements-ai.txt .
RUN pip install --no-cache-dir -r requirements-ai.txt
COPY src/ai/ ./src/ai/
EXPOSE 8001
CMD ["uvicorn", "src.ai.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

## Monitoring

| Công cụ | Mục đích |
|---|---|
| **Prometheus + Grafana** | Metrics: requests/sec, latency p50/p95/p99, error rate, CPU, RAM |
| **Sentry** | Error tracking & alerting |
| **pg_stat_statements** | Slow query monitoring |
| **Celery Flower** | Task queue monitoring (pending, active, failed tasks) |
| **Healthcheck endpoints** | `/api/health`, `/api/health/db`, `/api/ai/health` |

## Healthcheck Endpoints

```
GET /api/health       → 200: { "app": "GovOne", "version": "0.1.0", "uptime": 86400 }
GET /api/health/db    → 200: { "status": "connected", "latency_ms": 2 }
GET /api/ai/health    → 200: { "ocr": { "loaded": true }, "stt": { "loaded": true } }
```

## Backup Strategy

| Dữ liệu | Tần suất | Phương pháp |
|---|---|---|
| **PostgreSQL** | Hàng giờ (incremental) + Hàng ngày (full) | `pg_dump` + WAL archiving |
| **MinIO (scans)** | Hàng ngày | `mc mirror` đến secondary MinIO/S3 |
| **Configs** | Mỗi lần deploy | Git versioned |

## Bảo mật triển khai

- **HTTPS:** TLS 1.3 qua Let's Encrypt / chứng chỉ nội bộ
- **Network:** Internal services không expose port ra ngoài (chỉ qua nginx)
- **Secrets:** Không hardcode — dùng Docker secrets / Kubernetes secrets / env files `.gitignore`d
- **Firewall:** Chỉ mở port 80/443, whitelist IP quản trị
- **Audit:** Log tất cả request admin, thay đổi cấu hình
