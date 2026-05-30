# Local Development Setup

> Last updated: **2026-05-30**

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Node.js | 20 LTS | [nodejs.org](https://nodejs.org) |
| npm | 10+ | bundled with Node |
| Docker Desktop | 4.x | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Expo CLI | latest | `npm install -g expo` |
| EAS CLI | latest | `npm install -g eas-cli` |
| Python | 3.11+ | [python.org](https://www.python.org) |

---

## 1. Clone All Repos

```bash
mkdir rivheal && cd rivheal
git clone https://github.com/Iterative-Lead-Systems/rivheal-api
git clone https://github.com/Iterative-Lead-Systems/rivheal-frontend
git clone https://github.com/Iterative-Lead-Systems/rivheal-mobile-app
git clone https://github.com/Iterative-Lead-Systems/rivheal-infra
# Optional:
git clone https://github.com/Iterative-Lead-Systems/rivheal-ml-service
git clone https://github.com/Iterative-Lead-Systems/rasa-bot
```

---

## 2. Start Infrastructure (Docker)

```bash
cd rivheal-infra
cp .env.vpn.example .env       # edit: fill in DB password, JWT secret etc.
docker compose up -d           # starts: postgres, keycloak, redis, ml-service, rasa
```

Wait for Keycloak to be healthy (~2 min):
```bash
docker compose logs -f keycloak | grep "Running the server"
```

---

## 3. Backend (rivheal-api)

```bash
cd rivheal-api
cp .env.example .env           # edit env vars (see environment-variables.md)
npm install
npm run typeorm migration:run  # apply all DB migrations
npm run start:dev              # hot reload on :8000
```

Swagger: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

**Key .env values for local dev:**
```bash
NODE_ENV=development
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=rivheal
DB_USERNAME=rivheal
DB_PASSWORD=rivheal_dev
JWT_SECRET=dev-jwt-secret-change-me
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=redis_dev
ENABLE_AI_FEATURES=true        # optional — enable AI endpoints
ANTHROPIC_API_KEY=sk-ant-...   # optional — for Claude LLM triage
```

---

## 4. Admin Frontend (rivheal-frontend)

```bash
cd rivheal-frontend
cp .env.example .env           # set VITE_API_URL=http://localhost:8000
npm install
npm run dev                    # Vite dev server on :5173
```

---

## 5. Mobile App (rivheal-mobile-app)

```bash
cd rivheal-mobile-app
cp .env.example .env           # set API_URL, Keycloak config
npm install
npx expo start                 # Metro bundler
# Press 'a' for Android emulator, 'i' for iOS simulator, scan QR for device
```

> **Note:** You need an Expo account and `eas login` to build native dev clients. For basic JS changes, Metro is sufficient.

---

## 6. ML Service (optional)

```bash
cd rivheal-ml-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

FastAPI docs: [http://localhost:8001/docs](http://localhost:8001/docs)

---

## 7. Rasa Bot (optional)

Requires the Rasa CLI installed:
```bash
pip install rasa==3.6.21
cd rasa-bot
rasa train                     # trains NLU model (~5 min)
rasa run --enable-api --cors "*" &
cd actions && rasa run actions &
```

---

## Verify Everything Is Running

```bash
curl http://localhost:8000/api/health     # → { status: "ok" }
curl http://localhost:8001/health         # → ML service health
curl http://localhost:5005/               # → Rasa version
open http://localhost:8080               # Keycloak admin console
```
