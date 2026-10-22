---
name: sca-audit
description: Scan project dependencies for known vulnerabilities (CVEs). Use when reviewing dependency files (package.json, requirements.txt, go.mod, pom.xml, Gemfile, Cargo.toml, etc.), triaging Dependabot/Renovate alerts, or performing pre-deployment security checks.
license: CC-BY-4.0
---

# Software Composition Analysis Audit

Scan dependencies for known CVEs by following the full procedure in `plays/sca-audit.md`.

## Steps

1. **Identify Dependency Manifests** — Scan for all dependency files and lockfiles across ecosystems (Node.js, Python, Go, Java, Ruby, Rust, .NET, PHP). Prefer lockfiles for exact resolved versions.

2. **Run Vulnerability Scan** — Use available tools in preference order:
   - `osv-scanner --lockfile=<path> --format=json` (recommended, multi-ecosystem)
   - `npm audit --json` (Node.js)
   - `pip-audit -r requirements.txt --format=json` (Python)
   - `govulncheck ./...` (Go)
   - `trivy fs --format json --scanners vuln <path>` (multi-ecosystem)
   - If no scanner is available, continue manifest/lockfile inventory and reachability work and report advisory matching as not assessed. Record the missing tooling and ask the user before installing a scanner (e.g., `brew install osv-scanner`); never report the result as a clean scan. For individual package triage, use [OSV.dev](https://osv.dev/list).

3. **Analyze Results** — For each vulnerability: determine reachability (is the vulnerable code path used?), check exploitability context (deployment matters), and identify fix availability (patch vs major version bump).

4. **Dependency Health** — Beyond CVEs, flag unmaintained packages (2+ years inactive), typosquatting risks, license concerns, and version pinning issues.

## Output

Scan summary (ecosystems, dependency count, scanner used), findings sorted by severity using `templates/finding.md`, condensed table for medium/low, dependency health flags, and exact remediation commands.

## OWASP References

- A03:2025: Software Supply Chain Failures
- OWASP Dependency-Check
- OWASP SCVS
