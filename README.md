# Week 2 — Fitness API Security: OWASP & Reconnaissance

Deliverables for Week 2 of the Fitness API Security Assessment & Hardening Framework internship.

> **Note on the target:** The Week 2 brief did **not** provide a target API (no URL, application,
> or dataset — only the task description and general reference links). To perform genuine
> reconnaissance, a minimal **local practice Flask API** was built and run on `127.0.0.1:5000`,
> and all recon was carried out against that authorized, locally-owned instance. The methodology,
> scripts, and findings transfer directly to the real target API if/when one is supplied.

## What's here
- `deliverables/01_OWASP_API_Top10_Summary.md` — summary of OWASP API Security Top 10 (2023).
- `deliverables/02_API_Endpoint_Map.md` — endpoint map (methods, parameters) from live recon.
- `deliverables/endpoint_scan_results.json` — raw scan evidence.
- `target_app/app.py` — local practice Flask API (the course supplied no target, so this stands in).
- `scripts/recon.py` — reusable endpoint-discovery script.

## Reproduce the recon
```bash
# 1. start the practice target
cd target_app && python3 app.py          # serves http://127.0.0.1:5000

# 2. in another terminal, run recon
cd scripts && python3 recon.py
```

## Scope / ethics
All activity targets a locally-run API you own. Only recon + mapping was done this week —
no exploitation. Do not point these scripts at systems you are not authorized to test.
