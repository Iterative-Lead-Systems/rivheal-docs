# RivHeal Design Principles & Coding Standards

> Last updated: **2026-05-30**

These principles are extracted from the codebase and represent the patterns that must be followed for consistency and correctness.

---

## 1. API Design

<!-- AUTO-GENERATED: api-principles-start -->

### RESTful + Versioned
- Global prefix: `/api` · URI versioning: `/api/v1/`
- All routes follow REST conventions (`GET` read, `POST` create, `PUT` full update, `PATCH` partial, `DELETE`).
- New breaking changes increment the version (`/api/v2/...`); existing routes must not break.

### Public vs Protected
```typescript
@Public()          // No auth — guests and external consumers
@UseGuards(JwtAuthGuard)  // JWT required
@Roles(SYSTEM_ROLES.DOCTOR)  // JWT + role check
```
Every new endpoint must explicitly choose one of these patterns. **Default is protected.**

### Multi-tenant Context
- Admin endpoints require `X-Hospital-Id` and `X-Branch-Id` HTTP headers.
- Services receive a typed `IRequestContext` with `hospitalId`, `branchId`, `userId`.
- Never expose data across hospital boundaries — all queries include `WHERE hospital_id = $1`.

### DTOs and Validation
- All request bodies use `class-validator` DTOs with `ValidationPipe` globally enabled.
- Response shapes are typed DTOs. No raw entity exposure to clients.
- `ClassSerializerInterceptor` is globally applied — use `@Exclude()` on sensitive fields.

### Swagger
- Every endpoint must have `@ApiTags()`, `@ApiOperation()`, and `@ApiResponse()`.
- Swagger UI is available at `/api/docs`.

<!-- AUTO-GENERATED: api-principles-end -->

---

## 2. Database

<!-- AUTO-GENERATED: db-principles-start -->

### Entity Conventions
- All entities extend `BaseEntity` or `BranchScopedEntity` (from `@/common/base`).
- `BaseEntity` provides: `id` (UUID), `createdAt`, `updatedAt`, `deletedAt` (soft delete), `createdBy`, `updatedBy`, `version` (optimistic locking).
- `BranchScopedEntity` adds `hospitalId` + `branchId`.
- **No TypeORM enums in the DB** — columns are `VARCHAR`. Constants and types are defined in `@/common/constants/index.ts`.

### Repository Pattern
- Every module uses a typed repository class extending `BranchScopedRepository<T>` or `BaseRepository<T>`.
- Direct `DataSource` queries (via `this.dataSource.query(...)`) are acceptable for complex analytics; use parameterised queries always.

### Migrations
- All schema changes are in `src/database/migrations/`. Timestamp prefix: `YYYYMMDDHHMMSS`.
- **Never use `synchronize: true` in production.** Only allowed in `development`.
- Every migration has a matching `down()` method.
- Run: `npm run typeorm migration:run`.

### Soft Deletes
- Use `deletedAt` (already in `BaseEntity`) for all user-facing records.
- Hard-deletes are only for infrastructure tables (e.g., `queue_snapshots` older than 90 days — add a cron cleanup job).

<!-- AUTO-GENERATED: db-principles-end -->

---

## 3. Security

<!-- AUTO-GENERATED: security-principles-start -->

### Authentication Flow
1. Patient/staff registers or logs in → API issues JWT (access + refresh tokens).
2. Keycloak SSO tokens are also accepted — dual-lookup JWT strategy.
3. JWT secret lives in `JWT_SECRET` env var. Refresh secret in `JWT_REFRESH_SECRET`.
4. Access token TTL: configurable via `JWT_EXPIRES_IN`. Refresh: `JWT_REFRESH_EXPIRES_IN`.

### Password Storage
- `bcrypt` with salt rounds. Password history table prevents reuse of last N passwords.

### Input Sanitisation
- Helmet middleware for HTTP security headers.
- Global `ValidationPipe` with `whitelist: true` strips unknown properties.
- Parameterised queries — no string concatenation in SQL.

