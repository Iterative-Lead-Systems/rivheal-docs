# Flow: Symptom Checker + Claude LLM Triage

> Last updated: **2026-05-30**

---

```mermaid
sequenceDiagram
    participant App as Patient App (Guest or Auth)
    participant API as NestJS API
    participant Claude as Anthropic Claude API
    participant DB as PostgreSQL

    App->>App: Patient selects symptoms from chip list
    App->>API: POST /symptom-checker/analyze
    Note over App,API: Body: { symptoms: ["fever","cough","fatigue"] }<br/>Header: x-guest-session-id: <uuid> (if guest)

    alt ANTHROPIC_API_KEY is set and ENABLE_AI_FEATURES=true
        API->>Claude: messages.create (claude-haiku-4-5-20251001)
        Note over API,Claude: System: "Nigerian health triage — return JSON<br/>{triage, suggestion, possibleConditions}"<br/>User: "Symptoms: fever, cough, fatigue"
        Claude-->>API: { triage:"medium", suggestion:"See doctor within 24h",<br/>possibleConditions:["Malaria","Influenza","Typhoid"] }
    else LLM unavailable / no API key
        API->>API: analyzeWithRules(symptoms)
        Note over API: Keyword match:<br/>high → chest pain, difficulty breathing<br/>medium → fever, cough, vomiting<br/>low → everything else
        API-->>API: { triage: "medium", ... }
    end

    alt x-guest-session-id header present
        API->>DB: INSERT guest_symptom_checks<br/>{ guestSessionId, symptoms, triage, suggestion, possibleConditions }
        DB-->>API: ok
    end

    API-->>App: { triage, suggestion, possibleConditions }
    App->>App: Navigate to SymptomResultScreen

    Note over App,DB: After login — guest data merge
    App->>API: POST /auth/merge-guest-session<br/>{ guestSessionId: "abc-123" }
    API->>DB: SELECT guest_symptom_checks WHERE guestSessionId=...
    DB-->>API: [ checks ]
    API->>DB: INSERT patient_symptom_checks (linked to patientId)
    API->>DB: DELETE guest_symptom_checks WHERE guestSessionId=...
    API-->>App: { success: true }
```

---

## Triage Levels

| Level | Color | Advice | Example Symptoms |
|---|---|---|---|
| `high` | 🔴 Red | Seek urgent care immediately | chest pain, difficulty breathing, severe headache |
| `medium` | 🟡 Amber | Consult a doctor within 24 hours | fever, cough, vomiting, fatigue |
| `low` | 🟢 Green | Monitor at home | mild sore throat, runny nose |

## Claude Prompt Design

```typescript
system: `You are a Nigerian health triage assistant. Given a list of symptoms, 
return a JSON object with:
- triage: "low" | "medium" | "high"
- suggestion: string (actionable advice in plain English)
- possibleConditions: string[] (2-4 likely conditions, include tropical diseases 
  relevant in Nigeria)

Return ONLY valid JSON, no markdown.`

user: `Symptoms: fever, cough, fatigue`
```

## Feature Flag

- Requires `ENABLE_AI_FEATURES=true` AND `ANTHROPIC_API_KEY` to be set.
- Without both, the rule-based engine runs silently (no error returned to client).
- Mobile and admin UIs receive the same response shape regardless of engine used.

## Data Tables

| Table | Purpose |
|---|---|
| `guest_symptom_checks` | Stores triage results for unauthenticated users |
| `patient_symptom_checks` | Stores triage results after merge to authenticated patient |
