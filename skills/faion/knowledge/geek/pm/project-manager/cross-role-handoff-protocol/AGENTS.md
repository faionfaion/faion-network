---
slug: cross-role-handoff-protocol
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Canonical handoff protocol (definition-of-ready, artifact list, sign-off mechanism) for BA -> Architect -> Dev -> QA -> DevOps transitions in multi-week product-team flows.
content_id: "0cebd3002dd379d3"
tags: [pm, handoff, definition-of-ready, definition-of-done, sign-off, cross-functional]
---

# Cross-Role Handoff Protocol

## Summary

**One-sentence:** A handoff protocol that defines the artifact bundle + acceptance gate + named sign-off owner for every cross-role transition in a multi-week feature flow.

**One-paragraph:** Replaces tribal "Slack ping the next role" handoffs with a documented bundle + gate. Mechanism: each role pair (BA->Architect, Architect->Dev, Dev->QA, QA->DevOps) has a fixed Definition-of-Ready (artifacts the upstream role MUST produce), an acceptance gate (downstream role's checklist), and a single named sign-off owner whose Yes/No is recorded with timestamp + delta-since-last-check. Primary output: a signed handoff record per role-pair, attached to the feature ticket, that proves the gate was met before downstream work started.

## Applies If (ALL must hold)

- multi-week feature involves >= 3 distinct roles
- team is >= 4 people OR includes any external contractor / vendor
- feature ticket exists in a single source of truth (Jira, Linear, GitHub Issues)
- each role has at least one named individual (not a generic queue)

## Skip If (ANY kills it)

- solo founder doing all roles — no handoff exists; use a personal checklist instead
- feature is a one-line fix / hotfix — protocol overhead > benefit; use the inline-PR-review path
- team is 2 people in constant sync — synchronous review is faster than artifact bundle
- no shared ticket system — protocol depends on a single record per handoff

## Prerequisites

- ticket system permits attachments + comments with @mentions
- each role pair has at least one named individual on each side
- feature spec exists at least at one-paragraph fidelity (the BA->Architect handoff fills it in)
- team agreed on a sign-off mechanism: ticket field, label, or PR-approval — pick one and stick with it

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/sdd-planning/definition-of-ready-template` | DoR sub-document is per-handoff; this protocol composes them across all role pairs |
| `pro/ba/business-analyst/requirements-traceability` | BA->Architect handoff bundle includes traceability matrix; consume from there |
| `pro/pm/project-manager/raci-matrix` | Sign-off owner identity per handoff is derived from RACI; consume don't redefine |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: single-sign-off-owner, dated-delta, no-skipping-gates, blocking-rejections-with-reason, sign-off-record-immutability | ~1000 |
| `content/02-output-contract.xml` | essential | Handoff-record schema per role-pair + forbidden patterns (verbal handoff, ambiguous owner, etc.) | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (silent-pass, group-sign-off, scope-drift-at-handoff, etc.) with detector + repair | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `handoff_bundle_assembly` | sonnet | Collect named artifacts from upstream, verify presence — bounded |
| `acceptance_gate_check` | sonnet | Run downstream checklist against bundle, return pass/fail/needs-info |
| `sign_off_record_draft` | haiku | Template fill: who, when, gate, delta-link |
| `cross_handoff_audit` | opus | End-of-feature audit: did every role pair complete the protocol? Cross-record synthesis |

## Templates

| File | Purpose |
|------|---------|
| `templates/handoff-record.json` | JSON Schema for one handoff sign-off record |
| `templates/dor-ba-to-architect.md` | BA->Architect Definition-of-Ready bundle list |
| `templates/dor-architect-to-dev.md` | Architect->Dev Definition-of-Ready bundle list |
| `templates/dor-dev-to-qa.md` | Dev->QA Definition-of-Ready bundle list |
| `templates/dor-qa-to-devops.md` | QA->DevOps Definition-of-Ready bundle list |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-handoff-record.py` | Checks one sign-off record against schema + immutability rules | After downstream role marks gate passed, before they start work |
| `scripts/audit-feature-handoffs.py` | Walks a feature's handoff records, flags missing or out-of-order sign-offs | At feature-done, before close |

## Related

- parent skill: `geek/pm/project-manager/`
- peer methodologies: `raci-matrix`, `escalation-protocol`, `cross-team-dependency-graph`
- external: [Atlassian Handoff Patterns](https://www.atlassian.com/agile/project-management/handoffs) · [SAFe Continuous Delivery Pipeline](https://scaledagileframework.com/continuous-delivery-pipeline/) · [Spotify Engineering Culture](https://engineering.atspotify.com/2014/03/spotify-engineering-culture-part-1/)
