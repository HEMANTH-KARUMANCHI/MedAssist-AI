#!/usr/bin/env bash
# ==============================================================================
# MedAssist-AI — Automated Cloud & VM Deployment Script
# ==============================================================================

set -euo pipefail

echo "============================================================"
echo "  🚀 Starting MedAssist-AI Production Deployment"
echo "============================================================"

# 1. Check Docker & Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Docker is installed: $(docker --version)"

# 2. Check or Create .env file
if [ ! -f .env ]; then
    echo "⚠️ No .env file found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        cat <<EOF > .env
DB_NAME=medassist_ai
DB_USER=postgres
DB_PASSWORD=$(openssl rand -hex 16)
SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_ORIGINS=*
PROD_HTTP_PORT=80
VITE_API_URL=http://localhost:8000
EOF
    fi
    echo "✅ .env created with secure randomly generated credentials."
fi

# 3. Pull / Build and Launch Containers
echo "📦 Building and starting Docker containers in detached mode..."
docker compose -f docker-compose.prod.yml up --build -d

# 4. Wait for Services to become Healthy
echo "⏳ Waiting for PostgreSQL and FastAPI services to report healthy status..."
sleep 10

# 5. Check running containers
echo "============================================================"
echo "  📊 Deployed Container Status:"
echo "============================================================"
docker compose -f docker-compose.prod.yml ps

echo "============================================================"
echo "  🎉 MedAssist-AI is successfully deployed!"
echo "  - Web Frontend : http://localhost:80"
echo "  - API Backend  : http://localhost:8000/docs"
echo "============================================================"
