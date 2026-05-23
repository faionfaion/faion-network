# Launch Retro Template

## Summary

**One-sentence:** Produces a marketing-specific launch retro artefact (5 sections + before/after metrics + keep/change/drop + one committed change) gated by a single accountable owner.

**One-paragraph:** Engineering retros (what shipped, what broke) miss the marketing dimensions of a launch. This methodology pins a 90-minute marketing retro: 5 sections (Audience reaction / Messaging fit / Creative performance / Channel ROI / Lessons), before/after metric per section, explicit Keep / Change / Drop decisions, and exactly one committed change with a named owner. Output: a launch-retro artefact.

**Ефективно для:**

- готова основа для повторюваної задачі «launch-retro-template» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Launch has shipped with ≥7 days of post-launch data.
- Metrics for before / after comparison are available.
- Named owner can be assigned for the committed change.

## Skip If (ANY kills it)

- Launch is mid-flight — wait for the data window.
- Operator wants an engineering-style retro — that runs separately.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pre-launch baseline metrics | dashboard / CSV | analytics |
| Post-launch metrics (≥7 days) | dashboard / CSV | analytics |
| Channel-by-channel ROI breakdown | spreadsheet | marketing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/content-marketer/messaging-house-template` | Messaging fit references the messaging house. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the launch-retro artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/launch-retro-template.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/launch-retro-template.json` | launch-retro JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-launch-retro-template.py` | Validate the launch-retro artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[messaging-house-template]]
- [[growth-webinar-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
