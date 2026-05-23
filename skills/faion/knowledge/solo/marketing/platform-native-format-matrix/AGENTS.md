---
slug: platform-native-format-matrix
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Platform × format × cadence matrix for X / LinkedIn / threads / shorts — produces a per-post spec naming platform-native shape, hook style, and adaptation rule."
content_id: "93a5db42baff3ca0"
complexity: medium
produces: spec
est_tokens: 4900
tags: [marketing, solo, social, format, matrix]
---
# Platform Native Format Matrix

## Summary

**One-sentence:** Platform × format × cadence matrix for X / LinkedIn / threads / shorts — produces a per-post spec naming platform-native shape, hook style, and adaptation rule.

**One-paragraph:** Platform × format × cadence matrix for X / LinkedIn / threads / shorts — produces a per-post spec naming platform-native shape, hook style, and adaptation rule. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator posts on 2+ social platforms (X, LinkedIn, Threads, IG, TikTok, YouTube Shorts).
- Current state is cross-posting identical content across platforms (visible 'platform-native: no' tells).
- A named owner is responsible for the social cadence's engagement metrics.
- Source-of-truth for upstream content (build-log / newsletter / podcast) is available before adaptation.

## Skip If (ANY kills it)

- Operator posts on only one platform — single-platform format guides apply (`build-in-public-cadence`).
- Operator outsources social entirely — the agency owns the matrix; do not over-spec.
- Posts are paid ads with separate creative pipeline — different methodology (`ppc-manager`).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Platform Native Format Matrix task | recent notes / tickets / interviews | operator's inbox or system of record |
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
| `templates/format-matrix.csv` | CSV matrix: rows=upstream-content-type, columns=platform, cells=format-name + hook-shape + char-budget. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-platform-native-format-matrix.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[repurposing-matrix-template]]
- [[build-in-public-cadence]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
