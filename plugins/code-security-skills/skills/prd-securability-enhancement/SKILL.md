---
name: prd-securability-enhancement
description: Enhance PRDs, feature specs, user stories, or product briefs with explicit OWASP ASVS coverage and FIASSE v1.0.4 SSEM implementation guidance — before code is written. Trigger on "harden the PRD/spec", "choose ASVS level", "map features to ASVS", "find missing security requirements", "add NFRs for security", "make these requirements securable", "security-review my product brief". For code review use securability-engineering-review; for code generation use securability-engineering.
license: CC-BY-4.0
---

# PRD Securability Enhancement (FIASSE/SSEM + ASVS)

Enhance PRD content so each feature has explicit, testable securability requirements aligned to OWASP ASVS and shaped by FIASSE v1.0.4 / SSEM. The goal is to upgrade the requirements artifact *before* implementation, so delivery teams build securable capabilities by design rather than retrofitting controls later.

This skill is requirements-centric. It does not review or write code. If the user wants code review, redirect to `securability-engineering-review`. If they want code generation, redirect to `securability-engineering`.

## When to Invoke

Trigger this skill when the user asks to:

- Strengthen or harden a PRD, spec, user-story set, or product brief with security requirements
- Choose an ASVS assurance level (Level 1, 2, or 3) for a product or feature
- Map features to ASVS controls or check ASVS coverage of a requirements doc
- Find missing security requirements before development starts
- Annotate features with SSEM attributes or FIASSE tenets
- Add testable security acceptance criteria to existing functional requirements

Adjacent phrasings: "security-review this spec", "what's missing security-wise from this feature list", "add NFRs for security to my PRD", "make these requirements securable".

## Inputs

Ask the user for whatever is missing before starting:

- The PRD, spec, or feature list (markdown, prose, ticket export, etc.)
- System context: user types, deployment model, data sensitivity, integration surfaces
- Compliance or risk context, if any (HIPAA, PCI, SOC 2, regulated industry)
- Whether they have an ASVS level preference, or want this skill to recommend one

If the artifact is large, parse the features inline; do not require the user to pre-extract them.

## Procedure

### Step 1 — Parse features

Extract each feature into a normalized record. Capture for each:

- Feature ID and title (assign IDs like `F-01` if absent)
- Actor (user role, system, external service)
- Data touched and sensitivity class
- Trust boundaries crossed (browser↔server, service↔service, server↔storage, internal↔external)
- Existing acceptance criteria (verbatim, even if weak)

If the source PRD lumps several capabilities into one bullet, split them so each feature is independently testable.

### Step 2 — Choose the ASVS level *first*

Selecting the level before mapping requirements prevents both under-scoping and over-scoping. Use this rubric:

| Level | Use when |
|-------|----------|
| **1** | Internal tooling, prototypes, low-sensitivity data, no regulatory pressure, limited blast radius if compromised |
| **2** | Typical production web/API systems with authenticated users, business-critical behavior, customer data, or moderate regulatory exposure (most products land here) |
| **3** | High-assurance contexts: payments, health records, government, identity providers, anything where compromise causes severe material impact or where attackers are well-resourced |

Default to Level 2 unless evidence pushes lower or higher. Document:

- Chosen level
- Why lower levels are insufficient (when level > 1)
- Any specific features that should escalate above the baseline (e.g., a payments endpoint inside a Level-2 product gets Level-3 treatment)

### Step 3 — Map each feature to ASVS

For every feature, use `data/asvs/README.md` (chapter index) and the `when_to_use` frontmatter in `data/asvs/V*.md` to identify applicable chapters. Common mappings:

- Auth flows → V6 (Authentication), V7 (Session Management)
- Authorization, ownership, multi-tenant scoping → V8 (Authorization)
- File upload/download → V5 (File Handling)
- Crypto/password hashing → V11 (Cryptography); self-contained tokens → V9; OAuth/OIDC → V10
- Logging, error handling, observability → V16 (Security Logging and Error Handling)
- PII and lifecycle → V14 (Data Protection); transport → V12 (Secure Communication)
- Public APIs → V4 (API and Web Service)
- Config, secrets, deployment → V13 (Configuration)
- Workflow rules, anti-automation and input validation → V2 (Validation and Business Logic)
- Encoding, sanitization and deserialization → V1 (Encoding and Sanitization)
- Browser controls → V3 (Web Frontend Security); WebRTC → V17
- Architecture, dependencies, defensive coding and concurrency → V15 (Secure Coding and Architecture)

Filter requirements by the chosen ASVS level, including lower levels. Verify IDs, text and levels against [ASVS v5.0.0](https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en). Label stricter product choices and above-baseline controls separately. PRD coverage is not evidence of implemented controls or compliance certification. For each requirement, classify coverage:

