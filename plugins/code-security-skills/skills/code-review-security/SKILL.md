---
name: code-review-security
description: Security-focused code review mapped to OWASP Top 10 and ASVS. Use when reviewing pull requests, auditing files or modules for vulnerabilities, or performing pre-merge security gate checks. Covers injection, auth, authorization, cryptography, data exposure, misconfiguration, and deserialization.
license: CC-BY-4.0
---

# Security Code Review

Review code for security vulnerabilities by following the full procedure in `plays/code-review-security.md`.

Follow `plays/assessment-contract.md` first. Produce per-control ASVS status rows only when the user asks to verify at a stated ASVS level (contract section 6).

## Steps

1. **Scope & Context** — Establish language/framework, trust boundary (server/client/library/CLI), data sensitivity (PII, credentials, financial), and exposure (internet-facing, internal, local).

2. **Systematic Review by Vulnerability Class** (priority order):
   - **Injection (A05:2025)** — SQL, command, XSS, SSTI, LDAP, header injection
   - **Authentication & Session (A07:2025)** — Hardcoded credentials, missing auth, weak sessions, JWT issues
   - **Authorization (A01:2025)** — Missing authz checks, IDOR, horizontal/vertical privilege escalation, path traversal, CSRF
   - **Cryptography (A04:2025)** — Weak algorithms, hardcoded keys, missing encryption, custom crypto
   - **Data Exposure (A01:2025; related CWEs map to A02/A07/A09/A10)** — Over-broad responses, sensitive data in errors/logs, credentials in code, debug mode
   - **Misconfiguration (A02:2025)** — Default credentials, permissive CORS (also A01), missing security headers
   - **Deserialization & Integrity (A08:2025)** — Untrusted deserialization, missing integrity checks, unsigned cookies/tokens
   - **Supply Chain (A03:2025)** — Dependency, build, registry and artifact trust
   - **Insecure Design (A06:2025)** — Business invariants, workflows, concurrency and anti-automation
   - **Logging / Exceptional Conditions (A09/A10:2025)** — Log injection, actionable alerts, fail-closed errors, resource bounds and recovery
   - **SSRF (A01:2025)** — Outbound destination policy and connection enforcement

3. **Framework-Specific Checks** — Apply checks for detected framework (React, Express, Django, Flask, Spring, Rails, Go).

4. **Diff-Specific Analysis** (for PRs) — Focus on changed lines plus context, verify security controls preserved, check new endpoints match auth patterns, look for removed security controls.

5. **Produce Findings** — Cite file:line, show vulnerable snippet, explain attack scenario, provide fixed code, rate confidence.

## Output

Scope summary, findings sorted by severity using `templates/finding.md`, positive observations (good security controls in place), and severity count table.

## OWASP References

- OWASP Web Top 10 (2025): A01-A10
- OWASP ASVS v5.0
- OWASP Code Review Guide
- OWASP Cheat Sheet Series
