# External Integrations

> Last updated: **2026-05-30**

---

<!-- AUTO-GENERATED: integrations-start -->

## Payment Gateways

| Provider | Env Var | Purpose | Status |
|---|---|---|---|
| Paystack | `PAYSTACK_SECRET_KEY`, `PAYSTACK_PUBLIC_KEY` | Card payments, bank transfer | 🟡 Config present |
| Flutterwave | `FLUTTERWAVE_SECRET_KEY`, `FLUTTERWAVE_PUBLIC_KEY` | Alternative payment gateway | 🟡 Config present |

## SMS / Messaging

| Provider | Env Var | Purpose | Status |
|---|---|---|---|
| Termii | `TERMII_API_KEY`, `TERMII_BASE_URL`, `TERMII_SENDER_ID` | OTP delivery, appointment SMS | 🟡 Config present |

## Cloud Storage

| Provider | Env Var | Purpose | Status |
|---|---|---|---|
| Cloudinary | `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` | Profile photos, report PDFs | 🟡 Config present |
| AWS S3 | `AWS_BUCKET_NAME`, `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | Backup file storage | 🟡 Config present |

## Maps & Location

| Provider | Env Var | Purpose | Status |
|---|---|---|---|
| Google Maps | `GOOGLE_MAPS_API_KEY` | Hospital search, distance calculation | 🟡 Config present |
| Expo Location | — | Patient device GPS for nearest-hospital lookup | ✅ Implemented |

## Identity & Verification

| Provider | Env Var | Purpose | Status |
|---|---|---|---|
| NIMC | `NIMC_API_KEY`, `NIMC_API_URL` | NIN verification | 🟡 Config present |
| MDCN | `MDCN_API_KEY`, `MDCN_API_URL` | Doctor credential verification | 🟡 Config present |
| Keycloak | `KEYCLOAK_URL`, `KEYCLOAK_REALM`, `KEYCLOAK_CLIENT_ID/SECRET` | SSO, OIDC, PKCE mobile auth | ✅ Implemented |

## HMO Partners

| Provider | Env Var | Purpose |
|---|---|---|
| AXA Mansard | `AXA_MANSARD_API_KEY` | HMO claim validation |
| Hygeia | `HYGEIA_API_KEY` | HMO claim validation |
| Reliance HMO | `RELIANCE_HMO_API_KEY` | HMO claim validation |
| HealthPlus | `HEALTHPLUS_API_KEY` | HMO claim validation |

## Push Notifications

| Provider | SDK | Purpose | Status |
|---|---|---|---|
| Expo Push | `expo-notifications` | Mobile push (appointment, queue) | ✅ Implemented |

## AI / ML (External APIs)

| Provider | Env Var | Purpose | Status |
|---|---|---|---|
| Anthropic (Claude) | `ANTHROPIC_API_KEY` | Symptom checker LLM triage | ✅ Implemented |
| OpenAI | `OPENAI_API_KEY` | Alternative LLM (not yet used) | ❌ Not wired |

## Observability

| Provider | Env Var | Purpose | Status |
|---|---|---|---|
| Sentry | `SENTRY_DSN` | Mobile crash reporting | 🟡 SDK installed, DSN not set |
| PostHog / Mixpanel | — | Mobile analytics | ❌ Stub only |

<!-- AUTO-GENERATED: integrations-end -->
