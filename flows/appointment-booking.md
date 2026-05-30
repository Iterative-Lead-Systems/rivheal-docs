# Flow: Appointment Booking

> Last updated: **2026-05-30**

---

```mermaid
sequenceDiagram
    participant App as Patient App
    participant API as NestJS API
    participant DB as PostgreSQL
    participant ML as ML Service
    participant Push as Expo Push

    App->>API: GET /hospitals?search=lagos
    API->>DB: SELECT hospitals WHERE name LIKE...
    DB-->>API: [ hospital list ]
    API-->>App: hospitals[]

    App->>API: GET /departments?hospitalId=...
    API->>DB: SELECT departments WHERE hospital_id=...
    DB-->>API: [ departments ]
    API-->>App: departments[]

    App->>API: GET /appointments/available-slots?staffId=&date=
    API->>DB: query booked slots
    DB-->>API: booked[]
    API-->>App: available slots[]

    App->>API: POST /appointments
    Note over App,API: { patientId, staffId, departmentId,<br/>appointmentDate, startTime, type }
    API->>DB: INSERT appointment (status=scheduled)
    DB-->>API: appointment { id, appointmentNumber }
    API-->>App: appointment confirmed

    API->>Push: send "appointment confirmed" notification
    Push-->>App: push notification

    Note over App,ML: On check-in day
    App->>API: POST /appointments/:id/check-in
    API->>DB: UPDATE status=checked_in, queueNumber=N
    DB-->>API: ok
    API-->>App: { queueNumber: 4 }

    App->>API: GET /predict/wait-time?branchId=...
    API->>ML: POST /predict/wait-time
    ML-->>API: { predictedWaitMinutes: 22 }
    API-->>App: { predictedWaitMinutes: 22, isFallback: false }
```

---

## Key Entities

| Entity | Table | Key Fields |
|---|---|---|
| Appointment | `appointments` | `status`, `queueNumber`, `checkedInAt`, `consultationStartedAt`, `actualWaitMinutes` |
| Patient | `patients` | `userId`, `patientId`, `hospitalId` |
| Staff | `staff` | `isBookable`, `staffId` |

## Status Lifecycle

```
scheduled → confirmed → checked_in → in_progress → completed
                     ↘ cancelled
                     ↘ no_show
                     ↘ rescheduled
```

## Notes

- Slot availability is checked in real time — concurrent bookings cannot claim the same slot (conflict detection in `AppointmentRepository.findOverlappingSlot`).
- `actualWaitMinutes` is computed automatically when `completeConsultation()` is called: `consultationStartedAt - checkedInAt`.
- The ML wait-time prediction uses `queue_snapshots` data (captured every 15 min by a cron job) as training features.
