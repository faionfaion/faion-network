---
slug: pattern-bank-tagging-schema
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Closed-vocabulary tagging schema for the inspiration / patterns bank so future retrieval is deterministic and AI agents can pre-filter by surface, intent, and severity.
content_id: "402ed90fcf2e92e6"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["pattern-bank", "tagging", "schema", "ux", "retrieval"]
---
# Pattern Bank Tagging Schema

## Summary

**One-sentence:** Closed-vocabulary tagging schema for the inspiration / patterns bank so future retrieval is deterministic and AI agents can pre-filter by surface, intent, and severity.

**One-paragraph:** Inspiration banks rot when tags are free-text. This schema pins a closed vocabulary: surface (auth | checkout | dashboard | nav | onboarding | settings), intent (educate | persuade | confirm | warn | delight | navigate), pattern_type (anti | good | neutral), severity (0..4), and source (real-product URL | competitor screenshot | research paper). Every bank entry carries the four tags; agents pre-filter by tag before reading the full entry.

**Ефективно для:**

- Solo founder running weekly inspiration sweeps who needs deterministic recall after 6 months.
- AI agent doing competitive-design synthesis that must pre-filter the bank by tag.
- Design-review rituals where 'find me all the checkout anti-patterns' needs to return in <30s.
- Onboarding handoff where the new agent must browse the bank by surface.

## Applies If (ALL must hold)

- Pattern bank exists or is being created with ≥10 entries.
- At least one downstream consumer (designer, agent, search) will retrieve by tag.
- A canonical source for surface / intent / pattern_type lists exists or can be defined.
- Bank is editable in a structured format (JSON, YAML, Notion DB).

## Skip If (ANY kills it)

- Bank is freeform Pinterest board with no structured retrieval need.
- Single-author bank with <10 entries — overhead exceeds benefit.
- Bank is being deprecated; do not invest in tagging.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pattern bank entries list | array | Bank repository (Notion, JSON, repo) |
| Surface vocabulary list | array | Product taxonomy |
| Intent vocabulary list | array | Design-intent taxonomy |
| Severity rubric | rubric | heuristic-eval-severity-rubric output |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/anti-pattern-rationale-template` | Anti-pattern entries are bank-shape consumers. |
| `solo/ux/heuristic-eval-severity-rubric` | Severity values reused from the rubric. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | End-to-end worked example | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tag-entry` | sonnet | Per-entry judgement on surface / intent / pattern-type. |
| `dedupe-tag-coverage` | haiku | Deterministic coverage check across entries. |
| `vocabulary-refresh` | opus | Quarterly review of vocabulary against bank growth. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-bank-tagging-schema.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/pattern-bank-tagging-schema.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pattern-bank-tagging-schema.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[anti-pattern-rationale-template]]
- [[heuristic-eval-severity-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
