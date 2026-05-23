# Methodology as JSON Feed

## Summary

**One-sentence:** JSON feed contract for `faion search --json` and `faion get-content --format json` so agents can consume faion methodology content as structured tool output, not Markdown prose.

**One-paragraph:** P7 ships agents -- agents read JSON, not Markdown. Faion had no `faion search --json` / `faion get-content --format json` contract documented as a methodology with a stable schema. Without it, P7 cannot embed faion as a context source. This methodology defines the JSON schema for both endpoints, the version-pinning rules, the pagination contract, and the citation block embedded in each item. Output is a stable JSON contract + verifier that downstream agents can rely on across faion releases.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «methodology as json feed» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- you build an AI agent that calls faion CLI as a tool to fetch methodology content.
- you need a parseable response format that survives faion content updates.
- you can pin the agent's adapter to a specific JSON schema version.

## Skip If (ANY kills it)

- you only read faion content as Markdown for human display.
- you embed faion content statically at build time and never call the CLI at runtime.
- your stack already adapts faion via a different protocol (RAG ingestion of raw files).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Methodology as JSON Feed task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdlc-ai/faion-cli-agent-adapter-pattern` | adapters consume this feed. |
| `pro/sdlc-ai/citation-contract-back-to-source` | supplies the citation block format. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/feed-schema.json` | JSON Schema draft-07 for both endpoints with citation + pagination. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-methodology-as-json-feed.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[faion-cli-agent-adapter-pattern]]
- [[citation-contract-back-to-source]]
- [[ai-debt-detection]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
