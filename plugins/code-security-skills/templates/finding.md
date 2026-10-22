# Finding Template

Use this structure for all security findings produced by skills. First apply the [assessment contract](report.md#assessment-contract).

```markdown
### [SEVERITY] Title

- **ID**: NDC-YYYY-NNN (auto-incrementing)
- **CWE**: CWE-XXX (if applicable)
- **CVE**: CVE-YYYY-NNNNN (if applicable)
- **OpenCRE**: [CRE-ID](https://www.opencre.org/cre/CRE-ID) — requirement name (optional external lookup)
- **OWASP Ref**: Web Top 10 A01:2025, ASVS v5.0.0 V8.2.1, MASVS-STORAGE-1, MASWE-0001, MASTG-TEST-0200, LLM01:2025, etc.
- **Location**: file_path:line_number or component name
- **Impact**: What an attacker can achieve (1-2 sentences)
- **Evidence**: Code snippet, command output, or proof-of-concept
- **Classification**: Confirmed vulnerability | Control gap | Unresolved question
- **Trace and defenses**: Attacker-controlled source → transformations/guards → sensitive sink, with file:line evidence
- **Prerequisites**: Attacker role/tenant, configuration and other necessary conditions; verified evidence or unresolved assumptions
- **Validation**: What was observed, what was not executed, and missing runtime evidence
- **Remediation**: Specific fix with code example
- **Confidence**: HIGH | MEDIUM | LOW (how certain is this finding)
```

### Resolving OpenCRE Links

When you have a CWE, look up its OpenCRE mapping via the API:

```
GET https://www.opencre.org/rest/v1/standard/CWE/sectionid/{cwe-number}
```

This returns the CRE ID and linked standards (ASVS, WSTG, NIST 800-53, cheat sheets). Include the CRE link in findings to give readers one-click access to all related standards and remediation guidance.

This lookup is external and optional. If unavailable, report the CWE and verified standard references without inventing a CRE mapping.

## Severity Definitions

| Severity | CVSS Range | Criteria |
|----------|-----------|----------|
| CRITICAL | 9.0-10.0 | Remote code execution, full system compromise, mass data breach |
| HIGH | 7.0-8.9 | Privilege escalation, significant data exposure, auth bypass |
| MEDIUM | 4.0-6.9 | Limited data exposure, requires user interaction or specific conditions |
| LOW | 0.1-3.9 | Information disclosure, minor misconfigurations |
| INFORMATIONAL | N/A | Best practice recommendations, defense-in-depth suggestions |

## Confidence Levels

| Level | Meaning |
|-------|---------|
| HIGH | Source-to-sink path and all exploit prerequisites supported by evidence (or a directly established control gap) |
| MEDIUM | Strong indicators but missing context; classify unresolved exploit claims separately |
| LOW | Heuristic candidate requiring investigation; not a confirmed vulnerability |