- **Covered** — the PRD already satisfies the intent
- **Partial** — partly covered; clarify or strengthen acceptance criteria
- **Missing** — requirement absent and must be added
- **N/A** — justified with a one-line rationale

Use the **ASVS Coverage Gap Pattern Table** below to spot the gaps that PRDs reliably miss.

### Step 4 — Add Securability Notes per feature

Write a *short* paragraph per feature surfacing only the SSEM and FIASSE points that materially shape implementation. Do not enumerate all ten SSEM attributes or all FIASSE tenets — that produces noise.

Useful lenses (mention only when relevant):

- Trust-boundary handling and input canonicalization (FIASSE v1.0.4 S4.3, S4.4.1)
- Derived Integrity — never trust client-supplied values for server-owned state (FIASSE v1.0.4 S4.4.1.2)
- Request Surface Minimization — process only the named values you expect (FIASSE v1.0.4 S4.4.1.1)
- Observability: what must be logged or auditable (FIASSE v1.0.4 S3.2.1.4 + Accountability; Transparency S2.5)
- Least Astonishment — predictable behavior at trust boundaries and error paths (FIASSE v1.0.4 S2.6)
- Resilience or availability drivers (rate limits, timeouts, graceful and **secure** failure)
- Testability or modifiability mandates (e.g., centralizing crypto/auth in a dedicated module)
- Dependency stewardship — ongoing relationship with third-party code (FIASSE v1.0.4 S4.6)

### Step 5 — Convert into testable acceptance criteria

For each added or strengthened requirement, write at least one acceptance criterion that is:

- Behaviorally observable (a test or audit can confirm pass/fail)
- Specific about boundary conditions (failure modes, unauthorized actors, malformed input)
- Tied to a verifiable artifact (log line, response code, denied action)

Ambiguous "secure" or "robust" language is not acceptable here.

### Step 6 — Emit the enhanced PRD artifact

Produce these sections in order, using the exact templates below.

## ASVS Coverage Gap Pattern Table

Use these prompts to identify candidate requirements, not to assert that every listed safeguard is mandated verbatim by ASVS. Read the cited sections, select exact requirement IDs and levels, and distinguish product-policy choices (for example expiry and rate thresholds) from normative requirements.

| PRD trigger phrasing (what the feature *says*) | Almost-always-missing requirements | ASVS section | Tag |
|---|---|---|---|
| "User logs in with email and password" | Enumeration resistance (L3); common/breached-password screening; auth-event logging; brute-force controls | V6.3.8, V6.2.4, V6.2.12, V6.3.1, V16.3.1 | "Auth surface gaps" |
| "User resets/forgets password" | Enumeration resistance (L3); secure reset preserving MFA; unpredictable single-use tokens with documented lifetime/storage policy; rate limits; issuance/redemption logs | V6.3.8, V6.4.3, V2.4, V11.5, V16.3 | "Reset flow gaps" |
| "User uploads a file" | Type allowlist; content validation; size limits; safe filename/storage and download authorization | V5.1, V5.2, V5.3, V5.4, V2.2 | "Upload gaps" |
| "User can edit their profile" / "update settings" | Allowlisted mutable fields; owner/tenant checks; separate verified identity-change flow; protected audit logs | V8.2, V2.2, V16.3, V16.4 | "Mass-assignment gaps" |
| "Admin can do X" / "role-based access" | Server-side authorization; deny by default; record-level scoping; log denied decisions (all decisions for L3) | V8.2, V8.3, V16.3.2 | "Authz gap" |
| "Public API endpoint" / "third-party integration" | Per-client resource limits; authentication where required by access policy; response field minimization; contract validation | V2.4, V4.1, V6.3, V14.2, V2.2 | "API gaps" |
| "Send email/SMS to user" | Context-specific encoding; per-recipient/actor limits; abuse-loop handling; opt-out policy and logs | V2.4, V2.2, V1.2, V16.3 | "Outbound-message gaps" |
| "Search / filter / list with user-supplied parameters" | Parameter allowlist; pagination/resource caps; parameterized queries; tenant/owner scoping | V8.2, V2.2, V1.2, V2.4 | "Query-surface gaps" |
| "Webhook receiver" / "callback URL" | Sender authentication; signature covering body and replay fields; atomic replay rejection; idempotency; rate limits; logs (IP allowlist alone is not sender authentication) | V4.1, V2.3, V2.4, V11.4, V16.3 | "Webhook gaps" |
| "Save user file/document/note" | Server-derived ownership; size/content caps; HTML sanitization; audit policy | V8.2, V5.2, V2.2, V1.3, V16.3 | "Server-owned state gaps (Derived Integrity)" |
| "Export data" / "download report" | Authorization at export; rate limits; audit policy; data minimization | V8.2, V2.4, V16.3, V14.2 | "Export gaps" |
| "Background job processes user-submitted data" | Validation and owner/tenant scoping; job logs; bounded retries and secure failure | V2.2, V8.2, V16.3, V16.5 | "Async-path boundary gaps" |
| "Configuration / feature flag / admin setting" | Authenticated authorized changes; protected audit records; secret handling; safe defaults | V8.2, V16.3, V13.1, V13.3 | "Config-surface gaps" |
| "PII/PHI/financial data" mentioned anywhere | Data classification; encryption; retention/disposal and privacy policy; access logging | V14.1, V14.2, V11.3, V12.1, V16.3 | "Sensitive-data lifecycle gaps" |
| "Real-time" / "websocket" / "streaming" feature | Connection/message authorization; resource caps; back-pressure; timeouts; lifecycle logs | V4.4, V8.2, V2.4, V7.3, V16.3 | "Streaming gaps" |
| "AI/LLM-backed feature" | Untrusted-input/output handling; tool authorization; cost caps; redacted audit policy; supplement with separately versioned LLM guidance | V2.2, V1.2, V8.2, V2.4, V14.2, V16.3 | "LLM boundary gaps" |

