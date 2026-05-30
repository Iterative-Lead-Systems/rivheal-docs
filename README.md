# RivHeal Platform Documentation

> Living documentation for the RivHeal EMR & patient-facing platform.  
> Last generated: **2026-05-30**

---

## What is RivHeal?

RivHeal is a multi-tenant Electronic Medical Records (EMR) platform built for Nigerian healthcare providers. It combines a full clinical EMR for hospital staff, a patient-facing mobile app with AI-powered health tools, and a data intelligence layer for predictive analytics.

---

## Repository Map

| Repo | Stack | Purpose |
|---|---|---|
| `rivheal-api` | NestJS 10, TypeORM, PostgreSQL | Core EMR backend + AI endpoints |
| `rivheal-frontend` | React 19, Vite, TanStack Query | Admin/clinical web dashboard |
| `rivheal-mobile-app` | Expo 56, React Native 0.85, NativeWind | Patient mobile app (iOS + Android) |
| `rivheal-infra` | Docker Compose, Traefik, Keycloak | Infrastructure and deployment config |
| `rivheal-ml-service` | Python 3.11, FastAPI, scikit-learn | ML prediction microservice |
| `rasa-bot` | Rasa 3.6 | NLU health chatbot (Nigerian languages) |
| `rivheal-website` | Next.js 14 | Public marketing website |

---

## Documentation Index

| Document | Description |
|---|---|
| [Architecture](./architecture.md) | System architecture, Mermaid diagrams, component responsibilities |
| [Principles](./principles.md) | Design principles, coding standards, security model |
| [Features → Patient App](./features/patient-app.md) | Mobile app screens and capabilities |
| [Features → Admin Panel](./features/admin-panel.md) | Clinical EMR features and pages |
| [Features → AI/ML](./features/ai-ml.md) | AI features, models, feature flags |
| [Features → Integrations](./features/integrations.md) | External services (payments, SMS, maps) |
| [Setup → Local Dev](./setup/local-development.md) | Getting started locally |
| [Setup → Environment Variables](./setup/environment-variables.md) | All env vars across services |
| [Setup → Docker Compose](./setup/docker-compose.md) | Running services with Docker |
| [Setup → Deployment](./setup/deployment.md) | Staging/production deployment guide |
| [Flows → Appointment Booking](./flows/appointment-booking.md) | End-to-end sequence diagram |
| [Flows → Queue Tracking](./flows/queue-tracking.md) | Real-time queue flow |
| [Flows → Symptom Checker + LLM](./flows/symptom-checker-llm.md) | AI-assisted triage flow |
| [Flows → Medication Adherence](./flows/medication-adherence.md) | Prescription tracking flow |
| [Flows → Telemedicine](./flows/telemedicine.md) | Video consultation flow |
| [API Overview](./api/README.md) | API structure, auth, versioning |
| [Changelog](./changelog.md) | Documentation update history |

---

## Quick Links

- **Swagger UI (local):** `http://localhost:8000/api/docs`
- **Swagger UI (staging):** `https://api-staging.rivheal.com/api/docs`
- **Keycloak Admin (local):** `http://localhost:8080`
- **ML Service (local):** `http://localhost:8001/docs`
