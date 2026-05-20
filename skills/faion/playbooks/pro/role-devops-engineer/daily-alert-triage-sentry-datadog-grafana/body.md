# Daily alert triage (Sentry / Datadog / Grafana)

**Slug:** `daily-alert-triage-sentry-datadog-grafana` · **Tier:** pro · **Complexity:** light

## Context

Inbox-zero on the alert console: each fired alert is either acknowledged with a follow-up ticket, silenced with an expiry + reason, or closed as auto-resolved noise. Pager handoff state reflects reality.

## Outcome

The playbook is done when each stage below has produced its artifact, the decision gate has been passed in writing, and the operator can show a teammate a clean evidence trail across the entire chain.

## Steps

### Step 1: Prepare

Achieve the 'prepare' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 2: Execute

Achieve the 'execute' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 3: Verify

Achieve the 'verify' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 4: Document

Achieve the 'document' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 5: Decide

Achieve the 'decide' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

## Decision points

Each stage in `playbook.yaml` carries an explicit `decision_gate`. Treat them as hard exits — do not advance on vibes. The two highest-stakes gates in this playbook:

- **Entry gate** — confirm prerequisites are real, not assumed. If a prerequisite is missing, stop and resolve it before starting Step 1.
- **Final gate** — the playbook closes with a written decision artifact. No 'see how it goes'.

## References

- `knowledge/geek/sdlc-ai/inc-read-only-investigation-default`
- `knowledge/geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `knowledge/pro/dev/software-developer/api-monitoring-alerting`
- `knowledge/pro/dev/software-developer/api-monitoring-logging`
- `knowledge/pro/dev/software-developer/microservices-observability`
- `knowledge/pro/infra/cicd-engineer/grafana-basics`
- `knowledge/pro/infra/devops-engineer/aiops`
- `knowledge/pro/infra/devops-engineer/devops-elk-queries-alerting`
