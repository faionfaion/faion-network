---
slug: mr-codemod-refactor-agent
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Cross-cutting refactors (Angular X→Y, SDK X→Y, rename User.id → User.uid) MUST go through a codemod (jscodeshift / ast-grep / comby / Roslyn refactor) the agent authors first; hand-edit is reserved for the residue.
content_id: "fb6ef0bde15b5f55"
complexity: deep
produces: playbook-step
est_tokens: 4200
tags: [codemod, refactor, ast, multi-agent, pull-request]
---
# Codemod-First Refactor Agent

## Summary

**One-sentence:** Cross-cutting refactors (Angular X→Y, SDK X→Y, rename User.id → User.uid) MUST go through a codemod (jscodeshift / ast-grep / comby / Roslyn refactor) the agent authors first; hand-edit is reserved for the residue.

**One-paragraph:** Codemod-First Refactor Agent produces a playbook-step artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Cross-cutting rename / signature-change spanning > 20 files.
- Framework / SDK upgrade with known codemod path.
- Multi-language repo where similar refactors recur.
- Risky refactor that needs deterministic, reviewable transform.

## Applies If (ALL must hold)

- Refactor touches > 20 call sites.
- An AST tool exists for the language (jscodeshift, ts-morph, ast-grep, comby, Roslyn).
- Refactor is mechanically describable as a transform.
- Team has CI to run tests after the codemod.

## Skip If (ANY kills it)

- Refactor < 5 files — hand-edit is faster.
- No AST tool for the language (template files only).
- Refactor requires deep semantic judgement per site — codemod can't capture.
- Repo lacks tests — codemod risk too high.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| AST tool | jscodeshift / ts-morph / ast-grep / comby / Roslyn | platform |
| Codemod script home | scripts/codemods/ | lead |
| Test suite | fast, green baseline | team |
| Multi-agent setup | transform-author + reviewer agents | agent ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-autofix-vs-flag-decision-rule]] | Sibling policy on auto-application |
| [[mr-graph-vs-diff-reviewer]] | Code review against codemod output |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `transform_design` | opus | Codemod author. |
| `transform_apply_and_test` | sonnet | Apply + run focused tests. |
| `residue_handle` | sonnet | Per-site hand-edit for un-codemod-able cases. |
| `review_and_pr` | opus | Final review + PR open. |

## Templates

| File | Purpose |
|------|---------|
| `templates/codemod.ts` | jscodeshift codemod skeleton. |
| `templates/codemod-pr.md` | PR body template documenting the codemod. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-codemod-refactor-agent.py` | Validate the playbook-step artefact. | pre-merge of codemod step |

## Related

- [[mr-graph-vs-diff-reviewer]]
- [[lint-autofix-vs-flag-decision-rule]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
