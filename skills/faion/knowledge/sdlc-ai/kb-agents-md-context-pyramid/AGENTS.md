# AGENTS.md Context Pyramid

## Summary

**One-sentence:** Project AGENTS.md follow a 4-tier context pyramid: 20-line root, per-directory leaves, .agents/ deep-dives, .aidocs/ SDD lifecycle — agents load only relevant tiers.

**One-paragraph:** Project context for AI agents tends toward two failure modes: too little (agent has no anchor and hallucinates) or too much (every read loads 50KB of context, burning budget). The Context Pyramid solves both: a 4-tier scheme where the root AGENTS.md is ≤80 lines and lives at the project root, every directory with logic has its own AGENTS.md (≤80 lines), deep references live in `.agents/<topic>.md` loaded only on demand, and lifecycle docs live in `.aidocs/`. Output is the AGENTS.md tree + an audit of compliance per directory.

**Ефективно для:**

- Multi-directory project with ≥10 directories containing logic.
- AI agents (Claude Code, Cursor, Copilot) work in the repo and load context per task.
- Team values onboarding speed for both humans and agents.

## Applies If (ALL must hold)

- Multi-directory project with ≥10 directories containing logic.
- AI agents (Claude Code, Cursor, Copilot) work in the repo and load context per task.
- Team values onboarding speed for both humans and agents.

## Skip If (ANY kills it)

- Single-file or single-directory project — pyramid overhead exceeds benefit.
- Team uses a different convention (e.g. `CLAUDE.md` only) and won't migrate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo file tree | files | Current git HEAD |
| AGENTS.md template | md | Repo at `.faion/AGENTS-TEMPLATE.md` |
| Audit script | py | Repo at `scripts/audit-agents-md.py` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-kb-agents-md-context-pyramid` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/AGENTS.md.template` | Per-directory AGENTS.md skeleton |
| `templates/CLAUDE.md.template` | Claude Code pointer skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-kb-agents-md-context-pyramid.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]
- [[ci-eval-gate-config]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
