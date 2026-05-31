# Flow: Rasa Chatbot — Deployment, Training & Message Handling

> Last updated: **2026-05-31**

---

## The Three Things Rasa Needs to Work

```
1. rasa-bot/ folder    ← your code (intents, stories, actions)
2. Trained model       ← output of `rasa train`, saved to rasa-bot/models/
3. Running containers  ← rasa + rasa-actions, both reading from rasa-bot/
```

All three must be present. The most common failure is having #1 and #3 but not #2 — rasa starts but every message returns an error.

---

## Architecture: How rasa-bot connects to everything

```mermaid
graph TB
    subgraph Server["AWS EC2 Server"]
        subgraph Docker["Docker Network: rivheal_net"]
            API[NestJS API<br/>api.rivheal.com]
            RASA[rasa container<br/>rasa/rasa:3.6.21<br/>port 5005]
            ACTIONS[rasa-actions container<br/>rasa/rasa-sdk:3.6.2<br/>port 5055]
        end

        subgraph Filesystem["Server Filesystem"]
            BOT["~/rasa-bot/<br/>data/nlu.yml<br/>data/stories.yml<br/>domain/domain.yml<br/>config.yml<br/>actions/actions.py<br/>models/*.tar.gz"]
        end
    end

    subgraph External["External"]
        MOBILE[Patient Mobile App]
        DEV[Developer Machine]
    end

    MOBILE -->|POST /assistant/chat| API
    API -->|POST http://rasa:5005/webhooks/rest/webhook| RASA
    RASA -->|calls custom action| ACTIONS
    ACTIONS -->|runs| BOT

    BOT -->|mounted as /app| RASA
    BOT -->|actions/ mounted as /app/actions| ACTIONS

    DEV -->|git push| BOT

    style Server fill:#f0fdf4,stroke:#16a34a
    style Docker fill:#dbeafe,stroke:#3b82f6
    style Filesystem fill:#fef9c3,stroke:#ca8a04
    style External fill:#f3e8ff,stroke:#9333ea
```

---

## Flow: First-Time Deploy

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Server as AWS Server
    participant DC as Docker Compose
    participant Rasa as rasa container
    participant Models as ~/rasa-bot/models/

    Dev->>Server: git clone rasa-bot to ~/rasa-bot
    Dev->>Server: echo "RASA_BOT_PATH=/home/ubuntu/rasa-bot" >> .env.prod

    Dev->>DC: docker compose up -d rasa rasa-actions
    DC->>Rasa: start container (mounts ~/rasa-bot as /app)
    Note over Rasa: starts but has no model yet
    Note over Rasa: POST /webhooks/rest/webhook returns 500

    Dev->>Rasa: docker compose exec rasa rasa train
    Note over Rasa: reads /app/data/nlu.yml<br/>reads /app/domain/domain.yml<br/>trains DIET classifier (~2-3 min)
    Rasa->>Models: saves models/20260531-123456.tar.gz

    Dev->>DC: docker compose restart rasa
    Note over Rasa: loads trained model
    Note over Rasa: POST /webhooks/rest/webhook now returns responses ✅
```

---

## Flow: Patient Sends a Chat Message

```mermaid
sequenceDiagram
    participant App as Patient App
    participant API as NestJS API
    participant Rasa as rasa:5005
    participant Actions as rasa-actions:5055

    App->>API: POST /assistant/chat
    Note over App,API: { message: "I have a fever", sessionId: "abc" }

    API->>Rasa: POST /webhooks/rest/webhook
    Note over API,Rasa: { sender: "abc", message: "I have a fever" }

    Rasa->>Rasa: NLU classifies intent
    Note over Rasa: intent: report_symptom<br/>entity: symptom = "fever"

    Rasa->>Actions: POST /webhook (action_assess_symptoms)
    Note over Rasa,Actions: calls custom action

    Actions->>Actions: actions.py runs assess logic
    Note over Actions: "fever" → medium urgency<br/>returns response text

    Actions-->>Rasa: { events: [...], responses: [{ text: "⚠️ Based on your symptoms..." }] }
    Rasa-->>API: [{ recipient_id: "abc", text: "⚠️ Based on your symptoms..." }]
    API-->>App: { sessionId: "abc", responses: [{ text: "..." }] }
    App->>App: displays message in chat bubble
