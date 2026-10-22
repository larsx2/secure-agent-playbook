---
title: "CWE-79 Cross-site Scripting (XSS)"
cwe_id: "CWE-79"
owasp_top10: "A05:2025 Injection"
opencre_mappings:
  - cre_id: "366-835"
    cre_name: "Escape output against XSS"
when_to_use:
  - reviewing code that renders user input in HTML pages
  - assessing template engines for auto-escaping behavior
  - evaluating client-side JavaScript for DOM-based XSS
  - auditing LLM output rendered in web interfaces
threats:
  - reflected XSS via URL parameters or form inputs
  - stored XSS via database-persisted user content
  - DOM-based XSS via client-side JavaScript
  - XSS via LLM-generated HTML or Markdown
summary: "Cross-site scripting occurs when untrusted data is included in web output without proper encoding, allowing attackers to run scripts in victim browsers."
---

# CWE-79: Cross-site Scripting (XSS)

## OpenCRE Mappings

| CRE ID | CRE Name | Link |
|--------|----------|------|
| 366-835 | Escape output against XSS | [opencre.org/cre/366-835](https://www.opencre.org/cre/366-835) |

## Cross-Standard References

Via OpenCRE 366-835:
- **ASVS v5.0.0 equivalent**: [V1.2.1](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x10-V1-Encoding-and-Sanitization.md#v12-injection-prevention) — Context-aware HTTP/HTML/XML output encoding (verified against the tagged standard; do not reuse the older V5.3.3 ID returned by historical mappings)
- **WSTG**: WSTG-INPV-01 — Testing for Reflected XSS
- **OWASP Cheat Sheet**: XSS Prevention
- **NIST 800-53**: SI-10 — Information Input Validation

## What to Look For

- User input rendered without output encoding in HTML, JavaScript, CSS, or URL contexts
- Template engines with auto-escaping disabled or bypassed (safe filters, raw output, unsafe HTML rendering props)
- DOM manipulation using innerHTML or unsafe DOM write methods with user data
- LLM-generated Markdown or HTML rendered without sanitization
- Missing Content-Security-Policy headers

## References

- [CWE-79](https://cwe.mitre.org/data/definitions/79.html)
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Scripting_Prevention_Cheat_Sheet.html)
