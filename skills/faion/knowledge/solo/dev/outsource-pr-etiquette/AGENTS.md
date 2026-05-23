---
slug: outsource-pr-etiquette
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Writes outsource-friendly pull requests with bounded scope, named reviewer, repro steps, screenshots, and a rollback plan so a timezone-shifted reviewer can decide without back-and-forth.
content_id: "0a0278c4c505fae9"
complexity: light
produces: checklist
est_tokens: 3400
tags: [pull-request, outsource, etiquette, code-review, communication]
---
# Outsource PR Etiquette

## Summary

**One-sentence:** Writes outsource-friendly pull requests with bounded scope, named reviewer, repro steps, screenshots, and a rollback plan so a timezone-shifted reviewer can decide without back-and-forth.

**One-paragraph:** Writes outsource-friendly pull requests with bounded scope, named reviewer, repro steps, screenshots, and a rollback plan so a timezone-shifted reviewer can decide without back-and-forth. Codifies the PR shape an outsource reviewer can land in one pass: ≤400 LOC diff, single intent, named reviewer, repro steps, before/after evidence, rollback plan. Decision tree, output contract, failure modes, and the decision tree live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Working with outsourced or external reviewers in a different timezone.
- Reviewer cannot ping the author synchronously to ask clarifying questions.
- Average review latency exceeds 24h and round-trips compound the delay.
- Output produces `checklist` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Working with outsourced or external reviewers in a different timezone.
- Reviewer cannot ping the author synchronously to ask clarifying questions.
- Average review latency exceeds 24h and round-trips compound the delay.

## Skip If (ANY kills it)

- Reviewer sits next to you and reviews synchronously — overhead doesn't pay back.
- Single-author repo with no reviewer at all — use a self-review checklist instead.
- PR is a one-line typo or trivial config bump where a templated note is overkill.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Linked issue/spec | URL | Jira/Linear/GitHub issue |
| Diff size baseline | int (LOC) | git diff --stat |
| Reviewer roster | list of handles | team CODEOWNERS |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[code-review-process]] | Underlying review etiquette this layers onto. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-pr-body` | sonnet | Compose summary, motivation, repro, rollback from the diff and linked issue. |
| `scrub-secrets` | haiku | Mechanical regex scrub of API keys / tokens before posting. |
| `name-reviewer` | haiku | Lookup CODEOWNERS by changed paths. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr_body.md` | Markdown skeleton for the artefact. |
| `templates/checklist.md` | Markdown checklist scaffolding the artefact items. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-outsource-pr-etiquette.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[code-review-process]]
- [[git-workflow]]
- [[pr-description-template]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the reviewer outsourced or timezone-shifted such that round-trips cost ≥1 working day?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
