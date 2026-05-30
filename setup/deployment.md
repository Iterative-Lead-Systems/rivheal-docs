# Deployment Guide

> Last updated: **2026-05-30**  
> See also: `rivheal-infra/DEPLOYMENT.md` for the detailed infra mental model.

---

## Deployment Targets

| Component | Host | Method |
|---|---|---|
| NestJS API | AWS EC2 (Docker) | GHCR image + Traefik |
| React Admin | AWS EC2 (Docker) or Cloudflare Pages | GHCR image + Traefik |
| Expo Mobile | App Store / Play Store | EAS Build + Submit |
| FastAPI ML | AWS EC2 (Docker) | GHCR image, internal only |
| Rasa Bot | AWS EC2 (Docker) | `rasa/rasa:3.6.21` |
| PostgreSQL | AWS EC2 (Docker) | Volume-backed, backed up nightly |
| Keycloak | AWS EC2 (Docker) | Realm auto-imported on first start |
| Marketing Website | Cloudflare Pages / Vercel | Next.js static export |

---

## Backend + Admin (Docker)

### First Deploy

```bash
# On the server
git clone https://github.com/Iterative-Lead-Systems/rivheal-infra /opt/rivheal
cd /opt/rivheal

# Generate secrets
bash scripts/generate-secrets.sh     # creates .env.prod
bash scripts/keycloak-bootstrap.sh   # fetches KC client secret

# Deploy all services
IMAGE_TAG=main docker compose \
  -f docker-compose.base.yml \
  -f docker-compose.prod.yml \
  --env-file .env.prod \
  up -d

# Run migrations
docker compose exec api npm run typeorm migration:run
```

### CI/CD (GitHub Actions)

The pattern used for the ML service (see `.github/workflows/deploy.yml` in `rivheal-ml-service`) applies to all services:

1. Push to `main` → build Docker image → push to `ghcr.io/iterative-lead-systems/rivheal-api:sha`.
2. Deploy step SSHs into the server and runs `docker compose up -d --no-deps api`.

### SSL / Domains

Traefik handles Let's Encrypt. Domain routing via Docker labels on each service:

| Service | Domain |
|---|---|
| API | `api.rivheal.com` |
| Admin | `emr.rivheal.com` |
| Keycloak | `auth.rivheal.com` |
| pgAdmin | `db-admin.rivheal.com` (VPN-only) |

---

## Mobile App (EAS)

### Prerequisites

```bash
npm install -g eas-cli
eas login
```

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

## ML Service

The ML service deploys as a Docker container. After training new models:

```bash
# Copy new model files to server
scp models/wait_time_model.pkl server:/opt/rivheal/ml-models/
scp models/no_show_model.pkl   server:/opt/rivheal/ml-models/

# Restart to pick up new models
docker compose restart ml-service
```

---

## Database Backups

`rivheal-infra/scripts/postgres-backup.sh` — run via cron:

```bash
# On server — daily at 2am
0 2 * * * docker exec rivheal_postgres bash /backup.sh >> /var/log/pg-backup.log 2>&1
```

Backups should be uploaded to S3 (`AWS_BUCKET_NAME`).
