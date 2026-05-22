---
slug: w3c-design-tokens-standard
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The W3C Design Tokens Community Group draft defines a vendor-neutral interchange format for design tokens using `$type` + `$value` + `$ref` fields.
content_id: "dd8560575ef51023"
tags: [design-tokens, w3c, design-systems, style-dictionary, standards]
---
# W3C Design Tokens Standard

## Summary

**One-sentence:** The W3C Design Tokens Community Group draft defines a vendor-neutral interchange format for design tokens using `$type` + `$value` + `$ref` fields.

**One-paragraph:** The W3C Design Tokens Community Group draft defines a vendor-neutral interchange format for design tokens using `$type` + `$value` + `$ref` fields. Adopting the draft format enables token files to survive tool migrations and work across Figma, Style Dictionary v4, and future tooling without conversion. The format is still a Community Group draft — not a W3C Recommendation — so pin a snapshot date and validate in CI on every PR.

## Applies If (ALL must hold)

- Migrating an existing token set to a vendor-neutral, future-proof format.
- Greenfield design systems aiming for interoperability across Figma, code, and documentation tools.
- Auditing token files for compliance with the latest community-group draft.
- Generating Style Dictionary transforms that consume W3C-formatted source.

## Skip If (ANY kills it)

- Locked into a vendor format (Adobe Spectrum, IBM Carbon, Material 3) with no portability need — conversion adds overhead without gain.
- Pre-MVP products where the token contract is unstable — chasing a moving spec wastes cycles.
- Single-platform design systems where standardization gives no portability win.
- Agencies producing one-off campaign tokens — interchange is not worth it.

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

- parent skill: `pro/ux/ui-designer/`
