# DeepClean AI Studio

**Production-ready SaaS for metadata removal and AI signature reduction from images and videos.**

---

## Architecture

```
deepclean-ai-studio/
├── frontend/          # React + Vite (deploy to Vercel)
│   └── src/
│       ├── App.jsx
│       ├── pages/
│       │   ├── AuthPage.jsx
│       │   └── Dashboard.jsx
│       └── components/
│           ├── UploadView.jsx
│           └── HistoryView.jsx  (also contains UsageView, SettingsView)
│
├── backend/           # Node.js + Express (deploy to Railway/Render)
│   └── src/
│       ├── index.js           # Express app entry
│       ├── db.js              # SQLite via better-sqlite3
│       ├── middleware/
│       │   └── auth.js        # JWT authentication
│       ├── routes/
│       │   ├── auth.js        # /api/auth/register, /api/auth/login
│       │   ├── upload.js      # POST /api/upload
│       │   ├── jobs.js        # GET /api/job/:id
│       │   ├── user.js        # GET /api/user/usage|history, PUT /api/user/update
│       │   └── process.js     # GET /api/download/:id
│       └── services/
│           ├── processor.js   # Core Sharp + FFmpeg processing
│           └── cleanup.js     # Auto file deletion
│
└── README.md
```

---

## Quick Start (Local Development)

### Prerequisites
- **Node.js 18+**
- **FFmpeg** (for video processing)
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt install ffmpeg`
  - Windows: [ffmpeg.org/download](https://ffmpeg.org/download.html)

### 1. Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your JWT_SECRET (required)

npm install
npm run dev
# Runs on http://localhost:4000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

Open http://localhost:3000 — register an account and start cleaning files.

---

## API Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register` | No | Register new user |
| POST | `/api/auth/login` | No | Login, get JWT |
| POST | `/api/upload` | Yes | Upload + queue file for processing |
| GET | `/api/job/:id` | Yes | Poll job status + download URL |
| GET | `/api/download/:id` | Yes | Direct file download |
| GET | `/api/user/usage` | Yes | Daily/total usage stats |
| GET | `/api/user/history` | Yes | Processing history |
| PUT | `/api/user/update` | Yes | Update name/password |
| GET | `/api/health` | No | Health check |

### Upload Request
```
POST /api/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <binary>
options: {"removeExif": true, "noiseInjection": true, "reEncode": false, "stripAudio": true}
```

### Job Polling Response
```json
{
  "id": "uuid",
  "status": "queued|processing|done|error",
  "progress": 0-100,
  "downloadUrl": "/files/uuid.jpg",
  "metadata": { "removedFields": 7, "processedAt": "...", "operations": [...] },
  "error": null
}
```

---

## Processing Details

### Image Processing (Sharp.js)
1. **EXIF Stripping** — All EXIF metadata removed: GPS coordinates, camera make/model, timestamps, lens info, color profiles
2. **Re-encoding** — Full pixel re-encode through Sharp's processing pipeline (mozjpeg for JPEG, optimal PNG compression)
3. **AI Signature Reduction** — Subtle brightness/saturation modulation (±0.1%) to disrupt statistical patterns used by AI detection watermarking

### Video Processing (FFmpeg)
1. **Metadata Stripping** — `-map_metadata -1` removes all global metadata: GPS, creation_time, encoder info, handler names, vendor IDs
2. **Chapter Removal** — `-map_chapters -1` removes embedded chapter metadata
3. **Re-encoding** — H.264 with `libx264` at CRF 23 for full re-encode option (removes bitrate fingerprinting)
4. **Audio** — AAC re-encode strips audio stream metadata

### ⚠️ Important Disclaimer
AI signature reduction uses statistical noise injection and re-encoding. This **does not guarantee bypass** of all AI detection systems. Detection accuracy varies by:
- The specific detection tool used
- Version of AI model used to generate content
- Quality and strength of the original watermark

---

## Deployment

### Frontend → Vercel

```bash
cd frontend
npm run build
# Deploy dist/ to Vercel
```

Or connect your GitHub repo to Vercel and set:
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Environment Variable**: `VITE_API_URL=https://your-backend.railway.app`

Update `vite.config.js` proxy target to your backend URL for production.

### Backend → Railway

1. Create a Railway project
2. Connect GitHub repo
3. Set root directory to `backend/`
4. Add environment variables from `.env.example`
5. Railway auto-detects Node.js and runs `npm start`

**Required env vars for production:**
```
JWT_SECRET=<64-char random string>
NODE_ENV=production
FRONTEND_URL=https://your-app.vercel.app
PORT=4000
```

### Persistent Storage on Railway
Railway's filesystem is ephemeral. For production, either:

**Option A: Railway Volume** (simplest)
```
Add a Volume in Railway → mount at /app/data
Set DB_PATH=/app/data/deepclean.db
```

**Option B: AWS S3** for processed files
```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=deepclean-files
USE_S3=true
```

---

## Monetization

### Freemium Model
- **Free**: 5 files/day, 30-min file retention
- **Pro** ($9/mo or $19/mo): Unlimited files, 24h retention, priority queue

### Adding Stripe

```bash
cd backend
npm install stripe
```

Add to routes:
```js
// POST /api/billing/create-checkout
// POST /api/billing/webhook (Stripe webhook → set user.plan = 'pro')
```

---

## Security

- All uploads validated by MIME type + file extension
- Files stored with UUID names (no original filename exposure)
- JWT tokens expire in 7 days
- Rate limiting on auth routes (20 req/15min)
- Files auto-deleted after 30 minutes
- Helmet.js for HTTP security headers
- No permanent file storage for free users

---

## Dependencies

### Backend
| Package | Purpose |
|---------|---------|
| express | HTTP server |
| multer | Multipart file upload |
| sharp | Image processing + metadata stripping |
| fluent-ffmpeg | Video processing wrapper |
| better-sqlite3 | Database (zero-config, fast) |
| jsonwebtoken | JWT auth |
| bcryptjs | Password hashing |
| express-rate-limit | Rate limiting |
| helmet | HTTP security headers |
| node-schedule | Cron jobs |
| uuid | Unique IDs |

### Frontend
| Package | Purpose |
|---------|---------|
| react | UI framework |
| vite | Build tool |
| tailwindcss | Utility CSS (optional) |

---

## License
MIT
