# Flow: Medication Adherence Tracking

> Last updated: **2026-05-30**

---

```mermaid
sequenceDiagram
    participant Doctor as Doctor (Frontend)
    participant API as NestJS API
    participant DB as PostgreSQL
    participant App as Patient App
    participant Push as Local Notifications

    Note over Doctor,DB: After consultation — prescription created
    Doctor->>API: POST /opd/prescriptions
    Note over Doctor,API: { items: [{ name:"Amoxicillin", dosage:"500mg",<br/>frequency:"3x daily", duration:"7 days" }] }
    API->>DB: INSERT prescription + prescription_items
    DB-->>API: prescription { id }
    API->>DB: INSERT medication_dose_logs (21 records = 3×7 days)
    Note over DB: scheduledTimes: [8am, 2pm, 8pm] × 7 days
    DB-->>API: dose logs created

    Note over App,Push: Patient views medications in app
    App->>API: GET /prescriptions?patientId=...
    API->>DB: SELECT prescriptions WHERE patient_id=...
    DB-->>API: [ prescriptions ]
    API-->>App: prescriptions[]

    App->>Push: scheduleMedicationReminder("Amoxicillin", hour=8, minute=0)
    Push-->>App: notification scheduled (local)

    Note over Push,App: At 8am each morning
    Push-->>App: 📱 "Time to take your Amoxicillin"
    App->>App: Patient taps "Taken" button

    App->>API: POST /medications/dose-logs/:doseLogId/log
    Note over App,API: { status: "taken", takenAt: "2026-05-30T08:05:00Z" }
    API->>DB: UPDATE medication_dose_logs SET status=taken, taken_at=...
    DB-->>API: ok
    API-->>App: { status: "taken", ... }

    Note over App,API: View adherence stats
    App->>API: GET /patients/:id/adherence?from=2026-05-01&to=2026-05-30
    API->>DB: SELECT COUNT(*) GROUP BY status WHERE patient_id=... AND scheduled_time BETWEEN...
    DB-->>API: { total:21, taken:18, missed:2, skipped:1 }
    API-->>App: { adherenceRate: 86, ... }
```

---

## Dose Status Lifecycle

```
pending → taken     (patient marks as taken)
        → skipped   (patient consciously skips)
        → missed    (no action by next scheduled dose)
```

## Key Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/medications/dose-logs/:id/log` | Log a dose (taken/skipped/missed) |
| `GET` | `/medications/prescriptions/:id/dose-logs` | Dose schedule for a prescription |
| `GET` | `/patients/:id/adherence?from=&to=` | Adherence stats over date range |

## Scheduled Hours

| Frequency | Times |
|---|---|
| Once daily (1×) | 8:00 |
| Twice daily (2×) | 8:00, 20:00 |
| Three times daily (3×) | 8:00, 14:00, 20:00 |
| Four times daily (4×) | 8:00, 12:00, 16:00, 20:00 |
