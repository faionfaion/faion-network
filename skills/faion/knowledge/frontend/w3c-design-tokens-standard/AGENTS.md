# W3C Design Tokens Standard

## Summary

**One-sentence:** Generates a DTCG-compliant tokens.json with $type/$value/$description and {alias} references that round-trips between Figma, Style Dictionary v4, and native platforms.

**One-paragraph:** A methodology for authoring design tokens that conform to the W3C Design Tokens Community Group (DTCG) format module — using `$type`, `$value`, `$description`, and `{alias}` references — so that the same token file can round-trip between Figma, Style Dictionary v4, and native platforms without lossy remapping. The output is a validated tokens.json with primitive + semantic layers and a resolved alias map.

**Ефективно для:**

- Authoring a token source-of-truth that must round-trip Figma ↔ code.
- Migrating Style Dictionary, Theo, or Tokens Studio JSON to vendor-neutral DTCG.
- Setting up a shared token pipeline across web, iOS, Android, RN.
- Preparing for DTCG-aware tooling (Style Dictionary v4, Tokens Studio, Specify, Penpot).

## Applies If (ALL must hold)

- Token system has ≥50 tokens and ≥2 target platforms.
- Team commits to DTCG as the source of truth.
- Tooling that consumes DTCG is in place or scheduled.
- There is a primitive/semantic layer split (or willingness to introduce one).

## Skip If (ANY kills it)

- Single-platform single-app project — DTCG overhead unjustified.
- Fast spike or throwaway prototype.
- Team has no naming discipline yet — fix primitives/semantic split first via `token-organization`.
- Tooling cannot consume DTCG and migration not on roadmap.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Token inventory | raw token list with current platform values | design system owner |
| Naming convention | primitive vs semantic split documented | design system owner |
| Target platforms | Web / iOS / Android / RN list | tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[wcag-22-compliance]] | color tokens must satisfy contrast |
| [[vpat-acr-template]] | downstream — DTCG tokens feed VPAT a11y rows |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory` | haiku | Mechanical catalogue. |
| `dtcg-conversion` | sonnet | Naming + type judgment. |
| `contrast-check` | haiku | Pure arithmetic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tokens.json` | DTCG tokens.json skeleton with primitive + semantic layers |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-w3c-design-tokens-standard.py` | Validate w3c-design-tokens-standard artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[wcag-22-compliance]]
- [[vpat-acr-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on platform count, layer split, alias resolution, then contrast. Failure at any gate routes to the corresponding repair rule.
