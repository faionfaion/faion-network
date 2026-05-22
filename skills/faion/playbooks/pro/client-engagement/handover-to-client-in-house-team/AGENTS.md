---
slug: handover-to-client-in-house-team
tier: pro
group: client-engagement
persona: P4
goal: migrate-rebuild
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Engagement ending → client in-house team operates the product alone with code, runbooks, ADRs, on-call rota, training videos, and a 90-day defect SLA; vendor exits with a referenceable signed accep...
content_id: 70654f304038f35f
methodology_refs:
  - onboarding
  - onboarding-30-day
  - onboarding-60-90-day
  - 30-60-90-day-plan
  - solution-assessment
  - architecture-decision-records
  - design-docs-patterns
  - living-documentation
  - scope-management
  - grafana-dashboards
  - prometheus-monitoring
  - devops-aws-monitoring-dr
  - api-monitoring-alerting
  - api-monitoring-logging
  - secrets-management
  - cicd-tls-renewal-automation
  - post-handover-warranty-runbook
  - lessons-learned
  - ai-agent-prompt-handover
  - project-closure
  - benefits-realization
  - client-handover-master-checklist
---

# Handover to client in-house team (3 weeks)

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** deep · **Angle:** global

## Why this playbook exists

Engagement ending → client in-house team operates the product alone with code, runbooks, ADRs, on-call rota, training videos, and a 90-day defect SLA; vendor exits with a referenceable signed acceptance letter.

Three-week structured handover from the outsource vendor to a client in-house team. Output: code + runbooks + ADRs in client hands, on-call rota populated, training videos recorded, 90-day defect SLA active, and signed acceptance letter. No Slack call to the outgoing dev for 30 days after the cutover.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Receiving team readiness

**Intent:** Profile the in-house team and shape the handover to their gaps.

**Tasks**
- Map team skills vs deployed stack
- Run gap-analysis on top operational scenarios
- Sketch onboarding 30-60-90 day plan for the receiving team
- Negotiate hold-back resources from vendor side (escalation contacts)

**Outputs**
- Receiving-team skills map
- Gap analysis
- 30-60-90 plan for in-house team

**Decision gate**

Advance once the in-house team accepts the 30-60-90 plan AND vendor escalation rota is signed. Otherwise re-scope handover.

### Stage 2 — Documentation deep-clean

**Intent:** Burn down doc debt before knowledge walks out the door.

**Tasks**
- Audit ADRs; backfill missing decisions
- Refresh design docs to match current state
- Adopt living-documentation conventions (AGENTS.md per module)
- Document scope boundaries explicitly so the in-house team knows what was NOT built

**Outputs**
- ADR set complete, dated, indexed
- Refreshed design docs
- Living-documentation pattern adopted

**Decision gate**

Advance when a new hire on the receiving team can read the docs and answer top-10 system questions unaided.

### Stage 3 — Ops, monitoring, runbooks

**Intent:** Hand over the production levers, not just the source.

**Tasks**
- Set up Grafana dashboards aligned to NFRs
- Migrate or share Prometheus alerts
- Document API monitoring, logging, alerting
- Rotate secrets; client team holds the keys
- Verify backup + DR rotation (AWS monitoring DR)
- Renew TLS automation in client CI/CD

**Outputs**
- Dashboards in client tenancy
- Alerts in client paging tool
- Top-10 runbooks (deploy, rollback, restore, scale, etc.)
- Secrets rotation log

**Decision gate**

Advance when client on-call can complete a full incident drill unaided.

### Stage 4 — Knowledge transfer sessions

**Intent:** Live walkthroughs + recordings the in-house team can rewatch.

**Tasks**
- Record top user-facing flows as training videos
- Pair an in-house dev with a vendor dev per module
- Run two architecture deep-dives with the receiving lead
- Hand over AI-agent prompts and constraints used during build

**Outputs**
- Recorded sessions per module
- Paired-shipping log (PRs reviewed jointly)
- AI-agent prompt pack handed over

**Decision gate**

Advance when each module has ≥1 in-house dev who has merged a PR unaided.

### Stage 5 — Cutover & acceptance

**Intent:** Sign the closure paperwork; activate the warranty SLA.

**Tasks**
- Run benefits-realisation review with client sponsor
- Project closure ceremony (vendor + client)
- Stand up 90-day warranty SLA + intake channel
- Capture testimonial / referenceability
- Decommission vendor access (laptops, accounts, VPN)

**Outputs**
- Signed acceptance letter
- Warranty SLA active
- Closure deck
- Vendor access revoked

**Decision gate**

Engagement closes only with a signed acceptance letter AND zero open critical defects.

## Common pitfalls

- Treating handover as a deck — the doc burns in a fortnight, the runbooks live forever
- Holding back tribal knowledge to preserve future work — kills referenceability
- Skipping AI-agent prompt handover; the receiving team will reinvent unsafe defaults

## Quality checklist

- Did the in-house team merge a real PR before cutover?
- Could an on-call rotation answer a 3am page without phoning the vendor?
- Did the sponsor sign the acceptance letter — not just the PM?

## Related playbooks

- `project-closure-debrief`
- `engagement-handover-transition-out`
- `weekly-status-report`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `client-handover-master-checklist` (blocks stage 5)
- `ai-agent-prompt-handover` (blocks stage 4)
- `post-handover-warranty-runbook` (blocks stage 3)
