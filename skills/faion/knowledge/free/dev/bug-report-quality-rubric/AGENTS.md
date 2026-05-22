---
slug: bug-report-quality-rubric
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a 0-100 scored, 8-field bug report rubric output that gates triage and forces actionable repro steps + severity/priority split.
content_id: "17f240734aed34db"
complexity: light
produces: rubric
est_tokens: 3600
tags: [qa, bug-report, rubric, triage]
---
# Bug Report Quality Rubric

## Summary

**One-sentence:** Scores an incoming bug report against an 8-dimension rubric (title, repro, env, expected/actual, severity, priority, evidence, AI-context) and emits a pass/block decision with field-level fixes.

**One-paragraph:** A bug filed without a clear repro path, an environment snapshot, expected-vs-actual, and severity-vs-priority splits drains developer time on triage rather than fix. This methodology produces a versioned `rubric` artefact: a score (0-100) per dimension, a binary `accept|block` verdict, and per-field repair instructions the reporter can act on. For AI features it adds dimensions for prompt id, model id, seed, and full conversation context. The rubric runs as a CI gate on the ticket-tracker side (GitHub Action / Linear webhook / Jira automation) and refuses tickets below a threshold until the reporter completes the missing fields.

**Ефективно для:**

- Гейтінг вхідних bug-репортів у QA-черзі: відсікає неповні тикети до того, як вони з'їдять час інженера.
- Тренування junior-QA: рубрика — це детермінований чек-лист "що має бути в репорті".
- AI-фічі (LLM-output, RAG): додаткові поля (prompt-id, model, seed) роблять баг відтворюваним за умови, що команда не контролює недетермінізм самостійно.
- Аудит accuracy/quality QA-процесу: можна historical-scanуй closed-as-not-reproducible тикети і побачити, скільки з них ловила би рубрика.

## Applies If (ALL must hold)

- Team receives ≥5 bug reports per week from non-engineers (PMs, customer support, end-users).
- Ticket tracker (GitHub Issues / Linear / Jira / Notion DB) supports custom fields or templates.
- A named QA owner exists who can enforce the rubric (no rubric without an enforcer).

## Skip If (ANY kills it)

- Team is ≤2 engineers and every bug becomes a Slack DM — overhead exceeds payoff.
- Bugs are mostly observability-tool generated (Sentry, Datadog) — those already carry full stack + environment; the rubric duplicates them.
- Regulated context (medical, aviation) where bug-tracking shape is fixed by an external standard (ISO 25010, IEC 62304) — defer to the standard.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Incoming bug report draft | Markdown / Issue body | Reporter (PM, support, user) |
| Tracker template definition | YAML (GitHub) / JSON (Linear) | Repo `.github/ISSUE_TEMPLATE/` |
| Severity/priority matrix | Markdown | Team's QA handbook |
| AI-feature inventory (if any) | YAML | Engineering directory listing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — runs at ticket intake, no upstream artefacts. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: repro-from-known-state, evidence-attached, sev-vs-pri-split, env-snapshot, ai-context-when-ai | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for rubric output: per-dimension score, verdict, field-level fixes | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: severity-conflated-with-priority, "doesn't work" titles, missing env, post-hoc repro | 800 |
| `content/05-examples.xml` | reference | Worked rubric application on a real LLM-output bug | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree: is-AI? known-repro? evidence? → accept/block | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `parse_incoming_report` | haiku | Field extraction; structured parsing of known template. |
| `score_against_rubric` | haiku | Deterministic scoring; pattern match per dimension. |
| `draft_repair_comment` | sonnet | Human-readable, context-aware repair guidance back to reporter. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bug-report-quality-rubric.json` | JSON Schema for the rubric output |
| `templates/bug-report-quality-rubric.md` | Markdown skeleton issue body the reporter fills in |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bug-report-quality-rubric.py` | Validate a rubric output JSON against the schema | After scoring, before posting verdict back to tracker |

## Related

- [[code-review]] — same artefact-gate pattern applied to PRs.
- [[code-coverage]] — rubric for tests instead of bug reports.

## Decision tree

See `content/06-decision-tree.xml`. The tree branches first on `is_ai_feature` — if true, AI-specific dimensions (prompt id, model id, seed) become mandatory before evidence checks. For non-AI bugs it falls back to the 6-dimension classical rubric. Leaves emit `accept`, `block-need-repro`, `block-need-evidence`, or `block-need-ai-context`, each referencing a rule in `01-core-rules.xml`.
