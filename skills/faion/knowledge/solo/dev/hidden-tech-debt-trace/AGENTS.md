---
slug: hidden-tech-debt-trace
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Hidden-tech-debt report: catalogue + scan recipes for AI-era patterns (silent-skip tests, hallucinated abstractions, mock-only coverage, copy-paste-via-LLM).
content_id: "d8ffa7837b692237"
complexity: medium
produces: report
est_tokens: 4900
tags: [tech-debt, ai-era, code-quality, audit, dev]
---
# Hidden Tech Debt Trace

## Summary

**One-sentence:** Hidden-tech-debt report: catalogue + scan recipes for AI-era patterns (silent-skip tests, hallucinated abstractions, mock-only coverage, copy-paste-via-LLM).

**One-paragraph:** Hidden-tech-debt report: catalogue + scan recipes for AI-era patterns (silent-skip tests, hallucinated abstractions, mock-only coverage, copy-paste-via-LLM). Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script `scripts/validate-hidden-tech-debt-trace.py` enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- Hidden Tech Debt Trace — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `hidden-tech-debt-trace` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Codebase has accepted AI-generated changes over the last 3+ months without a debt audit.
- Test suite is showing green but defect rate in production has not dropped.
- Refactor or hand-off is planned and trust-in-tests must be re-established.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Codebase is < 1 month old — audit cost > finding rate.
- No AI-generated code in tree — generic tech-debt methodology applies instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[library-evaluation-rubric]] | Workflow context: related methodology in the same family |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/05-examples.xml` | essential | Worked end-to-end example anchored to the output contract | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-hidden-tech-debt-trace-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-hidden-tech-debt-trace.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hidden-tech-debt-trace.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[library-evaluation-rubric]]
- [[migration-impact-mapping]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (AI-change density, test trust, audit horizon) to full-scan / spot-scan / defer. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
