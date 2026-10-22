---
name: web-security-review
description: Review web applications against the OWASP Top 10 for Web Applications (2025). Use when auditing web apps, reviewing server-side code, or assessing web frameworks for access control, supply chain, injection, authentication, and exceptional-condition risks.
license: CC-BY-4.0
---

# Web Security Review (OWASP Top 10)

Review web applications against all 10 OWASP Top 10 risks by following the full procedure in `plays/owasp-top10-web-review.md`.

## Steps

1. **Application Mapping** — Identify framework/language, deployment model (monolith/microservices), trust boundaries (internet/internal/local), data sensitivity (PII, financial, health), and authentication mechanisms.

2. **Assess Each OWASP Top 10 Risk**:
   - **A01 Broken Access Control** — Missing authz checks, IDOR, tenant isolation, privilege escalation, CORS (also A02 via CWE-942) and SSRF
   - **A02 Security Misconfiguration** — Unsafe defaults, unnecessary features, exposed services and missing hardening
   - **A03 Software Supply Chain Failures** — Vulnerable dependencies, build/publish permissions, provenance and registry trust
   - **A04 Cryptographic Failures** — Weak algorithms, missing TLS, hardcoded keys and improper key management
   - **A05 Injection** — SQLi, command injection, XSS, SSTI and interpreter boundaries
   - **A06 Insecure Design** — Missing security requirements, business logic and workflow invariants
   - **A07 Authentication Failures** — Password length/blocklists (not composition rules), MFA, session and recovery controls
   - **A08 Software or Data Integrity Failures** — Unsafe deserialization, unverified updates and data integrity
   - **A09 Security Logging and Alerting Failures** — Security-event coverage, actionable alerts and response ownership
   - **A10 Mishandling of Exceptional Conditions** — Fail-open errors, partial transactions, resource exhaustion and insecure recovery

3. **Framework-Specific Analysis** — Apply checks for detected framework (React, Angular, Vue, Express, Django, Flask, Rails, Spring, ASP.NET, Laravel).

4. **Configuration Review** — Examine web server configs (nginx, Apache), application configs, and deployment manifests for security settings.

## Output

Application overview, risk matrix for all 10 categories with severity/status, detailed findings using `templates/finding.md`, positive controls observed, and prioritized remediation roadmap.

## OWASP References

- OWASP Top 10 for Web Applications (2025)
- OWASP ASVS v5.0 — Application Security Verification Standard
- OWASP Testing Guide (WSTG)
- OWASP Cheat Sheet Series
