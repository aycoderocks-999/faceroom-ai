# Next Steps After GitHub Push

Repo: https://github.com/aycoderocks-999/faceroom-ai

## 1. Connect GitHub to Vercel (one-time, 1 minute)

Vercel CLI login is done, but GitHub must be linked in the dashboard:

1. Go to https://vercel.com/account/integrations
2. Click **GitHub** → **Connect**
3. Authorize access to `aycoderocks-999/faceroom-ai`
4. Open project **frontend** → Settings → General → **Root Directory** → set to `frontend`
5. Settings → Environment Variables → set `VITE_API_URL` to your Render API URL (after step 3)

## 2. Deploy Backend on Render (free)

1. Sign up at https://render.com with GitHub
2. **New → Blueprint**
3. Connect repo `aycoderocks-999/faceroom-ai`
4. Render reads `render.yaml` automatically
5. Add these env vars when prompted:

| Variable | Where to get it |
|----------|-----------------|
| `DATABASE_URL` | Supabase → Settings → Database → URI |
| `SUPABASE_URL` | Supabase → Settings → API |
| `SUPABASE_KEY` | Supabase → service_role key |
| `QDRANT_URL` | Qdrant Cloud cluster URL |
| `QDRANT_API_KEY` | Qdrant Cloud API key |
| `REDIS_URL` | Upstash → Redis URL |
| `CORS_ORIGINS` | `https://frontend-gray-pi-59.vercel.app` |

6. Deploy → copy API URL (e.g. `https://faceroom-api.onrender.com`)

## 3. Update Vercel API URL

```powershell
cd frontend
echo "https://YOUR-RENDER-API.onrender.com/api/v1" | vercel env add VITE_API_URL production
vercel --prod --yes
```

## 4. Free service sign-up links

- Supabase: https://supabase.com
- Qdrant Cloud: https://cloud.qdrant.io
- Upstash Redis: https://upstash.com
