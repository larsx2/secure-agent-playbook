# Play: Security Code Review

A security code review identifies vulnerabilities in application logic, authentication, authorization, cryptography, and data handling. This play structures the review around OWASP weakness classes (injection, auth, crypto, etc.) and is applicable to any language or framework. Reviews can target full codebases, pull request diffs, or specific modules, and findings are mapped to OWASP standards and OpenCRE for multi-framework traceability.

Review code changes or codebases for security vulnerabilities, mapping findings to OWASP standards and OpenCRE cross-references for multi-framework traceability.

## Trigger Conditions

Use this skill when:
- Reviewing a pull request or diff for security issues
- A user asks for a security review of their code
- Auditing a specific file, module, or feature for vulnerabilities
- Performing a pre-merge security gate check

## Inputs

- Code diff (PR), specific files, or entire codebase to review
- (Optional) Language and framework context
- (Optional) ASVS level to verify against (L1, L2, or L3)
- (Optional) Specific concern areas to focus on

## Procedure

### 1. Scope & Context

Before diving in, establish:
- **Language/Framework**: Determines which vulnerability classes are relevant
- **Trust boundary**: Is this server-side, client-side, library, CLI, infrastructure code?
- **Data sensitivity**: Does this code handle PII, credentials, financial data, health data?
- **Exposure**: Is this internet-facing, internal, or local-only?

### 2. Systematic Review by Vulnerability Class

Review in priority order — highest-impact classes first:

#### A. Injection (CWE-74, OWASP A05:2025, [OpenCRE 161-451](https://www.opencre.org/cre/161-451))

> ASVS refs: `data/asvs/V2.2.md` (Input Validation), `data/asvs/V1.2.md` (Injection Prevention / Output Encoding)

| Subtype | What to Look For |
|---------|-----------------|
| SQL Injection | String concatenation in queries, missing parameterization, ORM raw queries |
| Command Injection | User input in exec/spawn/system calls, unsanitized shell arguments |
| XSS | User input rendered without output encoding, unsafe DOM manipulation, unescaped template output |
| SSTI | User input in template strings that get evaluated server-side |
| LDAP Injection | User input in LDAP filters without escaping |
| Header Injection | User input in HTTP headers (CRLF injection) |

Path traversal (CWE-22) is reviewed under C (A01:2025) and log injection (CWE-117) under J (A09:2025).

#### B. Authentication & Session (CWE-287, OWASP A07:2025, [OpenCRE 633-428](https://www.opencre.org/cre/633-428))

> ASVS refs: `data/asvs/V6.1.md`–`V6.8.md` (Authentication), `data/asvs/V7.1.md`–`V7.6.md` (Session Management)

- Hardcoded credentials or API keys
- Missing authentication on endpoints
- Weak password requirements
- Session tokens in URLs or logs
- Missing session invalidation on logout/password change
- JWT issues: none algorithm, missing expiry, weak signing key, secrets in payload
- Missing MFA enforcement for sensitive operations

#### C. Authorization (CWE-862, OWASP A01:2025, [OpenCRE 724-770](https://www.opencre.org/cre/724-770))

> ASVS refs: `data/asvs/V8.1.md`–`V8.4.md` (Authorization), `data/asvs/V5.3.md` (File Storage, path traversal), `data/asvs/V3.5.md` (Browser Origin Separation, CSRF)

