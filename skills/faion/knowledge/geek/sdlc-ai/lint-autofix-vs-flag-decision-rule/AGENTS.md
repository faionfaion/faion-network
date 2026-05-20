---
slug: lint-autofix-vs-flag-decision-rule
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A coding agent applies a linter or scanner autofix automatically if and only if all four of the following hold: (1) the fix is purely syntactic (formatter, import sort, type annotation, dead-code removal); (2) the tool ships an explicit --fix / --write / --autofix mechanism with a fix: block (ruff, biome, eslint --fix, semgrep --autofix where the rule has fix:, prettier); (3) the test suite still passes after the fix; (4) the diff is smaller than 50 lines or every change matches a single rule ID.
content_id: "463c3013642acb19"
tags: [lint, autofix, agent-policy, sast, security]
---
# Autofix-vs-Flag Decision Rule for Coding Agents

## Summary

**One-sentence:** A coding agent applies a linter or scanner autofix automatically if and only if all four of the following hold: (1) the fix is purely syntactic (formatter, import sort, type annotation, dead-code removal); (2) the tool ships an explicit --fix / --write / --autofix mechanism with a fix: block (ruff, biome, eslint --fix, semgrep --autofix where the rule has fix:, prettier); (3) the test suite still passes after the fix; (4) the diff is smaller than 50 lines or every change matches a single rule ID.

**One-paragraph:** A coding agent applies a linter or scanner autofix automatically if and only if all four of the following hold: (1) the fix is purely syntactic (formatter, import sort, type annotation, dead-code removal); (2) the tool ships an explicit --fix / --write / --autofix mechanism with a fix: block (ruff, biome, eslint --fix, semgrep --autofix where the rule has fix:, prettier); (3) the test suite still passes after the fix; (4) the diff is smaller than 50 lines or every change matches a single rule ID. Findings that fail any of those four — CodeQL alerts without a fix block, secrets, CVEs without a patch version, license conflicts, SonarQube cognitive-complexity hotspots — are FLAGGED, not auto-applied: the agent posts a PR suggestion or draft PR for human review and never lands the change in the same loop.

## Applies If (ALL must hold)

- Always — this is the meta-rule that wraps every other lint/SAST/SCA methodology in this knowledge base.
- Encoded in the agent's system prompt as a checklist: "for finding X, do conditions 1-4 hold? if yes autofix, else flag."
- Encoded in the CI agent's logic: a fix that fails any condition becomes a draft-PR comment, not a commit.

## Skip If (ANY kills it)

- Read-only audit runs (the agent is reporting, not fixing) — the gate is moot.
- One-shot bulk migrations (e.g., codemod sweeps) where the rule is "all-or-nothing" by design — encode the all-or-nothing exception explicitly, do not let the four-condition rule fight the migration.
- Stateful side effects outside the repository (rotating a secret, opening a JIRA ticket) — these are governed by approval-token and incident methodologies, not by autofix policy.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
