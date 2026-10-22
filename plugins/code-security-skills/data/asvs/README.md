# ASVS 5.0 Reference Data

80 structured ASVS 5.0 section files sourced from the [OWASP Agent Skills Project](https://github.com/eoftedal/owasp-agent-skills-project) by Erlend Oftedal.

## Source & License

These files are from `references/ASVS/` in the OWASP Agent Skills Project. OWASP ASVS is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

Routing and requirement IDs are verified against [OWASP ASVS v5.0.0](https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en). Use that tagged standard for normative text and levels; the index is navigation, not a replacement for requirements.

## File Format

Each file has YAML frontmatter with:

```yaml
---
title: "V6.2 Password Security"
asvs_chapter: "V6.2"
when_to_use:                          # Task-matching triggers
  - implementing password-based login
  - storing or verifying user passwords
threats:                              # Relevant threat categories
  - password cracking via weak hashing
  - credential stuffing
summary: "Requirements for securely handling user passwords."
---
```

Followed by the ASVS section content with requirements in a table:

```
| # | Description | Level |
| 6.2.1 | Verify that... | 1 |
```

Level indicates ASVS assurance level (1 = baseline, 2 = standard, 3 = advanced).

## Usage in Skills

### Code Review (`/code-review-security`)

When a finding maps to an ASVS section, reference the specific requirement:

```markdown
- **OWASP Ref**: ASVS V6.2.1
```

### Task-Based Lookup

Use the `when_to_use` frontmatter to match tasks to relevant ASVS sections. For example, if reviewing code that handles file uploads, check:
- `V5.1` — File Handling Documentation
- `V5.2` — File Upload and Content
- `V5.3` — File Storage

## Chapter Index

| Chapter | Topic | Sections |
|---------|-------|----------|
| V1 | Encoding and Sanitization | V1.1-V1.5 |
| V2 | Validation and Business Logic | V2.1-V2.4 |
| V3 | Web Frontend Security | V3.1-V3.7 |
| V4 | API and Web Service | V4.1-V4.4 |
| V5 | File Handling | V5.1-V5.4 |
| V6 | Authentication | V6.1-V6.8 |
| V7 | Session Management | V7.1-V7.6 |
| V8 | Authorization | V8.1-V8.4 |
| V9 | Self-contained Tokens | V9.1-V9.2 |
| V10 | OAuth and OIDC | V10.1-V10.7 |
| V11 | Cryptography | V11.1-V11.7 |
| V12 | Secure Communication | V12.1-V12.3 |
| V13 | Configuration | V13.1-V13.4 |
| V14 | Data Protection | V14.1-V14.3 |
| V15 | Secure Coding and Architecture | V15.1-V15.4 |
| V16 | Security Logging and Error Handling | V16.1-V16.5 |
| V17 | WebRTC | V17.1-V17.3 |

## Updating

To refresh from upstream:

```bash
cd /tmp && git clone --depth 1 https://github.com/eoftedal/owasp-agent-skills-project.git
cp /tmp/owasp-agent-skills-project/references/ASVS/*.md data/asvs/
```

Before committing a refresh, re-verify every requirement row (ID, text and level) against the tagged [OWASP ASVS v5.0.0](https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en) chapter files, and re-check the chapter index above. The upstream mirror is a convenience copy, not the normative source; if a row differs, keep the tagged text. If upstream publishes a newer ASVS tag, update the version references in the plays and skills that cite ASVS IDs in the same change.
