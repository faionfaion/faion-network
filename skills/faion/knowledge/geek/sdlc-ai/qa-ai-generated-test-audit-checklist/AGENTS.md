---
slug: qa-ai-generated-test-audit-checklist
tier: solo
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 12-item audit checklist a reviewer walks on every AI-generated test PR — catches happy-path bias, structural-only assertions, missing failure cases, boundary gaps, over-mocking, and generic naming before merge.
content_id: "635122073df72050"
complexity: medium
produces: checklist
est_tokens: 3500
tags: [ai-generated-tests, audit, pr-review, qa, claude-code, copilot]
---
# AI-Generated Test PR Audit Checklist

## Summary

**One-sentence:** 12-item audit checklist a reviewer walks on every AI-generated test PR — catches happy-path bias, structural-only assertions, missing failure cases, boundary gaps, over-mocking, and generic naming before merge.

**One-paragraph:** AI-generated tests (Copilot, Cursor, Claude Code, Cody) exhibit a consistent bias profile: happy-path coverage, plausible-looking structural assertions, dodged failure cases, mocked everything, and generic test names that sound thorough. This methodology produces a 12-item checklist a human reviewer walks on every AI-test PR, with a pass/flag verdict and a one-line repair suggestion per item. Output is a filled checklist in the PR description plus go/no-go verdict tied to a behavioral-assertion floor.

**Ефективно для:**

- AI-generated test PR (Copilot, Cursor, Claude, Cody) перед merge.
- Solo dev, що ревьюить AI tests без QA-команди.
- Team з історією silent regressions від AI tests, що "pass-but-test-nothing".
- Merge gate, де reviewer може блокувати на quality grounds.

## Applies If (ALL must hold)

- PR includes tests authored or significantly assisted by an AI coding assistant.
- Reviewer is a human (not the AI self-reviewing).
- Merge gate exists where the reviewer can block on quality grounds.
- Team has 10–15 minutes per PR for the walk.

## Skip If (ANY kills it)

- PR has no test changes.
- AI assistance was minor (single-line completion) — overhead exceeds benefit.
- Throwaway prototype phase with no real users.
- Mature TDD-driven team where AI tests follow human-written test specs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PR template | Markdown with checklist section | platform |
| Filled checklist | YAML in PR description | reviewer |
| AC mapping | Markdown / tracker link | product / dev |
| Mutation kill-rate baseline | numeric % per file | CI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[mr-graph-vs-diff-reviewer]] | Graph-based reviewer catches structural-only assertions at scan time. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 700 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 600 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pre_review_lint_pass` | haiku | Automated detector pass on the diff. |
| `assertion_class_classification` | sonnet | Per-test bounded judgement. |
| `failure_case_gap_analysis` | sonnet | Per-AC judgement on missing failure cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-checklist.yaml` | The 12 items with pass / flag fields per item. |
| `templates/pr-description-section.md` | PR description snippet the reviewer fills in. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-ai-generated-test-audit-checklist.py` | Validate filled checklist artefact against schema + forbidden patterns. | At PR-ready gate |

## Related

- [[mr-graph-vs-diff-reviewer]]
- [[regression-eval-before-fix-rule]]
- [[mr-codemod-refactor-agent]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (PR touches tests? AI involvement detected? reviewer slot available?) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether to invoke the audit — the tree terminates either on the active rule or on `skip-this-methodology`.
