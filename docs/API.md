# API Documentation

Base URL: `/api/v1`

Interactive docs: `http://localhost:8000/docs`

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, returns JWT tokens |
| POST | `/auth/logout` | Logout (client clears tokens) |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/auth/me` | Current user profile |

## Rooms

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rooms/create` | Create room |
| POST | `/rooms/join` | Join by room code |
| GET | `/rooms` | List user's rooms |
| GET | `/rooms/{id}` | Room details |
| DELETE | `/rooms/{id}` | Delete room (owner only) |
| POST | `/rooms/{id}/leave` | Leave room |
| GET | `/rooms/{id}/images` | Paginated room images |
| GET | `/rooms/{id}/clusters` | Room face clusters |

## Images

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/images/upload` | Upload images (multipart) |
| GET | `/images/{id}` | Image details |

## Clusters

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/clusters/{id}` | Cluster details |
| GET | `/clusters/{id}/images` | Images in cluster |
| POST | `/clusters/merge?room_id=` | Merge clusters |
| POST | `/clusters/split?room_id=` | Split cluster |
| PATCH | `/clusters/{id}` | Rename / mark unknown |
| POST | `/clusters/rooms/{id}/recluster` | Re-run DBSCAN |

## Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/search/face` | Face search (selfie upload) |
| GET | `/search/face/{face_id}/similar` | Similar face search |
| GET | `/search/history` | User search history |

## System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/processing/status` | Processing queue status |
| GET | `/admin/stats` | Admin statistics |
| GET | `/dashboard/stats` | User dashboard stats |

## Face Search Example

```bash
curl -X POST "http://localhost:8000/api/v1/search/face" \
  -H "Authorization: Bearer <token>" \
  -F "room_id=1" \
  -F "query_image=@selfie.jpg"
```

Response:

```json
{
  "matches": [
    {"image_id": 12, "image_url": "...", "similarity": 0.95, "face_id": 45}
  ],
  "match_count": 1,
  "search_time_ms": 142.5,
  "threshold": 0.5
}
```
