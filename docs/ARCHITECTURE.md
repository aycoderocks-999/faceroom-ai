# FaceRoom AI — Architecture

## System Overview

```
┌─────────────┐     HTTPS      ┌──────────────────┐
│   Vercel    │ ──────────────▶│  Render (API)    │
│  React SPA  │                │  FastAPI Gateway │
└─────────────┘                └────────┬─────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          ▼                             ▼                             ▼
┌─────────────────┐           ┌─────────────────┐           ┌─────────────────┐
│ Supabase        │           │ Upstash Redis   │           │ Qdrant Cloud    │
│ PostgreSQL      │           │ Task Queue      │           │ Vector Search   │
│ + Storage       │           └────────┬────────┘           └─────────────────┘
└─────────────────┘                    │
                                       ▼
                              ┌─────────────────┐
                              │ Celery Worker   │
                              │ RetinaFace      │
                              │ ArcFace         │
                              │ DBSCAN          │
                              └─────────────────┘
```

## Service Layers

| Layer | Responsibility |
|-------|----------------|
| API Routes | HTTP endpoints, validation, auth |
| Services | Business logic, orchestration |
| Repositories | Database access (Repository Pattern) |
| Workers | Async face processing pipeline |
| External | Supabase, Qdrant, Redis |

## Face Processing Pipeline

1. User uploads image → stored in Supabase Storage
2. API creates `images` record + Celery task
3. Worker downloads image
4. RetinaFace (via InsightFace) detects faces
5. ArcFace generates 512-d embeddings
6. Embeddings stored in Qdrant with `room_id` filter
7. Face metadata stored in PostgreSQL
8. DBSCAN clusters faces per room
9. Cluster assignments updated

## Face Search (CBIR)

1. User uploads selfie
2. Detect face + generate query embedding
3. Qdrant cosine similarity search (room-scoped)
4. Results ranked by similarity score
5. Search logged for analytics

## Multi-Face Support

One image → many `faces` rows. Each face links to one cluster. An image appears in multiple cluster galleries when it contains multiple people.

## Security

- JWT access + refresh tokens
- bcrypt password hashing
- Room membership checks on all room operations
- Rate limiting (SlowAPI)
- CORS allowlist
- File type + size validation
