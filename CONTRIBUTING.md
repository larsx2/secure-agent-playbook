# Contributing to agent-security-playbook

Thanks for your interest in contributing to the OWASP Secure Agent Playbook. This guide covers how to add new plays, skills, and reference data.

## Ways to Contribute

- **New plays** — Add security procedures for uncovered vulnerability classes or standards
- **New skills** — Create the invocation layer for existing or new plays
- **New agents** — Add autonomous specialists that orchestrate skills for focused assessments
- **Reference data** — Add or update OWASP datasets in `plugins/<group>/data/` (bundled with a plugin) or `data/` (research datasets no skill uses yet)
- **Improvements** — Enhance existing plays with better checklists, examples, or tool coverage
- **Bug reports** — File issues for inaccurate findings, broken references, or missing coverage

## Adding a New Play

Plays live in the `plays/` folder of the plugin whose skills use them, so they ship with the marketplace install:

| Plugin | Plays folder | Focus |
|--------|--------------|-------|
| `code-security-skills` | `plugins/code-security-skills/plays/` | Code review, dependency audit, secrets, API, web, mobile, IaC, securability |
| `ai-security-skills` | `plugins/ai-security-skills/plays/` | Agent security, LLM risks, prompt injection, MCP review, AISVS verification, threat modeling |

Name the play after its task (e.g. `mcp-server-review.md`). Every template or data file a play or skill cites must live inside the same plugin folder, because files outside it are not installed.

A good play should:

1. **Solve one well-defined security task** — "Scan dependencies for CVEs" not "do a full security audit"
2. **Include trigger conditions** — When should this play run? What inputs does it need?
3. **Follow a structured procedure** — Numbered steps with clear decision criteria
4. **Produce findings using the standard format** — See `plugins/<group>/templates/finding.md`
5. **Reference OWASP standards** — Map findings to CWE, ASVS, WSTG, or relevant Top 10
6. **Prefer existing tools** — Use semgrep, trivy, osv-scanner, trufflehog, etc. over reimplementing detection logic

## Adding a New Skill

Skills are the invocation layer that wraps plays for Claude Code plugin installation.

1. Decide which plugin group your skill belongs to (see groups below)
2. Create a new directory under `plugins/<group>/skills/` with your skill name
3. Add a `SKILL.md` file following `template/SKILL.md.example` (the template itself is not an installable skill). Its frontmatter needs a `name`, a `description` that says when to use the skill, and `license: CC-BY-4.0`
4. Reference the corresponding play with a skill-root path (`plays/<play>.md`). Use explicit `plays/`, `templates/`, `data/<dataset>/` and `references/<peer-skill>.md` pointers for bundled dependencies. Markdown links inside plays/templates should be relative to those documents.
5. Don't add an `allowed-tools` line that pre-approves `Bash`, `WebFetch`, or `Agent`. These skills read untrusted code and content, and pre-approval removes the permission prompt that would catch an injected command

Skills are auto-discovered from `plugins/<group>/skills/` — no manifest registration step needed.

### Standalone and Release Packaging

Canonical content stays in each plugin's `plays/`, `templates/`, `data/` and `skills/*/SKILL.md`. After changing dependencies, run `python3 scripts/package_skills.py --sync` and commit the generated relative resource symlinks inside the skill directories (and plugin `references/` for peer procedures). Do not edit through these links or maintain copied text. The same transitive dependency graph builds release ZIPs; unknown local dependencies fail rather than being silently omitted. MASTG bundles MASVS-linked tests and their locally available transitive test references; upstream-only entities remain explicit online lookups.

Validation from the repository root (use an isolated virtual environment with `python3 -m pip install -r scripts/requirements.txt` for the existing extractor tests; the packager itself uses only Python's standard library):

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
scripts/package_skills.sh
```

Each release archive must remain at or below 200 files. Test actual CLI copying after layout changes, not just archive contents, using an isolated temporary HOME/project (never your normal agent configuration):

```sh
repo="$PWD"
smoke="$(mktemp -d)"
mkdir -p "$smoke/home" "$smoke/project"
(cd "$smoke/project" && HOME="$smoke/home" XDG_CONFIG_HOME="$smoke/home/.config" \
  npm_config_cache="$smoke/npm-cache" npx --yes skills add "$repo" \
  --skill '*' --agent claude-code --copy --yes)
```

Inspect each installed skill's procedures, templates, data and peer-reference closure against the source; confirm that no installed link depends on the source checkout. This verifies packaging, not the effectiveness of security findings. Standalone installs do not include plugin agents/orchestration. If an external reference cannot be fetched, report the missing evidence instead of inventing a mapping.

**Plugin groups:**
- `code-security-skills` — Code, infrastructure, and dependency analysis
- `ai-security-skills` — AI/agent-specific security assessment

## Adding a New Agent

Agents are autonomous specialists that invoke one or more skills to perform focused security assessments.

1. Decide which plugin the agent belongs to based on the skills it invokes
2. Create a new `.md` file in `plugins/<group>/agents/` named after your agent (e.g., `plugins/code-security-skills/agents/my-agent.md`)
3. Use YAML frontmatter with required fields: `name`, `description`, `tools`, `model`, `skills`
4. Optionally add `isolation: worktree` so the agent works on an isolated copy of the repo (recommended for agents that may run in parallel as part of a team)
5. The system prompt should describe the agent's approach, which skills to invoke and when, and the expected output format

Agents are auto-discovered from `plugins/<group>/agents/` — no manifest registration step needed.

**Note:** Plugin agents cannot use `hooks`, `mcpServers`, or `permissionMode` fields for security reasons.

See existing agents in `plugins/code-security-skills/agents/` and `plugins/ai-security-skills/agents/` for examples.

## Finding Format

All findings must use the structure defined in `plugins/<group>/templates/finding.md`:

```markdown
### [SEVERITY] Title

- **CWE**: CWE-XXX
- **CVE**: CVE-YYYY-NNNNN (if applicable)
- **OpenCRE**: [CRE-ID](https://www.opencre.org/cre/CRE-ID) — requirement name
- **OWASP Ref**: Top 10 A01, ASVS V#.#.#, LLM01, etc.
- **Location**: file_path:line_number
- **Impact**: What an attacker can achieve
- **Evidence**: Code snippet, command output, or proof-of-concept
- **Remediation**: Specific fix with code example
- **Confidence**: HIGH | MEDIUM | LOW
```

Resolve OpenCRE links via the API: `GET https://www.opencre.org/rest/v1/standard/CWE/sectionid/{cwe-number}`

Common mappings are pre-populated in `data/opencre/README.md`.

## Pull Request Guidelines

- One play or skill per PR (unless tightly coupled)
- Include a clear description of what the play/skill covers and why it's needed
- If adding a skill, ensure it lives under the correct `plugins/<group>/skills/` directory, and update the README skills table and skill count
- Test your play against a real or deliberately-vulnerable target where possible

## License

By contributing, you agree that your contributions will be licensed under the same [CC-BY-4.0](LICENSE.md) license as the rest of the project.
