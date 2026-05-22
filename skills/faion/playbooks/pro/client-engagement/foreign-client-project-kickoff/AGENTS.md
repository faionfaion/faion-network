---
slug: foreign-client-project-kickoff
tier: pro
group: client-engagement
persona: P4
goal: plan-design
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Brand-new engagement with a US/EU/UK/AU client → signed SoW, ratified architecture, RACI + cadence, dev env on client stack, first sprint groomed, and an inception report a senior promotion panel w...
content_id: f054b074200ba293
methodology_refs:
  - stakeholder-analysis
  - elicitation-techniques
  - stakeholder-register
  - competitive-intelligence
  - requirements-documentation
  - requirements-validation
  - requirements-traceability
  - acceptance-criteria
  - use-case-modeling
  - scope-management
  - cloud-architecture
  - quality-attributes-analysis
  - architecture-decision-records
  - writing-design-documents
  - design-doc-structure
  - client-conventions-reverse-engineering
  - ai-agent-guardrails-pack
  - raci-matrix
  - communications-management
  - stakeholder-engagement
  - docker-image-optimization
  - github-actions-cicd
  - secrets-management
  - foreign-client-kickoff-checklist
  - scrum-ceremonies
  - six-core-principles
  - hybrid-delivery
  - risk-register
---

# Foreign-client project kickoff (2 weeks)

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** deep · **Angle:** global

## Why this playbook exists

Brand-new engagement with a US/EU/UK/AU client → signed SoW, ratified architecture, RACI + cadence, dev env on client stack, first sprint groomed, and an inception report a senior promotion panel would accept.

Two-week onboarding sprint. By end-of-week-2 the outsource senior owns: signed SoW, validated requirements baseline, architecture skeleton fitting client conventions, RACI + comms cadence, dev environment matching client stack, first sprint backlog groomed, and an inception report sent. Output is reviewer-ready and survives a senior/lead promotion panel.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Engagement intake

**Intent:** Inhale every artifact the client already has and surface the gaps in 48h.

**Tasks**
- Read MSA + SoW skeleton end-to-end, mark every undefined term
- Run stakeholder mapping workshop with client PM + sponsor
- Pull existing architecture diagrams, ADRs, runbooks into a shared dossier
- Audit competitive context for the client product (positioning, peers)

**Outputs**
- Stakeholder register v1
- Open-questions log with named owner per item
- Existing-artifacts dossier

**Decision gate**

Advance only when ≥80% of client artifacts have been read AND every open question has a named owner with a target answer date. Otherwise extend intake.

### Stage 2 — Scope & SoW lock

**Intent:** Convert SoW skeleton into a defendable scope baseline with acceptance criteria.

**Tasks**
- Draft requirements doc tied to client business goals
- Walk each requirement through an INVEST + acceptance criteria pass
- Validate scope with client PM + sponsor; capture sign-off
- Annotate use-cases for the top-3 customer journeys

**Outputs**
- Requirements doc v1 with acceptance criteria
- Use-case map for top journeys
- Signed scope baseline (SoW Annex A)

**Decision gate**

Advance when client PM countersigns scope baseline and acceptance criteria. If sponsor pushes back on >2 acceptance criteria, loop back into intake.

### Stage 3 — Architecture & client conventions

**Intent:** Stand up an architecture skeleton that fits the client's house style, not yours.

**Tasks**
- Reverse-engineer client conventions from existing repos (lint, CI, naming, branching)
- Map quality attributes (NFRs) for performance / security / availability
- Pick cloud architecture pattern aligned with client mandate
- Open initial ADRs for top-5 contested decisions
- Establish AI coding agent guardrails — what the agent may NOT auto-emit

**Outputs**
- Architecture skeleton repo (compiles, passes client lint)
- ADR set #001-005
- AI-agent guardrails written into AGENTS.md

**Decision gate**

Advance once ADRs are merged AND a hello-world PR passes client's CI without rework. If lint/CI fails, fix conventions before sprint planning.

### Stage 4 — RACI, cadence, dev environment

**Intent:** Make the working week predictable on both sides.

**Tasks**
- Publish RACI for top-10 deliverables and decisions
- Lock comms cadence (daily async, weekly sync, monthly steerco)
- Provision dev environments matching client stack on every machine
- Configure CI/CD skeleton with secrets management baseline
- Document onboarding in a 30-day plan a new joiner can follow

**Outputs**
- RACI matrix v1
- Comms cadence published
- Reproducible dev environment doc
- CI/CD skeleton merged

**Decision gate**

Advance when a brand-new joiner can clone the repo, follow the doc, and produce a green CI run in <1 day. Loop back if not.

### Stage 5 — Sprint zero + inception report

**Intent:** Groom the first sprint, send the inception report, get the client steerco to sign off the engagement is open for delivery.

**Tasks**
- Run sprint zero ceremonies with the joint team
- Risk register draft with top-10 risks + mitigations
- Hybrid delivery plan (Scrum cadence + traditional reporting outward)
- Send inception report covering 6 sections (scope, arch, RACI, risks, plan, AI usage)

**Outputs**
- First sprint backlog committed
- Risk register v1
- Inception report sent and acknowledged

**Decision gate**

Advance to delivery only when client steerco acknowledges inception report AND first sprint is committed by both PMs. Otherwise iterate.

## Common pitfalls

- Copy-pasting your own conventions over the client's — every audit later flags this
- Skipping AI-agent guardrails — the agent will helpfully emit unsafe defaults nobody reviews
- Leaving stakeholder register as 'people I emailed once' — write down decision authority

## Quality checklist

- Could a brand-new joiner read the artifacts and ship a tiny PR end-to-end in week 3?
- Did the AI coding agent get an explicit perimeter, not just vibes?
- Did I countersign client-side, not just verbal nods?

## Related playbooks

- `scoping-workshop`
- `statement-of-work`
- `weekly-status-report`
- `sprint-planning-agency`
- `production-cicd-pipeline`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `foreign-client-kickoff-checklist` (blocks stage 4)
- `client-conventions-reverse-engineering` (blocks stage 3)
- `ai-agent-guardrails-pack` (blocks stage 3)
