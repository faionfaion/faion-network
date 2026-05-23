---
slug: topical-authority
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Topical-authority development: pillar / cluster / supporting structure, entity coverage, internal-link graph — produces a topic-map spec for a chosen cluster."
content_id: "6875354fb217d4df"
complexity: deep
produces: spec
est_tokens: 4900
tags: [marketing, solo, seo, topical-authority, content-cluster]
---
# Topical Authority

## Summary

**One-sentence:** Topical-authority development: pillar / cluster / supporting structure, entity coverage, internal-link graph — produces a topic-map spec for a chosen cluster.

**One-paragraph:** Topical-authority development: pillar / cluster / supporting structure, entity coverage, internal-link graph — produces a topic-map spec for a chosen cluster. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator has picked one focused topic to win (not a multi-topic site).
- Existing or planned content inventory covers ≥1 pillar + ≥6 cluster posts.
- A named owner will publish on cadence and maintain the link graph.
- Live SERP analysis for the topic's head + long-tail queries is reachable.

## Skip If (ANY kills it)

- Site is multi-topic without focus — pick the focus topic first.
- Operator wants a single high-volume article — use `search-intent-to-brief` instead.
- Cluster cannot be sustained (no editorial capacity for 6+ posts) — defer.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Topical Authority task | recent notes / tickets / interviews | operator's inbox or system of record |
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
| `templates/topical-authority-map.md` | Markdown topic-map spec: pillar / cluster / supporting structure with entity coverage matrix and internal-link plan. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-topical-authority.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[seo-manager/seo-techniques]]
- [[search-intent-to-brief]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
