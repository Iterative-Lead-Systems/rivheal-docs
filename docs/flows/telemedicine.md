# Flow: Telemedicine (Video Consultation)

> Last updated: **2026-05-30**

---

```mermaid
sequenceDiagram
    participant App as Patient App
    participant API as NestJS API
    participant DB as PostgreSQL
    participant Doctor as Doctor (Frontend)
    participant Video as Video Provider (external)

    Note over App,API: Patient books telemedicine appointment
    App->>API: POST /appointments
    Note over App,API: { type: "telemedicine", isTelemedicine: true, ... }
    API->>DB: INSERT appointment (isTelemedicine=true)
    DB-->>API: appointment
    API-->>App: appointment confirmed

    Note over Doctor,API: Admin/Doctor sets video call URL
    Doctor->>API: PUT /appointments/:id/video-call-url
    Note over Doctor,API: { url: "https://meet.rivheal.com/room/xyz" }
    API->>DB: UPDATE appointments SET video_call_url=...
    DB-->>API: ok
    API-->>Doctor: updated appointment

    Note over App,Video: At appointment time
    App->>API: GET /appointments/my
    API->>DB: SELECT appointments WHERE patient_id=... AND is_telemedicine=true
    DB-->>API: [ appointments with videoCallUrl ]
    API-->>App: appointment { videoCallUrl: "https://..." }

    App->>App: Show "Join Call" button when appointment is active

    App->>Video: Open video URL in Expo WebBrowser
    Note over App,Video: expo-web-browser opens the call link<br/>(WebRTC via external provider)

    Note over App,API: After consultation
    Doctor->>API: POST /appointments/:id/complete
    API->>DB: UPDATE status=completed, consultationEndedAt=now(), actualWaitMinutes=...
    API-->>Doctor: completed
```

---

## Current State

- **Booking:** ✅ — `isTelemedicine: true` on appointment creation.
- **Video URL:** ✅ — Staff sets URL via `PUT /appointments/:id/video-call-url`.
- **Join flow:** ✅ (basic) — `TelemedicineScreen` exists; video URL displayed.
- **Integrated WebRTC:** ❌ Planned — no embedded video SDK yet (Daily.co / Agora / 100ms).
- **Recording:** ❌ Planned.

## Required Env Vars (when video SDK is added)

| Variable | Description |
|---|---|
| `VIDEO_PROVIDER_API_KEY` | API key for WebRTC provider |
| `VIDEO_ROOM_PREFIX` | Room name prefix (e.g., `rivheal-`) |
