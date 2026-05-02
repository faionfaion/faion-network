# Feature 048: Tier Playbooks — Design

## Folder shape

```
skills/faion/playbooks/
├── CLAUDE.md           @AGENTS.md
├── AGENTS.md           orientation, ≤80 lines, lists tier roots + boundary vs workflow playbook
├── free/
│   ├── CLAUDE.md       @AGENTS.md
│   ├── AGENTS.md       free-tier index, ≤80 lines, lists groups
│   ├── tech-setup/
│   │   ├── AGENTS.md           group index, ≤80 lines
│   │   ├── github-account-and-first-repo/
│   │   │   ├── playbook.md          REQUIRED
│   │   │   ├── checklist.md         OPTIONAL
│   │   │   └── references.md        OPTIONAL
│   │   ├── ssh-key-setup-github/
│   │   │   └── playbook.md
│   │   └── ...
│   ├── hosting-infra/
│   ├── dev-fundamentals/
│   ├── business-discovery/
│   ├── mvp-essentials/
│   ├── marketing-fundamentals/
│   ├── cost-free-stack/
│   └── ops-basics/
├── solo/
│   └── (groups from catalog: sdd-workflow, frontend-launch, api-design, server-craft, automation, product-planning, product-ops, ui-design, content-marketing, seo-essentials, comms-stakeholder, launch-operations, solo-ops-finance)
├── pro/
│   └── (groups: client-engagement, delivery-ops, team-management, business-analysis, product-management, devops-cicd, infra-engineering, backend-systems, ux-research, growth-marketing, paid-acquisition, smm-cro, market-research, hr-ops)
└── geek/
    └── (groups: rag-pipelines, ai-agents, llm-integration, prompt-engineering, context-engineering, mcp-protocol, claude-code-skills, evaluation, ai-safety, ml-ops, fine-tuning, multimodal, cost-optimization, ai-product-positioning, ai-consultancy-ops)
```

Empty groups (those without TIER-1 selections in priority-120) are not created in phase 3 — only groups that hold ≥1 priority playbook get a folder. TIER-2 groups get folders when their playbooks are authored later.

## Playbook file shape

```
<slug>/
├── playbook.md           REQUIRED  the canonical body (8 sections + frontmatter)
├── checklist.md          OPTIONAL  printable step-by-step checklist
├── templates.md          OPTIONAL  copy-paste artifacts (configs, snippets)
├── examples.md           OPTIONAL  worked example with real names
└── references.md         OPTIONAL  separate citation file (otherwise inline in playbook.md ## References)
```

## Front-matter schema (required keys)

```yaml
---
name: <slug>
description: <one-line, ≤200 chars, action-leading>
tier: free|solo|pro|geek
group: <kebab>
status: active|draft|deprecated
owner: <handle>
last_verified: YYYY-MM-DD
version: <semver>
---
```

## Required H2 sections (in order)

1. `## Goal` — one paragraph; "after this playbook you will have <X>"
2. `## Prerequisites` — bullet list; assumed knowledge, accounts, tools, prior playbooks
3. `## Steps` — numbered list; action-leading verbs; real commands/snippets, no placeholders
4. `## Verify` — concrete check (curl, browser, log line, file exists); explicit pass/fail
5. `## Troubleshooting` — table or list; pitfall → diagnosis → fix
6. `## Next` — pointers to follow-up playbooks/methodologies
7. `## References` — methodology citations (validated paths) with playbook-specific rationale

## Citation rule

Inside `## References`:

```markdown
- [knowledge/<tier>/<group>/<skill>/<methodology>](path) — <why this methodology applies to this playbook>
```

Validator checks:
1. Path resolves under `skills/faion/knowledge/`
2. Citation tier ≤ playbook tier
3. Rationale present (the "—" segment is non-empty and ≥10 chars)
4. Rationale non-generic (no "explains X", "covers Y" without specificity)

## Boundary vs. workflow-bound playbook (in detail)

