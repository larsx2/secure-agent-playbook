# Security Assessment Report: SCA Audit Sample

**Illustrative report, not an executed scan.** Package versions below are hypothetical inventory entries; advisory links are real. No application source, deployed configuration or exploit prerequisites were verified. This example shows how to report advisory matches without claiming confirmed application vulnerabilities.

**Scope**: Targeted Node.js dependency inventory (`package.json` and `package-lock.json`), not a whole-repository audit.
**Revision**: Not supplied in this example.
**Skills Used**: `sca-audit`
**Authorized operations**: Read-only inventory and public advisory lookup; no installation, target execution, active testing or source upload.

## Executive Summary

Three example package versions match published advisories; application reachability and impact remain unresolved. A fourth historical advisory is withdrawn and must not be counted as a confirmed vulnerability. Comprehensive reporting retains medium-severity matches, unknown reachability and unassessed components rather than hiding them behind a severity threshold.

## Coverage Inventory

| Component | Evidence available | Missing evidence / exclusions |
|-----------|--------------------|-------------------------------|
| Example Node.js service | Hypothetical package versions below | Actual lockfile/revision, complete direct/transitive inventory |
| Runtime/build/CI entrypoints | None | Source-to-sink paths, scripts, deployment configuration, ownership and provenance |
| Advisory matching | Linked public advisories | No scanner executed; complete matching and other ecosystems not assessed |

## Advisory Triage (Not Confirmed Application Exploits)

| Package / example version | Advisory | Published severity | Classification / prerequisites | First fix on example branch |
|---------------------------|----------|--------------------|--------------------------------|-----------------------------|
| lodash 4.17.20 | [CVE-2020-28500 / GHSA-29mw-wpgm-hmr9](https://github.com/advisories/GHSA-29mw-wpgm-hmr9) | MEDIUM | Unresolved: untrusted input must reach vulnerable `toNumber`, `trim` or `trimEnd` processing; this is ReDoS, not prototype pollution | 4.17.21 |
| jsonwebtoken 8.5.1 | [CVE-2022-23529 / GHSA-27h2-hvpr-p74q](https://github.com/advisories/GHSA-27h2-hvpr-p74q) | Withdrawn | Historical key-retrieval-input issue, not proof of JWT forgery; malicious control of `secretOrPublicKey` was a prerequisite. Do not count the withdrawn advisory as an active vulnerability | 9.0.0 was listed historically |
| express 4.18.2 | [CVE-2024-29041 / GHSA-rv95-896h-c2vc](https://github.com/expressjs/express/security/advisories/GHSA-rv95-896h-c2vc) | MEDIUM | Unresolved: malformed user-controlled URL must reach `res.location()` / `res.redirect()` and bypass the application's redirect policy | 4.19.2 |
| semver 6.3.0 | [CVE-2022-25883 / GHSA-c2qf-rxjj-qqgw](https://github.com/advisories/GHSA-c2qf-rxjj-qqgw) | HIGH | Unresolved: untrusted range input must reach `new Range`; a development/transitive dependency is not automatically reachable or harmless | 6.3.1 |

These are historical first-patched versions for the named advisories, not recommendations to install old versions today. Recheck current advisories and supported releases before proposing an upgrade. Advisory severity and application-context severity are separate; this example lacks evidence for the latter.

## Example Finding Record

### [MEDIUM advisory severity; application severity unresolved] lodash ReDoS candidate

- **CWE**: CWE-1333 (Inefficient Regular Expression Complexity)
- **CVE**: CVE-2020-28500
- **OWASP Ref**: Web Top 10 A03:2025 Software Supply Chain Failures
- **Location**: Hypothetical `package-lock.json` entry for lodash 4.17.20; actual file:line evidence not supplied
- **Classification**: Unresolved question — advisory/version match is not a confirmed application exploit
- **Evidence**: The linked advisory identifies the affected functions and version range; no scanner output or application behavior is claimed
- **Trace and defenses**: Not established. Locate inputs reaching `toNumber`, `trim` or `trimEnd`; inspect transformations, input limits and all runtime/build callers
- **Prerequisites**: Attacker-controlled input of sufficient size reaches the affected operation under deployed resource limits; not verified
- **Impact**: Potential CPU exhaustion if those prerequisites hold
- **Remediation**: Upgrade through the owning dependency to a current compatible supported version containing the fix; review lockfile changes and separately authorize installation/tests
- **Confidence**: High in the advisory's documented version mapping; unresolved application reachability
- **Validation**: No target execution or active test performed

## Control Gaps and Unresolved Questions

- No real application evidence is supplied, so this example establishes no application control failure or pass.
- Complete manifest/lockfile inventory, advisory matching, call paths and supply-chain provenance remain not-assessed.
- If a scanner is unavailable, retain the inventory and these missing-evidence entries; do not label the dependency graph clean.
- Record any deferral with rationale, owner and review date. Retain lower-severity/unknown findings even when the detailed presentation is filtered.

## Standards Coverage

Web Top 10 mappings are risk classification, not ASVS verification. Relevant ASVS 5.0 sections for subsequent review include **V15.2 Security Architecture and Dependencies**, **V1.2 Injection Prevention** (including regex/redirect controls), and **V2.4 Anti-automation**. Read the [tagged standard](https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en) before assigning exact controls and levels. No ASVS control is passed by this sample, and no compliance certification is implied. OpenCRE mappings are omitted rather than inferred from unrelated or older-version IDs.

## Recommendations

1. Complete the actual inventory and capture scanner version, advisory database timestamp, failures and unsupported ecosystems.
2. Trace each candidate through runtime, build and deployment paths before classifying exploitability.
3. Review compatible upgrades and verify remediations in separately authorized tests; do not run forced upgrades automatically.
4. Review registry trust, dependency scripts, CI permissions, artifact integrity and response processes in addition to known CVEs.
