# Security Assessment Report: SCA Audit Sample

**Date**: 2026-10-22
**Assessor**: Illustrative (OSV.dev queries)
**Scope**: Illustrative Node.js/Express application — the four direct dependencies listed below
**Skills Used**: `sca-audit`

**Illustrative report, not an executed scan.** The package versions are a hypothetical inventory. The advisory matches are real: each package version was queried against the [OSV.dev API](https://api.osv.dev/v1/query) on the report date, and every returned advisory is listed. No application source was reviewed, so reachability and application-level severity are unresolved for every finding.

---

## Executive Summary

The four example dependencies match 11 published advisories (4 HIGH, 6 MEDIUM, 1 LOW advisory severity). Every match is retained below regardless of severity; a twelfth, withdrawn advisory is listed separately and not counted. All matches have fixed versions. An advisory match shows that a vulnerable version is present, not that the application is exploitable: each finding states the conditions the application must meet before it is affected.

## Findings Summary

| # | Severity (highest advisory) | Title | CWE | OWASP Ref | Status |
|---|----------|-------|-----|-----------|--------|
| 1 | HIGH | lodash 4.17.20: 5 advisories (code/command injection, prototype pollution, ReDoS) | CWE-94, CWE-77, CWE-1321, CWE-1333, CWE-400 | A03:2025 | Open |
| 2 | HIGH | jsonwebtoken 8.5.1: 3 advisories (token verification weaknesses) | CWE-327, CWE-347, CWE-287, CWE-1259 | A03:2025 | Open |
| 3 | HIGH | semver 6.3.0: ReDoS | CWE-1333 | A03:2025 | Open |
| 4 | MEDIUM | express 4.18.2: 2 advisories (open redirect, redirect XSS) | CWE-601, CWE-1286, CWE-79 | A03:2025 | Open |

Severity is the highest published advisory severity per package. Application severity depends on the reachability conditions in each finding.

## Findings Detail

### [HIGH] lodash 4.17.20: 5 advisories

- **ID**: NDC-2026-001
- **CWE**: CWE-94, CWE-77, CWE-1321, CWE-1333, CWE-400 (per advisory below)
- **CVE**: CVE-2021-23337, CVE-2026-4800, CVE-2020-28500, CVE-2025-13465, CVE-2026-2950
- **OpenCRE**: Not looked up (optional external lookup)
- **OWASP Ref**: A03:2025 Software Supply Chain Failures
- **Location**: `package-lock.json` (lodash@4.17.20)
- **Impact**: Depends on which functions receive untrusted input. Template injection can execute code on the server; prototype pollution can alter application objects; ReDoS can exhaust CPU.
- **Evidence**: OSV.dev query for `lodash@4.17.20` (npm):

  | Advisory | Severity | Affected functionality / application is affected if | Fixed in |
  |----------|----------|------------------------------------------------------|----------|
  | [GHSA-35jh-r3h4-6jhm](https://github.com/advisories/GHSA-35jh-r3h4-6jhm) / CVE-2021-23337 | HIGH | Command injection via `_.template`; untrusted input reaches template options | 4.17.21 |
  | [GHSA-r5fr-rjxr-66jc](https://github.com/advisories/GHSA-r5fr-rjxr-66jc) / CVE-2026-4800 | HIGH | Code injection via `_.template` `imports` key names; untrusted input controls those keys | 4.18.0 |
  | [GHSA-29mw-wpgm-hmr9](https://github.com/advisories/GHSA-29mw-wpgm-hmr9) / CVE-2020-28500 | MEDIUM | ReDoS in `toNumber`, `trim`, `trimEnd`; large untrusted strings reach them | 4.17.21 |
  | [GHSA-xxjr-mmjv-4gpg](https://github.com/advisories/GHSA-xxjr-mmjv-4gpg) / CVE-2025-13465 | MEDIUM | Prototype pollution in `_.unset` / `_.omit`; untrusted input controls the path | 4.17.23 |
  | [GHSA-f23m-r3pf-42rh](https://github.com/advisories/GHSA-f23m-r3pf-42rh) / CVE-2026-2950 | MEDIUM | Prototype pollution via array-path bypass in `_.unset` / `_.omit` | 4.18.0 |

- **Remediation**: Upgrade to a release that fixes all five (4.18.0 or later; 4.18.1 was current on the report date). If lodash is transitive, use an `overrides` entry and confirm the resolved version in the lockfile. Then search the code for `_.template`, `_.unset`, `_.omit`, `toNumber`, `trim` and `trimEnd` calls on untrusted input.
- **Confidence**: HIGH that the version is affected; reachability not assessed

---

### [HIGH] jsonwebtoken 8.5.1: 3 advisories

- **ID**: NDC-2026-002
- **CWE**: CWE-327, CWE-347, CWE-287, CWE-1259 (per advisory below)
- **CVE**: CVE-2022-23539, CVE-2022-23540, CVE-2022-23541
- **OpenCRE**: Not looked up (optional external lookup)
- **OWASP Ref**: A03:2025 Software Supply Chain Failures
- **Location**: `package-lock.json` (jsonwebtoken@8.5.1)
- **Impact**: Under the configurations below, forged or weakly signed tokens can pass `jwt.verify()`, allowing authentication bypass.
- **Evidence**: OSV.dev query for `jsonwebtoken@8.5.1` (npm):

  | Advisory | Severity | Application is affected if | Fixed in |
  |----------|----------|----------------------------|----------|
  | [GHSA-8cf7-32gw-wr33](https://github.com/advisories/GHSA-8cf7-32gw-wr33) / CVE-2022-23539 | HIGH | It verifies with legacy key types or key/algorithm combinations outside the advisory's allowed list (e.g. DSA keys with RS256) | 9.0.0 |
  | [GHSA-qwph-4952-7xr6](https://github.com/advisories/GHSA-qwph-4952-7xr6) / CVE-2022-23540 | MEDIUM | `jwt.verify()` is called with no `algorithms` option and a falsy secret/key, so unsigned (`none`) tokens verify | 9.0.0 |
  | [GHSA-hjrf-2m68-5959](https://github.com/advisories/GHSA-hjrf-2m68-5959) / CVE-2022-23541 | MEDIUM | One key retrieval function serves both symmetric and asymmetric keys, allowing RSA-to-HMAC algorithm confusion | 9.0.0 |

  Not counted: [GHSA-27h2-hvpr-p74q](https://github.com/advisories/GHSA-27h2-hvpr-p74q) / CVE-2022-23529 (also `<= 8.5.1`) was **withdrawn** on 2023-01-27 and OSV no longer returns it. Older scanners or databases may still report it; list it as withdrawn rather than as a vulnerability.
- **Remediation**: Upgrade to 9.0.0 or later (9.0.3 was current on the report date); v9 has breaking changes, see the [migration notes](https://github.com/auth0/node-jsonwebtoken/wiki/Migration-Notes:-v8-to-v9). Regardless of version, always pass an explicit `algorithms` allowlist to `jwt.verify()` (ASVS 9.1.2).
- **Confidence**: HIGH that the version is affected; the configuration conditions were not assessed

---

### [HIGH] semver 6.3.0: ReDoS

- **ID**: NDC-2026-003
- **CWE**: CWE-1333
- **CVE**: CVE-2022-25883
- **OpenCRE**: Not looked up (optional external lookup)
- **OWASP Ref**: A03:2025 Software Supply Chain Failures
- **Location**: `package-lock.json` (semver@6.3.0)
- **Impact**: CPU exhaustion if untrusted range strings reach `new Range()` (including via `satisfies()` and similar functions).
- **Evidence**: OSV.dev query for `semver@6.3.0` (npm) returned [GHSA-c2qf-rxjj-qqgw](https://github.com/advisories/GHSA-c2qf-rxjj-qqgw) / CVE-2022-25883, HIGH, fixed in 6.3.1 (also 5.7.2 and 7.5.2).
- **Remediation**: Upgrade to 6.3.1 or later within the 6.x line, or move to a current 7.x release.
- **Confidence**: HIGH that the version is affected; reachability not assessed

---

### [MEDIUM] express 4.18.2: 2 advisories

- **ID**: NDC-2026-004
- **CWE**: CWE-601, CWE-1286, CWE-79
- **CVE**: CVE-2024-29041, CVE-2024-43796
- **OpenCRE**: Not looked up (optional external lookup)
- **OWASP Ref**: A03:2025 Software Supply Chain Failures
- **Location**: `package-lock.json` (express@4.18.2)
- **Impact**: If user-controlled URLs reach `res.redirect()` or `res.location()`, attackers can redirect users to another site or inject script into the redirect response.
- **Evidence**: OSV.dev query for `express@4.18.2` (npm):

  | Advisory | Severity | Application is affected if | Fixed in |
  |----------|----------|----------------------------|----------|
  | [GHSA-rv95-896h-c2vc](https://github.com/advisories/GHSA-rv95-896h-c2vc) / CVE-2024-29041 | MEDIUM | Malformed user-controlled URLs reach `res.location()` / `res.redirect()` and bypass the app's allowlist | 4.19.2 |
  | [GHSA-qw6h-vgh9-j6wx](https://github.com/advisories/GHSA-qw6h-vgh9-j6wx) / CVE-2024-43796 | LOW | Untrusted input reaches `res.redirect()` | 4.20.0 |

- **Remediation**: Upgrade to the latest 4.x release (4.22.3 on the report date). 4.20.0 fixes both express advisories, but its pinned dependencies still carry 9 advisories (body-parser, cookie, path-to-regexp, qs, send). A tree resolved from express 4.22.3 (68 packages) had no OSV matches on the report date. Re-scan the lockfile after upgrading. Validate redirect targets against an allowlist (ASVS 3.7.2).
- **Confidence**: HIGH that the version is affected; reachability not assessed

---

## Out of Scope

- **Transitive dependencies.** This illustrative inventory lists only four packages. A real lockfile for express@4.18.2 also pins body-parser 1.20.1, cookie 0.5.0, path-to-regexp 0.1.7, qs 6.11.0, send 0.18.0 and serve-static 1.15.0. On the report date OSV returned 11 more advisories for those versions. A real report must list them too.
- Application source review: reachability of the affected functions was not assessed
- License compliance review
- Dependency health and provenance (maintainer activity, typosquatting, install scripts, registry trust)
- Container image scanning

## Standards Coverage

Each finding maps to A03:2025 (vulnerable components). These ASVS v5.0.0 requirements decide whether the matches matter, and each needs evidence from the application before it can be marked pass or fail:

| ASVS requirement (level) | Relevance | Findings |
|--------------------------|-----------|----------|
| 15.2.1 (L1) | Components within documented update and remediation time frames | #1–#4 |
| 9.1.2 (L1) | Explicit JWT algorithm allowlist, no `none` | #2 |
| 1.3.7 (L2) | No templates built from untrusted input | #1 |
| 15.3.6 (L2) | JavaScript written to prevent prototype pollution | #1 |
| 3.7.2 (L2) | Redirects to other hosts only to allowlisted destinations | #4 |
| 15.2.2 (L2) | Defenses against resource-exhaustion functionality | #1, #3 |

OpenCRE mappings are omitted rather than guessed; resolve them through the OpenCRE API if needed.

## Recommendations

1. **High priority**: Upgrade `lodash` (≥ 4.18.0) and `semver` (≥ 6.3.1); both are drop-in within their major versions.
2. **High priority**: Upgrade `express` to the latest 4.x (4.22.3 on the report date) and re-scan the resolved lockfile.
3. **Plan migration**: Upgrade `jsonwebtoken` to ≥ 9.0.0 (breaking changes). Until then, confirm every `jwt.verify()` call passes an explicit `algorithms` list and a non-empty key.
4. **Verify**: Search the code for the affected functions listed in each finding to set application-level severity.
5. **Process**: Run an SCA scanner (`osv-scanner`, `npm audit`) in CI. Make sure its advisory database excludes withdrawn advisories, or flags them as withdrawn.
