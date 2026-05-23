# SEO & AEO Mastery

## Summary

**One-sentence:** Comprehensive SEO + AEO audit covering technical / on-page / hreflang / schema / llms.txt / Core Web Vitals / accessibility — produces a per-site audit report.

**One-paragraph:** Comprehensive SEO + AEO audit covering technical / on-page / hreflang / schema / llms.txt / Core Web Vitals / accessibility — produces a per-site audit report. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator is running a full SEO + AEO audit on a single site (new or existing).
- Site is indexable, has at least 10 content URLs, and GSC + analytics are connected.
- A named owner will triage findings into a 4-week remediation backlog.
- Source-of-truth for content inventory (sitemap / CMS export) is available.

## Skip If (ANY kills it)

- Single-page audit only — use `on-page-seo-checklist-2026` instead.
- Content strategy is the actual question — `content-marketer` instead.
- Site is staged / non-indexable — fix indexing first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the SEO & AEO Mastery task | recent notes / tickets / interviews | operator's inbox or system of record |
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
| `templates/seo-aeo-audit-report.md` | Markdown audit report: pillar-by-pillar findings, evidence anchors, prioritised remediation backlog. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-seo.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[seo-manager/seo-basics]]
- [[seo-manager/seo-techniques]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
