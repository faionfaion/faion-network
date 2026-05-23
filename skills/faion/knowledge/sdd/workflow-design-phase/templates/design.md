<!--
purpose: Canonical design.md skeleton for the SDD design phase.
consumes: spec.md (Accepted status), constitution.md, codebase survey
produces: a workflow-design-phase artefact validating against scripts/validate-workflow-design-phase.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~10-30k once filled
-->
---
artefact_id: design-<feature>
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
feature: <feature-name>
status: Draft
spec_ref: .aidocs/features/<status>/<feature>/spec.md
---

# Design: <Feature Name>

## Codebase Survey

- `<path>:<lines>` — <pattern observed>.
- `<path>:<lines>` — <pattern observed>.
- `<path>:<lines>` — <pattern observed>.

## Architectural Decisions

### AD-<N>: <decision headline>

- Chosen: <one sentence>.
- Rejected: <option A>, <option B>.
- Rationale: <2-3 sentences>.
- Satisfies: FR-<N>, NFR-<N>.
- Trade-off: <one sentence>.

## File Table

| Action | Path | Scope |
|--------|------|-------|
| CREATE | <path> | <one-sentence scope> |
| MODIFY | <path> | <one-sentence scope> |

## Data Models

<schemas, ORM models, JSON shapes>

## API Contracts

| Method | Path | Request | Response |
|--------|------|---------|----------|
| <verb> | <path> | <shape> | <shape> |

## Testing Strategy

- AD-<N> covered by <unit|integration|e2e|contract> tests at `<test-path>`.

## FR Coverage

| FR | AD |
|----|-----|
| FR-<N> | AD-<N> |
