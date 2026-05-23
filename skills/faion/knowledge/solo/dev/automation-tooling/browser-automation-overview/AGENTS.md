---
slug: browser-automation-overview
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Routing layer: compare Puppeteer vs Playwright using the feature matrix and pick one — load the sibling methodology (puppeteer-*, playwright-automation, web-scraping-*) for implementation.
content_id: "6a4adc6cf5506ced"
complexity: light
produces: decision-record
est_tokens: 3400
tags: [browser-automation, puppeteer, playwright, routing, headless]
---
# Browser Automation Overview

## Summary

**One-sentence:** Routing layer: compare Puppeteer vs Playwright using the feature matrix and pick one — load the sibling methodology (puppeteer-*, playwright-automation, web-scraping-*) for implementation.

**One-paragraph:** Routing layer: compare Puppeteer vs Playwright using the feature matrix and pick one — load the sibling methodology (puppeteer-*, playwright-automation, web-scraping-*) for implementation. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Need to pick a headless browser library for a new automation project.
- Migrating between Puppeteer and Playwright and need a comparison frame.
- Choosing between testing-focused vs scraping-focused automation strategy.
- Output produces `decision-record` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Need to pick a headless browser library for a new automation project.
- Migrating between Puppeteer and Playwright and need a comparison frame.
- Choosing between testing-focused vs scraping-focused automation strategy.

## Skip If (ANY kills it)

- Tool already chosen and in production — go straight to the implementation methodology.
- Need API-only test (no JS rendering) — use HTTP clients (httpx, axios).
- Workload is one-time data export — use a one-off Python script with requests.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Use-case classification | list of target sites + auth needs + browser features | team |
| Language preference | Python / TypeScript / Node | team |
| Scale | single-run / batch / parallel / serverless | team |

## Assumes Loaded

none

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-use-case` | haiku | Map use-case to feature matrix row. |
| `pick-tool` | sonnet | Reasoning over feature trade-offs. |
| `hand-off` | haiku | Generate hand-off pointer to the right sibling methodology. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision_record.json` | Decision record: tool picked + rationale + sibling methodology to load next |
| `templates/feature_matrix.md` | Puppeteer vs Playwright vs web-scraping feature matrix |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-browser-automation-overview.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[playwright-automation]]
- [[puppeteer-launch-setup]]
- [[web-scraping-resilience]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Does the workload need JS rendering AND is the tool not already chosen?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
