#!/usr/bin/env python3
"""Build the single-PDF Week 2 submission report."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable)

OUT = "/home/kali/week2_api_security/deliverables/Week2_API_Security_Report.pdf"

GREEN = colors.HexColor("#1b6b3a")
LGREEN = colors.HexColor("#2e9e57")
GREY = colors.HexColor("#555555")
LIGHT = colors.HexColor("#eef5ef")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("CoverTitle", parent=styles["Title"], fontSize=24,
                          textColor=GREEN, spaceAfter=6, leading=28))
styles.add(ParagraphStyle("CoverSub", parent=styles["Normal"], fontSize=12,
                          textColor=GREY, alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle("H1", parent=styles["Heading1"], fontSize=15,
                          textColor=GREEN, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12,
                          textColor=LGREEN, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=9.5,
                          leading=13, spaceAfter=4))
styles.add(ParagraphStyle("Small", parent=styles["Normal"], fontSize=8,
                          leading=10, textColor=GREY))
styles.add(ParagraphStyle("Cell", parent=styles["Normal"], fontSize=7.5, leading=9))
styles.add(ParagraphStyle("CellB", parent=styles["Normal"], fontSize=7.5,
                          leading=9, textColor=colors.white))
styles.add(ParagraphStyle("CodeBlk", parent=styles["Normal"], fontName="Courier",
                          fontSize=8, leading=11, textColor=colors.HexColor("#222222"),
                          backColor=LIGHT, borderPadding=4, spaceAfter=4))

S = styles
story = []


def p(txt, st="Body"):
    story.append(Paragraph(txt, S[st]))


def sp(h=6):
    story.append(Spacer(1, h))


def rule():
    story.append(HRFlowable(width="100%", thickness=0.6, color=LGREEN,
                            spaceBefore=4, spaceAfter=8))


# ---------------- Cover ----------------
sp(60)
p("Fitness API Security Assessment<br/>&amp; Hardening Framework", "CoverTitle")
sp(4)
p("Week 2 of 12 — Introduction to OWASP API Security &amp; Reconnaissance", "CoverSub")
p("[Foundation]", "CoverSub")
sp(30)
p("Submission Report", "CoverSub")
sp(40)
cover_meta = Table([
    ["Author", "chocholucky33@gmail.com"],
    ["Date", "2026-10-21"],
    ["Program", "JPR Solutions · Internship Project"],
    ["Target", "Local practice Flask API (127.0.0.1:5000)"],
    ["Scope", "Reconnaissance & mapping only — no exploitation"],
], colWidths=[40*mm, 110*mm])
cover_meta.setStyle(TableStyle([
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("TEXTCOLOR", (0, 0), (0, -1), GREEN),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.HexColor("#cccccc")),
]))
story.append(cover_meta)
story.append(PageBreak())

# ---------------- Section 0: Context ----------------
p("1. Engagement Context &amp; Scope", "H1")
rule()
p("This report documents Week 2 of the Fitness API Security Assessment &amp; Hardening "
  "Framework internship project. The objective this week is foundational: to study the "
  "OWASP API Security Top 10 and perform initial reconnaissance against the target Flask API, "
  "producing an endpoint map and a summary of the OWASP risks.")
p("<b>Note on the target:</b> the course materials did not supply a live target API (no URL, "
  "application, or dataset). To carry out genuine reconnaissance, a minimal stand-in Fitness "
  "Flask API was built and run locally on <font face='Courier'>127.0.0.1:5000</font>, and all "
  "recon was performed against that authorized, locally-owned instance. The methodology, "
  "scripts, and findings transfer directly to the real target once provided.")
p("<b>Scope &amp; ethics:</b> this week covers reconnaissance and attack-surface mapping only. "
  "No authorization bypass or exploitation was performed. The OWASP \"candidate\" notes record "
  "where testing should focus in later weeks.")

# ---------------- Section 2: OWASP Top 10 ----------------
p("2. OWASP API Security Top 10 (2023) — Summary of Understanding", "H1")
rule()
p("Each risk below is described with a fitness-API example, how it is tested during recon, "
  "and the core mitigation that drives the later hardening phase.")

owasp = [
    ("API1 — Broken Object Level Authorization (BOLA)",
     "Object IDs are exposed but ownership is not checked, so changing an ID reaches another "
     "user's data. The most common and damaging API flaw.",
     "Swap an object ID (e.g. <font face='Courier'>/users/42/profile</font>) for one owned by "
     "another user and see if data returns.",
     "Enforce an ownership check on every object access; prefer unguessable IDs as defence-in-depth."),
    ("API2 — Broken Authentication",
     "Weak/missing auth: no login rate limiting, guessable or unverified tokens, credentials in URLs.",
     "Attempt login without credentials, inspect/decode tokens, test tokens after logout/expiry.",
     "Strong passwords, rate limiting + lockout, short-lived signed tokens, verify JWT alg/signature."),
    ("API3 — Broken Object Property Level Authorization",
     "Returns more fields than allowed (data exposure) or accepts fields the user shouldn't set "
     "(mass assignment).",
     "Inspect responses for sensitive fields; send extra fields in writes and check persistence.",
     "Allow-list fields for both serialization and request binding; never bind bodies onto ORM models."),
    ("API4 — Unrestricted Resource Consumption",
     "No limits on requests, payload size, or expensive operations — enables DoS and cost spikes.",
     "Send large <font face='Courier'>limit</font>/page values and oversized payloads (in scope).",
     "Rate limiting, pagination caps, payload-size limits, timeouts, quotas."),
    ("API5 — Broken Function Level Authorization (BFLA)",
     "A normal user can invoke admin functions or privileged methods.",
     "As a low-privilege user, call admin routes and PUT/DELETE methods.",
     "Deny-by-default role checks on every endpoint, enforced server-side."),
    ("API6 — Unrestricted Access to Sensitive Business Flows",
     "A legitimate flow (sign-up, rewards) can be automated and abused at scale.",
     "Identify high-value flows and assess bot-abuse feasibility.",
     "Behaviour/device detection, CAPTCHA where appropriate, per-flow rate limiting."),
    ("API7 — Server Side Request Forgery (SSRF)",
     "The API fetches a user-supplied URL, letting an attacker reach internal services/metadata.",
     "Supply internal/loopback/metadata URLs where the API fetches remote resources.",
     "Allow-list schemes/hosts, block private ranges and metadata IPs, disable redirects."),
    ("API8 — Security Misconfiguration",
     "Debug mode, verbose errors, missing security headers, permissive CORS, default creds.",
     "Trigger errors for stack traces, check headers, test CORS with a foreign Origin.",
     "Hardened per-environment config, disable debug, security headers, least-privilege CORS."),
    ("API9 — Improper Inventory Management",
     "Forgotten old versions and undocumented 'shadow' endpoints stay exposed and unpatched.",
     "Enumerate versions (v1/v2/beta), look for /swagger or /openapi.json, diff environments.",
     "Maintain a full API inventory, retire old versions, document every endpoint."),
    ("API10 — Unsafe Consumption of APIs",
     "Blindly trusting data returned by third-party APIs the app itself calls.",
     "Review outbound integrations and how their responses are validated.",
     "Validate/sanitize third-party data, use TLS, treat upstream data as untrusted."),
]

hdr = [Paragraph("<b>Risk</b>", S["CellB"]), Paragraph("<b>What it is</b>", S["CellB"]),
       Paragraph("<b>How to test</b>", S["CellB"]), Paragraph("<b>Mitigation</b>", S["CellB"])]
rows = [hdr]
for name, what, test, mit in owasp:
    rows.append([Paragraph(name, S["Cell"]), Paragraph(what, S["Cell"]),
                 Paragraph(test, S["Cell"]), Paragraph(mit, S["Cell"])])
t = Table(rows, colWidths=[34*mm, 42*mm, 37*mm, 42*mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), GREEN),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
]))
sp(2)
story.append(t)
sp(6)
p("<b>Key takeaways:</b> authorization flaws (BOLA/BFLA) dominate API risk and receive most test "
  "effort; recon must yield a complete endpoint and parameter inventory before testing (ties to "
  "API9); hardening must be deny-by-default, schema-validated, rate-limited and environment-specific.")

story.append(PageBreak())

# ---------------- Section 3: Endpoint Map ----------------
p("3. API Endpoint Map — Reconnaissance Results", "H1")
rule()
p("<b>Target:</b> http://127.0.0.1:5000 &nbsp;·&nbsp; <b>Tools:</b> curl, custom Python recon "
  "script (recon.py), manual observation.")
p("<b>Method:</b> (1) start the target API; (2) enumerate candidate paths/methods via status-code "
  "probing; (3) confirm each live endpoint with curl, recording method, parameters and a response "
  "sample; (4) note the OWASP risk each endpoint is a candidate for.")
sp(4)
p("3.1 Endpoint Inventory", "H2")

eh = [Paragraph("<b>#</b>", S["CellB"]), Paragraph("<b>Method</b>", S["CellB"]),
      Paragraph("<b>Path</b>", S["CellB"]), Paragraph("<b>Parameters</b>", S["CellB"]),
      Paragraph("<b>Auth</b>", S["CellB"]), Paragraph("<b>Status</b>", S["CellB"]),
      Paragraph("<b>Response sample</b>", S["CellB"]), Paragraph("<b>OWASP</b>", S["CellB"])]
endpoints = [
    ("1", "GET", "/api/health", "—", "none", "200",
     '{"service":"fitness-api","status":"ok","version":"v1"}', "API9"),
    ("2", "POST", "/api/login", "body: username", "none", "200",
     '{"message":"login endpoint","received_user":"test"}', "API2"),
    ("3", "GET", "/api/users/&lt;id&gt;/profile", "path: user_id", "none", "200",
     '{"id":1,"name":"Alice","plan":"pro"}', "API1 (BOLA)"),
    ("4", "GET", "/api/users/&lt;id&gt;/workouts", "path: user_id; query: limit", "none", "200",
     '[{"id":10,"minutes":30,"type":"run"}]', "API1, API4"),
    ("5", "POST", "/api/users/&lt;id&gt;/workouts", "path: user_id; JSON body", "none", "201",
     '{"echo":{},"message":"created"}', "API3"),
    ("6", "GET", "/api/admin/stats", "—", "none", "200",
     '{"total_users":2,"total_workouts":2}', "API5 (BFLA)"),
]
erows = [eh]
for r in endpoints:
    erows.append([Paragraph(c, S["Cell"]) for c in r])
et = Table(erows, colWidths=[6*mm, 13*mm, 33*mm, 30*mm, 11*mm, 12*mm, 45*mm, 18*mm], repeatRows=1)
et.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), GREEN),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
]))
story.append(et)
sp(5)
p("Probed but absent (useful negatives): <font face='Courier'>GET /swagger</font> → 404, "
  "<font face='Courier'>GET /openapi.json</font> → 404 (no machine-readable spec; manual mapping required).", "Small")
sp(6)

p("3.2 Parameter Notes", "H2")
p("• <b>user_id</b> (path integer, endpoints 3–5): directly indexes an object → primary BOLA "
  "target; sequential integers are trivially enumerable.<br/>"
  "• <b>limit</b> (query integer, endpoint 4): controls result size → API4 if uncapped.<br/>"
  "• <b>username / request body</b> (endpoints 2, 5): user-controlled input echoed/processed → "
  "check API3 and input validation.")

p("3.3 Attack-Surface Summary", "H2")
p("• 6 live endpoints across two resource groups (users, admin) plus a health route.<br/>"
  "• No authentication observed on any route, including <font face='Courier'>/api/admin/stats</font> "
  "→ high-priority area for testing (API2, API5).<br/>"
  "• Object IDs are sequential integers → BOLA enumeration is feasible (API1).<br/>"
  "• Version string <font face='Courier'>v1</font> leaked by the health route → supports version "
  "enumeration (API9).<br/>"
  "• No API documentation endpoint found → inventory must be maintained manually.")

story.append(PageBreak())

# ---------------- Section 4: Artifacts / reproduce ----------------
p("4. Artifacts &amp; Reproduction", "H1")
rule()
p("The following artifacts accompany this report:")
p("• <font face='Courier'>deliverables/01_OWASP_API_Top10_Summary.md</font> — full OWASP summary.<br/>"
  "• <font face='Courier'>deliverables/02_API_Endpoint_Map.md</font> — full endpoint map.<br/>"
  "• <font face='Courier'>deliverables/endpoint_scan_results.json</font> — raw scan evidence.<br/>"
  "• <font face='Courier'>scripts/recon.py</font> — reusable endpoint-discovery script.<br/>"
  "• <font face='Courier'>target_app/app.py</font> — local practice Flask target.")
sp(4)
p("Reproduce the reconnaissance:", "H2")
story.append(Paragraph(
    "# 1. start the practice target<br/>"
    "cd target_app &amp;&amp; python3 app.py&nbsp;&nbsp;# serves http://127.0.0.1:5000<br/><br/>"
    "# 2. in another terminal, run recon<br/>"
    "cd scripts &amp;&amp; python3 recon.py", S["CodeBlk"]))
sp(6)
p("Deliverables for Week 2 are complete: the OWASP API Security Top 10 summary and the API "
  "endpoint map, both backed by live reconnaissance evidence. The next phase (Week 3+) will use "
  "this map to test the prioritised authorization risks (API1/API5) against the authorized target.", "Body")
sp(10)
p("JPR Solutions · Internship Project · Week 2 Submission", "Small")

doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=18*mm, bottomMargin=16*mm,
                        leftMargin=16*mm, rightMargin=16*mm,
                        title="Week 2 — Fitness API Security Report",
                        author="chocholucky33@gmail.com")
doc.build(story)
print("WROTE", OUT)
