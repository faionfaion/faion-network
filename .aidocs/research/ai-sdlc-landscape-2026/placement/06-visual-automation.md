# Placement — Visual / No-Code Automation
**Slice:** n8n, Make, Dify, Flowise · **Author pass:** 6 of 10 · **Date:** 2026-08-04

## Verdict summary

| Tool | Exec a local binary | Dossier | Placement decision | Target path |
|---|---|---|---|---|
| n8n | **Yes** — self-hosted only, node off by default | 🟡 | 1 playbook + 1 gating methodology | `playbooks/build-ship/wire-faion-into-self-hosted-n8n/`, `knowledge/automation-tooling/unattended-automation-boundary/` |
| Make / Maia | **No** — On-Premise Agent is HTTP-only, Enterprise | 🔴 | Named-and-rejected line in the playbook's alternatives; no slug | `…/wire-faion-into-self-hosted-n8n/content/01-playbook.xml` |
| Dify | **No** — seccomp sandbox, self-host included | 🔴 | as Make | same file |
| Flowise | **Unconfirmed** — Custom Tool likely | 🟡 | Not shipped; open until a hands-on test | `../layer3-orchestration/visual-automation-tools.md` |

The boundary ("visual automation is needed only when something fires without you") **is right, and media-ops proves it**: `media-ops/decisions.xml` already rejected per-outlet cron for one central media-manager scheduler; n8n there would be a *third* orchestration surface. The boundary needs enforcing, not restating — hence a gate methodology, not a tooling one.

## Workflow changes

Only `media-ops`, only to close the door.

1. `media-ops/decisions.xml` — append `<decision date="2026-08-04" topic="unattended-scheduling-surface">`: **chose** media-manager cron as sole unattended trigger; **rejected** an n8n/visual layer; rationale = the exec gate plus the drift argument that killed per-outlet crontab on 2026-04-15.
2. `media-ops/content/07-anti-patterns.xml` — one `<rule>` in **Operations anti-patterns**, under the crontab rule it generalises: do NOT introduce n8n, Make, Dify or Flowise as an outlet scheduler or publisher.
3. `media-ops/AGENTS.md` frontmatter — `version: 2.0.0 → 2.1.0`, `last_verified: → 2026-08-04`. Body untouched; stays 64 lines.
4. `workflows/catalog.json` — mirror both fields.

`idea-to-prod` and `poll-agents` unchanged: their cron ticks are heartbeats under a present agent — the side of the boundary needing no visual tool.

## New content proposed

### 1. Methodology — `unattended-automation-boundary`
- **Domain:** `automation-tooling` · **Tier:** `solo` — all 20 existing slugs there are `solo`; its commonest output is "install nothing".
- **Produces:** an *Unattended Automation Record* (`decision-record`): trigger source (schedule / webhook / human-present), machine availability, blast radius, chosen surface (agent hooks → cron/systemd timer → n8n, in that order). Stop: human present at trigger time → `no-surface`.
- **Shape:** mirrors `context-graph-engineering/` — `AGENTS.md` (no frontmatter) + `CLAUDE.md` + `meta.json` + `content/{01-core-rules,02-output-contract,03-failure-modes,06-decision-tree}.xml` + `scripts/validate-unattended-automation-boundary.py` (`--self-test`) + 2 templates.
- **Slugs checked:** `backend/cron-automation`, `infra/cronjob-overrun-monitoring`, `infra/scheduled-job-decommission-checklist`, `product/backlog-hygiene-cron-checklist`, `operate-ritual/cron-scheduled-job-audit-monthly` — all operate an existing job; none gates whether a surface is warranted. Manifest grep for n8n/zapier/make/dify/flowise: zero hits.
- **Registration:** create dirs → `regen-tier-manifest.py` → hand-add one `<methodology slug tier path>` block to `automation-tooling/INDEX.xml` **and bump `count="20"` → `21`** → `validate-methodology-v2.py` + `-scripts.py` + `-templates.py` → `CHANGELOG.md`. Never `build-domain-index-v2.py`.

