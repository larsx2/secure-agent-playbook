# Security Assessment Report Template

Review skills apply `plays/assessment-contract.md` before inspecting the target; this template carries its results.

## Report: [Target Name]

**Date**: YYYY-MM-DD
**Assessor**: Claude Code (agent-security-playbook)
**Scope**: Diff (base..head) | Whole repository | Targeted — [target and revision]
**Skills Used**: [List of skills invoked]
**Approved Operations**: Read-only | [operations the user approved, with limits]

---

## Executive Summary

[2-3 sentences: what was tested, highest-severity finding, overall risk posture]

## Findings Summary

| # | Severity | Classification | Title | CWE | OpenCRE | OWASP Ref | Remediation |
|---|----------|----------------|-------|-----|---------|-----------|-------------|
| 1 | CRITICAL | Confirmed vulnerability | ... | CWE-XXX | [CRE-ID](https://www.opencre.org/cre/CRE-ID) | ... | Open |
| 2 | HIGH | Control gap | ... | CWE-XXX | [CRE-ID](https://www.opencre.org/cre/CRE-ID) | ... | Open |

## Findings Detail

[Full findings in templates/finding.md format, grouped as confirmed vulnerabilities, then control gaps, then unresolved questions]

## Coverage

Everything not reviewed goes in the last column, including steps skipped for lack of approval.

| Area (changed file or component) | Reviewed evidence | Excluded or not assessed (reason) |
|----------------------------------|-------------------|-----------------------------------|
| ... | file:line, configuration, approved test | ... |

## Verification Status

Only for a requested verification at a stated level (contract section 6); otherwise omit this section.

| Requirement | Status | Evidence / rationale | Missing runtime or deployment evidence |
|-------------|--------|----------------------|----------------------------------------|
| ASVS v5.0.0 V6.2.1 (L1) | not assessed | Diff adds a password-change endpoint; minimum length is read from deployment configuration | Deployed password policy |

## Standards Coverage

OpenCRE cross-references are optional external lookups at https://www.opencre.org, not bundled dependencies. Verify the returned standard version:

| CRE ID | Requirement | CWE | ASVS | WSTG | NIST 800-53 | Findings |
|--------|-------------|-----|------|------|-------------|----------|
| [CRE-ID](https://www.opencre.org/cre/CRE-ID) | ... | CWE-XXX | V#.#.# | WSTG-XXX-## | XX-## | #1, #2 |

## Recommendations

[Prioritized list of next steps, ordered by risk reduction impact]
