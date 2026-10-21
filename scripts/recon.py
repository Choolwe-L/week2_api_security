#!/usr/bin/env python3
"""
Week 2 reconnaissance script — Fitness API Security Assessment.

Passive/light-touch endpoint discovery against a LOCALLY-RUN, AUTHORIZED target.
Default target is the bundled practice app at http://127.0.0.1:5000.

Only run this against systems you own or are explicitly authorized to test.

Usage:
    python3 recon.py                       # scans http://127.0.0.1:5000
    python3 recon.py http://127.0.0.1:5000
"""
import sys
import json
import urllib.request
import urllib.error

# Candidate paths and methods to probe during reconnaissance.
CANDIDATES = [
    ("GET", "/api/health"),
    ("GET", "/api/users/1/profile"),
    ("GET", "/api/users/2/profile"),
    ("GET", "/api/users/1/workouts"),
    ("POST", "/api/users/1/workouts"),
    ("POST", "/api/login"),
    ("GET", "/api/admin/stats"),
    ("GET", "/swagger"),
    ("GET", "/openapi.json"),
]


def probe(base, method, path):
    url = base.rstrip("/") + path
    data = b"{}" if method == "POST" else None
    req = urllib.request.Request(url, method=method, data=data)
    if method == "POST":
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=4) as r:
            body = r.read(400).decode("utf-8", "replace")
            return r.status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read(200).decode("utf-8", "replace")
    except Exception as e:
        return None, str(e)


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000"
    print(f"# Reconnaissance against {base}\n")
    results = []
    for method, path in CANDIDATES:
        status, body = probe(base, method, path)
        marker = "OK " if status and 200 <= status < 400 else "-- "
        print(f"{marker}{method:4} {path:35} -> {status}")
        results.append({"method": method, "path": path, "status": status,
                        "sample": body[:120] if body else None})
    out = "endpoint_scan_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved structured results to {out}")


if __name__ == "__main__":
    main()
