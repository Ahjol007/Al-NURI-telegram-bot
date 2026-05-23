# Al-NURI Telegram Bot

Telegram bot for Al-NURI company — client reception, lead generation, AI chat, admin panel.

**Stack:** Python 3.11, aiogram 3.x, FastAPI, SQLAlchemy 2.x async, Gemini API, PostgreSQL, Railway

---

## Project Structure

```
al-nuri-bot/
├── bot/                    # Bot Service (aiogram webhook)
├── ai_service/             # AI Service (FastAPI + Gemini)
├── admin_service/          # Admin Service (FastAPI)
└── db/schema.sql           # Database schema
```

## Railway Deployment

### 1. Create Railway Project

1. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub repo
2. Add PostgreSQL plugin: New → Database → PostgreSQL
3. Run `db/schema.sql` in the Railway PostgreSQL Query editor

### 2. Bot Service

- **Root Directory:** `bot`
- **Start Command:** `python main.py`

**Environment Variables:**
```
BOT_TOKEN=<telegram_bot_token>
ADMIN_TELEGRAM_ID=<your_telegram_id>
DATABASE_URL=<Railway PostgreSQL URL — replace postgresql:// with postgresql+asyncpg://>
AI_SERVICE_URL=http://ai-service.railway.internal:8001
WEBHOOK_BASE_URL=https://<bot-service-domain>.up.railway.app
```

### 3. AI Service

- **Root Directory:** `ai_service`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
```
GEMINI_API_KEY=<gemini_api_key>
```

### 4. Admin Service

- **Root Directory:** `admin_service`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
```
BOT_TOKEN=<telegram_bot_token>
ADMIN_TELEGRAM_ID=<your_telegram_id>
DATABASE_URL=<Railway PostgreSQL URL — replace postgresql:// with postgresql+asyncpg://>
```

### 5. Set Admin Service Webhook

After deploying admin service, run:
```bash
curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://<admin-service-domain>.up.railway.app/admin-webhook"}'
```

> **Note:** The bot service sets its own webhook automatically on startup.

---

## Admin Commands

| Command | Description |
|---------|-------------|
| `/admin_help` | List all commands |
| `/admin_stats` | User count and new consultations |
| `/admin_users` | Last 10 registered users |
| `/admin_consults` | New consultation requests |
| `/admin_broadcast <text>` | Send message to all users |

---

## Local Testing (AI Service only)

```bash
cd ai_service
pip install -r requirements.txt
GEMINI_API_KEY=your_key uvicorn main:app --port 8001

curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "message": "Фитогель туралы айтшы", "language": "kk"}'
```
