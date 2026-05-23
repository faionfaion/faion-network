---
slug: search-intent-to-brief
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Convert a target query into a structured content brief — intent class, must-cover entities, JTBD framing, SERP-feature inventory — produces a brief spec drafters cannot ignore."
content_id: "54158e9655d2ec69"
complexity: medium
produces: spec
est_tokens: 4900
tags: [marketing, solo, seo, search-intent, brief]
---
# Search Intent To Brief

## Summary

**One-sentence:** Convert a target query into a structured content brief — intent class, must-cover entities, JTBD framing, SERP-feature inventory — produces a brief spec drafters cannot ignore.

**One-paragraph:** Convert a target query into a structured content brief — intent class, must-cover entities, JTBD framing, SERP-feature inventory — produces a brief spec drafters cannot ignore. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- A single target query (head term or long-tail) is selected for content.
- Live SERP for that query is reachable (manual or API).
- Output will be handed to a drafter (human or AI), not used internally.
- Tier == solo or higher (gating enforced by tier-manifest).

## Skip If (ANY kills it)

- Query has zero search volume (CTR is meaningless) — pick a different target.
- Site is non-indexable or staged — fix indexing first.
- Drafter has no contract authority — briefs become suggestions and are ignored.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Search Intent To Brief task | recent notes / tickets / interviews | operator's inbox or system of record |
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
| `templates/search-intent-brief.md` | Markdown brief: intent / entities / JTBD / SERP-features / contract blocks per rule. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-search-intent-to-brief.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[on-page-seo-checklist-2026]]
- [[seo-manager/seo-techniques]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
