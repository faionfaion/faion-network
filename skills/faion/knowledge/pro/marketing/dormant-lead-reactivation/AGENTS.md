---
slug: dormant-lead-reactivation
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Reactivation sequence for service-business dormant pipeline — past clients, lost proposals, nurture leads — 3-touch sequence per segment with explicit kill-rule and consent re-confirmation.
content_id: "5e4a389171a579f4"
complexity: medium
produces: spec
est_tokens: 3600
tags: [reactivation, dormant-leads, service-business, freelance, agency, lifecycle]
---
# Dormant Lead Reactivation

## Summary

**One-sentence:** Reactivation sequence for service-business dormant pipeline — past clients, lost proposals, nurture leads — 3-touch sequence per segment with explicit kill-rule and consent re-confirmation.

**One-paragraph:** B2C reactivation playbooks assume large lists + automated discounts. Service businesses (freelance + agency) have small pipelines where each name matters: past clients (high signal), lost proposals (medium), nurture leads (low). This methodology pins a 3-touch sequence per segment, each touch designed for the segment's prior context. Core rules: segments must not be conflated (past client ≠ lost proposal); each sequence has ≤3 touches before kill; first touch in non-EU jurisdictions re-confirms consent; every touch personalizes by referencing the prior interaction; outcomes are recorded (engaged / killed / pending) to feed the next quarter's plan.

**Ефективно для:**

- Freelancer / consultant — quarterly pipeline rebalance, 30-100 dormant contacts.
- Agency — re-engage past clients after 6-12 month gap.
- Service business with proposal pipeline — recover lost proposals after a quarter.
- Pipeline audit — segment + score dormants before mass reactivation.

## Applies If (ALL must hold)

- Service business with a tracked CRM / spreadsheet pipeline (≥30 dormant contacts).
- Quarterly portfolio rebalance (cash / clients / capacity) is a recurring ritual.
- Owner has consent + recent contact data per contact.
- Authority to send 1-to-few personalized emails (not bulk blasts).

## Skip If (ANY kills it)

- B2C business with large lists — use marketing automation, not this methodology.
- No CRM / pipeline tracking — fix pipeline tracking first.
- Contacts without consent for outbound (EU / UK / California etc.) — defer to legal.
- Past clients with explicit "do not contact" status — never reactivate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Dormant contact list | CSV / CRM export | CRM / spreadsheet |
| Prior interaction per contact | timeline / notes | CRM |
| Consent status (jurisdiction + opt-in date) | field | CRM |
| Outcome log (engaged / killed / pending) | table | CRM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[freelance-pilot-pricing]] | Reactivation offer often anchors on pilot pricing. |
| [[founder-led-qualification-rubric]] | Re-qualify dormants before deep effort. |
| [[late-invoice-dunning-sequence]] | Adjacent tone pattern; different goal. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: segment-distinct, max-3-touches, consent-reconfirm-first-touch, prior-context-reference, outcome-recorded | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the reactivation sequence spec + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: segment → score → draft sequence → send touch 1 → record outcomes | 700 |
| `content/05-examples.xml` | essential | Worked example: 47 dormant contacts segmented + 3 sequences drafted | 500 |
| `content/06-decision-tree.xml` | essential | Tree: segment + consent + score → sequence variant | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `segment-and-score` | sonnet | Per-contact judgment with bounded inputs. |
| `draft-touch-1-copy` | sonnet | Personalized copy, bounded by rules. |
| `lint-consent-and-personalization` | haiku | Schema + token check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/reactivation-spec.json` | JSON example of one reactivation sequence spec matching the output contract |
| `templates/sequence-touches.md` | Markdown skeleton for the 3-touch sequence per segment |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dormant-lead-reactivation.py` | Validate the sequence spec JSON against the schema | After draft; before send |

## Related

- [[freelance-pilot-pricing]]
- [[founder-led-qualification-rubric]]
- [[late-invoice-dunning-sequence]]
- [[experiment-verdict-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by segment + consent + score to one of three sequence variants and pins the rule from `01-core-rules.xml`. Use it before drafting copy — wrong segment-to-sequence mapping is the most common failure.
