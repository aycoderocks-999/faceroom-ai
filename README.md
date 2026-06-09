# FaceRoom AI

**Distributed Face Recognition & Event Photo Retrieval Platform**

FaceRoom AI is a production-grade full-stack platform for shared event photo management. Upload event photos, automatically detect and group faces, and search for photos using a single selfie — similar to Google Photos face grouping.

![Architecture](docs/ARCHITECTURE.md)

## Features

- JWT authentication with refresh tokens
- Shared rooms with unique join codes (`ROOM-ABX72Z`)
- Bulk image upload with drag & drop
- Async face processing (RetinaFace + ArcFace via InsightFace)
- Automatic face clustering (DBSCAN)
- Vector similarity search (Qdrant, cosine similarity)
- Find Me — search all photos of a person with one selfie
- Cluster management (merge, split, rename)
- Dark / light mode UI
- Docker & cloud deployment ready

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, Vite, TailwindCSS, ShadCN UI, React Query |
| Backend | FastAPI, SQLAlchemy, Alembic, Pydantic |
| Database | PostgreSQL (Supabase) |
| Storage | Supabase Storage |
| Vector DB | Qdrant Cloud |
| Queue | Redis + Celery |
| CV | InsightFace (RetinaFace + ArcFace), DBSCAN |
| Deploy | Vercel, Render, Docker |

## Project Structure

```
smart_photo_sharing/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # HTTP endpoints
│   │   ├── core/            # Config, security, database
│   │   ├── models/          # SQLAlchemy models
│   │   ├── repositories/    # Data access layer
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── workers/         # Celery tasks
│   ├── alembic/             # Migrations
│   ├── tests/               # Pytest suite
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── pages/           # Route pages
│   │   └── lib/             # API, auth, theme
│   └── Dockerfile
├── docs/                    # Architecture, API, deployment
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Quick Start (Local)

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker (optional, recommended)

### Option A: Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:3000
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

### Option B: Manual Setup

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-base.txt
# For face processing locally (Linux/Docker recommended):
pip install -r requirements-ml.txt
cp ../.env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

**Worker (separate terminal):**

```bash
cd backend
celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

**Frontend:**

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_KEY` | Supabase API key |
| `QDRANT_URL` | Qdrant cluster URL |
| `QDRANT_API_KEY` | Qdrant API key |
| `REDIS_URL` | Redis connection URL |
| `JWT_SECRET` | Secret for JWT signing |

## Testing

```bash
# Backend
cd backend && pytest -v

# Frontend
cd frontend && npm test
```

## API Overview

| Group | Endpoints |
|-------|-----------|
| Auth | `/auth/register`, `/auth/login`, `/auth/refresh` |
| Rooms | `/rooms/create`, `/rooms/join`, `/rooms/{id}` |
| Images | `/images/upload`, `/rooms/{id}/images` |
| Clusters | `/rooms/{id}/clusters`, `/clusters/merge` |
| Search | `/search/face`, `/search/history` |

Full API docs: [docs/API.md](docs/API.md)

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for step-by-step deployment to:

- **Frontend** → Vercel (free)
- **Backend** → Render (free)
- **Database** → Supabase (free)
- **Storage** → Supabase Storage (free)
- **Vector DB** → Qdrant Cloud (free tier)
- **Queue** → Upstash Redis (free)

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/ER_DIAGRAM.md](docs/ER_DIAGRAM.md).

## License

MIT
