# Deployment Guide

> Last updated: **2026-05-31**  
> See also: `rivheal-infra/DEPLOYMENT.md` for the detailed infra mental model.

---

## Deployment Targets

<!-- AUTO-GENERATED: targets-start -->

| Component | Host | Method | Image source |
|---|---|---|---|
| NestJS API | AWS EC2 (Docker) | GHCR image → Traefik | GitHub Actions → `ghcr.io/.../rivheal-api` |
| React Admin | AWS EC2 (Docker) or Cloudflare Pages | GHCR image → Traefik | GitHub Actions → `ghcr.io/.../rivheal-emr-frontend` |
| FastAPI ML Service | AWS EC2 (Docker) | GHCR image, internal only | GitHub Actions → `ghcr.io/.../rivheal-ml-service` |
| Rasa NLU | AWS EC2 (Docker) | Official image + volume mount | `docker.io/rasa/rasa:3.6.21` (Docker Hub) |
| Rasa Actions | AWS EC2 (Docker) | Official image + volume mount | `docker.io/rasa/rasa-sdk:3.6.2` (Docker Hub) |
| Expo Mobile | App Store / Play Store | EAS Build + Submit | EAS cloud build |
| PostgreSQL | AWS EC2 (Docker) | Volume-backed, backed up nightly | `postgres:16-alpine` |
| Keycloak | AWS EC2 (Docker) | Realm auto-imported on first start | `quay.io/keycloak/keycloak:26.1.4` |
| Marketing Website | Cloudflare Pages / Vercel | Next.js static export | — |

<!-- AUTO-GENERATED: targets-end -->

---

## How Deployment Works — The Pattern

Every service that has custom code follows the same flow:

```
Developer pushes code to GitHub
        ↓
GitHub Actions:
  1. Builds a Docker image from the code
  2. Pushes it to GHCR (GitHub Container Registry)
        ↓
Server (AWS EC2):
  - docker compose pull <service>   ← downloads the pre-built image
  - docker compose up -d <service>  ← swaps old container for new one
  - server never builds anything itself
```

Services that use **official images** (Rasa, PostgreSQL, Redis, Keycloak) skip the build step entirely — Docker Hub hosts them.

---

## First Deploy — Full Server Setup

```bash
# 1. Clone the infra repo
git clone https://github.com/Iterative-Lead-Systems/rivheal-infra /opt/rivheal
cd /opt/rivheal

# 2. Clone rasa-bot (needed for Rasa volume mount)
git clone https://github.com/Iterative-Lead-Systems/rasa-bot ~/rasa-bot

# 3. Generate secrets and fill in .env.prod
bash scripts/generate-secrets.sh     # creates .env.prod with random secrets
bash scripts/keycloak-bootstrap.sh   # fetches Keycloak client secret after start

# 4. Add required non-generated values to .env.prod:
#    RASA_BOT_PATH=/home/ubuntu/rasa-bot   ← absolute path to rasa-bot clone
#    ANTHROPIC_API_KEY=sk-ant-...          ← Claude API key (if AI features enabled)
#    ENABLE_AI_FEATURES=true               ← set to true when ready

# 5. Start all core services
IMAGE_TAG=main docker compose \
  -f docker-compose.base.yml \
  -f docker-compose.prod.yml \
  --env-file .env.prod \
  up -d

# 6. Run database migrations
docker compose exec api npm run typeorm migration:run

# 7. Train the Rasa NLU model (see Rasa section below)
docker compose exec rasa rasa train
docker compose restart rasa
```

---

## CI/CD — Deploying Code Changes

### NestJS API
```
Push to main branch in rivheal-api repo
    → GitHub Actions builds + pushes image to GHCR
    → SSH into server
    → IMAGE_TAG=<sha> docker compose up -d --no-deps api
```

### FastAPI ML Service
```
Push to main branch in rivheal-ml-service repo
    → GitHub Actions (.github/workflows/deploy.yml) builds image (context: .)
    → Pushes to ghcr.io/iterative-lead-systems/rivheal-ml-service:<sha>
    → SSH into server
    → IMAGE_TAG=<sha> docker compose up -d --no-deps ml-service
```

> **Note:** `rivheal-ml-service` must be its own GitHub repo. Push the local folder:
> ```bash
> cd rivheal-ml-service
> git init && git remote add origin https://github.com/your-org/rivheal-ml-service
> git push -u origin main
> ```

### Rasa Bot (no CI/CD — git pull + retrain)
Rasa uses official Docker Hub images, not custom-built ones. Updating it is a manual git pull + retrain:
```bash
# On the server:
cd ~/rasa-bot && git pull
docker compose exec rasa rasa train
docker compose restart rasa
```

---

## Rasa — Full Deployment & Training Guide

### What `rasa-bot/` contains

