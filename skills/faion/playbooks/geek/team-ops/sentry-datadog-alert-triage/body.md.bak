# Sentry / Datadog alert triage (in-hours)

**Playbook slug:** `sentry-datadog-alert-triage`
**Tier:** geek
**Complexity:** medium
**Persona:** P6 — Product-Dev Team

## Intent

Alert fires → on-call triages within minutes → every alert closes with a verdict (noise / known / new incident) + audit log.

## Scope

An alert lands in production during business hours. On-call engineer triages within minutes using AI-classified context, decides: noise / known / new incident. Noise → mute with documented reason. Known → cross-link to existing thread + delta. New incident → enter the incident-postmortem-preventive-backlog playbook. Every alert closes with a written verdict + audit log entry.

### What this playbook covers

Three short stages: classify, investigate under read-only default, close with verdict. The discipline is the *every alert closes with a written verdict* rule. Without it, alerts accumulate as ambient anxiety and the team stops trusting the signal — which is the first step toward a real incident slipping through.

### Non-goals

- Out-of-hours paging escalation — runbook handles that
- Full postmortem flow — see `incident-postmortem-preventive-backlog`
- Alert engineering / reducing noise upstream — separate workstream

### Prerequisites

- Sentry / Datadog alerts wired with service-ownership map
- AI triage classifier in front of the alert stream
- Runbook system (markdown tagged steps)

## Success criteria

The playbook is done when:
- Every alert reaches a verdict within target SLA
- Audit log entry per alert with verdict + reasoning
- Noise alerts have a mute justification logged
- Known issues cross-linked to canonical thread
- New incidents handed off to postmortem flow

## Stages

### Stage 1: Receive + classify

**Intent:** AI classifier routes; on-call reads service-ownership map.

**Methodologies in chain:**
- `tracker-ai-triage-classify-route` → `geek/sdlc-ai/tracker-ai-triage-classify-route`
- `task-agent-fixable-triage-gate` → `geek/sdlc-ai/task-agent-fixable-triage-gate`
- `api-monitoring-alerting` → `pro/dev/software-developer/api-monitoring-alerting`
- `api-monitoring-metrics` → `pro/dev/software-developer/api-monitoring-metrics`
- `api-monitoring-logging` → `pro/dev/software-developer/api-monitoring-logging`

**Decision gate:**
> Advance only with an explicit verdict; "we'll see what it does" is not a verdict.

### Stage 2: Investigate under read-only default

**Intent:** If 'new', investigate read-only; respect approval-gate boundaries.

**Methodologies in chain:**
- `inc-read-only-investigation-default` → `geek/sdlc-ai/inc-read-only-investigation-default`
- `inc-runbook-as-markdown-tagged-steps` → `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `inc-tool-tier-approval-gate` → `geek/sdlc-ai/inc-tool-tier-approval-gate`
- `mistake-memory` → `solo/sdd/sdd/mistake-memory`

**Decision gate:**
> If escalation is needed, hand off to `incident-postmortem-preventive-backlog` cleanly. Don't keep investigating solo past 15 minutes.

### Stage 3: Close with verdict

**Intent:** Document verdict; trigger postmortem flow if needed.

**Methodologies in chain:**
- `inc-postmortem-auto-draft-no-publish` → `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`

**Decision gate:**
> Required: written verdict. An alert that closes silently is a future trap.

## Common pitfalls

- Muting a "noise" alert without documenting why — next on-call re-investigates from scratch
- Skipping read-only default — accidental writes during investigation
- Stretching investigation past 15 min instead of escalating
- Closing alerts in chat-only without an audit log

## Quality checklist (self-review)

- Can I point to every alert from yesterday and read its verdict?
- Did any noise mute carry an explicit reason and expiry?
- Did the new incidents hand off cleanly to the postmortem flow?

## Related playbooks

- `incident-postmortem-preventive-backlog`
- `daily-standup-ai-prebrief`
- `rfc-to-production-feature-delivery`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **alert-triage-decision-tree** (tier `geek`, blocks stage 1) — Classify stage needs a written decision tree for noise / known / new
- **service-ownership-map-template** (tier `geek`, blocks stage 1) — Classify stage references service ownership map but no concrete template exists

## CLI usage

```
faion get-content sentry-datadog-alert-triage --format md       # human-readable rendering
faion get-content sentry-datadog-alert-triage --format context  # agent-optimised context bundle
faion get-content sentry-datadog-alert-triage --format json     # raw structured form
```
