# Client Style Guide Importer

## Summary

**One-sentence:** Ingests a client's 30-80-page Markdown / Confluence / PDF style guide and emits a machine-readable `conventions.yaml`, lint config, and AI-agent rule pack -- with a manual review gate before any rule ships.

**One-paragraph:** Most clients hand a 30-80 page style guide on engagement bootstrap (Markdown, Confluence, PDF). A reusable pipeline that ingests it and emits machine-readable artefacts is the single highest-leverage gap for senior outsource devs. This methodology defines the extraction passes (TOC-aware chunking, rule-shaped clause detection, normalization to `conventions.yaml` shape), the manual review gate (every machine-extracted rule reviewed before ship), and the round-trip check (regenerate vs original to detect drift). Output is a `conventions.yaml` + lint config + AI-agent rule pack, each tagged with source-section IDs.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «client style guide importer» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- the client has a style guide >= 5 pages in a parseable format (Markdown, Confluence export, PDF with text layer).
- you have permission to extract and copy the guide's normative clauses into the repo.
- the downstream methodology `client-conventions-as-code` is in scope for the engagement.

## Skip If (ANY kills it)

- the style guide is image-scanned PDF with no text layer -- OCR + manual review is cheaper than this pipeline.
- the style guide is < 5 pages -- hand-author conventions.yaml directly.
- the client forbids machine extraction (legal restriction) -- escalate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Client Style Guide Importer task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/client-conventions-as-code` | downstream consumer of the imported rules. |
| `pro/sdlc-ai/citation-contract-back-to-source` | supplies the source-tagging contract for emitted rules. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
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
| `templates/conventions-import.yaml` | Skeleton: source-tagged candidate rules + review-gate signatures. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-style-guide-importer.py` | Validate the config artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[client-conventions-as-code]]
- [[ai-agent-guardrails-pack]]
- [[decision-log-reconstruction-from-git]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
