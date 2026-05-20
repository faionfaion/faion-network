---
slug: ai-pairing-decision-tree
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Decision tree that decides per task whether to defer to the AI agent, co-drive, or override it before changes land.
content_id: "8f08362a48dafb60"
tags: [ai-pairing-decision-tree, dev, solo]
---
# Ai Pairing Decision Tree

## Summary

**One-sentence:** Decision tree that decides per task whether to defer to the AI agent, co-drive, or override it before changes land.

**One-paragraph:** Solo devs spend 60-80% of coding time with an AI agent (Cursor/Claude Code/aider) but have no explicit rubric for WHEN the agent is allowed to drive vs when the human must take the wheel. This methodology gives a 6-axis scoring tree (reversibility, blast radius, novelty, test coverage, regulatory exposure, fatigue) that maps to one of four modes: AGENT-DRIVES, AGENT-DRAFTS, AGENT-ASSISTS, HUMAN-ONLY. Mechanism: assign each axis 0-3, sum, route via threshold table. Primary output: mode decision + rationale + override-trigger conditions logged into the PR description.

## Applies If (ALL must hold)

- task_type ∈ {code_change, refactor, infra_change, schema_change}
- AI agent integrated into the dev loop (Cursor / Claude Code / aider / Windsurf)
- Repo has at least one CI gate (lint / typecheck / tests)
- Solo or pair workflow — no separate code reviewer immediately downstream

## Skip If (ANY kills it)

- Pure pairing with another human — human review supersedes
- Greenfield prototype with no production users — speed > safety
- Compliance-bound change (PCI, HIPAA, GDPR deletion) — always HUMAN-ONLY

## Prerequisites

- AI agent available with repo context loaded
- Reversibility classification known for the change (revert-safe vs not)
- Last 30-day defect log available to estimate novelty

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer/code-review-self` | consumes the self-review checklist as input |
| `solo/dev/software-developer/pre-commit-hooks` | depends on baseline CI gates being green |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-six-axes, r2-fatigue-veto, r3-threshold-table, r4-override-trigger, r5-pr-record | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score_axes` | haiku | Template fill with bounded 0-3 ranges |
| `propose_mode` | haiku | Threshold lookup; no judgment |
| `draft_override_triggers` | sonnet | Need to read change diff and write specific signals |

## Templates

| File | Purpose |
|------|---------|
| `templates/pairing-mode.json` | JSON schema for the rubric block |
| `templates/pr-pairing-block.md` | Markdown snippet pasted into PR description |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pairing-block.py` | Enforce the rubric appears in PR description | Pre-merge CI check |

## Related

- parent skill: `solo/dev/software-developer/`
- peer methodology: `code-review-self`
- external: [Cursor docs](https://cursor.sh/docs) · [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code)
