# Documentation Changelog

Changes to this documentation set. Newest entries first.

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
