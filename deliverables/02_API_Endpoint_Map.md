# API Endpoint Map — Fitness API (Reconnaissance)

**Project:** Fitness API Security Assessment & Hardening Framework
**Week 2 Deliverable — Foundation**
**Author:** chocholucky33@gmail.com
**Date:** 2026-10-21
**Target:** `http://127.0.0.1:5000` (local practice instance — course supplied no external target;
a bundled stand-in Flask API was built and reconned on localhost with full authorization)
**Tools used:** `curl`, custom Python recon script (`scripts/recon.py`), manual observation.

---

## 1. Method
1. Started the target Flask API locally.
2. Enumerated candidate paths/methods with `recon.py` (status-code probing).
3. Confirmed each live endpoint with `curl`, recording method, parameters, and a response sample.
4. Noted which OWASP API Top 10 risk each endpoint is a candidate for (recon observation only —
   no exploitation performed this week).

---

## 2. Endpoint Inventory

| # | Method | Path | Parameters | Auth? (observed) | Status | Response sample | OWASP candidate |
|---|--------|------|-----------|------------------|--------|-----------------|-----------------|
| 1 | GET  | `/api/health`                 | — | none | 200 | `{"service":"fitness-api","status":"ok","version":"v1"}` | API9 (version disclosed) |
| 2 | POST | `/api/login`                  | body: `username` (`password` expected) | none | 200 | `{"message":"login endpoint","received_user":"test"}` | API2 (Broken Auth) |
| 3 | GET  | `/api/users/<user_id>/profile`| path: `user_id` (int) | none | 200 | `{"id":1,"name":"Alice","plan":"pro"}` | **API1 (BOLA)** |
| 4 | GET  | `/api/users/<user_id>/workouts`| path: `user_id`; query: `limit` (int) | none | 200 | `[{"id":10,"minutes":30,"type":"run"}]` | API1 (BOLA), API4 (`limit`) |
| 5 | POST | `/api/users/<user_id>/workouts`| path: `user_id`; JSON body (echoed) | none | 201 | `{"echo":{},"message":"created"}` | API3 (mass assignment) |
| 6 | GET  | `/api/admin/stats`            | — | none | 200 | `{"total_users":2,"total_workouts":2}` | **API5 (BFLA)** |

### Probed but not present (useful negatives)
| Method | Path | Status | Note |
|--------|------|--------|------|
| GET | `/swagger`      | 404 | No Swagger UI exposed |
| GET | `/openapi.json` | 404 | No machine-readable spec exposed (manual mapping required) |

---

## 3. Parameter Notes
- **`user_id`** (path, integer, endpoints 3–5): directly indexes an object → primary **BOLA** test target.
  Sequential integers are trivially enumerable (`1`, `2`, …).
- **`limit`** (query, integer, endpoint 4): controls result size → **API4** (resource consumption) if uncapped.
- **`username` / request body** (endpoints 2, 5): user-controlled input echoed/processed → check **API3**
  (property-level authz / mass assignment) and input validation.

---

## 4. Attack-Surface Summary
- **6 live endpoints** across 2 resource groups (`users`, `admin`) + 1 health route.
- **No authentication observed** on any route, including `/api/admin/stats` → high-priority finding
  area for the testing phase (API2, API5).
- **Object IDs are sequential integers** → BOLA enumeration is feasible (API1).
- **Version string `v1` leaked** by `/api/health` → supports version enumeration (API9).
- No API documentation endpoint found → inventory must be maintained manually.

> Scope note: This week is reconnaissance and mapping only. The OWASP "candidate" column records
> *where to test next week*; no authorization bypass or exploitation was carried out. Testing was
> confined to a locally-owned instance.

---

## 5. Artifacts
- `scripts/recon.py` — reusable endpoint-discovery script.
- `scripts/endpoint_scan_results.json` — raw structured scan output (evidence).
- `target_app/app.py` — the local practice target.
