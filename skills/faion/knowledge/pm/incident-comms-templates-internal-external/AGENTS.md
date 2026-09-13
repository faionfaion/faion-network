# Incident Comms Templates Internal External

## Summary

**One-sentence:** Ships ready-to-edit incident comms templates (status page + customer email + exec brief + internal channel) so outage minute-cost is not template-authoring time.

**One-paragraph:** Ships ready-to-edit incident comms templates (status page + customer email + exec brief + internal channel) so outage minute-cost is not template-authoring time. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** PM/IM-у під час інциденту — шаблони готові, не треба писати з нуля під тиском.

## Applies If (ALL must hold)

- The org runs a service with paying customers or a published SLA, and sees at least one P1 / P2 a quarter, so the four templates are exercised rather than written for a drawer.
- The incident runbook defines severity levels (P1-P4 or SEV1-4) the matrix can map to audiences, first-post deadlines and update intervals.
- A named incident commander and a communications lead are on rotation and can approve every external send.
- A status-page tool with component statuses and the four lifecycle states, a customer comms list and an exec distribution list exist.
- A game day or tabletop can be run at least quarterly so every template carries a `last_drilled` date inside 90 days.

## Skip If (ANY kills it)

- Pre-launch product with no customers and no SLA: there is nobody to post to; defer until the first paying customer.
- No on-call rotation or no named commander: templates without someone to approve the send rot; build the rotation first.
- A regulator mandates the incident notification format (banking, healthcare, telecoms): use the regulator's template and deadlines instead of this matrix.
- The only status channel is a shared internal chat with no public page: the highest severity cannot include the status page the rules require; stand one up first.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Severity definitions (P1-P4 or SEV1-4) with the audiences, first-post deadline and update interval per level | runbook table | incident-management runbook |
| Status-page tool with component list and the Investigating / Identified / Monitoring / Resolved states | API / UI | Statuspage / Atlassian Statuspage / equivalent |
| Customer comms list and the customer-email sender | CRM export | support tool |
| Exec brief recipients with the figures they need (customers, revenue at risk, SLA credits) | list | leadership roster / account team |
| On-call rotation naming the incident commander and comms lead per shift | rota | incident-management runbook |
| Previous `IncidentCommsBundle` with its `last_drilled` dates and past incidents | JSON, this contract | this methodology (prior cycle) |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/pm/distressed-project-diagnostic-script` | Project-level rescue — incident templates plug into it. |
| `geek/pm/exception-driven-standup-protocol` | Companion ritual for post-incident standups. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~2100 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for `IncidentCommsBundle`: severity x audience matrix with deadlines and intervals, token list, four templates with required tokens and `last_drilled`, per-incident updates with state / timestamp / impact / next update and external-review flags, internal post with named commander, five-field exec brief, Resolved block with postmortem date; valid + invalid examples, forbidden patterns | ~6750 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~1300 |
| `content/04-procedure.xml` | essential | 9 steps: matrix, token list, four templates, drill and stamp last_drilled; then per incident: internal post first, first external post inside the deadline, exec brief on one screen, updates on the interval through the states, Resolved with window and postmortem date | ~2250 |
| `content/05-examples.xml` | recommended | Complete checkout-api bundle with a P1 run from Investigating to Resolved in 91 minutes and a note per non-obvious value, and a bad bundle with the validator output and what the commander sees | ~4000 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~750 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-template-bundle` | haiku | Boilerplate fill across the four templates. |
| `severity-audience-mapping` | sonnet | Bounded judgement: which placeholders per severity. |
| `post-incident-narrative` | opus | Cross-channel synthesis for customer + exec. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Four-template bundle: status-page update, customer email, exec brief, internal channel — each with severity-aware placeholders. |
| `templates/skeleton.md` | Four-template bundle: status-page update, customer email, exec brief, internal channel — each with severity-aware placeholders. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-incident-comms-templates-internal-external.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[distressed-project-diagnostic-script]]
- [[exception-driven-standup-protocol]]
- [[delivery-maturity-rubric]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to ship the template bundle (paid service + recurring incidents + commander), block until commander rotation exists, or skip (pre-launch / no incidents). Run before authoring any template.
