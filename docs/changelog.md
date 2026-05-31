# Documentation Changelog

Changes to this documentation set. Newest entries first.

---

## 2026-05-31 — Rasa & ML Deployment Fixes

**Trigger:** Clarification session — docs did not explain how `rasa-bot/` and `rivheal-ml-service/` connect to Docker and the server. Three infrastructure bugs were also discovered and fixed.

**Bugs fixed (in compose files):**
1. `rasa-actions` in staging/prod pointed to a nonexistent custom GHCR image. Changed to official `rasa/rasa-sdk:3.6.2` with a volume mount.
2. `rasa` in staging/prod mounted an empty Docker named volume instead of the actual `rasa-bot/` repo. Changed to `${RASA_BOT_PATH}:/app`.
3. ML service GitHub Actions had wrong `context: ./rivheal-ml-service` (monorepo path). Fixed to `context: .` for standalone repo.
4. `RASA_SERVER_URL`, `RASA_ACTIONS_URL`, `ML_SERVICE_URL` missing from staging/prod API env block. Added.

**Docs updated:**
- `setup/deployment.md` — full rewrite of Rasa section; added step-by-step first-deploy checklist, Rasa training guide, how to update intents vs actions.
- `setup/docker-compose.md` — updated services table to clarify how each service gets its code (GHCR image / Docker Hub official / volume mount); added explanation of volume mount pattern.
- `setup/environment-variables.md` — added `RASA_BOT_PATH` with prominent warning note.

**Docs created:**
- `flows/rasa-deployment.md` — architecture diagram, first-deploy sequence, live message flow, update-intents flow, update-actions flow, troubleshooting table.

---

## 2026-05-30 — Initial Generation

**Trigger:** First run of `rivheal-doc` skill after major AI/ML implementation sprint.

**Created:**
- `README.md` — documentation index and quick links.
- `architecture.md` — full Mermaid system diagram including FastAPI ML service, Rasa, Claude API integration, and feature flag architecture.
- `principles.md` — extracted coding standards, security model, offline-first mobile strategy, AI/ML principles.
- `features/patient-app.md` — all 19 mobile screens inventoried with auth requirements and local storage strategy.
- `features/admin-panel.md` — all 20 admin pages inventoried; AI dashboard widgets documented.
- `features/ai-ml.md` — full AI feature status matrix (19 features), endpoint docs, formula for RivHealth Score.
- `features/integrations.md` — all external integrations (payments, SMS, storage, identity, HMO, AI).
- `setup/local-development.md` — end-to-end local setup for all 6 services.
- `setup/environment-variables.md` — complete env var reference (70+ variables).
- `setup/docker-compose.md` — compose file roles, services table, common commands.
- `setup/deployment.md` — server deploy, EAS mobile, ML model deploy, DB backup.
- `flows/appointment-booking.md` — full Mermaid sequence including ML wait-time prediction.
- `flows/queue-tracking.md` — Socket.io real-time + ML + REST fallback strategy.
- `flows/symptom-checker-llm.md` — Claude API triage flow with guest session merge.
- `flows/medication-adherence.md` — prescription scheduling, dose logging, adherence stats.
- `flows/telemedicine.md` — current state and planned WebRTC integration.
- `api/README.md` — auth, endpoint families, public routes, versioning, error codes.

**Codebase state at generation:**
- `rivheal-api`: 28 modules, NestJS 10, TypeORM, Keycloak SSO, Anthropic SDK `^0.100.1`.
- `rivheal-mobile-app`: Expo 56, React Native 0.85, WatermelonDB, 19 screens.
- `rivheal-frontend`: React 19, Vite, 20 feature pages, AI dashboard widgets.
- `rivheal-ml-service`: FastAPI 0.115, scikit-learn 1.5 (rule-based fallback; models not yet trained).
- `rasa-bot`: Rasa 3.6 scaffolding with Nigerian English + Pidgin NLU data.
- 5 TypeORM migrations added (queue snapshots, actual wait minutes, lab result previous value, dose log, hospital AI flag).

---

<!-- Add new entries above this line -->
