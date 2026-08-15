<!--
purpose: Canonical implementation-plan.md skeleton for the SDD planning phase.
consumes: design.md (Accepted), spec.md (Accepted), repo testing convention
produces: a writing-implementation-plans artefact validating against scripts/validate-writing-implementation-plans.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~12-30k once filled
variables:
  - name: slug
    type: string
    required: true
    description: The feature's kebab-case slug, identical to its directory under .aidocs/features. A plan whose slug differs from its folder is a plan the lifecycle tooling will not find.
  - name: owner
    type: string
    required: true
    description: The human who reviews this plan for promotion to Accepted. The status line at the bottom is waiting on this person specifically - a team name there means the plan stays Draft forever.
  - name: email
    type: string
    required: true
    description: The owner's email, reachable after they change teams. This is the address the next engineer writes to before undoing what this document decided.
  - name: date
    type: string
    required: true
    description: The day this was agreed, ISO - not the day it was typed up. Downstream reviews are scheduled off it, so a placeholder date silently disables the review.
  - name: feature_title
    type: string
    required: true
    description: The feature in title case as the spec names it. If it does not match the spec heading, the traceability column below is checking two documents that only look related.
  - name: design_ref
    type: path
    required: true
    description: Path to the Accepted design.md this plan implements. If the design is still Draft, stop - planning against an unaccepted design is how a whole wave gets rewritten.
  - name: first_task_title
    type: text
    required: true
    description: The first task as an imperative that names the change - "Add the migration for order.status". Not "work on orders". Tasks are the unit an executor picks up alone.
  - name: rollout_gate
    type: text
    required: true
    description: The named gate that lets this reach users - the flag, the canary percentage, the metric that must hold. "Deploy to production" is not a rollout strategy, it is the moment one is needed.
  - name: rollback_procedure
    type: text
    required: true
    description: The concrete reversal for the last wave - the command, the flag flip, the migration that has to be reversible. Write it while the design is fresh, not while the graph is red.
-->
---
artefact_id: plan-{{slug}}
owner: {{owner}} <{{email}}>
version: 1.0.0
last_reviewed: {{date}}
feature: {{slug}}
status: Draft
design_ref: {{design_ref}}
---

# Implementation Plan: {{feature_title}}

## Tasks

| ID | Title | Files | est_tokens | Depends on | Traces to |
|----|-------|-------|------------|------------|-----------|
| TASK_001 | {{first_task_title}} | [path, path] | [int ≤100000] | — | AD-[N], FR-[N] |
| TASK_002 | [imperative title] | [path, path] | [int ≤100000] | TASK_001 | AD-[N] |

## Waves

- Wave 1: TASK_001
- Wave 2: TASK_002

## Critical Path

TASK_001 → TASK_002

## Risks

- [risk statement] (mitigation: [action]).

## Testing Strategy

- AD-[N] covered by [unit|integration|e2e|contract] tests at TASK_[NNN].

## Rollout

{{rollout_gate}}

## Rollback

{{rollback_procedure}}

> Status: Draft — awaiting review by {{owner}} for Accepted promotion.
