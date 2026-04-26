# W3C Design Tokens Standard

## Summary

The W3C Design Tokens Community Group draft defines a vendor-neutral interchange format for design tokens using `$type` + `$value` + `$ref` fields. Adopting the draft format enables token files to survive tool migrations and work across Figma, Style Dictionary v4, and future tooling without conversion. The format is still a Community Group draft — not a W3C Recommendation — so pin a snapshot date and validate in CI on every PR.

## Why

Proprietary token formats (Tokens Studio JSON, Adobe Spectrum, old Style Dictionary input) lock systems into specific toolchains. The W3C draft provides a common schema that Style Dictionary v4 already consumes natively. Migration now avoids a forced re-migration when the ecosystem converges; `$description` fields preserve design intent that raw values discard.

## When To Use

- Migrating an existing token set to a vendor-neutral, future-proof format.
- Greenfield design systems aiming for interoperability across Figma, code, and documentation tools.
- Auditing token files for compliance with the latest community-group draft.
- Generating Style Dictionary transforms that consume W3C-formatted source.

## When NOT To Use

- Locked into a vendor format (Adobe Spectrum, IBM Carbon, Material 3) with no portability need — conversion adds overhead without gain.
- Pre-MVP products where the token contract is unstable — chasing a moving spec wastes cycles.
- Single-platform design systems where standardization gives no portability win.
- Agencies producing one-off campaign tokens — interchange is not worth it.

## Content

| File | What's inside |
|------|---------------|
| `content/01-format-rules.xml` | W3C draft field rules (`$type`, `$value`, `$ref`, `$description`), supported types, alias graph requirements. |
| `content/02-migration-and-gotchas.xml` | Migration workflow, CI validation pattern, agent pitfalls (dialect confusion, flattened aliases). |

## Templates

| File | Purpose |
|------|---------|
| `templates/tokens-w3c.json` | Minimal W3C-compliant token file with color, dimension, and alias examples. |
| `templates/w3c-tokens-validate.sh` | CI shell script that validates a token file against the W3C draft JSON Schema. |

## Scripts

none
