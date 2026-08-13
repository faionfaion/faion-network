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
- `inc-read-only-investigation-default` → `sdlc-ai/inc-read-only-investigation-default`
- `inc-tool-tier-approval-gate` → `sdlc-ai/inc-tool-tier-approval-gate`
- `inc-runbook-as-markdown-tagged-steps` → `sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `tracker-ai-triage-classify-route` → `sdlc-ai/tracker-ai-triage-classify-route`
- `microservices-circuit-breaker` → `dev/microservices-circuit-breaker`
- `lb-high-availability` → `infra/lb-high-availability`

**Decision gate:**
> Advance once user-facing impact is contained AND a senior engineer has confirmed read-only default was respected.

### Stage 2: Root cause

**Intent:** Walk logs, metrics, traces; chaos-eval evidence; reconstruct causal chain.

**Methodologies in chain:**
- `devops-elk-queries-alerting` → `infra/devops-elk-queries-alerting`
- `elk-stack-logging` → `infra/elk-stack-logging`
- `grafana-basics` → `infra/grafana-basics`
- `prometheus-monitoring` → `infra/prometheus-monitoring`
- `aiops-cicd` → `infra/aiops-cicd`
- `chaos-eval-fault-injection` → `ai-agents/chaos-eval-fault-injection`

**Decision gate:**
> Advance when the causal chain spans technical + organisational layers (not just 'a config was wrong').

### Stage 3: Postmortem — drafted, human-published

**Intent:** AI drafts; humans edit + publish. Blameless tone enforced.

**Methodologies in chain:**
- `inc-postmortem-auto-draft-no-publish` → `sdlc-ai/inc-postmortem-auto-draft-no-publish`
- `communications-management-pm-traditional` → `pm/communications-management-pm-traditional`
- `stakeholder-engagement-advanced` → `pm/stakeholder-engagement-advanced`
- `mistake-memory` → `sdd/mistake-memory`

**Decision gate:**
> Required output: published postmortem with timeline + actions. No 'we'll publish later'.

### Stage 4: Preventive backlog

**Intent:** Action items become costed PRs slotted into the backlog with owners.

**Methodologies in chain:**
- `sec-codeql-autofix-on-pr` → `sdlc-ai/sec-codeql-autofix-on-pr`
- `risk-register-pm-traditional` → `pm/risk-register-pm-traditional`
- `lessons-learned-pm-traditional` → `pm/lessons-learned-pm-traditional`
- `security-sast` → `infra/security-sast`
- `security-dast` → `infra/security-dast`
- `gitops-progressive-delivery` → `infra/gitops-progressive-delivery`

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