When a feature triggers one of these patterns, read the cited sections and prefill the specific ASVS requirements you select (at the chosen level) as **Missing** in the coverage matrix unless the PRD explicitly addresses them — most of the time it doesn't. List product-policy safeguards from the table that no selected requirement mandates as recommendations, not as Missing ASVS coverage.

## Output Templates

### A. ASVS Level Decision

```markdown
## ASVS Level Decision

**Chosen Level**: [1 | 2 | 3]

**Rationale**: [2–4 sentences. Cover data sensitivity, user population, regulatory context, and material-impact reasoning. Note why lower levels are insufficient if Level > 1.]

**Feature-Level Escalations**: [List any features that need a higher level than baseline, with one-line justification, or "None".]
```

### B. Coverage Matrix

```markdown
## Feature ↔ ASVS Coverage Matrix

| Feature | ASVS Section | Requirement ID | Level | Coverage | PRD Change Needed |
|---------|--------------|----------------|-------|----------|-------------------|
| F-01    | V6.3         | 6.3.3          | 2     | Missing  | Specify MFA or combined single-factor mechanisms and documented exception safeguards |
| F-01    | V16.3        | 16.3.1         | 2     | Partial  | Specify logging of all authentication operations and factor metadata |
| F-02    | V2.4         | 2.4.1          | 2     | Covered  | PRD specifies anti-automation controls; implementation not assessed |
```

Aim for completeness over brevity here — every feature × every applicable requirement gets a row. Where the gap pattern table applies, include the named requirements it surfaces.

### C. Enhanced Feature Specifications

For each feature, emit exactly this shape:

```markdown
### Feature F-01: [Title]

**Actor**: [user role / system]
**Data**: [data classes touched]
**Trust Boundaries**: [boundaries crossed]

**ASVS Mapping**: V6.3.3, V16.3.1, ...

**Updated Requirements**:
- [Original requirement, kept or rewritten]
- [Newly added requirement from ASVS mapping]
- [Newly added requirement from ASVS mapping]

**Acceptance Criteria**:
- [Testable criterion tied to a requirement above]
- [Testable criterion tied to a requirement above]

**Securability Notes**: [Short paragraph — only material SSEM/FIASSE points for this feature. Do not enumerate all attributes.]
```

### D. Cross-Cutting Securability Requirements

Controls that span multiple features (centralized logging, secrets management, dependency policy, baseline TLS, error-handling standards). One bullet each, with the ASVS reference.

### E. Open Gaps and Assumptions

Anything you could not resolve from the input: missing system context, unclear data sensitivity, unstated user populations, deferred decisions. Be explicit so the team can close these before implementation.

## Worked Example (Mini)

**Input feature (from a PRD):**

> F-03: Users can reset their password by clicking "Forgot Password" and entering their email. The system emails a reset link.

This trips the "Reset flow gaps" pattern in the gap table — so the missing requirements are predictable.

**Enhanced output:**

