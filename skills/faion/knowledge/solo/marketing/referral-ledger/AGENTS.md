---
slug: referral-ledger
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Append-only ledger for affiliate / referral check + payout cycles — produces a versioned ledger spec with fixed columns, evidence links, retention policy."
content_id: "f50c54543d6941be"
complexity: medium
produces: spec
est_tokens: 4900
tags: [marketing, solo, referral, ledger, affiliate]
---
# Referral Ledger

## Summary

**One-sentence:** Append-only ledger for affiliate / referral check + payout cycles — produces a versioned ledger spec with fixed columns, evidence links, retention policy.

**One-paragraph:** Append-only ledger for affiliate / referral check + payout cycles — produces a versioned ledger spec with fixed columns, evidence links, retention policy. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Indie operator runs an affiliate / referral program with at least one payout cycle per month.
- A named owner is accountable for monthly check + payout (or escalates ownership formally).
- A version-controlled or wiki-style space exists where the ledger lives.
- The trigger event (check + payout) fires at a published cadence (monthly, quarterly).

## Skip If (ANY kills it)

- No affiliate / referral program exists — defer the methodology.
- Program runs on a third-party platform with auditable native ledger (Rewardful, FirstPromoter) — use the platform's report, do not duplicate.
- Cadence is irregular and unpublished — fix cadence first, then apply.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Referral Ledger task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `solo/sdd/sdd/AGENTS.md` | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end | 700 |
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
| `templates/referral-ledger.csv` | CSV ledger schema: append-only columns covering referrer, referred, evidence link, cycle, payout, status. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-referral-ledger.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[lifetime-deal-pricing]]
- [[outreach-crm-minimal-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
