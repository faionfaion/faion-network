<!--
purpose: ADR skeleton with score sheet + alternatives + consequences.
consumes: see AGENTS.md ## Prerequisites
produces: decision-record
depends-on: content/02-output-contract.xml schema for llm-decision-framework
token-budget-impact: ≤500 tokens to fill
variables:
  - name: adr_number
    type: string
    required: true
    description: Sequence number for this ADR, zero-padded to three digits. Next free number in the decision log; a reused number silently overwrites the reasoning somebody is relying on.
  - name: feature_name
    type: string
    required: true
    description: The feature this decision serves, as product names it. One feature per record - "our LLM strategy" is a category, not a decision, and cannot be superseded cleanly.
  - name: problem_statement
    type: text
    required: true
    description: What has to be solved, stated without naming a technique. If the sentence already contains "RAG" or "fine-tune" you have written the answer and are now shopping for evidence.
  - name: selected_approach
    type: enum
    required: true
    options: [prompt-engineering, rag, fine-tuning, raft]
    description: Which approach won. That order is also the order of increasing cost to change your mind - skipping a rung needs a measured reason, not an intuition about capability.
  - name: eval_metric
    type: string
    required: true
    description: The metric and the threshold that decided it - "exact-match F1 at or above 0.82". Agree the threshold before the runs, or whatever number appears becomes the threshold.
  - name: dataset_size
    type: integer
    required: true
    description: How many labelled examples the eval ran on. Below a couple of hundred the gap between approaches sits inside the error bar and you are choosing on noise you can reproduce.
  - name: cost_ceiling
    type: string
    required: true
    description: Monthly API spend above which this decision is re-opened, with currency. Set it now - a ceiling chosen after the invoice arrives is not a trigger, it is a reaction.
-->

# ADR-{{adr_number}}: LLM Architecture Decision — {{feature_name}}

## Status

Proposed / Accepted / Superseded by ADR-YYY

## Context

- **Problem statement:** {{problem_statement}}
- **Current approach:** [What is in place now]
- **Why re-evaluating:** [Accuracy gap / cost pressure / new requirement]

## Options Evaluated

| Approach | Accuracy (eval) | Latency p50 | Monthly cost | Complexity |
|----------|-----------------|-------------|--------------|------------|
| Prompt engineering | | | | Low |
| RAG | | | | Medium |
| Fine-tuning | | | | High |
| RAFT | | | | Very High |

## Decision

**Selected:** {{selected_approach}}

**Rationale:**
- [Primary reason]
- [Secondary reason]
- [Constraints that ruled out alternatives]

## Evaluation Results

- **Dataset size:** {{dataset_size}} labeled examples
- **Eval metric:** {{eval_metric}}
- **Baseline (prompt only):** [X%]
- **Selected approach score:** [Y%]
- **Test set:** [description of test set]

## Consequences

**Positive:**
- [benefit 1]
- [benefit 2]

**Negative / Trade-offs:**
- [cost / complexity / maintenance burden]

## Re-evaluation Trigger

Review this decision if any of the following occur:
- Monthly API cost exceeds {{cost_ceiling}}
- Accuracy on the eval set drops below the {{eval_metric}} threshold
- Task requirements change significantly
- New model releases change the cost/quality trade-off

**Scheduled review:** [date or milestone]
