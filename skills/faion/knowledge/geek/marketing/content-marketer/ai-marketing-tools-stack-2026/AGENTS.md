---
slug: ai-marketing-tools-stack-2026
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Decision record curating an AI marketing tools stack across GEO/AEO, content, SEO, ads, and workflow automation, with selection criteria and integration constraints."
content_id: "96d1d96155290638"
complexity: medium
produces: decision-record
est_tokens: 2900
tags: [marketing-tools, stack-design, ai-search, automation, marketing, geek]
---

# AI Marketing Tools Stack 2026

## Summary

**One-sentence:** Decision record curating an AI marketing tools stack across GEO/AEO, content, SEO, ads, and workflow automation, with selection criteria and integration constraints.

**One-paragraph:** Tool sprawl is the 2026 marketing failure mode. This methodology curates the stack into five buckets (GEO/AEO optimisation, content creation, SEO optimisation, ad optimisation, workflow automation) and emits a decision record per tool: function bucket, integrates-with list, automates-handoff yes/no, management overhead score, monthly cost, contingency. Output is the record finance and the team agree on before procurement.

**Ефективно для:** marketing teams evaluating new AI tools quarterly; founders consolidating overlapping subscriptions; agencies standardising their client stack.

## Applies If (ALL must hold)

- Evaluating ≥3 AI tool candidates for the same function
- Existing stack already has overlap or unclear ownership
- Budget review or procurement decision is upcoming
- Stack is expected to integrate with at least one existing system (CRM, analytics, CMS)

## Skip If (ANY kills it)

- Single-tool decision with no overlap risk — overkill
- Budget is severely constrained — pick one function and iterate
- Marketing workflows undefined — tools amplify process, do not replace it
- Engineering or product workflow — this stack is marketing-specific

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current stack inventory with owners + monthly cost | CSV / sheet | ops |
| Function bucket the candidate fills | Markdown note | RFP / brief |
| Integration target list (CRM, analytics, CMS) | YAML | engineering |
| Trial access or vendor demo notes | Markdown | vendor management |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/marketing/content-marketer` | parent role skill |
| [[ai-content-strategy]] | consumer of the content-creation slot in the stack |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect_vendor_specs` | haiku | Mechanical extraction across vendor docs |
| `score_candidate` | sonnet | Bounded scoring across integration / overhead / cost |
| `write_decision_record` | opus | Synthesised rationale for procurement |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-evaluation.md` | Per-tool evaluation skeleton with function bucket and scoring axes |
| `templates/ai-marketing-tools-stack-2026.json` | JSON schema for the decision record |
| `templates/_smoke-test.md` | Minimum-viable filled evaluation |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-marketing-tools-stack-2026.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- [[ai-content-strategy]]
- [[anti-slop-rubric]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether ai-marketing-tools-stack-2026 applies: root question — "Are ≥3 AI tool candidates being evaluated for the same function bucket?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-function-bucket, r2-integration-required, r3-handoff-automation, r4-management-overhead, r5-versioned-record, r6-contingency-named.
