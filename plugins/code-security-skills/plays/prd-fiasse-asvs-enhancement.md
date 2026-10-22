# PRD FIASSE / ASVS Enhancement — Step-by-Step Runbook

The authoritative mapping, gap patterns and output templates live in `references/prd-securability-enhancement.md` (the bundled canonical skill). Read it before applying this sequence.

## Intent

Enhance PRDs, feature specs, user stories, or product briefs with explicit OWASP ASVS v5.0 coverage and FIASSE v1.0.4 / SSEM implementation guidance — **before** code is written.

The goal is to upgrade the requirements artifact so delivery teams build securable capabilities by design rather than retrofitting controls during/after implementation.

## Procedure

Use the detailed steps and completion checks in the authoritative procedure:

1. **Parse features** — normalize each feature with actor, data sensitivity, trust boundaries, and existing acceptance criteria.
2. **Choose ASVS level** — recommend or accept Level 1/2/3 per feature based on data sensitivity and exposure.
3. **Map features to ASVS chapters** — use `data/asvs/README.md` and the `when_to_use` frontmatter in `data/asvs/V*.md`.
4. **Apply FIASSE principles** — overlay SSEM attribute coverage (Maintainability, Trustworthiness, Reliability umbrellas plus Observability and Transparency).
5. **Add securability acceptance criteria** — testable, traceable to ASVS requirement IDs.
6. **Emit enhanced PRD** — preserve original structure; add a per-feature "Security Requirements" block.

## Output

Emit the procedure's ASVS Level Decision, Feature Coverage Matrix, Enhanced Feature Specifications, Cross-Cutting Requirements, and Open Gaps/Assumptions. Preserve existing functional intent; separate product policies from verified ASVS requirements and implemented-control evidence from PRD coverage.

## References

- Authoritative procedure and templates: `references/prd-securability-enhancement.md`
- OWASP ASVS v5.0 chapter index: `data/asvs/README.md`
- OWASP ASVS v5.0 chapters: `data/asvs/V*.md`
- FIASSE v1.0.4 foundational principles: `data/fiasse/S2.1.md`–`S2.6.md`
- FIASSE v1.0.4 SSEM attribute umbrellas: `data/fiasse/S3.2.1.md`–`S3.2.3.md`
