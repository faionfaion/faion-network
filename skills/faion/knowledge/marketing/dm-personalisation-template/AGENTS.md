# DM Personalisation Template

## Summary

**One-sentence:** Produces a cold-DM outreach artefact (10 prospects + 1-line personalisation each + ask + tracking) gated by the no-SDR-script rule and a per-prospect citation.

**One-paragraph:** Solo operators blast 50-prospect cold DMs with SDR-cliché openers and get filtered as spam. This methodology pins a per-prospect personalisation pattern: batches of 10, each DM carries a 1-line personalisation citing a specific public artefact, no SDR clichés, one explicit ask matching relationship stage, and per-prospect response tracking. Output: a DM-batch artefact for ongoing iteration.

**Ефективно для:**

- готова основа для повторюваної задачі «dm-personalisation-template» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator has access to ≥10 public-artefact-rich prospect profiles per batch.
- Operator can commit to ≤10 DMs per batch (not bulk).
- Operator has a tracking surface for response status.

## Skip If (ANY kills it)

- Operator's audience has zero public footprint — personalisation impossible.
- Operator wants 100+/day volume — wrong methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prospect shortlist (10 with public artefacts) | spreadsheet | research |
| DM opener pattern (non-cliché) | doc | operator |
| Response tracking column | spreadsheet / CRM | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/` | Parent group / operating context. |
| `solo/marketing/content-marketer/indie-mini-crm-notion` | CRM substrate tracking the batches. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the dm-personalisation artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/dm-personalisation-template.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/dm-personalisation-template.json` | dm-personalisation JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dm-personalisation-template.py` | Validate the dm-personalisation artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[indie-mini-crm-notion]]
- [[growth-reddit-marketing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
