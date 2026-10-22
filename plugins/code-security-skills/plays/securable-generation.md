# Securable Generation — Full Loop Play

Follow the bundled skill references below when a peer skill is not separately installed; they are links to the canonical skill procedures, not independent copies to maintain.

## Intent

End-to-end securable code delivery loop: **PRD-enhance → generate → review → enhance → report**.

When activated (via `--full-loop`, "end-to-end securable", or an explicit reference), this play chains together three skills so a single user intent produces (1) a securability-enhanced requirements artifact, (2) generated code that satisfies those requirements, and (3) an SSEM scorecard validating the output.

In **Default Mode**, the `securability-engineering` skill alone handles single-shot code generation. This play is **only** for the opt-in full-loop flow.

## Procedure

Complete each stage before advancing; retain unmet requirements and unresolved review evidence in the final report.

1. **PRD enhancement** — follow `references/prd-securability-enhancement.md` to add explicit ASVS controls and SSEM acceptance criteria to the incoming feature/spec. Finish with the level decision and feature coverage matrix.
2. **Generation** — follow `references/securability-engineering.md` (Default Mode) with the enhanced PRD as input. Apply SSEM constraints and emit a Securability Notes block; do not recursively invoke Full Loop Mode.
3. **Review** — follow `references/securability-engineering-review.md` to score the generated code against the SSEM rubric and produce evidence-backed findings.
4. **Enhancement pass** — feed review findings back to `securability-engineering` for a remediation iteration. Bounded retries (default: 1 pass).
5. **Report** — emit a consolidated artifact: enhanced PRD + final code + SSEM scorecard + remediation diff.

## Output

Emit Requirements (enhanced PRD and ASVS matrix), Generated Code (changed files), SSEM Scorecard, and Remediation Notes (findings addressed, diff and remaining gaps). Report only authorized checks actually performed; unverified controls remain unassessed, not passed.

## References

- Generation procedure: `references/securability-engineering.md`
- Dependent procedures: `references/prd-securability-enhancement.md`, `references/securability-engineering-review.md`
- FIASSE v1.0.4: `data/fiasse/` (foundational principles + SSEM attributes)
- OWASP ASVS v5.0: `data/asvs/`