- Missing authorization checks on endpoints or functions
- IDOR: object references without ownership validation
- Horizontal privilege escalation (accessing other users' data)
- Vertical privilege escalation (accessing admin functions)
- Missing RBAC/ABAC enforcement
- Direct database queries that don't filter by user/tenant
- Path traversal (CWE-22): user input in file paths without canonicalization, `../` not blocked
- Missing CSRF protection on state-changing operations (CWE-352)

#### D. Cryptography (CWE-327, OWASP A04:2025, [OpenCRE 278-646](https://www.opencre.org/cre/278-646))

> ASVS refs: `data/asvs/V11.1.md`–`V11.7.md` (Cryptography), `data/asvs/V12.1.md`–`V12.3.md` (Secure Communication)

- Weak algorithms: MD5, SHA1 for passwords, DES, RC4
- ECB mode usage
- Hardcoded encryption keys or IVs
- Missing encryption at rest for sensitive data
- Missing TLS enforcement
- Custom crypto implementations (don't roll your own)
- Insufficient key lengths (RSA < 2048, AES < 128)

#### E. Data Exposure (CWE-200, OWASP A01:2025, [OpenCRE 126-668](https://www.opencre.org/cre/126-668))

> ASVS refs: `data/asvs/V14.1.md`–`V14.3.md` (Data Protection), `data/asvs/V16.1.md`–`V16.5.md` (Security Logging & Error Handling)

Related weaknesses map to different 2025 categories; cite the category of the specific CWE:

- API responses including more fields than necessary (CWE-200, A01:2025)
- Sensitive data in error messages or stack traces (CWE-209, A10:2025)
- Verbose logging of requests/responses containing PII or secrets (CWE-532, A09:2025)
- Credentials or tokens in source code or configs (CWE-798, A07:2025)
- Debug mode enabled in production configs (CWE-489, A02:2025)

#### F. Security Misconfiguration (OWASP A02:2025, [OpenCRE 233-748](https://www.opencre.org/cre/233-748))

> ASVS refs: `data/asvs/V13.1.md`–`V13.4.md` (Configuration)

- Default credentials or configurations
- Unnecessary features enabled (debug endpoints, admin panels)
- Missing security headers
- Overly permissive CORS (CWE-942, A02:2025; also described under A01:2025, so cite both)
- Directory listing enabled
- Missing rate limiting on sensitive endpoints

#### G. Deserialization & Data Integrity (CWE-502, OWASP A08:2025, [OpenCRE 854-643](https://www.opencre.org/cre/854-643))

> ASVS refs: `data/asvs/V1.5.md` (Safe Deserialization), `data/asvs/V9.1.md` (Token Source and Integrity), `data/asvs/V3.3.md` (Cookie Setup)

- Deserializing untrusted data (unsafe deserialization in any language — Python, Java, PHP, Ruby, .NET)
- Missing integrity checks on data from untrusted sources
- Unsigned cookies or tokens

#### H. Software Supply Chain (OWASP A03:2025)

> ASVS refs: `data/asvs/V15.2.md` (Security Architecture and Dependencies)

- Inventory direct/transitive dependencies, build tools, registries and CI/CD trust boundaries; follow `plays/sca-audit.md`.
- Review lockfile provenance, install scripts, dependency confusion, update verification, build credentials and artifact publication permissions. A clean advisory scan does not establish supply-chain integrity.

#### I. Insecure Design (OWASP A06:2025)

> ASVS refs: `data/asvs/V2.3.md`, `data/asvs/V2.4.md`

- Trace business invariants through multi-step workflows, concurrent requests, quotas and recovery paths; check server-owned prices, ownership and tenant scope.

#### J. Logging and Exceptional Conditions (OWASP A09:2025, A10:2025)

> ASVS refs: `data/asvs/V16.2.md`–`V16.5.md`, `data/asvs/V15.3.md`, `data/asvs/V15.4.md`

- Review security-event logging, tamper protection, actionable alerts and response ownership.
- Log injection (CWE-117): user input written to logs without encoding (ASVS 16.4.1).
- Trace errors, timeouts, resource exhaustion and partial failures: fail closed, roll back partial transactions, release resources, bound retries and preserve authorization on fallback paths.

#### K. Server-Side Request Forgery (CWE-918, OWASP A01:2025)

> ASVS refs: `data/asvs/V1.3.md` (requirement 1.3.6, SSRF), `data/asvs/V13.2.md` (requirements 13.2.4–13.2.5, outbound allowlists)

- Trace user-influenced outbound requests, including webhooks and redirects. Check egress policy, allowed destinations, all IPv4/IPv6 answers and DNS check/use races; URL validation alone is not connection pinning.

### 3. Framework-Specific Checks

Apply checks specific to the detected framework:

| Framework | Key Checks |
|-----------|-----------|
| React/Next.js | XSS via unsafe HTML rendering, SSRF in server-side data fetching, exposed API routes |
| Express/Node | Missing helmet, no rate limiting, prototype pollution, regex DoS |
| Django | Raw SQL, CSRF exemptions, DEBUG=True, SECRET_KEY exposure |
| Flask | Jinja2 autoescape disabled, unsafe session serialization, debug mode |
| Spring | SpEL injection, actuator exposure, mass assignment |
| Rails | Mass assignment, render user input, SQL fragments |
| Go net/http | Missing timeouts, TOCTOU in file operations, integer overflow |

### 4. Diff-Specific Analysis (for PR reviews)

When reviewing a diff rather than a full codebase:
- Focus on changed lines and their immediate context
- Check if security controls in surrounding (unchanged) code are preserved
- Verify that new endpoints have auth/authz matching existing patterns
- Check if new dependencies introduce vulnerabilities (cross-reference with sca-audit)
- Look for removed security controls (deleted validation, removed auth checks)

### 5. Produce Findings

For each issue:
- Cite the specific code location (file:line)
- Show the vulnerable code snippet
- Explain the attack scenario concretely
- Provide a fixed code snippet
- Rate confidence (HIGH if confirmed path, MEDIUM if contextual, LOW if heuristic)

## Output Format

```markdown
## Security Code Review: [Target]

### Scope
- **Files reviewed**: [count or list]
- **Language/Framework**: [detected]
- **Review type**: Full | PR diff | Targeted

### Findings
[Standard finding template for each issue, sorted by severity]

### Positive Observations
[Security controls that ARE in place — acknowledge good practices]

### Summary
| Severity | Count |
|----------|-------|
| CRITICAL | N |
| HIGH | N |
| MEDIUM | N |
| LOW | N |
| INFO | N |
```

## Tools & Resources

### Static Analysis Tools
- **Semgrep** — Multi-language pattern-based SAST; highly customizable rules
- **CodeQL (GitHub)** — Query-based code analysis for Java, C++, C#, Go, Python, TypeScript, JavaScript, Ruby
- **SonarQube** — Code quality and security scanning with OWASP Top 10 mappings
- **Checkmarx/CxSAST** — Enterprise SAST with custom rule authoring
- **Snyk Code** — Developer-first SAST integrated into IDEs and CI/CD

### Language-Specific
- **Bandit** (Python) — Finds common security issues in Python code
- **Brakeman** (Ruby) — Scans Rails apps for OWASP risks
- **go-vuln-check** (Go) — Detects known vulnerabilities in Go code
- **ShiftLeft/Taint** (Java, Python, Go) — Data flow analysis for injection detection

### Code Review Checkers
- **OWASP Cheat Sheet Series** — Per-vulnerability quick guides and remediation
- **CWE Top 25** — Prioritized list of most dangerous weakness patterns
- **ASVS Interactive** — Maps review items to ASVS verification levels (L1/L2/L3)

## References

- [OWASP Top 10 (2025)](https://owasp.org/Top10/2025/): A01-A10 (Web; distinct from API Top 10:2023)
- [OWASP ASVS v5.0.0](https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en) (for requirement text and verification levels)
- OWASP Code Review Guide
- OWASP Cheat Sheet Series (per-topic)
- OWASP Proactive Controls
- [OpenCRE](https://www.opencre.org) — Cross-standard requirement mappings (CWE, ASVS, WSTG, NIST 800-53, ISO 27001)
- [CWE](https://cwe.mitre.org) v4.19 — Common Weakness Enumeration
- ASVS 5.0 reference data in `data/asvs/` — sourced from [OWASP Agent Skills Project](https://github.com/eoftedal/owasp-agent-skills-project)
