---
slug: postmortem-action-item-slo-tracking
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Append-only ledger that tracks every postmortem action item against an SLO (P1<2w, P2<6w) with named owner, evidence link, and a published review cadence.
content_id: "28261d371cb5191a"
complexity: medium
produces: report
est_tokens: 3700
tags: [postmortem, action-items, slo, incident-response, tracking]
---
# Postmortem Action Item SLO Tracking

## Summary

**One-sentence:** Append-only ledger that tracks every postmortem action item against an SLO (P1<2w, P2<6w) with named owner, evidence link, and a published review cadence.

**One-paragraph:** Auto-drafted postmortems exist and incident retros happen, but tracking action-item completion against an SLO (e.g. P1 fixes &lt; 2 weeks, P2 &lt; 6 weeks) is the chronic failure point. This methodology pins the artefact shape — append-only ledger, fixed column schema, named owner, evidence anchor on every row, published review cadence, archive-not-delete retention — so the incident → postmortem → preventive backlog loop stops being folklore and becomes a reviewable operating tool with measurable SLO compliance.

**Ефективно для:**

- Команда з постмортем-культурою, але без tracking action-items.
- Repo / wiki space, де артефакти versioned і ownable.
- Recurring cadence (weekly / monthly review) з named owner.
- SLO-driven org (P1 &lt; 2w, P2 &lt; 6w) для preventive actions.

## Applies If (ALL must hold)

- Team runs postmortems on incidents (&gt;= 3 per year).
- Team has a published action-item SLO (e.g. P1 &lt; 2w, P2 &lt; 6w).
- A named owner is accountable for ledger refresh + outcome review.
- Ledger lives in a version-controlled or wiki-style space.

## Skip If (ANY kills it)

- Team has &lt; 3 incidents per year — review cadence cost &gt; return.
- One-shot work with no recurrence — write a single doc, not a ledger.
- Regulated context mandates a different shape — use the regulator's template.
- No named owner available — defer until ownership resolved.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Action-item SLO policy | Markdown | lead |
| Tracker integration | Linear / Jira / GitHub Issues | platform |
| Ledger location | repo path or wiki page | platform |
| Named owner | person + role | mgmt |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[regression-eval-before-fix-rule]] | Decides whether incident needs eval-replay before fix. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/05-examples.xml` | essential | Worked report example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-ledger` | haiku | Mechanical template fill. |
| `populate-evidence-fields` | sonnet | Per-row judgement: select correct evidence, summarise. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/ledger-skeleton.md` | Canonical ledger header + first-row example with all required columns. |
| `templates/review-digest.md` | Weekly review digest skeleton (SLO compliance %, overdue items, archived this period). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-postmortem-action-item-slo-tracking.py` | Validate ledger artefact against schema + forbidden patterns. | Pre-merge of every ledger change |

## Related

- [[regression-eval-before-fix-rule]]
- [[task-agent-drafts-spec-before-coding]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (incident count, SLO policy presence, owner availability) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether to spin up a ledger — the tree terminates either on the active rule or on `skip-this-methodology`.
