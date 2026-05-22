---
slug: validate-an-ai-feature-before-it-consumes-a-quarter
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
summary: "Bridge the canyon between 'leadership wants AI' and 'team commits roadmap slot'."
content_id: 32bdbb03d737e4df
methodology_refs:
  - agentic-ai-product-development
  - ai-native-product-development
  - experimentation-at-scale
  - jobs-to-be-done
  - ai-feature-de-risking
---

# Validate an AI feature before it consumes a quarter

## Context

Bridge the canyon between 'leadership wants AI' and 'team commits roadmap slot'. PM proves or kills an AI feature on user value (not model novelty) before it touches the roadmap. Faion has agentic-ai-product-development at geek tier but no de-risking playbook for AI feature commits specifically.

Tier: **geek**. Complexity: **deep**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- De-noveltied feature statement with non-AI counterfactual.
- WoZ test report from 5+ sessions.
- 20+ frozen eval scenarios.
- Written commit / hold / kill verdict.

## Steps

### 1. De-novelty

Strip the model novelty and look at user value.

Tasks:
- Restate the feature as a JTBD the user already has.
- Test if a non-AI solution would also serve the JTBD.
- Note the genuine reason the agent must be involved.

Outputs:
- De-noveltied feature statement.

Decision gate: Advance when the feature has a non-AI counterfactual that loses against the AI version on a real reason.

### 2. Wizard-of-Oz test

Fake the agent with a human in the loop.

Tasks:
- Mock the agent response with a human responder.
- Run 5+ user sessions with the WoZ setup.
- Watch user reactions to imperfect-but-fast vs slow-but-perfect responses.

Outputs:
- WoZ session report.

Decision gate: Advance when WoZ shows clear value, not curiosity-only engagement.

### 3. Eval-first sketch

Sketch the eval set before any model work.

Tasks:
- Draft 20+ frozen eval scenarios.
- Define passing criteria.
- Confirm eval is achievable with the candidate model.

Outputs:
- Eval set sketch.

Decision gate: Advance when 20+ scenarios are documented and reviewable.

### 4. Risk + trust read

Map the failure surface and the user trust requirement.

Tasks:
- Enumerate the top 5 failure modes.
- Score each by user-trust impact.
- Decide if the feature can ship behind a 'tentative answer' frame.

Outputs:
- Failure-mode + trust read.

Decision gate: Advance when failure modes have an explicit acceptable-trust threshold.

### 5. De-risk vote

Convert evidence into a roadmap-commit decision.

Tasks:
- Score the feature on user value, eval feasibility, and trust requirement.
- Decide commit / hold / kill.
- Document the rationale for any commit decision.

Outputs:
- Commit / hold / kill decision with rationale.

Decision gate: Required: a written de-risk verdict; no 'let's see' allowed.

## Decision points

- Commit vs hold — commit only when WoZ + eval feasibility + trust threshold all clear; otherwise hold.
- Kill vs hold — kill when WoZ shows no genuine user value; hold when the value is real but the model is not ready.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `geek/product/product-manager/agentic-ai-product-development`
- `geek/product/product-manager/ai-native-product-development`
- `pro/product/product-manager/experimentation-at-scale`
- `solo/research/researcher/jobs-to-be-done`
- `geek/product/product-manager/ai-feature-de-risking`
