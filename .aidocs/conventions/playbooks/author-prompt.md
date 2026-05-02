---
status: active
audience: agents
owner: ruslan
last_verified: 2026-05-02
applies_to: orchestrator dispatch to faion-sdd-executor-agent for tier-playbook authoring
---

# Tier-Playbook Author Prompt Template

Render this template per playbook by interpolating the variables in `{}`. The orchestrator passes the rendered prompt to a `faion-sdd-executor-agent` (model: sonnet; haiku for revision passes only) running with `isolation: worktree` and `run_in_background: true`.

---

## Prompt body

```
You are authoring a tier-playbook in the faion-network repo.

Slug: {slug}
Tier: {tier}
Group: {group}
Title: {title}
Catalog brief: {problem} → {solution_outline}
Persona: {persona}
Impact: {impact}
Effort: {effort}

## Read first (non-negotiable)

1. .aidocs/conventions/playbooks/playbook-spec.md — full spec (front-matter, 8 sections, citation rule, anti-patterns, inline template)
2. .aidocs/conventions/playbooks/AGENTS.md — entity boundary

## Allowed methodology citations

Citation tier ≤ playbook tier ({tier}). You MUST cite ≥1 methodology from these allowed paths:

{allowed_methodology_paths}

(Other knowledge paths are off-limits for this tier.)

## Deliverable

Create exactly:

skills/faion/playbooks/{tier}/{group}/{slug}/playbook.md

Optional companion files (only if the body would exceed 5k tokens otherwise):

- skills/faion/playbooks/{tier}/{group}/{slug}/checklist.md
- skills/faion/playbooks/{tier}/{group}/{slug}/templates.md
- skills/faion/playbooks/{tier}/{group}/{slug}/examples.md

Required structure (validator enforces):

- Front-matter: name (=slug), description (≤200 chars), tier ({tier}), group ({group}), status (active), owner (your handle), last_verified (today), version (1.0.0)
- 7 H2 sections in fixed order: Goal, Prerequisites, Steps, Verify, Troubleshooting, Next, References
- Steps use real commands/URLs (no foo/bar/example.com placeholders)
- Verify section runnable as one observable check
- Troubleshooting has ≥1 named pitfall (Symptom → Cause → Fix)
- References has ≥1 citation with playbook-specific rationale (≥10 chars, non-generic)

## Validate before commit

python3 scripts/validate-tier-playbook.py skills/faion/playbooks/{tier}/{group}/{slug}/playbook.md

Must exit 0. If it fails, fix the reported errors and re-run. Do not commit a failing playbook.

## Update indexes

1. Append a one-line entry under skills/faion/playbooks/{tier}/AGENTS.md group table (only if the group folder is new in this wave).
2. CHANGELOG.md — under `## [Unreleased]`, add a single line: `- add: tier-playbook {tier}/{group}/{slug}`.

## Commit

Single granular commit:

```
git add skills/faion/playbooks/{tier}/{group}/{slug}/ CHANGELOG.md skills/faion/playbooks/{tier}/AGENTS.md
git commit -m "add: tier-playbook {tier}/{group}/{slug}"
```

NO --no-verify. NO Co-Authored-By. NO emojis.

## Push under merge lock

flock /tmp/faion-network-merge.lock git push origin _temp_main:main

## Last-line marker

Print exactly one line at the very end of your response:

done={slug} commit=<short-sha>

The orchestrator parses this marker. Anything else printed after this line is ignored.

## Constraints

- Body ≤5k tokens.
- Action-leading verbs in step headers.
- No theory paragraphs in Steps (link to a knowledge methodology in References instead).
- Citation rationale must be playbook-specific (not "this methodology covers X").
- Use real domain names where helpful (mydomain.com, myapp). Mark genuinely-secret values as <your-secret> and explain in Prerequisites.
```

## Variables (orchestrator-supplied)

| Variable | Source |
|----------|--------|
| `slug`, `tier`, `group`, `title`, `problem`, `solution_outline`, `persona`, `impact`, `effort` | `catalog/priority-120.md` row |
| `allowed_methodology_paths` | `tier-manifest.json` → tiers ≤ `tier` → `knowledge_paths` |
| `repo_branch`, `repo_path` | orchestrator (faion-network = `_temp_main` → `main`) |

## Pool config (orchestrator side)

- Pool size: 5–8 parallel subagents
- Batch: 1–2 playbooks per dispatch
- Subagent: `faion-sdd-executor-agent`
- Model: `sonnet` (default), `haiku` for retries only — see `feedback_failed_retry_sonnet`
- Isolation: `worktree`
- Background: `run_in_background: true`
- Lock: `flock /tmp/faion-network-merge.lock` for push serialization
- Wake on completion via task-notification

## Failure handling

If validator exits non-zero:
1. Re-dispatch with sonnet (escalate from haiku) and a "fix the validator errors" wrapper prompt.
2. If second attempt fails, escalate to user (paused-loop).

If wave failure rate >10%, pause dispatch and triage: spec ambiguity → fix spec; prompt issue → fix this template; content issue → manual revision.
