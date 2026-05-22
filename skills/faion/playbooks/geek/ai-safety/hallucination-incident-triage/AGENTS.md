---
slug: hallucination-incident-triage
tier: geek
group: ai-safety
persona: P7
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Customer-reported fabricated answer → reproduce, attribute, ship fix or guardrail, log to permanent eval-set within the working day.
content_id: 2b2d3ce919c875d0
methodology_refs:
  - record-replay-debugging
  - trajectory-eval-otel
  - rerank-before-reasoning
  - refusal-field-strict-schema
  - compaction-preserve-refs
  - rag-eval-retrieval-metrics
  - agents-safety-guardrails
  - eu-ai-act-compliance
---

# Hallucination incident triage

**Playbook slug:** `hallucination-incident-triage`  
**Tier:** geek  
**Complexity:** medium  
**Persona:** P7 — LLM Agent Developer

## Intent

Customer-reported fabricated answer → reproduce, attribute, ship fix or guardrail, log to permanent eval-set within the working day.

## Scope

Customer reported a fabricated answer. Reproduce, attribute, ship a fix or guardrail, log to permanent eval-set within the working day. Intended as a single-day incident response, not a long investigation.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Full root-cause forensic — see blameless postmortem playbook
- Pricing/comms response — out of scope

### Prerequisites

- Trace id from customer report
- Eval harness reachable

## Success criteria

The playbook is done when:
- Failure reproduced from trace
- Cause attributed to layer (model / prompt / tool / context)
- Fix or guardrail shipped
- Regression eval row added
- Customer-facing note drafted

## Stages

### Stage 1: Reproduce

**Intent:** Replay the bad trace.

**Tasks:**
- Pull trace by id
- Replay with record-replay

**Methodologies in chain:**
- `record-replay-debugging` → `geek/ai/ai-agents/record-replay-debugging`
- `trajectory-eval-otel` → `geek/ai/ai-agents/trajectory-eval-otel`

**Outputs:**
- Reproduced failure

**Decision gate:**
> Advance only when failure reproduces deterministically.

### Stage 2: Attribute

**Intent:** Layer attribution: model vs prompt vs tool vs context.

**Tasks:**
- Inspect rerank order
- Check refusal-field strictness
- Audit context compaction

**Methodologies in chain:**
- `rerank-before-reasoning` → `geek/ai/ai-agents/rerank-before-reasoning`
- `refusal-field-strict-schema` → `geek/ai/ai-agents/refusal-field-strict-schema`
- `compaction-preserve-refs` → `geek/ai/ai-agents/compaction-preserve-refs`
- `rag-eval-retrieval-metrics` → `geek/ai/rag-engineer/rag-eval-retrieval-metrics`

**Outputs:**
- Attribution note

**Decision gate:**
> Advance only when one layer is clearly implicated.

### Stage 3: Mitigate & Log

**Intent:** Ship guardrail and add regression eval.

**Tasks:**
- Wire safety guardrail
- Check EU AI Act applicability
- Add row to permanent eval
- Draft customer-facing note

**Methodologies in chain:**
- `agents-safety-guardrails` → `geek/ai/ml-engineer/agents-safety-guardrails`
- `eu-ai-act-compliance` → `geek/ai/ai-agents/eu-ai-act-compliance`
- `rag-eval-retrieval-metrics` → `geek/ai/rag-engineer/rag-eval-retrieval-metrics`

**Outputs:**
- Guardrail PR
- Eval row added
- Customer note

**Decision gate:**
> Close incident only after eval row and guardrail both land.

## Common pitfalls

- Treating eval scores as ground truth without judge calibration
- Shipping prompt or model changes without a regression gate
- Skipping shadow rollout for routing or model swaps

## Quality checklist (self-review)

- Can I roll back this change in one step?
- Is the regression eval committed BEFORE the fix?
- Are tool / schema versions pinned in the manifest?

## Related playbooks

- `eval-harness-continuous-benchmark-suite`
- `agent-observability-drift-detection-rollout`
- `production-agent-eval-harness-week-1`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **hallucination-attribution-checklist** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **agent-postmortem-template** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

One working day, end-to-end. Drift past one day and the customer will follow up; drift past two and you owe a postmortem (see `blameless-agent-incident-postmortem`). Treat the day as a sprint: reproduce, attribute, ship, log.

Reproduction with record-replay is mandatory; the customer's screenshot is not enough. If you cannot reproduce, the failure is non-deterministic and the fix path changes — investigate the model temperature, the rerank tie-breaker, and any tool that depends on wall-clock state.

Attribution is the riskiest step because the cheap answer ("the model hallucinated") is rarely the real one. Most hallucinations attribute to context: a relevant chunk was evicted by compaction, the retrieval missed the canonical source, or the refusal field was not strict enough. Stage 2 mandates inspecting compaction, rerank order, and refusal schema. Walk all three before blaming the model.

Ship a guardrail, not a model swap. Guardrails are reversible and testable; model swaps are policy decisions and need broader review. EU AI Act applicability check is part of the close-out — if the incident touches a high-risk-system surface, the playbook is not done at ship; the governance log entry must also be filed.

Add the failure to the permanent eval set BEFORE the guardrail merges. Brainstorm flags hallucination-attribution-checklist and agent-postmortem-template as gaps; until authored, write the close-out note longhand.

## CLI usage

```
faion get-content hallucination-incident-triage --format md       # human-readable rendering
faion get-content hallucination-incident-triage --format context  # agent-optimised context bundle
faion get-content hallucination-incident-triage --format json     # raw structured form
```