| Property | Workflow playbook | Tier playbook |
|----------|-------------------|---------------|
| Spec | `.aidocs/conventions/workflows/playbook-spec.md` | `.aidocs/conventions/playbooks/playbook-spec.md` (NEW) |
| Path | `workflows/<slug>/playbooks/<surface>.md` | `skills/faion/playbooks/<tier>/<group>/<slug>/` |
| Front-matter `applies_to` | workflow slug | tier (free/solo/pro/geek) |
| Front-matter `surface` | required (faion-net-fe, etc.) | n/a |
| Bound | one workflow + one surface | one tier + one topic |
| Required sections | 12 fixed (Goal, Surface choices, Methodologies, Repo and branch, ...) | 8 fixed (this doc) |
| Required `## Methodologies` table | yes (surface-specific) | embedded in `## References`, tier-bound |
| Granularity | per-surface adapter | per-task how-to |
| File name | `<surface>.md` (single file in workflow's playbooks/) | `playbook.md` (in own folder) |

The shared term "playbook" is intentional — both adapt underlying knowledge into actionable form. They differ in axis of adaptation: workflow playbooks adapt *along surface*, tier playbooks adapt *along topic and audience-tier*.

## Convention spec creation

Create `.aidocs/conventions/playbooks/`:

- `CLAUDE.md` — `@AGENTS.md`
- `AGENTS.md` — entity boundary, when to author, validation, related (≤80 lines)
- `playbook-spec.md` — full spec content:
  - Definition + boundary
  - Where playbooks live (slug regex, location)
  - Front-matter schema
  - 8 H2 sections (the canonical order)
  - Citation rule (tier ≤, path resolves, rationale specific)
  - Drift sentinels
  - Anti-patterns (≥10 named, e.g., "foo/bar examples", "command not in repo", "generic citation rationale", "tier exceeds")
  - Inline minimal template

Update `.aidocs/conventions/workflows/AGENTS.md` § "Boundary" to add a row pointing at the new spec.

## faion skill amendments

### `skills/faion/SKILL.md` — body append

Add new section after current explanation (no frontmatter change):

```markdown
## Playbooks

Beyond knowledge methodologies, the faion umbrella now hosts **tier playbooks** at `playbooks/<tier>/<group>/<slug>/playbook.md`. Playbooks are standalone how-to guides (e.g., "Buy a domain", "Build an MCP server"). Tier-gated on the same boundary as knowledge: free reads `playbooks/free/`; solo reads `free/ + solo/`; etc.

Spec: `.aidocs/conventions/playbooks/playbook-spec.md`
```

### `skills/faion/CLAUDE.md` — extend

Add playbooks tree parallel to existing knowledge tree. Append to "How to Use" section a row noting the tier inheritance is identical.

### `skills/CLAUDE.md` — index row

Append to skills directory listing:

```markdown
| `faion/playbooks/` | Standalone how-to guides, tier-gated. Parallel to `faion/knowledge/`. |
```

### `skills/tier-manifest.json` — extend each tier

```json
"free": {
  ...existing keys...,
  "playbook_root": "faion/playbooks/free",
  "playbook_paths": [
    "faion/playbooks/free/tech-setup",
    "faion/playbooks/free/hosting-infra",
    "..."
  ]
}
```

Same shape for solo, pro, geek.

## Validator script

`scripts/validate-tier-playbook.py`:

```python
# pseudocode
def validate(playbook_md_path):
    fm = parse_frontmatter(playbook_md_path)
    require_keys(fm, ["name", "description", "tier", "group", "status", "owner", "last_verified", "version"])
    sections = parse_h2_sections(playbook_md_path)
    require_order(sections, ["Goal", "Prerequisites", "Steps", "Verify", "Troubleshooting", "Next", "References"])
    refs = parse_references(sections["References"])
    for ref in refs:
        assert path_exists(f"skills/{ref.path}")
        assert tier_order(ref.tier) <= tier_order(fm["tier"])
        assert len(ref.rationale) >= 10
        assert not is_generic(ref.rationale)
    assert re.match(r"^[a-z][a-z0-9-]{2,40}$", fm["name"])
    return 0  # or list of errors
```

Implementation language: Python (path/JSON/YAML manipulation native; tier-manifest.json drives tier ordering).

CI integration: optional pre-commit hook + manual `python3 scripts/validate-tier-playbook.py skills/faion/playbooks/**/playbook.md`.

## Subagent prompt template (phase 3 deliverable)

`prompts/playbook-author-prompt.md` — to be created in phase 3. Template variables:
- `{tier}`, `{group}`, `{slug}`
- `{problem}`, `{solution_outline}`, `{persona}`, `{impact}`, `{effort}` (from catalog row)
- `{allowed_methodologies}` (path list filtered by tier)
- `{repo_context}` (branch, working dir)

Subagent contract: produce `playbook.md` matching spec, optionally companion files, self-validate, commit, emit last-line marker `done=<slug> commit=<sha>`.

## Open questions / decisions deferred

| Question | Default | Defer to |
|----------|---------|----------|
| Should `/faion` retrieval index playbooks alongside methodologies? | NO for v1 | Future feature |
| Should each group folder have its own AGENTS.md? | YES, ≤80 lines | Phase 3 |
| Should playbooks have versioning + changelog like methodologies? | YES, semver in front-matter | This feature |
| Should public site render playbooks? | NO | Separate FE feature |
| Translation strategy? | Out of scope | Future feature |

## Decisions log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-02 | Use `tier-playbook` as the entity name (vs. "guide", "runbook") | Aligns with industry SRE/PagerDuty usage; "playbook" already in repo vocabulary; namespace collision with workflow playbook resolved by location boundary |
| 2026-05-02 | Each playbook in own folder, not single-file | Allows companion files (checklist, templates, examples) without polluting parent group dir |
| 2026-05-02 | 8 H2 sections fixed (vs. variable) | Validator simplicity + cross-playbook navigability for users |
| 2026-05-02 | Citation rule: tier ≤ + rationale specific | Mirrors workflow-playbook spec; prevents "free playbook cites geek methodology" leakage |
| 2026-05-02 | TIER-2 catalog (280) deferred to future feature | Scope discipline; first wave proves the entity |
