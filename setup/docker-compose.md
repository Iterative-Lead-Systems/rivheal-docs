# Docker Compose Guide

> Last updated: **2026-05-31**

---

## File Roles

<!-- AUTO-GENERATED: compose-files-start -->

| File | Purpose | How to Use |
|---|---|---|
| `docker-compose.yml` | Local development | `docker compose up -d` (standalone) |
| `docker-compose.base.yml` | Shared image definitions and healthchecks | Never used alone — always combined |
| `docker-compose.staging.yml` | Staging overlay (pre-built images) | `docker compose -f base.yml -f staging.yml up -d` |
| `docker-compose.prod.yml` | Production overlay (restart:always, no ports exposed) | `docker compose -f base.yml -f prod.yml up -d` |
| `docker-compose.vpn.yml` | WireGuard VPN service | `docker compose -f vpn.yml up -d` |

<!-- AUTO-GENERATED: compose-files-end -->

---

## Services

<!-- AUTO-GENERATED: compose-services-start -->

| Service | Image source | Port (dev) | How it gets its code |
|---|---|---|---|
| `postgres` | Docker Hub `postgres:16-alpine` | `5432` | Official image — no code |
| `keycloak_db` | Docker Hub `postgres:16-alpine` | internal | Official image — no code |
| `keycloak` | `quay.io/keycloak:26.1.4` | `8080` | Official image + realm JSON mounted |
| `redis` | Docker Hub `redis:7-alpine` | `6379` | Official image — no code |
| `api` | **Dev:** build from `../rivheal-api` / **Prod:** GHCR image | `8000` | Dev: hot-reload source mount / Prod: pre-built image |
| `ml-service` | **Dev:** build from `../rivheal-ml-service` / **Prod:** GHCR image | `8001` | Dev: source build / Prod: pre-built image via GitHub Actions |
| `rasa` | Docker Hub `rasa/rasa:3.6.21` | `5005` | **Volume mount:** `${RASA_BOT_PATH}:/app` |
| `rasa-actions` | Docker Hub `rasa/rasa-sdk:3.6.2` | `5055` | **Volume mount:** `${RASA_BOT_PATH}/actions:/app/actions` |
| `traefik` | Docker Hub `traefik:v3.2` | `80`, `443` | Prod only — config files mounted |
| `mongodb` | Docker Hub `mongo:7` | internal | Prod only — no code |

<!-- AUTO-GENERATED: compose-services-end -->

---

## How Each Service Gets Its Code

This is the most important thing to understand about the compose setup:

| Pattern | Services | Explanation |
|---|---|---|
| **Pre-built image (GHCR)** | `api`, `ml-service` | GitHub Actions builds + pushes image → server pulls it. Server never builds. |
| **Official image (Docker Hub)** | `postgres`, `redis`, `keycloak`, `traefik` | No custom code. Docker pulls the published image directly. |
| **Official image + volume mount** | `rasa`, `rasa-actions` | Uses official Rasa image. Your `rasa-bot/` folder is mounted in at runtime. Rasa reads your NLU data and actions from the mount. |

### Why Rasa uses volume mount instead of a custom image

Building a custom Rasa image would require baking the trained model into the image — which means rebuilding every time you update intents or retrain. The volume mount approach is simpler:
- Update `rasa-bot/` → `git pull` on server → `rasa train` → `restart rasa`
- No image build, no CI/CD pipeline required for Rasa changes

---

## Common Commands

```bash
# Start all dev services
cd rivheal-infra && docker compose up -d

# Start only core (postgres + keycloak + redis)
docker compose up -d postgres keycloak redis

# Rebuild API image after code changes
docker compose up -d --build api

# View logs
docker compose logs -f api
docker compose logs -f ml-service

# Run a DB migration inside the API container
docker compose exec api npm run typeorm migration:run

# Open a psql shell
docker compose exec postgres psql -U rivheal rivheal

# Restart a single service
docker compose restart ml-service
```

## Staging / Production Deploy

```bash
export IMAGE_TAG=v1.2.3

# Staging
docker compose \
  -f docker-compose.base.yml \
  -f docker-compose.staging.yml \
  --env-file .env.staging \
  up -d --no-deps api

# Production
docker compose \
  -f docker-compose.base.yml \
  -f docker-compose.prod.yml \
  --env-file .env.prod \
  up -d --no-deps api
```
