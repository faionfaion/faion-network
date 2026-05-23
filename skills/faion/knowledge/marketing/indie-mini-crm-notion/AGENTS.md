# Indie Mini-CRM (Notion)

## Summary

**One-sentence:** Produces a 4-database Notion CRM artefact (Contacts + Outreach + Partners + Touches) with linked relations and 3 rituals (morning batch + weekly partner review + monthly community pulse).

**One-paragraph:** Indie hackers operate many-to-many flows (subscribers + partners + DM outreach) that HubSpot doesn't fit and a single spreadsheet collapses past ~50 contacts. This methodology pins a 4-database Notion workspace (Contacts + Outreach + Partners + Touches) with linked relations, closed contact-type enum, a last_touch_date pattern, three rituals (morning outreach batch + weekly partner review + monthly community pulse), and templated outreach. Output: an indie-CRM workspace spec.

**Ефективно для:**

- готова основа для повторюваної задачі «indie-mini-crm-notion» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Indie operator has ≥30 active contacts but no CRM.
- Operator already uses Notion or is willing to.
- Operator can commit to the 3 weekly + monthly rituals.

## Skip If (ANY kills it)

- Operator already runs a paid CRM (HubSpot / Pipedrive) and wants to migrate to it.
- Operator refuses Notion as the substrate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing contact list | CSV / spreadsheet | current store |
| Outreach template drafts | doc | operator |
| Notion workspace access | workspace URL | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/dm-personalisation-template` | Outreach methodology feeding the Outreach DB. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the indie-crm-spec artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/indie-mini-crm-notion.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/indie-mini-crm-notion.json` | indie-crm-spec JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-indie-mini-crm-notion.py` | Validate the indie-crm-spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[dm-personalisation-template]]
- [[growth-newsletter-growth]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