```

---

## Flow: Updating the Bot (adding new intents)

```mermaid
sequenceDiagram
    participant Dev as Developer (local)
    participant GitHub as GitHub
    participant Server as AWS Server
    participant Rasa as rasa container

    Dev->>Dev: edit rasa-bot/data/nlu.yml
    Note over Dev: add examples for new intent<br/>e.g. ask_prescription_refill

    Dev->>Dev: edit rasa-bot/domain/domain.yml
    Note over Dev: declare new intent + response

    Dev->>GitHub: git commit && git push

    Dev->>Server: ssh in
    Server->>Server: cd ~/rasa-bot && git pull
    Server->>Rasa: docker compose exec rasa rasa train
    Note over Rasa: retrains model (~2-3 min)<br/>new model saved to ~/rasa-bot/models/
    Server->>Rasa: docker compose restart rasa
    Note over Rasa: loads new model<br/>new intent now works ✅
```

---

## Flow: Updating Custom Actions Only (no retrain needed)

```mermaid
sequenceDiagram
    participant Dev as Developer (local)
    participant GitHub as GitHub
    participant Server as AWS Server
    participant ActionsC as rasa-actions container

    Dev->>Dev: edit rasa-bot/actions/actions.py
    Note over Dev: e.g. add hospital lookup logic

    Dev->>GitHub: git commit && git push

    Dev->>Server: ssh in
    Server->>Server: cd ~/rasa-bot && git pull
    Server->>ActionsC: docker compose restart rasa-actions
    Note over ActionsC: Python process restarts<br/>reads updated actions.py<br/>no model retrain needed ✅
```

---

## What's in Each File

### `data/nlu.yml` — Training Examples
```yaml
- intent: report_symptom
  examples: |
    - I have [fever](symptom)
    - body dey pain me         ← Nigerian Pidgin
    - I'm experiencing [chest pain](symptom)
```
More examples = more accurate intent detection. Add at least 10 per intent.

### `domain/domain.yml` — Bot Vocabulary
```yaml
intents:
  - report_symptom
  - book_appointment
  - emergency

responses:
  utter_emergency:
    - text: "🚨 Call 999 immediately!"

actions:
  - action_assess_symptoms    ← must match a class name in actions.py
```

### `actions/actions.py` — Custom Logic
```python
class ActionAssessSymptoms(Action):
    def name(self): return "action_assess_symptoms"

    def run(self, dispatcher, tracker, domain):
        symptoms = tracker.get_slot("symptoms") or []
        # ... triage logic ...
        dispatcher.utter_message(text="Based on your symptoms...")
        return []
```

### `config.yml` — Model Configuration
Controls which ML algorithms Rasa uses. The default DIET classifier + TEDPolicy is appropriate for MVP. No changes needed unless you're tuning accuracy.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `rasa` container keeps restarting | No model trained yet | `docker compose exec rasa rasa train` |
| `POST /webhooks/rest/webhook` returns `{"version":"3.6.21"}` but no response | Model loaded but no matching intent | Add more training examples to `nlu.yml`, retrain |
| `rasa-actions` container exits immediately | Syntax error in `actions.py` | `docker compose logs rasa-actions` to see error |
| API returns `"AI assistant is temporarily unavailable"` | `rasa` container not running or `RASA_SERVER_URL` wrong | Check `docker compose ps rasa`, verify `RASA_SERVER_URL=http://rasa:5005` |
| New intent not being recognised | Retrained but model not loaded | `docker compose restart rasa` after train |
| `RASA_BOT_PATH` not set | Compose can't mount the volume | Add `RASA_BOT_PATH=/home/ubuntu/rasa-bot` to `.env.prod` |
