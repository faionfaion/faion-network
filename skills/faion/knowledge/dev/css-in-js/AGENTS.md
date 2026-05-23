# Css In Js

## Summary

**One-sentence:** Produces a CSS-in-JS strategy decision: zero-runtime (vanilla-extract / linaria / Panda) for RSC, runtime (emotion / styled-components) only for client SPAs; styled at module scope; transient props; TS theme augmentation.

**One-paragraph:** Produces a CSS-in-JS strategy decision: zero-runtime (vanilla-extract / linaria / Panda) for RSC, runtime (emotion / styled-components) only for client SPAs; styled at module scope; transient props; TS theme augmentation. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- A React project (any framework: Next, Remix, vanilla) considering or using a CSS-in-JS library.
- TypeScript is in use (theme typing is part of the deliverable).
- Decision is still open OR the team is auditing an existing setup.

## Skip If (ANY kills it)

- Project uses Tailwind / utility-first CSS exclusively — CSS-in-JS is out of scope.
- Project is non-React (Vue / Svelte / Solid) — load the framework-specific styling methodology.
- Project ships zero client JS (pure static site).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Output target path | string | constitution / SDD spec |
| Owner (role:person) | string | team roster |
| Trigger event | event/threshold/schedule | constitution |
| Evidence anchor (URL / ticket / commit) | string | upstream context |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/best-practices-2026` | React 19 / Next 15 baseline this decision plugs into. |
| `free/dev/software-developer/documentation` | Documents the file table + AGENTS.md pair this methodology depends on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to css-in-js | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/04-procedure.xml` | medium | Step-by-step procedure (when complexity >= medium) | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold the output skeleton | sonnet | Mechanical, deterministic. |
| Refine domain-specific content | opus | Needs judgement. |
| Validate against output contract | sonnet | Schema check, deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/css-in-js-detect.sh` | Heuristic scanner: detects emotion/styled-components/vanilla-extract usage and reports library. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-css-in-js.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

- [[best-practices-2026]] — see methodology AGENTS.md for context.
- [[code-review]] — see methodology AGENTS.md for context.
- [[documentation]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.
