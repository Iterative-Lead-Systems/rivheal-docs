# Flow: Real-time Queue Tracking

> Last updated: **2026-05-30**

---

```mermaid
sequenceDiagram
    participant App as Patient App
    participant WS as Socket.io (/queue)
    participant API as NestJS API
    participant ML as ML Service
    participant DB as PostgreSQL
    participant Cron as Cron Job (15 min)

    Note over Cron,DB: Background — every 15 minutes
    Cron->>DB: SELECT COUNT(*) per branch/department
    DB-->>Cron: queue counts
    Cron->>DB: INSERT queue_snapshots

    Note over App,WS: Patient has checked in
    App->>WS: connect (socket.io) to /queue namespace
    App->>WS: join room "appointment:<id>"

    WS-->>App: emit { queueNumber, position, estimatedWaitMinutes, status }

    Note over App,ML: ML-enhanced wait time
    App->>API: GET /predict/wait-time?branchId=...
    API->>DB: SELECT latest queue_snapshot WHERE branch_id=...
    DB-->>API: { queueLength: 8 }
    API->>ML: POST /predict/wait-time { hour:10, dayOfWeek:2, queueLength:8, doctorAvgTime:25 }
    ML-->>API: { predicted_wait_minutes: 22 }
    API-->>App: { predictedWaitMinutes: 22, confidence: 0.80, isFallback: false }

    Note over App: Displays "~22 min (AI Est.)"

    Note over WS: When doctor calls next patient
    WS-->>App: emit { queueNumber: 4, position: 1, status: "NEXT" }
    App->>App: show "You're next!" alert

    Note over WS,App: Polling fallback (every 10s if WS unavailable)
    App->>API: GET /appointments/:id
    API->>DB: SELECT * FROM appointments WHERE id=...
    DB-->>API: appointment data
    API-->>App: { queuePosition, estimatedWaitTime }
```

---

## Socket.io Events

| Event | Direction | Payload |
|---|---|---|
| `queue:update` | Server → Client | `{ queueNumber, currentNumber, position, estimatedWaitMinutes, status }` |
| `queue:called` | Server → Client | `{ message: "Your turn!" }` |
| `join-queue` | Client → Server | `{ appointmentId }` |

## Fallback Strategy

1. **Primary:** Socket.io real-time updates via `/queue` namespace.
2. **Secondary:** ML-predicted wait time from `GET /predict/wait-time` (polled every 3 min).
3. **Tertiary:** `appointment.estimatedWaitTime` field from REST polling every 10s.

If ML service is unreachable → `isFallback: true` → display socket or static estimate.
