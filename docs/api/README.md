# API Overview

> Base URL: `https://api.rivheal.com/api/v1`  
> Swagger UI: `https://api.rivheal.com/api/docs`  
> Last updated: **2026-05-30**

---

<!-- AUTO-GENERATED: api-overview-start -->

## Authentication

RivHeal uses two complementary JWT mechanisms:

### 1. App-Issued JWT (Primary)
- **Login:** `POST /auth/login` → returns `{ accessToken, refreshToken, expiresIn, user }`.
- **Token type:** Bearer, sent as `Authorization: Bearer <token>`.
- **Refresh:** `POST /auth/refresh` with `{ refreshToken }` → new token pair.
- **Logout:** `POST /auth/logout` invalidates the refresh token.

### 2. Keycloak OIDC (SSO)
- Used for staff SSO login via browser (admin dashboard).
- The NestJS JWT strategy accepts both app-issued JWTs (sub = user.id) and Keycloak JWTs (sub = keycloak UUID) transparently.
- Mobile app uses PKCE flow via `expo-web-browser`.

### Request Headers

| Header | Required On | Description |
|---|---|---|
| `Authorization: Bearer <token>` | All protected routes | JWT access token |
| `X-Hospital-Id: <uuid>` | Admin endpoints | Hospital context |
| `X-Branch-Id: <uuid>` | Admin endpoints | Branch context |
| `X-Guest-Session-Id: <uuid>` | Public mobile endpoints | Guest session tracking |
| `X-Client-Type: mobile` | Mobile app requests | Client identification |

---

## API Families

| Tag | Base Path | Description |
|---|---|---|
| Authentication | `/auth` | Login, register, refresh, logout, verify, merge-guest |
| Patients | `/patients` | Patient CRUD, enrollment, health score, lab alerts, adherence |
| Appointments | `/appointments` | Scheduling, queue, slots, status transitions |
| OPD | `/opd` | Consultations, vitals, diagnoses, prescriptions |
| Laboratory | `/laboratory` | Lab tests, orders, results |
| Pharmacy | `/pharmacy` | Drug stock, dispense orders |
| Billing | `/billing` | Invoices, payments, HMO claims, wallet |
| Inventory | `/inventory` | Items, purchase orders, suppliers, stock |
| Emergency | `/emergency` | Emergency cases, ambulances |
| Ward | `/ward` | Beds, admissions, nursing notes, transfers |
| Radiology | `/radiology` | Imaging orders |
| Home Care | `/homecare` | Home care requests and practitioners |
| Hospitals | `/hospitals` | Hospital management |
| Branches | `/branches` | Branch management |
| Departments | `/departments` | Department management |
| Staff | `/staff` | Staff management |
| Notifications | `/notifications` | Push tokens, templates, user notifications |
| Dashboard | `/dashboard` | KPI statistics |
| AI Health Assistant | `/assistant` | Rasa chat, symptom assessment |
| Symptom Checker | `/symptom-checker` | Standalone triage (LLM + rules) |
| ML Predictions | `/predict` | Wait-time, no-show prediction |
| Mobile | `/mobile` | App version, health tips |
| Health Score | `/patients/:id/health-score` | RivHealth Score |
| Lab Alerts | `/patients/:id/lab-alerts` | Abnormal lab alerts |
| Medication Adherence | `/medications`, `/patients/:id/adherence` | Dose logs and adherence stats |

---

## Key Public Endpoints

These endpoints require no authentication (marked `@Public()`):

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/login` | Login |
| `POST` | `/auth/register` | Register patient |
| `POST` | `/auth/refresh` | Refresh tokens |
| `POST` | `/auth/forgot-password` | Request password reset |
| `POST` | `/auth/reset-password` | Reset password |
| `POST` | `/auth/verify-email` | Verify email address |
| `POST` | `/symptom-checker/analyze` | AI symptom triage |
| `POST` | `/assistant/chat/guest` | Guest AI chat |
| `POST` | `/assistant/symptoms/assess/guest` | Guest symptom assessment |
| `GET` | `/mobile/version` | App version check |
| `GET` | `/health-tips` | Static health tips |
| `GET` | `/hospitals` | List hospitals (public discovery) |
| `GET` | `/assistant/health` | AI service health check |

---

## Versioning Policy

- Current version: **v1** (path prefix `/api/v1/`).
- Breaking changes increment the version number.
- Old versions are maintained for a minimum of 6 months after a new version is released.
- Deprecation notices are added to the relevant Swagger operations (`@ApiOperation({ deprecated: true })`).

---

## Rate Limiting

Default limits (configurable via `THROTTLE_TTL` and `THROTTLE_LIMIT`):
- **100 requests per 60 seconds** per IP address.
- Auth endpoints have a lower limit via Traefik middleware (`auth-ratelimit`).

---

## Error Responses

All errors follow the standard NestJS exception format:

```json
{
  "statusCode": 400,
  "message": "Appointment time slot is not available",
  "error": "Bad Request"
}
```

Common status codes:

| Code | Meaning |
|---|---|
| `400` | Bad request / validation error |
| `401` | Unauthenticated |
| `403` | Forbidden (wrong role or AI feature disabled) |
| `404` | Resource not found |
| `409` | Conflict (e.g., duplicate appointment slot) |
| `422` | Unprocessable entity |
| `503` | External service unavailable (Rasa, ML service) |

<!-- AUTO-GENERATED: api-overview-end -->
