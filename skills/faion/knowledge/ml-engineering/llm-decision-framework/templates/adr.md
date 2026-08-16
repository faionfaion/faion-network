<!--

purpose: ADR skeleton with score sheet + alternatives + consequences.
consumes: see AGENTS.md ## Prerequisites
produces: decision-record
depends-on: content/02-output-contract.xml schema for llm-decision-framework
token-budget-impact: ≤500 tokens to fill
-->



# ADR-<adr_number>: LLM Architecture Decision — <feature_name>

## Status

Proposed / Accepted / Superseded by ADR-YYY

## Context

- **Problem statement:** <problem_statement>
- **Current approach:** [What is in place now]
- **Why re-evaluating:** <why_re_evaluating>

## Options Evaluated

| Approach | Accuracy (eval) | Latency p50 | Monthly cost | Complexity |
|----------|-----------------|-------------|--------------|------------|
| Prompt engineering | | | | Low |
| RAG | | | | Medium |
| Fine-tuning | | | | High |
| RAFT | | | | Very High |

## Decision

**Selected:** <selected_approach>

**Rationale:**
- <primary_reason>
- <secondary_reason>
- [Constraints that ruled out alternatives]

## Evaluation Results

- **Dataset size:** <dataset_size> labeled examples
- **Eval metric:** <eval_metric>
- **Baseline (prompt only):** <x>
- **Selected approach score:** <y>
- **Test set:** [description of test set]

## Consequences

**Positive:**
- <benefit_1>
- <benefit_2>

**Negative / Trade-offs:**
- [cost / complexity / maintenance burden]

## Re-evaluation Trigger

Review this decision if any of the following occur:
- Monthly API cost exceeds <cost_ceiling>
- Accuracy on the eval set drops below the <eval_metric> threshold
- Task requirements change significantly
- New model releases change the cost/quality trade-off

**Scheduled review:** <scheduled_review>
