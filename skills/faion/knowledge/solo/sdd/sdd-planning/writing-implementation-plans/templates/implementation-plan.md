<!--
purpose: Canonical implementation-plan.md skeleton for the SDD planning phase.
consumes: design.md (Accepted), spec.md (Accepted), repo testing convention
produces: a writing-implementation-plans artefact validating against scripts/validate-writing-implementation-plans.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~12-30k once filled
-->
---
artefact_id: plan-<feature>
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
feature: <feature-name>
status: Draft
design_ref: .aidocs/features/<status>/<feature>/design.md
---

# Implementation Plan: <Feature Name>

## Tasks

| ID | Title | Files | est_tokens | Depends on | Traces to |
|----|-------|-------|------------|------------|-----------|
| TASK_<NNN> | <imperative title> | <path[, path]> | <int ≤100000> | <TASK_NNN[, ...] or —> | AD-<N>[, FR-<N>] |

## Waves

- Wave 1: <TASK_NNN[, ...]>
- Wave 2: <TASK_NNN[, ...]>

## Critical Path

<TASK_NNN → TASK_NNN → ...>

## Risks

- <risk statement> (mitigation: <action>).

## Testing Strategy

- AD-<N> covered by <unit|integration|e2e|contract> tests at TASK_<NNN>.

## Rollout

<feature-flag / canary / staged-release strategy, named gate>.

## Rollback

<concrete reversal procedure for the last wave>.

> Status: Draft — awaiting human owner review for Accepted promotion.
