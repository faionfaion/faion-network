<!--
purpose: ADR skeleton with score sheet + alternatives + consequences.
consumes: see AGENTS.md ## Prerequisites
produces: decision-record
depends-on: content/02-output-contract.xml schema for llm-decision-framework
token-budget-impact: ≤500 tokens to fill
-->

# ADR-XXX: LLM Architecture Decision — [Feature Name]

## Status

Proposed / Accepted / Superseded by ADR-YYY

## Context

Describe the task or feature:
- **Problem statement:** What needs to be solved?
- **Current approach:** What is in place now?
- **Why re-evaluating:** Accuracy gap / cost pressure / new requirement

## Options Evaluated

| Approach | Accuracy (eval) | Latency p50 | Monthly cost | Complexity |
|----------|-----------------|-------------|--------------|------------|
| Prompt engineering | | | | Low |
| RAG | | | | Medium |
| Fine-tuning | | | | High |
| RAFT | | | | Very High |

## Decision

**Selected:** [Approach]

**Rationale:**
- [Primary reason]
- [Secondary reason]
- [Constraints that ruled out alternatives]

## Evaluation Results

- **Dataset size:** N labeled examples
- **Eval metric:** [metric name + threshold]
- **Baseline (prompt only):** X%
- **Selected approach score:** Y%
- **Test set:** [description of test set]

## Consequences

**Positive:**
- [benefit 1]
- [benefit 2]

**Negative / Trade-offs:**
- [cost / complexity / maintenance burden]

## Re-evaluation Trigger

Review this decision if any of the following occur:
- Monthly API cost exceeds $[budget]
- Accuracy on eval set drops below [threshold]
- Task requirements change significantly
- New model releases change cost/quality trade-offs

**Scheduled review:** [date or milestone]