```markdown
### Feature F-03: Password Reset via Email

**Actor**: Unauthenticated user (claiming an account)
**Data**: Email address (PII), password (credential), reset token
**Trust Boundaries**: browser → public API; API → email provider; API → credential store

**ASVS Mapping**: V6.4.3 (L2), V6.2.1 (L1), V6.2.4 (L1), V6.2.5 (L1), V6.2.12 (L2), V16.3.1 (L2), V16.4 (L2), V2.4.1 (L2), V2.2.1 (L1), V6.3.8 (L3 escalation)

**Updated Requirements**:
- User can request a password reset by entering an account email at `/reset`; the process preserves any enabled MFA (V6.4.3).
- The system returns equivalent responses for existing and nonexistent accounts (V6.3.8, explicitly adopted above the L2 baseline).
- Product policy: CSPRNG-generated high-entropy reset tokens are single-use, expire within 10 minutes, and are stored as hashes; this policy supports secure reset (V6.4.3) rather than quoting a password-security requirement.
- New passwords have at least 15 characters because the password is the only login factor (NIST SP 800-63B-4 requires 15 for single-factor passwords; ASVS V6.2.1 sets an 8-character floor and strongly recommends 15), no required character classes (V6.2.5), and common/breached-password screening (V6.2.4, V6.2.12).
- Authentication operations are logged (V16.3.1); product policy includes reset issuance/redemption and outcome with appropriate redaction and retention (V16.4).
- Reset requests are rate-limited per account and source IP (V2.4.1); thresholds below are product policy.
- Validate email input at the service boundary (V2.2.1); apply the account system's consistent identity-normalization rules, not transformations of the password.

**Acceptance Criteria**:
- Submitting a non-existent email returns the same response body, status code, and timing characteristics as a valid email (within tolerance).
- A reset token cannot be redeemed after 10 minutes or after first successful use; both cases produce a generic failure response and a logged `reset_token_invalid` event without the token value.
- More than 5 reset requests for the same email within 10 minutes are rejected with HTTP 429 and logged.
- Audit log lines for reset events are queryable by user ID and contain the fields above.

**Securability Notes**: This feature crosses an unauthenticated trust boundary (FIASSE v1.0.4 S4.3), so input handling and rate limiting are the load-bearing concerns. The reset token is server-owned state; never accept client-supplied token attributes beyond the opaque token itself (Derived Integrity, FIASSE v1.0.4 S4.4.1.2). Centralize token generation, hashing, and verification in a single module so the policy can evolve without touching call sites (Modifiability). All reset events must be observable in the audit pipeline so abuse patterns can be detected (Accountability + Observability, FIASSE v1.0.4 S3.2.1.4; Transparency S2.5).
```

This is the level of specificity the output should hit — concrete, testable, and traceable back to ASVS.

## Quality Checklist (run before emitting)

**Coverage**
- [ ] Every feature has an ID, actor, data classification, and trust-boundary list
- [ ] ASVS level is chosen and justified before per-feature mapping
- [ ] Every feature mapped against all applicable ASVS chapters at the chosen level
- [ ] Gap patterns from the table above were applied to every relevant feature
- [ ] Every Missing/Partial item produced a concrete PRD change

**Output discipline**
- [ ] Coverage matrix is present and includes change-needed column
- [ ] Each feature follows the exact output shape (Actor / Data / Trust Boundaries / ASVS Mapping / Updated Requirements / Acceptance Criteria / Securability Notes)
- [ ] Acceptance criteria are behaviorally testable, not aspirational
- [ ] Securability Notes are surgical — only material SSEM/FIASSE points, not exhaustive enumeration

**Traceability**
- [ ] Every added standard requirement cites a verified ASVS ID/level; additional product policies are labeled separately
- [ ] Cross-cutting requirements section captures shared controls
- [ ] Open gaps and assumptions are listed explicitly

## When in doubt

- Prefer adding a missing requirement over assuming coverage; mark it explicitly so reviewers see it.
- Prefer fewer, sharper ASVS references per feature over a long list that nobody will action.
- Prefer plain language in Securability Notes — these are read by product managers, not just security engineers.

## Reference Material

- Step-by-step runbook: [plays/prd-fiasse-asvs-enhancement.md](../../plays/prd-fiasse-asvs-enhancement.md)
- ASVS chapter index: `data/asvs/README.md`
- ASVS requirements (per chapter): `data/asvs/V*.md`
- FIASSE v1.0.4 foundational principles: `data/fiasse/S2.1.md`–`S2.6.md` (Transparency S2.5, Least Astonishment S2.6)
- FIASSE v1.0.4 SSEM attribute umbrellas: `data/fiasse/S3.2.1.md`–`S3.2.3.md`; leaf files (e.g. `S3.2.1.4.md` Observability) for attribute-specific guidance
- FIASSE v1.0.4 Boundary Control and Resilient Coding: `data/fiasse/S4.3.md`, `S4.4.md`, and the canonical-input-handling leaves `S4.4.1.md`, `S4.4.1.1.md`, `S4.4.1.2.md`
- FIASSE v1.0.4 Dependency Management and Stewardship: `data/fiasse/S4.5.md`, `S4.6.md`
