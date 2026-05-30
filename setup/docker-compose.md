# Docker Compose Guide

> Last updated: **2026-05-30**

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

| Service | Image | Port (dev) | Description |
|---|---|---|---|
| `postgres` | `postgres:16-alpine` | `5432` | Primary database |
| `keycloak_db` | `postgres:16-alpine` | internal | Keycloak backing store |
| `keycloak` | `keycloak:26.1.4` | `8080` | SSO / OIDC |
| `redis` | `redis:7-alpine` | `6379` | Cache + Bull job queue |
| `api` | build from `../rivheal-api` | `8000` | NestJS backend (hot reload in dev) |
| `ml-service` | build from `../rivheal-ml-service` | `8001` | FastAPI ML predictions |
| `rasa` | `rasa/rasa:3.6.21` | `5005` | Rasa NLU chatbot |
| `rasa-actions` | `rasa/rasa-sdk:3.6.2` | `5055` | Rasa custom actions |
| `traefik` | `traefik:v3.2` | `80`, `443` | Reverse proxy (prod only) |
| `mongodb` | `mongo:7` | internal | Document store (prod only) |

<!-- AUTO-GENERATED: compose-services-end -->

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
