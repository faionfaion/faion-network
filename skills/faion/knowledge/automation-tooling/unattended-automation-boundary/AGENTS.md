# Unattended Automation Boundary

## Summary

**One-sentence:** Produces an Unattended Automation Record that decides whether an automation runtime is warranted at all — the honest answer is usually "install nothing" — and, when one is, which of three surfaces is the cheapest that can actually express the trigger.

**One-paragraph:** Visual automation tools are bought as a general capability and are in fact a narrow one: they exist to make something happen when nobody is there. If every trigger in your system fires while you are present, your agent's own hooks and the scheduler already on the machine cover the whole surface, and adding a workflow builder buys a second orchestration layer whose only durable effect is drift between the two. So the gate is a single question — does anything have to fire with no human present — and most systems fail it. When something does pass, the escalation order is fixed: agent hooks, then the operating system's scheduler, then a self-hosted workflow runtime, and each step up must name what the step below could not express. The exec question decides the last step outright, because most of these tools cannot run a local binary at all: n8n can, self-hosted only, with the node disabled by default; Make's cloud cannot and its on-premise path is an HTTP bridge on an enterprise plan; Dify cannot even self-hosted, because its sandbox blocks exec; Flowise's custom function runs in a VM with process spawning removed.

**Ефективно для:**

- Anyone about to install n8n, Make, Zapier, Dify or Flowise because automation is the next obvious step.
- Solo operators whose "automation" is really an agent session they start themselves.
- A system that already has one scheduler and is about to grow a second.
- Any workflow that must shell out to a local binary — that requirement alone eliminates three of the four tools.

## Applies If (ALL must hold)

- Some piece of work is a candidate for running without you starting it.
- You control what gets installed, and installing something has a real cost — money, a machine, an update surface, a second place to look when something breaks.
- The triggers can be enumerated: you can list what would start each run and when.

## Skip If (ANY kills it)

- The runtime is already chosen for you by an employer or a client — you are operating it, not deciding it. Use the cron and job-operation methodologies instead.
- Nothing in the system is time- or event-triggered; everything begins with you typing.
- You are debugging or monitoring a job that already exists — see `cronjob-overrun-monitoring` and `cron-automation`.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Seven testable rules. R1 is the gate most systems fail; R2 fixes the escalation order and R3 the exec constraint. |
| `content/02-output-contract.xml` | The Unattended Automation Record: trigger inventory, the `no-surface` stop, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six ways an automation layer becomes the problem it was bought to solve. |
| `content/06-decision-tree.xml` | Routing from the trigger inventory and the exec requirement to a surface, or to none. |
| `scripts/validate-unattended-automation-boundary.py` | Validates a record; enforces the gate, the escalation justifications and the per-tool exec capability table. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/unattended-automation-record.yaml` | Fill-in record for a warranted surface; ships valid against the contract. |
| `templates/unattended-automation-record-none.yaml` | The gate-stop record — the most common correct outcome, and it installs nothing. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `cron-automation` — how to write and operate the job once this record says a scheduler is the right surface.
- `cronjob-overrun-monitoring` — what to watch after an unattended job exists; this methodology decides whether it should.
- `scheduled-job-decommission-checklist` — the other end of the lifecycle, for the surface this record retired.

## Capability facts, dated

Exec capability was assessed 2026-08-04 against vendor documentation and the projects' own issue trackers: n8n Execute Command runs on self-hosted instances only, is unavailable on n8n Cloud, and is excluded by default so it must be explicitly re-enabled; Make (and Maia) cannot execute a local binary — the On-Premise Agent is an HTTP bridge and an enterprise-plan feature; Dify cannot execute a local binary even self-hosted, because its code sandbox applies a seccomp policy that blocks exec syscalls; Flowise's Custom Function runs inside a JavaScript VM sandbox with `child_process` unavailable. Re-check before relying on any of these — this is exactly the class of fact that changes in a minor release.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/unattended-automation-record.yaml`

```yaml
#
# If every trigger has a human present, do NOT edit this file - use
# unattended-automation-record-none.yaml, which installs nothing.
# Validate:  validate-unattended-automation-boundary.py unattended-automation-record.yaml

system: "nightly ingest of an external partner feed into the reporting database"

# --- The gate (r1). human_present is the only field that decides it. ---
triggers:
  - name: "partner drops the feed"
    kind: webhook
    human_present: false
    when: "between 02:00 and 04:00 UTC, whenever their batch finishes"
  - name: "manual re-run after a bad batch"
    kind: manual
    human_present: true
    when: "next morning, by hand"

failing_trigger: >
  On 2026-07-19 the partner posted at 03:10 UTC and the feed was not ingested until
  11:00 the next morning, so the daily report went out on stale numbers.

# --- Escalation (r2). Each step up names a missing capability, not a convenience. ---
chosen_surface: os-scheduler
why_hooks_insufficient: >
  Agent hooks fire on events inside a session; there is no session at 03:00 and
  nothing starts one. This is a capability gap, not an ergonomics one.

# --- Exec (r3). Decides the last surface outright. ---
needs_local_exec: true

# --- Operating conditions (r4, r5). ---
host: "the reporting VPS, already running the database"
host_availability: always-on
blast_radius: >
  May write to the staging schema and to /var/log/ingest only. Holds the partner's
  read-only feed token and no database superuser credential. Cannot publish
  anywhere and cannot spend against a paid API.
stop_switch: "systemctl disable --now ingest.timer; the on-call runbook names it first"

# --- One surface only (r6). Everything considered goes here, not alongside. ---
rejected_surfaces:
  - surface: workflow-runtime
    reason: >
      A systemd timer already expresses "run when the file lands, retry three
      times". A runtime would add a service to secure, back up and update for no
      capability we lack - and would become the system's second scheduler.
  - surface: agent-hooks
    reason: "no session exists at the trigger time"
```

### `templates/unattended-automation-record-none.yaml`

```yaml
#
# This is the most common correct outcome. Do not add a host, a blast radius or a
# runtime below - the validator rejects them, because a record that answers `none`
# and then specifies a surface has not accepted its own verdict (r1).
# Validate:  validate-unattended-automation-boundary.py unattended-automation-record-none.yaml

system: "weekly content pipeline: research, draft, review, publish"

triggers:
  - name: "start the week's batch"
    kind: manual
    human_present: true
    when: "Monday morning, when I sit down"
  - name: "re-run a failed draft stage"
    kind: manual
    human_present: true
    when: "immediately, while looking at the failure"
  - name: "publish after review"
    kind: manual
    human_present: true
    when: "after I have read it"

failing_trigger: >
  None. Checked the last three months of runs to 2026-08-04: every one began with
  me starting it, and no run was delayed by the absence of a scheduler.

chosen_surface: none

rejected_surfaces:
  - surface: workflow-runtime
    reason: >
      Was about to install n8n. Every trigger has me present, so the agent session
      I start already runs the whole pipeline and its hooks already fire on its own
      events. n8n would add a second place for the logic to live and a second place
      to look when it breaks, with no capability I do not have.
  - surface: os-scheduler
    reason: "nothing is time-triggered; a cron entry would fire into an empty room"
```
