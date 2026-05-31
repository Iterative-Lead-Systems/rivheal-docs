# AI / ML Features

> Last updated: **2026-05-30**  
> All AI features are gated by `ENABLE_AI_FEATURES=true` (global) + `hospitals.ai_features_enabled=true` (per-tenant).

---

<!-- AUTO-GENERATED: ai-status-start -->

## Feature Status Matrix

| Feature | Status | Implementation | Endpoint |
|---|---|---|---|
| Symptom Checker (rule-based fallback) | ✅ Live | `SymptomCheckerService.analyzeWithRules()` | `POST /symptom-checker/analyze` |
| Symptom Checker (Claude LLM) | ✅ Live* | `SymptomCheckerService.analyzeWithLlm()` | `POST /symptom-checker/analyze` |
| AI Health Assistant chat | 🟡 Scaffold | `RasaService` → requires Rasa server | `POST /assistant/chat` |
| Guest chat (no auth) | 🟡 Scaffold | `RasaService` | `POST /assistant/chat/guest` |
| Multi-language support | 🟡 Partial | Urgency strings in 5 languages in `rasa.service.ts` | — |
| Wait-time prediction | 🟡 Proxy ready | `MlProxyService` → FastAPI; models not yet trained | `GET /predict/wait-time` |
| No-show prediction | 🟡 Proxy ready | `MlProxyService` → FastAPI; models not yet trained | `POST /predict/no-show` |
| RivHealth Score | ✅ Live* | `HealthScoreService` formula-based | `GET /patients/:id/health-score` |
| Lab trend alerts | ✅ Live | `LabAlertsService` — queries `is_abnormal` + `is_critical` | `GET /patients/:id/lab-alerts` |
| Medication adherence tracking | ✅ Live | `MedicationAdherenceService` — dose log entity | `POST /medications/dose-logs/:id/log` |
| Queue snapshot collection | ✅ Live | `QueueSnapshotsService` cron — every 15 min | internal |
| Actual wait time persistence | ✅ Live | auto-computed on `completeConsultation()` | internal |
| Outbreak detection | ❌ Planned | — | — |
| Fraud detection | ❌ Planned | — | — |
| Dynamic pricing | ❌ Planned | — | — |
| Voice input (Nigerian accent) | ❌ Planned | — | — |
| Wearables integration | ❌ Planned | — | — |

*Requires `ENABLE_AI_FEATURES=true`

<!-- AUTO-GENERATED: ai-status-end -->

---

## Symptom Checker — LLM Flow

**Endpoint:** `POST /symptom-checker/analyze`  
**Auth:** Public (guest OK)  
**Headers:** `x-guest-session-id: <uuid>` (optional — persists result for merge after login)

**Request:**
```json
{ "symptoms": ["fever", "cough", "fatigue"] }
```

**Response:**
```json
{
  "triage": "medium",
  "suggestion": "Consult a doctor within 24 hours",
  "possibleConditions": ["Common cold", "Influenza", "Malaria", "Typhoid"]
}
```

**Logic:**
1. If `ANTHROPIC_API_KEY` is set → call Claude `claude-haiku-4-5-20251001`.
2. System prompt instructs the model to return JSON with Nigerian-relevant conditions.
3. On any LLM error → fall back to keyword-matching rules.
4. If `x-guest-session-id` header present → save result to `guest_symptom_checks` table.

---

## Wait-Time Prediction

**Endpoint:** `GET /predict/wait-time?branchId=<uuid>`  
**Auth:** JWT  
**Headers:** `X-Hospital-Id: <uuid>`

**Response:**
```json
{
  "predictedWaitMinutes": 22,
  "confidence": 0.80,
  "isFallback": false
}
```

**Architecture:**
```
NestJS MlProxyService
  ├── Checks FeatureFlagsService.isAiEnabled(hospitalId)
  ├── Fetches current queue length from QueueSnapshotsService
  ├── POST http://ml-service:8000/predict/wait-time
  │     { hour, dayOfWeek, queueLength, doctorAvgTime }
  └── On timeout/error → returns { predictedWaitMinutes: 30, isFallback: true }
```

**Training data collected:**
- `queue_snapshots` table — branch queue depth every 15 min.
- `appointments.actual_wait_minutes` — auto-persisted on consultation completion.

**Train a model:**
```bash
cd rivheal-ml-service
python trainers/train.py --model wait_time --csv data/appointments.csv
# Saves models/wait_time_model.pkl
docker compose restart ml-service
```

---

## RivHealth Score

**Endpoint:** `GET /patients/:id/health-score`  
**Auth:** JWT  
**Feature flag:** `ENABLE_AI_FEATURES=true`

**Response:**
```json
{
  "score": 76,
  "riskLevel": "low",
  "breakdown": {
    "labScore": 85,
    "chronicConditionScore": 70,
    "appointmentAdherenceScore": 80
  },
  "computedAt": "2026-05-30T10:00:00Z"
}
```

**Formula (v1):**
```
score = labScore × 0.35 + chronicConditionScore × 0.35 + appointmentAdherenceScore × 0.30
```

- **labScore**: Starts at 100; -8 per abnormal lab, -12 per critical lab (last 20 results).
- **chronicConditionScore**: Starts at 100; -15 per high-risk condition (diabetes, hypertension, cancer…), -8 per other.
- **appointmentAdherenceScore**: Fixed at 80 (placeholder; will use actual no-show history once accumulated).

---

## Medication Adherence

**Endpoints:**
- `POST /medications/dose-logs/:doseLogId/log` — Mark a dose as `taken | skipped | missed`
- `GET /medications/prescriptions/:prescriptionId/dose-logs` — Dose schedule for a prescription
- `GET /patients/:id/adherence?from=&to=` — Adherence rate over a date range

**Response (adherence stats):**
```json
{
  "total": 30,
  "taken": 25,
  "missed": 3,
  "skipped": 2,
  "adherenceRate": 83
}
```

**Scheduling doses:**  
`MedicationAdherenceService.scheduleDosesForPrescription()` inserts dose logs at configured hours (8am, 8pm for twice-daily, etc.).

---

## Lab Trend Alerts

**Endpoint:** `GET /patients/:id/lab-alerts?limit=20`  
**Auth:** JWT

Returns all lab results where `is_abnormal = true` OR `is_critical = true`, sorted newest first.

```json
[
  {
    "labResultId": "uuid",
    "testName": "Complete Blood Count",
    "isAbnormal": true,
    "isCritical": false,
    "interpretation": "WBC elevated",
    "reportedAt": "2026-05-28T09:00:00Z"
  }
]
```
