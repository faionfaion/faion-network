---
slug: agent-observability-drift-detection-rollout
tier: geek
group: ml-ops
persona: P7
goal: build-ship
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: "Blind-running agent → fully observed: per-step OTEL traces, eval-in-prod sampling, drift detection, alerting, on-call runbook."
content_id: 05193f4f74a3a6dd
methodology_refs:
  - trajectory-eval-otel
  - stream-json-orchestration
  - schema-version-pinning
  - llm-observability
  - llm-observability-stack
  - llm-judge-rubric-evidence-first
  - evaluation-framework
  - rag-eval-production-monitoring
  - vector-database-setup
  - guardrails-concepts
  - ai-governance-compliance
  - eu-ai-act-compliance
  - prompt-engineering-security
  - inc-runbook-as-markdown-tagged-steps
  - inc-read-only-investigation-default
  - inc-tool-tier-approval-gate
  - inc-postmortem-auto-draft-no-publish
---

# Observability + drift detection rollout (3 weeks)

**Playbook slug:** `agent-observability-drift-detection-rollout`  
**Tier:** geek  
**Complexity:** medium  
**Persona:** P7 — LLM Agent Developer

## Intent

Blind-running agent → fully observed: per-step OTEL traces, eval-in-prod sampling, drift detection, alerting, on-call runbook.

## Scope

Production agent goes from blind-running to fully observed: per-step OTEL traces, eval-in-prod sampling, drift detection on inputs/outputs/costs, alerting, and an on-call runbook.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Replacing existing APM — augments, not replaces
- Building a vendor observability product

### Prerequisites

- Existing production agent path
- Logging endpoint with retention

## Success criteria

The playbook is done when:
- OTEL traces visible per trajectory
- Eval-in-prod sampling running
- Drift detection firing on planted shifts
- On-call runbook signed off
- Alerts route to the right channel with tier-approval gating

## Stages

### Stage 1: Trace Wiring

**Intent:** Per-step OTEL traces with stable trajectory ids.

**Tasks:**
- Instrument every tool call + LLM call
- Stream-JSON orchestration where applicable
- Pin schema versions across traces

**Methodologies in chain:**
- `trajectory-eval-otel` → `geek/ai/ai-agents/trajectory-eval-otel`
- `stream-json-orchestration` → `geek/ai/ai-agents/stream-json-orchestration`
- `schema-version-pinning` → `geek/ai/ai-agents/schema-version-pinning`
- `llm-observability` → `geek/ai/ml-engineer/llm-observability`
- `llm-observability-stack` → `geek/ai/ml-engineer/llm-observability-stack`

**Outputs:**
- Trace dashboard
- Trajectory id contract

**Decision gate:**
> Advance when traces resolve per-step end-to-end.

### Stage 2: Eval-in-Prod

**Intent:** Sample production traffic into judges.

**Tasks:**
- Stratify and sample production traffic
- Run rubric judges on samples
- Track scores over time

**Methodologies in chain:**
- `llm-judge-rubric-evidence-first` → `geek/ai/ai-agents/llm-judge-rubric-evidence-first`
- `evaluation-framework` → `geek/ai/ml-ops/evaluation-framework`
- `rag-eval-production-monitoring` → `geek/ai/rag-engineer/rag-eval-production-monitoring`
- `vector-database-setup` → `geek/ai/rag-engineer/vector-database-setup`

**Outputs:**
- Eval-in-prod sampler
- Score timeline

**Decision gate:**
> Advance when scores look stable on a known-good window.

### Stage 3: Drift Detection

**Intent:** Detect input, output, and cost drift before users do.

**Tasks:**
- Wire input-distribution monitor
- Wire output-distribution monitor
- Wire cost spike monitor

**Methodologies in chain:**
- `guardrails-concepts` → `geek/ai/ml-engineer/guardrails-concepts`
- `ai-governance-compliance` → `geek/ai/ml-engineer/ai-governance-compliance`
- `eu-ai-act-compliance` → `geek/ai/ml-engineer/eu-ai-act-compliance`
- `prompt-engineering-security` → `geek/ai/ml-engineer/prompt-engineering-security`

**Outputs:**
- Drift dashboard
- Alert rules

**Decision gate:**
> Advance after planted-drift test fires correctly.

### Stage 4: On-Call

**Intent:** Read-only investigation default + runbook + approval gates.

**Tasks:**
- Author runbook as tagged markdown steps
- Default investigations to read-only
- Auto-draft postmortem on incident

**Methodologies in chain:**
- `inc-runbook-as-markdown-tagged-steps` → `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `inc-read-only-investigation-default` → `geek/sdlc-ai/inc-read-only-investigation-default`
- `inc-tool-tier-approval-gate` → `geek/sdlc-ai/inc-tool-tier-approval-gate`
- `inc-postmortem-auto-draft-no-publish` → `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`

**Outputs:**
- Runbook doc
- Approval gate config

**Decision gate:**
> Ship only when an end-to-end incident drill completes.

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
- **drift-detection-input-distribution** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **agent-on-call-runbook-template** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **eval-in-prod-sampling-policy** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

Observability is cheaper than blind running, but only if traces are actually queryable. The Trace Wiring stage should produce trajectory ids that survive across tool calls; if your spans cannot be reconstructed end-to-end, you do not have observability, you have logging.

Eval-in-prod sampling is the most-skipped step. Running judges against a 5-10% production sample gives you a continuous score timeline; without it, you only know quality at PR time. Pick a sampler that stratifies by intent class so rare paths do not vanish under volume-heavy paths.

Drift detection has three signals worth wiring: input distribution (user requests shifting), output distribution (agent behaviour shifting), and cost distribution ($/success drifting). Plant a known shift in a staging environment before declaring the detector real. If the planted shift does not fire, neither will the real one.

Stage 4 on-call runbook is a single document, not an architecture review. Default investigations to read-only, gate any state-changing tool behind tier approval, and auto-draft the postmortem so the team is not writing from scratch at 2am. Brainstorm lists drift detection input-distribution, agent on-call runbook template, and eval-in-prod sampling policy as gaps; the playbook leans on those slots in its chain.

## CLI usage

```
faion get-content agent-observability-drift-detection-rollout --format md       # human-readable rendering
faion get-content agent-observability-drift-detection-rollout --format context  # agent-optimised context bundle
faion get-content agent-observability-drift-detection-rollout --format json     # raw structured form
```
