---
slug: client-handover-package
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a handover-package report at engagement end — runbook, ops surface, credentials transfer log, SLA, open items, training plan — that closes a client engagement cleanly.
content_id: "chp1.0.0handover"
complexity: medium
produces: report
est_tokens: 3800
tags: [client-engagement, handover, freelance, runbook, ops, knowledge-transfer]
---
# Client Handover Package

## Summary

**One-sentence:** Produces a sign-off-gated handover package at engagement end: runbook, credentials transfer log, open items, training plan, and a 30-day support window definition — the artefact the client confirms before payment closes.

**One-paragraph:** Solo dev / outsource engagement ends fail predictably in three ways: client cannot run the system without you, credentials remain in your password manager, and "I'll send the docs Monday" never happens. This methodology pins the close: 7 sections of the handover package, each with a checkbox the client signs off. Includes a runbook (start / stop / debug), credential transfer log with rotation evidence, open items list with risk per item, 30-day support window terms, and a knowledge-transfer record (recordings / sessions / docs). Output is a versioned report committed to the client repo (or shared drive) — the artefact a future audit can read to understand what was delivered.

**Ефективно для:**

- Solo dev / outsource lead closing a client engagement and avoiding "what about X?" pings three months later.
- Multi-client agency standardising close — same artefact shape regardless of client.
- Liability protection: signed handover record evidences scope-completion for invoice + dispute defense.
- Knowledge transfer to a successor consultant — the package is their day-1 read.

## Applies If (ALL must hold)

- An engagement is ending OR a major handoff is happening (e.g. consultant rotation).
- The client has named a successor (in-house engineer OR new consultant).
- Working credentials, runbook fragments, and open-items list are available to capture.
- The engagement length warrants the handover overhead (typically ≥4 weeks).

## Skip If (ANY kills it)

- Single PR fix engagement — no system to hand over.
- Client refuses successor identification — escalate; close without handover is high risk.
- Existing handover record &lt; 30 days old.
- System being decommissioned — different closeout methodology applies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Engagement scope record | doc | client + consultant |
| Working credentials list | secrets vault | consultant |
| Runbook draft | Markdown | consultant |
| Open items list | tracker | consultant |
| Successor name + email | string | client |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/client-conventions-intake` | Sibling: the intake record at engagement start. |
| `solo/dev/ci-quality-gate-design` | CI design is one of the handover sections. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: 7 sections, credential transfer evidence, open items with risk, named successor, signed sign-off, 30-day window, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for handover package + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: vague runbook, untransferred secrets, open items hidden, no successor | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: draft → transfer secrets → review → sign-off → archive | 700 |
| `content/06-decision-tree.xml` | essential | Tree: sections complete? secrets transferred? successor named? signed? → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `runbook-from-repo` | sonnet | Compose start/stop/debug runbook from CI + deploy scripts. |
| `open-items-risk` | sonnet | Score each open item: severity + effort + blast radius. |
| `transfer-checklist` | haiku | Mechanical: per-credential transfer line items. |

## Templates

| File | Purpose |
|------|---------|
| `templates/client-handover-package.json` | JSON Schema for the handover artefact. |
| `templates/handover-package.md` | Markdown skeleton with the 7 sections. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-handover-package.py` | Validate handover JSON against schema + sign-off rule. | End of engagement, before final invoice. |

## Related

- [[client-conventions-intake]] — engagement-start sibling.
- [[ci-quality-gate-design]] — CI design is one section of the handover.
- [[changelog-automation-conventional-commits]] — release history at handover.

## Decision tree

See `content/06-decision-tree.xml`. The tree checks 7-section completeness, credential transfer evidence (rotated + acknowledged), open items each with risk score, named successor, and signed sign-off by both consultant and client. Leaves emit `archive-and-close`, `block-missing-sections`, `block-secrets-not-transferred`, `block-no-successor`, or `block-no-signoff`. Each leaf references a rule in `01-core-rules.xml`.
