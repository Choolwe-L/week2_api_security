# OWASP API Security Top 10 (2023) — Summary of Understanding

**Project:** Fitness API Security Assessment & Hardening Framework
**Week 2 Deliverable — Foundation**
**Author:** chocholucky33@gmail.com
**Date:** 2026-10-21

---

## Purpose
This document records my working understanding of the OWASP API Security Top 10 (2023 edition).
Each entry lists: what the risk is, how it typically appears in a Flask API, how to test for it
during reconnaissance, and the core mitigation. These notes drive the recon and later hardening
phases of the project.

---

## API1:2023 — Broken Object Level Authorization (BOLA)
- **What it is:** The API exposes object identifiers (e.g. `/users/123/workouts`) but fails to check
  that the *requesting* user actually owns object `123`. The single most common and most damaging API flaw.
- **Fitness-API example:** `GET /api/users/42/profile` returns any user's profile just by changing `42`.
- **How to test:** Authenticate as user A, capture a request, then replace the object ID with one
  belonging to user B. If data comes back, it's BOLA.
- **Mitigation:** Enforce an ownership check on every object access (`if object.owner_id != current_user.id: 403`).
  Prefer unguessable IDs (UUIDs) as defence-in-depth, never as the only control.

## API2:2023 — Broken Authentication
- **What it is:** Weak or missing authentication: no rate limiting on login, guessable tokens,
  JWTs with `alg:none`, credentials in URLs, no token expiry.
- **Fitness-API example:** `/login` accepts unlimited attempts; JWT signature not verified.
- **How to test:** Attempt login without credentials, inspect token structure (decode JWT), test
  token after logout/expiry, look for credentials passed as query strings.
- **Mitigation:** Strong password policy, rate limiting + lockout, short-lived signed tokens,
  verify JWT signature and `alg`, never put secrets in URLs.

## API3:2023 — Broken Object Property Level Authorization
- **What it is:** Merges old "Excessive Data Exposure" + "Mass Assignment". The API returns more
  object *fields* than the user should see, or lets the user *write* fields they shouldn't.
- **Fitness-API example:** `GET /profile` leaks `password_hash`/`is_admin`; `PATCH /profile` with
  `{"is_admin": true}` escalates privileges.
- **How to test:** Inspect every response for sensitive fields; send extra fields in write requests
  and check if they persist.
- **Mitigation:** Explicit allow-lists for both response serialization and request binding
  (schemas / DTOs). Never bind request bodies straight onto ORM models.

## API4:2023 — Unrestricted Resource Consumption
- **What it is:** No limits on requests, payload size, or expensive operations — enables DoS and
  cost spikes.
- **Fitness-API example:** `GET /workouts?limit=9999999`, unbounded file uploads, no rate limiting.
- **How to test:** Send large `limit`/`page` values, oversized payloads, rapid request bursts
  (within authorized scope only).
- **Mitigation:** Rate limiting, pagination caps, payload-size limits, timeouts, resource quotas.

## API5:2023 — Broken Function Level Authorization (BFLA)
- **What it is:** Like BOLA but for *actions/endpoints* — a normal user can call admin functions.
- **Fitness-API example:** A regular user calls `DELETE /api/admin/users/42` successfully.
- **How to test:** As a low-privilege user, try admin routes and privileged HTTP methods (PUT/DELETE).
- **Mitigation:** Deny-by-default role checks on every endpoint, enforced server-side, not by hiding UI.

## API6:2023 — Unrestricted Access to Sensitive Business Flows
- **What it is:** A legitimate flow (sign-up, reward claim, booking) can be automated/abused at scale.
- **Fitness-API example:** Automated creation of thousands of accounts to farm a referral bonus.
- **How to test:** Identify high-value flows and assess whether bots could abuse them.
- **Mitigation:** Device/behaviour detection, CAPTCHA where appropriate, rate limiting per flow.

## API7:2023 — Server Side Request Forgery (SSRF)
- **What it is:** API fetches a user-supplied URL, letting an attacker reach internal services.
- **Fitness-API example:** `POST /avatar {"image_url": "http://169.254.169.254/..."}` hits cloud metadata.
- **How to test:** Supply internal/loopback/metadata URLs where the API fetches remote resources.
- **Mitigation:** Allow-list schemes/hosts, block private ranges + metadata IPs, disable redirects.

## API8:2023 — Security Misconfiguration
- **What it is:** Debug mode on, verbose errors, missing security headers, permissive CORS,
  default credentials, unnecessary methods enabled.
- **Fitness-API example:** Flask running `debug=True` in prod exposing the Werkzeug console; `CORS(*)`.
- **How to test:** Trigger errors to see stack traces, check response headers, test CORS with a
  foreign `Origin`, probe `OPTIONS`/`TRACE`.
- **Mitigation:** Hardened config per environment, disable debug, security headers, least-privilege CORS.

## API9:2023 — Improper Inventory Management
- **What it is:** Forgotten/old API versions and undocumented ("shadow") endpoints remain exposed.
- **Fitness-API example:** `/api/v1/` deprecated but still live and unpatched alongside `/api/v2/`.
- **How to test:** Enumerate versions (`v1`,`v2`,`beta`), find docs (`/swagger`,`/openapi.json`),
  diff hosts/environments.
- **Mitigation:** Maintain a complete API inventory, retire old versions, document every endpoint.

## API10:2023 — Unsafe Consumption of APIs
- **What it is:** Blindly trusting data from *third-party* APIs the app itself calls.
- **Fitness-API example:** Importing workout data from a partner API without validating it.
- **How to test:** Review every outbound integration; assess validation of returned data.
- **Mitigation:** Validate/sanitize third-party responses, use TLS, treat upstream data as untrusted.

---

## Key takeaways for this project
1. **Authorization (BOLA/BFLA) dominates API risk** — most of the test effort goes here.
2. Recon must produce a **complete endpoint + parameter inventory** before any testing (ties to API9).
3. Hardening later must be **deny-by-default**, schema-validated, rate-limited, and env-specific.