### 2. Playbook — `wire-faion-into-self-hosted-n8n`
- **Category:** `build-ship` (one-time wiring yielding a running artifact; sits beside the two faion-integration playbooks). **Tier:** `pro` — precedent `faion-as-programmatic-context-source`; self-hosting is pro-shaped.
- **Stages:** 0 gate (run the boundary methodology; exit unless a surface is named) → 1 self-host n8n → 2 re-enable Execute Command, **re-checking n8n#23439 first** → 3 `faion` binary + token *inside the container* → 4 Schedule/Webhook → Execute Command `faion search --json "<q>" --top 5` → 5 route JSON downstream → 6 guardrails.
- **Shape:** `AGENTS.md` + `CLAUDE.md` + `meta.json` + `content/01-playbook.xml`.
- **Registration:** `regen-tier-manifest.py` → hand-add a `<playbook>` row to `by-goal/build-ship/INDEX.xml`, bump `count="77"` → `78`, **using `path="skills/faion/playbooks/build-ship/…"`** — existing rows carry stale `playbooks/pro/<group>/…` paths absent from disk → `validate-playbook-v3.py`, `validate-playbook-taxonomy.py` → `CHANGELOG.md`.

## The non-technical on-ramp — committed answer

**(c): both halves of the truth, split by surface.** There is no no-code on-ramp and we say so plainly in docs and pricing copy; the low-code path ships as the `pro` playbook, for the minority who cross the self-host line. n8n is never marketed as a no-code entry.

What a non-technical user literally does:

1. Rent a VPS (~€5/mo) or dedicate an always-on machine.
2. Install Docker.
3. Bring up n8n from the compose file; set port/domain and basic auth.
4. Get the `faion` binary **into the n8n container** — Execute Command runs in the container, not the host: bind-mount or custom image.
5. Run `faion login` there once; persist the token to a mounted volume.
6. Set the node-allow env var; restart.
7. In the UI: Schedule Trigger → Execute Command (`faion search --json …`) → Telegram/HTTP node.
8. Toggle the workflow Active.

Steps 1, 2, 4 and 6 are not non-technical acts; step 4 alone ends it for most. Step 7 is the only one resembling the no-code product they were sold.

## Sealing risk

Step 7 enables it: an Execute Command node inside a **Loop Over Items** over a slug list is a bulk `get-content` extractor writing whole bodies into a customer-controlled store — a listing surface built from legitimate authenticated calls. Tier gating still applies per call, so this is a ToS problem, not an auth bypass. The guardrail stage must forbid looping `get-content` over a static slug list, require slugs to come from that run's live `search` result, and cap items per run. Reject any example workflow containing a slug array.

## Rejected

- **Make, any tier** — Enterprise + a self-run HTTP bridge restores the always-on process the visual tool was meant to remove.
- **Dify** — no path, self-hosted included.
- **Flowise playbook** — unverified exec claim; would ship an untested assertion as sold content.
- **A faion n8n community node** — same self-host constraint, plus an npm package and a second distribution surface.
- **n8n inside `media-ops` phases** — contradicts that workflow's 2026-04-15 cron decision.

## Risks / conflicts with other slices

- `workflows/media-ops/{decisions.xml,content/07-anti-patterns.xml,AGENTS.md}` — any slice also editing media-ops.
- `workflows/catalog.json` — version-bump collision, every workflow-touching slice.
- `knowledge/automation-tooling/INDEX.xml` — `count` collides with any slice adding here.
- `playbooks/by-goal/build-ship/INDEX.xml` — `count="77"` plus the stale-path defect hit every slice adding a build-ship playbook.
- `skills/tier-manifest.json` — regenerate **once**, after all ten slices land.
- `CHANGELOG.md` — pre-commit blocks without an entry; all slices append.
