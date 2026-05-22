---
slug: ai-native-product-introduction
tier: geek
group: role-product-manager
persona: role-product-manager
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Stand up an AI-native product surface (new feature or new product) end-to-end: agentic capability shape, eval framework, safety + explainability, rollout, and steady-state operating model."
content_id: 07bc1f49a6322a6a
methodology_refs:
  - agentic-ai-product-development
  - agents
  - ai-native-product-development
  - market-sizing-with-ai
  - perplexity-ai-research
  - ai-persona-building
  - synthetic-users
  - experimentation-at-scale
  - learning-speed-competitive-moat
  - product-explainability
  - product-operations
  - product-analytics
  - release-planning
  - jobs-to-be-done
---

# AI-native product introduction

## Context

Stand up an AI-native product surface (new feature or new product) end-to-end: agentic capability shape, eval framework, safety + explainability, rollout, and steady-state operating model. Distinct from a normal MVP because of model risk, evals, and explainability.

Tier: **geek**. Complexity: **deep**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- Frozen, versioned eval set with 50+ scenarios.
- Failure-mode matrix with refusal/escalation paths.
- Agent rolled out behind kill switch + flag.
- Steady-state ops model documented and owned.

## Steps

### 1. Capability shape

Decide the agentic shape before any code lands.

Tasks:
- Pick the agent shape: assistant, autonomous worker, or in-product copilot.
- Map the JTBD the agent will own end-to-end.
- Articulate where the agent must defer to a human.

Outputs:
- Capability shape doc.
- Human-in-loop boundaries.

Decision gate: Advance when the agent shape is one of 3 named patterns and the human-in-loop boundary is explicit.

### 2. Evals first

Build the eval set before the agent.

Tasks:
- Draft 50+ frozen eval scenarios from real user JTBDs.
- Define passing criteria per scenario.
- Lock the eval set under version control.

Outputs:
- Frozen eval set.
- Passing-criteria doc.

Decision gate: Advance when the eval set is frozen, versioned, and has at least 50 scenarios.

### 3. Safety + explainability

Decide what failure looks like and how the agent explains itself.

Tasks:
- Enumerate top 5 failure modes with severity.
- Design refusal + escalation paths per failure.
- Define the user-facing explanation surface (citations, source, reasoning trace).

Outputs:
- Failure-mode matrix.
- Explainability surface spec.

Decision gate: Advance when every top-5 failure mode has an explicit refusal or escalation path.

### 4. Build

Implement the smallest agent that passes the eval set.

Tasks:
- Wire the agent against tools / retrieval / memory as needed.
- Run the eval set every commit.
- Gate merges on eval pass rate.

Outputs:
- Working agent passing eval set.
- CI-integrated eval pipeline.

Decision gate: Advance when the eval pass rate is above the documented threshold (no opinion-based shipping).

### 5. Trust testing

Run the agent in front of users with the brakes engaged.

Tasks:
- Run 10+ supervised sessions.
- Watch for refusal-rate, escalation-rate, and user-correction-rate.
- Iterate prompts/tools based on observed corrections.

Outputs:
- Trust-test report.

Decision gate: Advance when user-correction-rate is below the documented threshold across 3 consecutive sessions.

### 6. Rollout

Roll the agent out behind a kill switch.

Tasks:
- Roll out behind a feature flag with kill switch.
- Ramp exposure in 1% → 10% → 50% → 100% stages.
- Watch eval drift weekly.

Outputs:
- Rollout schedule.
- Kill-switch wiring.

Decision gate: Advance when 50% exposure holds the eval pass rate for 7 days.

### 7. Steady-state

Establish the operating model for the agent in production.

Tasks:
- Define ownership for eval set, incidents, and model upgrades.
- Schedule weekly drift review.
- Establish a model-upgrade re-eval ritual.

Outputs:
- Operating model doc.
- Weekly drift dashboard.

Decision gate: Required: a written steady-state ops model the on-call team can execute.

## Decision points

- Assistant vs autonomous vs copilot shape — pick the highest autonomy the eval set + user trust can support, not higher.
- Build vs buy vs orchestrate — if the eval set is small and stable, buy; if it is large and unique, build.
- Kill vs ramp — at 1% exposure, kill on a single P0 explainability failure; do not 'monitor harder'.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `geek/product/product-manager/agentic-ai-product-development`
- `geek/product/product-manager/agents`
- `geek/product/product-manager/ai-native-product-development`
- `geek/research/market-researcher/market-sizing-with-ai`
- `geek/research/market-researcher/perplexity-ai-research`
- `geek/research/researcher/ai-persona-building`
- `geek/research/researcher/synthetic-users`
- `pro/product/product-operations/experimentation-at-scale`
- `pro/product/product-operations/learning-speed-competitive-moat`
- `pro/product/product-operations/product-explainability`
- `pro/product/product-operations/product-operations`
- `solo/product/product-operations/product-analytics`
- `solo/product/product-planning/release-planning`
- `solo/research/researcher/jobs-to-be-done`
