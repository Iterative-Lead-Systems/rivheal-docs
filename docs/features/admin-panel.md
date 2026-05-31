# Admin / Clinical EMR Features

> Stack: **React 19 · Vite · TanStack Query v5 · Tailwind CSS**  
> Last updated: **2026-05-30**

---

<!-- AUTO-GENERATED: pages-start -->

## Page Inventory

| Page | Path | Role | Description |
|---|---|---|---|
| Dashboard | `/dashboard` | All staff | KPI stats (today's patients, appointments, queue, labs, revenue), recent patients, today's appointment list, AI wait-time prediction panel |
| Appointments | `/appointments` | Receptionist, Admin | List, filter, create appointments; appointment detail |
| OPD Queue | `/opd/queue` | Doctor, Nurse | Live queue management, consultation workspace |
| Consultation Workspace | `/opd/consultations/:id` | Doctor | Vitals, diagnoses, prescriptions, lab/radiology/pharmacy requests, notes |
| Patients | `/patients` | All clinical | Patient list, search; enroll new patient |
| Patient Detail | `/patients/:id` | All clinical | Demographics, medical history, appointments, labs, prescriptions |
| Laboratory | `/laboratory` | Lab tech | Lab orders, sample collection, result entry, print results |
| Pharmacy | `/pharmacy` | Pharmacist | Dispense orders, drug stock management |
| Billing | `/billing` | Cashier, Admin | Invoice list, create invoice, payment recording, HMO claims |
| Inventory | `/inventory` | Inventory manager | Items, purchase orders, suppliers, barcode scanning |
| Emergency | `/emergency` | ER staff | Emergency case management, ambulance tracking |
| Ward | `/ward` | Nurse, Admin | Beds, admissions, nursing notes, bed transfers |
| Radiology | `/radiology` | Radiologist | Radiology orders |
| Homecare | `/homecare` | Admin | Home care service requests and practitioner assignment |
| Reports | `/reports` | Admin | Analytics and reporting |
| Staff | `/staff` | Admin | Staff management, bookability, departments |
| Departments | `/departments` | Admin | Department CRUD |
| Branches | `/branches` | Super Admin | Branch management |
| Settings | `/settings` | Admin | Hospital settings, modules, preferences |
| Notifications | `/notifications` | All staff | Notification centre |

<!-- AUTO-GENERATED: pages-end -->

---

<!-- AUTO-GENERATED: dashboard-ai-start -->

## Dashboard AI Widgets

Added 2026-05-30:

| Widget | Component | Data Source | Feature Flag |
|---|---|---|---|
| Wait Time Prediction | `WaitTimePredictionPanel` | `GET /predict/wait-time` | `ENABLE_AI_FEATURES` |
| Patient Health Score | `HealthScoreGauge` | `GET /patients/:id/health-score` | `ENABLE_AI_FEATURES` |

Widgets degrade gracefully — hidden or show fallback text when AI is disabled or ML service is unreachable.

<!-- AUTO-GENERATED: dashboard-ai-end -->

---

## Key Clinical Workflow: OPD

1. Patient checks in at reception → appointment status → `checked_in`.
2. Nurse records vitals in consultation workspace.
3. Doctor starts consultation → status → `in_progress`.
4. Doctor records diagnosis, creates prescriptions, orders labs/radiology.
5. Doctor completes consultation → status → `completed`. `actualWaitMinutes` auto-computed and persisted.
6. Patient proceeds to pharmacy / lab / billing as needed.
