# Patient Mobile App Features

> Stack: **Expo 56 · React Native 0.85 · NativeWind v4 · WatermelonDB · MMKV**  
> Last updated: **2026-05-30**

---

<!-- AUTO-GENERATED: screens-start -->

## Screen Inventory

| Screen | File | Auth Required | Description |
|---|---|---|---|
| Home | `screens/home/HomeScreen.tsx` | Guest OK | Quick-action grid, symptom checker CTA, health tips, AI Assistant shortcut |
| Login | `screens/auth/LoginScreen.tsx` | — | Email/password JWT login |
| Register | `screens/auth/RegisterScreen.tsx` | — | New patient registration |
| Symptom Checker | `screens/symptomChecker/SymptomCheckerScreen.tsx` | Guest OK | Select symptoms → API triage (Claude LLM or rule-based fallback) |
| Symptom Result | `screens/symptomChecker/SymptomResultScreen.tsx` | Guest OK | Displays triage level, suggestion, possible conditions |
| AI Health Assistant | `screens/ChatAssistantScreen.tsx` | Guest OK | Free-text chat with Rasa NLU / LLM assistant |
| Emergency | `screens/emergency/EmergencyScreen.tsx` | Guest OK | Geo-sorted nearby hospitals, emergency call (999) |
| Hospital Search | `screens/hospitals/HospitalSearchScreen.tsx` | Guest OK | Search hospitals by name/location |
| Hospital Detail | `screens/hospitals/HospitalDetailScreen.tsx` | Guest OK | Hospital info, departments, contact |
| Appointment List | `screens/appointments/AppointmentListScreen.tsx` | ✅ | My appointments from `GET /appointments/my` |
| Book Appointment | `screens/appointments/BookAppointmentScreen.tsx` | ✅ | Select hospital → department → date → slot → confirm |
| Queue Tracking | `screens/appointments/QueueTrackingScreen.tsx` | ✅ | Live queue position, ML-predicted wait time |
| Medical Records | `screens/medicalRecords/MedicalRecordsScreen.tsx` | ✅ | Past consultations, lab results |
| Medical Record Detail | `screens/medicalRecords/MedicalRecordDetailScreen.tsx` | ✅ | Full detail view |
| Medications | `screens/medications/MedicationsScreen.tsx` | ✅ | Active prescriptions, schedule local push reminders |
| Telemedicine | `screens/telemedicine/TelemedicineScreen.tsx` | ✅ | Video consultation (video URL from appointment) |
| Wellness | `screens/wellness/WellnessScreen.tsx` | ✅ | BP, blood sugar, weight, mood, sleep, exercise charts (WatermelonDB) |
| Wellness Log | `screens/wellness/WellnessLogScreen.tsx` | ✅ | Daily metric entry form |
| Profile | `screens/ProfileScreen.tsx` | ✅ | User profile, settings |

<!-- AUTO-GENERATED: screens-end -->

---

<!-- AUTO-GENERATED: local-data-start -->

## Local Data Storage

| Store | Technology | Tables / Keys | Purpose |
|---|---|---|---|
| Symptom history | WatermelonDB (SQLite/JSI) | `symptom_histories` | Offline triage results; synced to `guest_symptom_checks` via merge |
| Wellness metrics | WatermelonDB | `wellness_metrics` | 30-day local health log |
| Auth tokens | Expo SecureStore | `access_token`, `refresh_token` | Secure keychain storage |
| Guest session | MMKV | `guest_session_id` | UUID identifying unauthenticated user |
| Preferences | MMKV | `wellness_reminders`, `onboarding_done`, `version_check_time` | Fast key-value config |

<!-- AUTO-GENERATED: local-data-end -->

---

<!-- AUTO-GENERATED: notifications-start -->

## Notifications

| Type | Trigger | Delivery |
|---|---|---|
| Medication reminder | Patient taps "Set Reminder" on a prescription | Local — `expo-notifications` scheduled at configured hour |
| Wellness check-in | Daily schedule configured by user | Local — recurring `expo-notifications` |
| Appointment update | Backend status change | Push — Expo Push token → API → `POST /notifications` |
| Queue position | Backend queue event | Real-time — Socket.io `/queue` namespace |
| App update | `GET /mobile/version` check (24h interval) | In-app sheet (`UpdateSheet` component) |

<!-- AUTO-GENERATED: notifications-end -->

---

## Guest Session Flow

1. App starts → `initGuestSession()` creates a UUID and stores it in MMKV (`guest_session_id`).
2. All API requests include `X-Guest-Session-Id: <uuid>` header.
3. Guest uses symptom checker → result saved to `guest_symptom_checks` in the API DB.
4. Patient registers/logs in → `POST /auth/merge-guest-session` moves records to their patient profile.
5. Guest ID is cleared from MMKV after successful merge.
