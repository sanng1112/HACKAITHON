#!/bin/bash
# Script chạy toàn bộ GovOne backend
# Chạy: bash /home/huong/hackaithon/HACKAITHON/start-backend.sh

set -e
echo "🚀 Khởi động GovOne Backend..."

# 1. Start PostgreSQL
echo "📦 Khởi động PostgreSQL..."
sudo systemctl start postgresql
sleep 2

# 2. Tạo DB và user nếu chưa có
echo "🗄️ Tạo database..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_user WHERE usename = 'govone'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE USER govone WITH PASSWORD 'govone';"
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = 'govone'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE DATABASE govone OWNER govone;"

# 3. Chạy migrations
echo "🔄 Chạy migrations..."
cd /home/huong/hackaithon/HACKAITHON/backend
.venv/bin/alembic upgrade head 2>/dev/null || echo "⚠️ Migrations skipped (OK nếu chưa có)"

# 4. Seed data
echo "🌱 Seed data..."
.venv/bin/python -m seed.seed_data 2>/dev/null || echo "⚠️ Seed skipped (OK nếu đã có data)"

# 5. Start FastAPI
echo "✅ Khởi động FastAPI tại http://localhost:8000"
.venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