### Data Privacy (NDPR)
- Patient PII is encrypted at rest via the `ENCRYPTION_KEY` env var.
- Audit logs stored in MongoDB with a 2-year TTL index (auto-delete via NDPR requirement).
- Soft deletes ensure patient records are recoverable within retention window.

### Network Security
- Production admin endpoints (`/keycloak`, `/pgadmin`, `/traefik`) are behind VPN-only Traefik middleware.
- ML service is internal only (no Traefik route in prod).
- WireGuard VPN managed by `rivheal-infra/scripts/`.

<!-- AUTO-GENERATED: security-principles-end -->

---

## 4. Mobile App

<!-- AUTO-GENERATED: mobile-principles-start -->

### Offline-First
- Symptom history and wellness metrics are stored locally in **WatermelonDB** (SQLite via JSI) before syncing.
- MMKV stores non-sensitive fast-access data (guest session ID, feature flags cache, onboarding state).
- Auth tokens use **Expo SecureStore** (Keychain / Keystore).

### Guest Sessions
- Unauthenticated users receive a `guestSessionId` (UUID stored in MMKV).
- Guest session ID is sent as `X-Guest-Session-Id` header on all API requests.
- On login, `POST /auth/merge-guest-session` migrates guest data to the authenticated patient.

### Navigation
- React Navigation v6 — native stack.
- Public screens (Symptom Checker, Hospitals, Emergency, Chat Assistant) are accessible without login.
- Auth-gated screens render a sign-in prompt instead of crashing.

### Push Notifications
- Expo Notifications SDK handles permission request + token registration.
- Medication reminders are local notifications (no server round-trip).
- Queue and appointment updates are server-sent via Expo Push tokens registered with the API.

### Real-time
- Socket.io-client connects to `/queue` namespace for live queue position updates.
- Polling fallback (`QUEUE_POLL_INTERVAL_MS = 10s`) if WebSocket is unavailable.

<!-- AUTO-GENERATED: mobile-principles-end -->

---

## 5. AI/ML Principles

<!-- AUTO-GENERATED: ai-principles-start -->

### Graceful Degradation
- Every AI endpoint has a deterministic fallback. No AI call should crash the user flow.
- `MlProxyService` has a 5-second timeout; on failure it returns `{ isFallback: true, predictedWaitMinutes: 30 }`.
- `SymptomCheckerService` tries Claude API first; if unavailable it falls back to keyword-matching rules.

### Feature Flag Gating
- `ENABLE_AI_FEATURES=true` is required globally.
- `hospitals.ai_features_enabled = true` is required per tenant.
- Both must be true for AI features to activate.

### No PII to External Models
- Patient names, IDs, and contact info are **never sent** to Claude or any external ML API.
- Symptom strings and anonymised features (age-bucket, hour-of-day, queue length) are the only inputs.

### Model Lifecycle
- ML models are trained offline via `rivheal-ml-service/trainers/train.py`.
- Trained models are stored as `.pkl` files in `rivheal-ml-service/models/`.
- Model updates require a container redeploy (`docker compose up -d ml-service`).
- Target: retrain monthly as new appointment data accumulates.

<!-- AUTO-GENERATED: ai-principles-end -->

---

## 6. Code Style

<!-- AUTO-GENERATED: code-style-start -->

### TypeScript
- Strict mode enabled. No `any` without a justification comment.
- Path aliases: `@/` maps to `src/` in both the API and mobile app.
- Barrel exports (`index.ts`) for each module's public surface.

### Naming
- Files: `kebab-case.ts`
- Classes: `PascalCase`
- Variables/functions: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Database columns: `snake_case` (mapped via TypeORM `name:` option)

### Comments
- Comments only where the "why" is non-obvious. No "what" comments.
- No multi-line block comments on obvious code.

<!-- AUTO-GENERATED: code-style-end -->