```
rasa-bot/
├── data/
│   ├── nlu.yml       ← training examples ("I have fever" → intent: report_symptom)
│   └── stories.yml   ← conversation flows (greet → assess → respond)
├── domain/
│   └── domain.yml    ← intents, responses, slots, actions declared here
├── config.yml        ← NLU model config (DIET classifier, TEDPolicy)
├── actions/
│   └── actions.py    ← custom Python logic run when Rasa calls an action
└── models/           ← trained model files land here after rasa train
```

### How the containers use this folder

```
~/rasa-bot/                    ← your folder, mounted into containers
      │
      ├─ mounted as /app          → rasa container
      │   reads: data/, domain/, config.yml
      │   serves: trained model at http://rasa:5005
      │   writes: models/ after rasa train
      │
      └─ actions/ mounted as /app/actions → rasa-actions container
          reads: actions.py
          serves: custom action calls at http://rasa-actions:5055
```

### Connection to NestJS API

```
Patient sends message in ChatAssistantScreen (mobile)
        ↓
POST /assistant/chat  (NestJS API)
        ↓
RasaService.sendMessage()
        ↓
POST http://rasa:5005/webhooks/rest/webhook
  { sender: "session-id", message: "I have a fever" }
        ↓
Rasa NLU classifies intent → report_symptom
        ↓
Rasa calls action: action_assess_symptoms
        ↓
rasa-actions container runs actions.py → returns response text
        ↓
NestJS returns response to mobile app
```

### Training the model

The model must be trained once before Rasa can respond to anything. Without a trained model, Rasa starts but returns errors on every message.

```bash
# Connect to the running rasa container
docker compose exec rasa rasa train

# What happens:
# - Reads data/nlu.yml, data/stories.yml, domain/domain.yml, config.yml
# - Trains a DIET classifier NLU model (~2-3 minutes)
# - Saves model to ~/rasa-bot/models/<timestamp>.tar.gz
# - That file is on the server (volume mount), not inside the container

# Restart Rasa to pick up the new model
docker compose restart rasa

# Verify it's working
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test", "message": "hello"}'
# Should return: [{"recipient_id":"test","text":"Hello! I'm your RivHeal health assistant..."}]
```

### Updating intents / responses

```bash
# 1. Edit files locally
vim rasa-bot/data/nlu.yml        # add new training examples
vim rasa-bot/domain/domain.yml   # add new intents / responses

# 2. Commit and push
git add . && git commit -m "add intent: ask_lab_results"
git push

# 3. On the server — pull and retrain
cd ~/rasa-bot && git pull
docker compose exec rasa rasa train
docker compose restart rasa
```

### Updating custom actions (actions.py)

```bash
# Edit locally, push, then on server:
cd ~/rasa-bot && git pull
docker compose restart rasa-actions   # no retrain needed — just reload Python
```

---

## ML Service — Deploying Model Updates

The ML service starts with rule-based fallback (no `.pkl` file needed). Once you have enough training data:

```bash
# 1. Export training data from the database
docker compose exec postgres psql -U rivheal rivheal \
  -c "\COPY (SELECT ...) TO '/tmp/appointments.csv' CSV HEADER"

# 2. Train locally
cd rivheal-ml-service
python trainers/train.py --model wait_time --csv data/appointments.csv
python trainers/train.py --model no_show   --csv data/appointments.csv
# Creates: models/wait_time_model.pkl, models/no_show_model.pkl

# 3. Commit the model files and push → GitHub Actions builds new image → deploy
git add models/ && git commit -m "update: retrained wait-time model May 2026"
git push
# GitHub Actions will build new image and deploy automatically
```

---

## Mobile App (EAS)

### Build Profiles (`eas.json`)

| Profile | Platform | Distribution | Use Case |
|---|---|---|---|
| `development` | Android + iOS | Internal | Dev client with Metro bundler |
| `preview` | Android APK | Internal | APK for QA testing |
| `production` | Android AAB + iOS IPA | Store | App Store / Play Store submission |

### Build Commands

```bash
cd rivheal-mobile-app

# Android dev client
eas build --platform android --profile development

# Android APK for testing
eas build --platform android --profile preview

# Production build (both platforms)
eas build --platform all --profile production

# Submit to stores
eas submit --platform ios
eas submit --platform android
```

### Environment per Profile

Set `extra.apiUrl` in `app.config.ts` per variant:

```typescript
const variants = {
  development: 'http://localhost:8000',
  preview:     'https://api-staging.rivheal.com',
  production:  'https://api.rivheal.com',
};
```

---

## SSL / Domains

Traefik handles Let's Encrypt automatically. Domain routing via Docker labels on each service:

| Service | Domain |
|---|---|
| API | `api.rivheal.com` |
| Admin | `emr.rivheal.com` |
| Keycloak | `auth.rivheal.com` |
| pgAdmin | `db-admin.rivheal.com` (VPN-only) |

---

## Database Backups

`rivheal-infra/scripts/postgres-backup.sh` — run via cron:

```bash
# On server — daily at 2am
0 2 * * * docker exec rivheal_postgres bash /backup.sh >> /var/log/pg-backup.log 2>&1
```

Backups should be uploaded to S3 (`AWS_BUCKET_NAME`).
