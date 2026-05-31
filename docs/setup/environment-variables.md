# Environment Variables Reference

> Last updated: **2026-05-30**  
> Sources: `rivheal-api/.env.example`, `rivheal-infra/docker-compose.yml`, `rivheal-mobile-app/src/utils/constants.ts`

---

<!-- AUTO-GENERATED: env-vars-start -->

## rivheal-api

### Core Application
| Variable | Default | Description |
|---|---|---|
| `NODE_ENV` | `development` | `development` \| `staging` \| `production` |
| `APP_PORT` | `3000` | HTTP server port |
| `APP_NAME` | — | Application name (used in emails) |
| `APP_URL` | — | Public URL (used in email links) |
| `FRONTEND_URL` | `http://localhost:5173` | CORS allowed origin |

### Database (PostgreSQL)
| Variable | Default | Description |
|---|---|---|
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_DATABASE` | `rivheal` | Database name |
| `DB_USERNAME` | `rivheal` | Database user |
| `DB_PASSWORD` | — | Database password |
| `DB_LOGGING` | `false` | Enable query logging (`true` = verbose) |
| `DB_SSL` | `false` | Enable SSL (`true` in production) |

### MongoDB
| Variable | Default | Description |
|---|---|---|
| `MONGODB_URI` | — | Full MongoDB connection string |

### Redis / Queue
| Variable | Default | Description |
|---|---|---|
| `REDIS_HOST` | `localhost` | Redis host |
| `REDIS_PORT` | `6379` | Redis port |
| `REDIS_PASSWORD` | — | Redis password |
| `REDIS_DB` | `0` | Redis database index |
| `QUEUE_PREFIX` | `rivheal` | Bull queue key prefix |

### Authentication (JWT)
| Variable | Default | Description |
|---|---|---|
| `JWT_SECRET` | — | JWT signing secret (min 32 chars) |
| `JWT_EXPIRES_IN` | `15m` | Access token TTL |
| `JWT_REFRESH_SECRET` | — | Refresh token signing secret |
| `JWT_REFRESH_EXPIRES_IN` | `7d` | Refresh token TTL |
| `ENCRYPTION_KEY` | — | AES key for PII encryption (32 bytes hex) |
| `OTP_SECRET` | — | OTP HMAC secret |
| `OTP_EXPIRY_MINUTES` | `10` | OTP validity window |

### Keycloak (SSO)
| Variable | Default | Description |
|---|---|---|
| `KEYCLOAK_URL` | `http://localhost:8080` | Keycloak server URL |
| `KEYCLOAK_REALM` | `rivheal` | Realm name |
| `KEYCLOAK_CLIENT_ID` | `api-server` | API client ID |
| `KEYCLOAK_CLIENT_SECRET` | — | API client secret |

### Email (SMTP)
| Variable | Default | Description |
|---|---|---|
| `MAIL_HOST` | — | SMTP host |
| `MAIL_PORT` | `587` | SMTP port |
| `MAIL_USER` | — | SMTP username |
| `MAIL_PASSWORD` | — | SMTP password |
| `MAIL_FROM` | — | Sender email |
| `MAIL_FROM_NAME` | `RivHeal` | Sender display name |

### AI / ML
| Variable | Default | Description |
|---|---|---|
| `ENABLE_AI_FEATURES` | `false` | Global AI feature toggle |
| `ANTHROPIC_API_KEY` | — | Claude API key (for LLM symptom checker) |
| `ML_SERVICE_URL` | `http://ml-service:8000` | FastAPI prediction service URL |
| `RASA_SERVER_URL` | `http://localhost:5005` | Rasa NLU webhook URL |
| `RASA_ACTIONS_URL` | `http://localhost:5055` | Rasa actions server URL |
| `RASA_AUTH_TOKEN` | — | Optional Rasa auth token |
| `RASA_MODEL_NAME` | `rivheal-health-assistant` | Rasa model name |
| `RASA_MODEL_VERSION` | `1.0.0` | Rasa model version |

### Payments
| Variable | Default | Description |
|---|---|---|
| `PAYSTACK_SECRET_KEY` | — | Paystack secret key |
| `PAYSTACK_PUBLIC_KEY` | — | Paystack public key |
| `FLUTTERWAVE_SECRET_KEY` | — | Flutterwave secret |
| `FLUTTERWAVE_PUBLIC_KEY` | — | Flutterwave public key |

