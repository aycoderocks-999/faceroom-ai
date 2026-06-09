# Deployment Guide

Deploy FaceRoom AI entirely on free-tier services.

## Prerequisites

- GitHub account
- [Supabase](https://supabase.com) project
- [Qdrant Cloud](https://cloud.qdrant.io) cluster
- [Upstash](https://upstash.com) Redis
- [Render](https://render.com) account
- [Vercel](https://vercel.com) account

---

## 1. Supabase (Database + Storage)

1. Create a new Supabase project
2. Go to **Settings → Database** and copy the connection string (URI mode)
3. Go to **Storage** → Create bucket `event-photos` (public read)
4. Copy **Project URL** and **anon/service key** from API settings

---

## 2. Qdrant Cloud

1. Create a free cluster at [cloud.qdrant.io](https://cloud.qdrant.io)
2. Copy cluster URL and API key
3. Collection `face_embeddings` is auto-created on first use

---

## 3. Upstash Redis

1. Create a Redis database at [upstash.com](https://upstash.com)
2. Copy the `rediss://` connection URL (TLS enabled)

---

## 4. Render — Backend API

1. New **Web Service** → Connect GitHub repo
2. Root directory: `backend`
3. Build: `pip install -r requirements.txt`
4. Start: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Environment variables:

```
DATABASE_URL=<supabase-connection-string>
SUPABASE_URL=<supabase-url>
SUPABASE_KEY=<supabase-service-key>
QDRANT_URL=<qdrant-url>
QDRANT_API_KEY=<qdrant-key>
REDIS_URL=<upstash-redis-url>
JWT_SECRET=<generate-random-64-char-string>
CORS_ORIGINS=https://your-app.vercel.app
```

---

## 5. Render — Celery Worker

1. New **Background Worker** → Same repo, root `backend`
2. Dockerfile path: `Dockerfile.worker`
3. Same environment variables as API
4. Instance type: at least 512MB RAM (InsightFace models)

---

## 6. Vercel — Frontend

1. Import GitHub repo
2. Root directory: `frontend`
3. Framework: Vite
4. Environment variable:

```
VITE_API_URL=https://your-api.onrender.com/api/v1
```

5. Deploy

---

## 7. Run Migrations

Migrations run automatically on Render start (`alembic upgrade head`).

For manual run:

```bash
cd backend
alembic upgrade head
```

---

## Local Docker Development

```bash
cp .env.example .env
# Edit .env with your keys (or use local services from docker-compose)

docker compose up --build
```

- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Health Checks

- API: `GET /api/v1/health`
- Processing: `GET /api/v1/processing/status`
