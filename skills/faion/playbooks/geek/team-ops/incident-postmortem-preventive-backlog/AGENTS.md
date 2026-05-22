---
slug: incident-postmortem-preventive-backlog
tier: geek
group: team-ops
persona: P6
goal: fix-incident
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Paging alert → contained impact → human-published postmortem → merged preventive PRs in backlog.
content_id: e006a47d5fe28451
methodology_refs:
  - inc-read-only-investigation-default
  - inc-tool-tier-approval-gate
  - inc-runbook-as-markdown-tagged-steps
  - tracker-ai-triage-classify-route
  - microservices-circuit-breaker
  - lb-high-availability
  - devops-elk-queries-alerting
  - elk-stack-logging
  - grafana-basics
  - prometheus-monitoring
  - aiops
  - chaos-eval-fault-injection
  - inc-postmortem-auto-draft-no-publish
  - communications-management
  - stakeholder-engagement-advanced
  - mistake-memory
  - sec-codeql-autofix-on-pr
  - risk-register
  - lessons-learned
  - security-sast
  - security-dast
  - gitops-progressive-delivery
---

# Incident → postmortem → preventive backlog

**Playbook slug:** `incident-postmortem-preventive-backlog`
**Tier:** geek
**Complexity:** medium
**Persona:** P6 — Product-Dev Team

## Intent

Paging alert → contained impact → human-published postmortem → merged preventive PRs in backlog.

## Scope

An alert pages. On-call contains customer impact, documents root cause, lets the AI auto-draft a postmortem (no auto-publish), and converts action items into costed preventive PRs slotted into the backlog with named owners. No naming-and-shaming. Every incident raises a guardrail.

### What this playbook covers

Four stages that turn a paging event into permanent product hardening. The chain enforces the *AI drafts, humans publish* rule: auto-publishing a wrong postmortem is worse than a delayed one. Action items leave the postmortem only with an owner and a due date — orphaned actions guarantee a repeat.

### Non-goals

- Routine alert triage — covered by `sentry-datadog-alert-triage`
- Annual audit prep — see `soc2-gdpr-audit-prep`
- Incident comms templating beyond what runbook prescribes

### Prerequisites

- On-call rotation with documented escalation path
- Runbook system (markdown tagged steps)
- AI postmortem drafter wired (no auto-publish)

## Success criteria

The playbook is done when:
- Customer impact contained and verifiable
- Root cause documented (technical + organisational layers)
- Postmortem published (human-edited, not auto)
- Action items costed (token + complexity)
- Action items slotted into backlog with named owners
- Risk register updated with new entry or modified existing
- Stakeholder comms loop closed

## Stages

### Stage 1: Contain + investigate

**Intent:** Stop the bleeding under read-only-investigation default and approval-gate boundaries.

**Methodologies in chain:**
- `inc-read-only-investigation-default` → `geek/sdlc-ai/inc-read-only-investigation-default`
- `inc-tool-tier-approval-gate` → `geek/sdlc-ai/inc-tool-tier-approval-gate`
- `inc-runbook-as-markdown-tagged-steps` → `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `tracker-ai-triage-classify-route` → `geek/sdlc-ai/tracker-ai-triage-classify-route`
- `microservices-circuit-breaker` → `pro/dev/software-developer/microservices-circuit-breaker`
- `lb-high-availability` → `pro/infra/cicd-engineer/lb-high-availability`

**Decision gate:**
> Advance once user-facing impact is contained AND a senior engineer has confirmed read-only default was respected.

### Stage 2: Root cause

**Intent:** Walk logs, metrics, traces; chaos-eval evidence; reconstruct causal chain.

**Methodologies in chain:**
- `devops-elk-queries-alerting` → `pro/infra/devops-engineer/devops-elk-queries-alerting`
- `elk-stack-logging` → `pro/infra/cicd-engineer/elk-stack-logging`
- `grafana-basics` → `pro/infra/cicd-engineer/grafana-basics`
- `prometheus-monitoring` → `pro/infra/cicd-engineer/prometheus-monitoring`
- `aiops` → `pro/infra/cicd-engineer/aiops`
- `chaos-eval-fault-injection` → `geek/ai/ai-agents/chaos-eval-fault-injection`

**Decision gate:**
> Advance when the causal chain spans technical + organisational layers (not just 'a config was wrong').

### Stage 3: Postmortem — drafted, human-published

**Intent:** AI drafts; humans edit + publish. Blameless tone enforced.

**Methodologies in chain:**
- `inc-postmortem-auto-draft-no-publish` → `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`
- `communications-management` → `pro/pm/pm-traditional/communications-management`
- `stakeholder-engagement-advanced` → `pro/pm/project-manager/stakeholder-engagement-advanced`
- `mistake-memory` → `solo/sdd/sdd/mistake-memory`

**Decision gate:**
> Required output: published postmortem with timeline + actions. No 'we'll publish later'.

### Stage 4: Preventive backlog

**Intent:** Action items become costed PRs slotted into the backlog with owners.

**Methodologies in chain:**
- `sec-codeql-autofix-on-pr` → `geek/sdlc-ai/sec-codeql-autofix-on-pr`
- `risk-register` → `pro/pm/pm-traditional/risk-register`
- `lessons-learned` → `pro/pm/pm-traditional/lessons-learned`
- `security-sast` → `pro/infra/cicd-engineer/security-sast`
- `security-dast` → `pro/infra/cicd-engineer/security-dast`
- `gitops-progressive-delivery` → `pro/infra/cicd-engineer/gitops-progressive-delivery`

**Decision gate:**
> Required: every action has an owner. Orphaned actions guarantee the next incident repeats.

## Common pitfalls

- AI auto-publishes the postmortem — destroys trust if it includes wrong facts
- Action items without owners — the repeat is just a matter of time
- Naming-and-shaming language — kills future psychological safety
- Skipping stakeholder comms — they hear about it from customers

## Quality checklist (self-review)

- Does the postmortem read as blameless and specific?
- Can I point to each action item's owner and due date?
- Did the risk register actually change as a result?

## Related playbooks

- `sentry-datadog-alert-triage`
- `rfc-to-production-feature-delivery`
- `biweekly-retro-mistake-memory`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **incident-comms-templates-internal-external** (tier `geek`, blocks stage 3) — Postmortem stage needs ready-to-send internal + external comms templates
- **postmortem-action-item-slo-tracking** (tier `geek`, blocks stage 4) — Preventive backlog stage needs SLO-style tracking for action-item completion

## CLI usage

```
faion get-content incident-postmortem-preventive-backlog --format md       # human-readable rendering
faion get-content incident-postmortem-preventive-backlog --format context  # agent-optimised context bundle
faion get-content incident-postmortem-preventive-backlog --format json     # raw structured form
```
