# Security Assessment Report Template

Review skills apply `plays/assessment-contract.md` before inspecting the target; this template carries its results.

## Report: [Target Name]

**Date**: YYYY-MM-DD
**Assessor**: Claude Code (agent-security-playbook)
**Scope**: [What was assessed — repo, service, architecture, agent config]
**Skills Used**: [List of skills invoked]
**Review Mode**: Diff (base..head) | Whole repository | Targeted — [revision]
**Authorized Operations**: Read-only | [operations the user approved, with limits]

---

## Executive Summary

[2-3 sentences: what was tested, highest-severity finding, overall risk posture]

## Findings Summary

| # | Severity | Title | CWE | OpenCRE | OWASP Ref | Status |
|---|----------|-------|-----|---------|-----------|--------|
| 1 | CRITICAL | ... | CWE-XXX | [CRE-ID](https://www.opencre.org/cre/CRE-ID) | ... | Open |
| 2 | HIGH | ... | CWE-XXX | [CRE-ID](https://www.opencre.org/cre/CRE-ID) | ... | Open |

## Findings Detail

[Include full findings using templates/finding.md format]

## Control Gaps and Unresolved Questions

[Kept separate from confirmed vulnerabilities: the missing control or evidence, and the next step to resolve it]

## Coverage

| Area (changed file, component, entrypoint, boundary) | Reviewed evidence | Excluded or not performed (reason) |
|------------------------------------------------------|-------------------|------------------------------------|
| ... | file:line, configuration, approved test | ... |

## Out of Scope

[Explicitly list what was NOT tested, including steps skipped for lack of authorization]

## Verification Status

Only for a requested verification at a stated level (contract section 5); otherwise omit this section.

| Requirement | Status | Evidence / rationale | Missing runtime or deployment evidence |
|-------------|--------|----------------------|----------------------------------------|
| ASVS v5.0.0 V6.2.1 (L1) | not-assessed | Diff adds a password-change endpoint; minimum length is read from deployment configuration | Deployed password policy |

## Standards Coverage

OpenCRE cross-references are optional external lookups at https://www.opencre.org, not bundled dependencies. Verify the returned standard version:

| CRE ID | Requirement | CWE | ASVS | WSTG | NIST 800-53 | Findings |
|--------|-------------|-----|------|------|-------------|----------|
| [CRE-ID](https://www.opencre.org/cre/CRE-ID) | ... | CWE-XXX | V#.#.# | WSTG-XXX-## | XX-## | #1, #2 |

## Recommendations

[Prioritized list of next steps, ordered by risk reduction impact]
