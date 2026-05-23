---
slug: ai-coding-of-qualitative-data-protocol
tier: geek
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Protocol for AI-assisted qualitative coding (codebook design, inter-coder agreement, audit trail) combining LLM proposal with human reconciliation to reach publishable kappa.
content_id: "dca5ac21121b5e3e"
complexity: deep
produces: playbook-step
est_tokens: 4300
tags: [qualitative-coding, codebook, kappa, inter-coder-agreement, ai-research]
---
# AI-Assisted Coding Protocol for Qualitative Data

## Summary

**One-sentence:** Protocol for AI-assisted qualitative coding (codebook design, inter-coder agreement, audit trail) combining LLM proposal with human reconciliation to reach publishable kappa.

**One-paragraph:** Protocol for AI-assisted qualitative coding (codebook design, inter-coder agreement, audit trail) combining LLM proposal with human reconciliation to reach publishable kappa. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Швидке coding of 20-200 транскриптів з кappa-validation > 0.7.
- Codebook design ітеративно: human seeds → AI expands → human prunes.
- Inter-coder agreement check: AI vs human reviewer на 10% sample.
- Audit trail: кожен код → segment_id + reviewer + codebook_version.

## Applies If (ALL must hold)

- Корпус 20-200 transcripts/segments; meaningful unit identifiable.
- Codebook v1 існує або готовий до итеративної побудови.
- Можливо залучити ≥1 додаткового coder для kappa-check.

## Skip If (ANY kills it)

- <20 segments — manual coding швидший і точніший.
- Codebook fluid без stable concepts — занадто рано для protocol.
- PII/sensitive content без redaction policy.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| segment corpus | JSONL {segment_id, text} | transcript pipeline |
| codebook v1 | YAML {code_id, definition, examples} | research lead |
| second-coder availability | yes/no flag + identifier | research ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-interview-analysis]] | single-interview analysis available |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure (input/action/output/decision-gate) | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule in 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| classify-input | sonnet | Light judgment; identifies branch in decision tree. |
| draft-output | sonnet | Drafting the output artefact per schema. |
| validate-output | haiku | Mechanical schema validation via script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/codebook.yaml` | Codebook skeleton |
| `templates/coded-segments.jsonl` | Sample coded segments with audit fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-coding-of-qualitative-data-protocol.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[ai-interview-analysis]]
- [[interview-note-synthesis-ai]]
- [[ai-assisted-persona-building]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Is corpus size >= 20 AND second coder available?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