### SMS (Termii)
| Variable | Default | Description |
|---|---|---|
| `TERMII_API_KEY` | — | Termii API key |
| `TERMII_BASE_URL` | — | Termii base URL |
| `TERMII_SENDER_ID` | `RivHeal` | SMS sender ID |

### Storage
| Variable | Default | Description |
|---|---|---|
| `CLOUDINARY_CLOUD_NAME` | — | Cloudinary cloud |
| `CLOUDINARY_API_KEY` | — | Cloudinary key |
| `CLOUDINARY_API_SECRET` | — | Cloudinary secret |
| `AWS_BUCKET_NAME` | — | S3 bucket |
| `AWS_REGION` | — | AWS region |
| `AWS_ACCESS_KEY_ID` | — | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | — | AWS secret key |

### Identity Verification
| Variable | Default | Description |
|---|---|---|
| `NIMC_API_KEY` | — | National Identity Management Commission |
| `NIMC_API_URL` | — | NIMC API base URL |
| `MDCN_API_KEY` | — | Medical and Dental Council of Nigeria |
| `MDCN_API_URL` | — | MDCN API base URL |

### HMO Partners
| Variable | Description |
|---|---|
| `AXA_MANSARD_API_KEY` | AXA Mansard HMO |
| `HYGEIA_API_KEY` | Hygeia HMO |
| `RELIANCE_HMO_API_KEY` | Reliance HMO |
| `HEALTHPLUS_API_KEY` | HealthPlus |
| `MEDPLUS_API_KEY` | MedPlus |

### Rate Limiting
| Variable | Default | Description |
|---|---|---|
| `THROTTLE_TTL` | `60` | Rate limit window (seconds) |
| `THROTTLE_LIMIT` | `100` | Max requests per window |

---

## rivheal-mobile-app (via `app.config.ts` `extra`)

| Variable | Source | Description |
|---|---|---|
| `API_URL` | `Constants.expoConfig.extra.apiUrl` | Backend API base URL |
| `KEYCLOAK_URL` | `extra.keycloakUrl` | Keycloak server URL |
| `KEYCLOAK_REALM` | `extra.keycloakRealm` | Realm name |
| `KEYCLOAK_CLIENT_ID` | `extra.keycloakClientId` | PKCE client ID (`mobile-app`) |
| `SENTRY_DSN` | `extra.sentryDsn` | Sentry crash reporting DSN |
| `APP_VARIANT` | `extra.appVariant` | `development` \| `preview` \| `production` |

---

## rivheal-infra

### Docker Compose overrides (`.env.staging` / `.env.prod`)
| Variable | Example | Description |
|---|---|---|
| `DB_DATABASE` | `rivheal_prod` | PostgreSQL database name |
| `DB_USERNAME` | `rivheal` | PostgreSQL user |
| `DB_PASSWORD` | (generated) | PostgreSQL password |
| `KEYCLOAK_ADMIN_USER` | `admin` | Keycloak admin username |
| `KEYCLOAK_ADMIN_PASSWORD` | (generated) | Keycloak admin password |
| `KEYCLOAK_DB_USER` | `keycloak` | Keycloak internal DB user |
| `KEYCLOAK_DB_PASSWORD` | (generated) | Keycloak internal DB password |
| `KEYCLOAK_CLIENT_SECRET` | (generated by bootstrap script) | API server client secret |
| `REDIS_PASSWORD` | (generated) | Redis password |
| `JWT_SECRET` | (generated) | JWT signing secret |
| `JWT_REFRESH_SECRET` | (generated) | JWT refresh signing secret |
| `ENCRYPTION_KEY` | (generated) | PII encryption key |
| `IMAGE_TAG` | `sha-abc1234` | Docker image tag to pull and deploy |
| `DOCKER_REGISTRY` | `ghcr.io/iterative-lead-systems` | Container registry prefix |
| `ENABLE_AI_FEATURES` | `true` | Global AI feature toggle — propagated to `api` and `ml-service` |
| **`RASA_BOT_PATH`** | `/home/ubuntu/rasa-bot` | **Absolute path to the cloned `rasa-bot/` repo on the server. Required for Rasa volume mount.** |

> **`RASA_BOT_PATH` is critical.** Without it, `docker compose up rasa rasa-actions` will fail because Docker cannot mount the volume. Set it to wherever you cloned the `rasa-bot` repo on the server (e.g. `/home/ubuntu/rasa-bot`).

<!-- AUTO-GENERATED: env-vars-end -->
