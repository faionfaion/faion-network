---
slug: decimal-as-string-pattern
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: For money, prices, exact decimals, large IDs, phone numbers, and any value where lossy float conversion would corrupt data, declare the schema field as `str` with a regex `pattern`, not `float` or `number`.
content_id: "65e6151170ae1998"
tags: [schemas, structured-output, decimal, money, precision]
---
# Decimal as Pattern-Constrained String

## Summary

**One-sentence:** For money, prices, exact decimals, large IDs, phone numbers, and any value where lossy float conversion would corrupt data, declare the schema field as `str` with a regex `pattern`, not `float` or `number`.

**One-paragraph:** For money, prices, exact decimals, large IDs, phone numbers, and any value where lossy float conversion would corrupt data, declare the schema field as `str` with a regex `pattern`, not `float` or `number`. The receiving side parses with `Decimal()` (or the language equivalent) only after the model has produced a known-good token sequence. The pattern constraint is enforced at sampling time on strict-mode and grammar-backed decoders, so the model cannot emit `19.999` when the schema demands two decimal places.

## Applies If (ALL must hold)

- Currency (USD, EUR, BTC, etc.) — always.
- Exact decimals in finance, science, or engineering reports.
- Big integers larger than 2^53 (JSON number cannot hold them safely).
- Account numbers, credit cards, phone numbers, postal codes, ISBNs.
- Version strings (semver), date-time stamps when ISO-8601 is mandatory.

## Skip If (ANY kills it)

- Counts, ranks, indices, scores — `int` is fine and saves tokens.
- Floating-point measurements where a few ULPs of drift do not matter (sensor noise, ML scores).
- Free-form numerics where the format is genuinely unknown — pattern-less string is safer than a wrong pattern.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ai-agents/`
