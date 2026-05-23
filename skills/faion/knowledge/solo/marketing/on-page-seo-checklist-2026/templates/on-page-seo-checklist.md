<!-- purpose: Markdown checklist with required-pass items grouped by section (meta / structure / schema / AEO / internal-links). -->
<!-- consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml -->
<!-- produces: a checklist artefact validating against scripts/validate-on-page-seo-checklist-2026.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~400-1500 tokens once filled -->

# On Page SEO Checklist 2026 — Artefact Skeleton

## Metadata

- `artefact_id`: <slug>-<context>-<YYYY-MM-DD>
- `owner`: <Full Name> <email>
- `version`: 1.0.0
- `last_reviewed`: 2026-05-23

## Sections

Fill against the schema in `content/02-output-contract.xml`. Each section below maps to a required JSON field for `produces: checklist`.

- inputs_used — list every input with `name` + `source` (path or URL).
- decision / findings / sections / items — see schema for which applies.
- rationale (when present) — cite at least one entry from `inputs_used` by name.

## Validation

Run `python scripts/validate-on-page-seo-checklist-2026.py --file <path-to-filled-json>`. Exit 0 = valid, exit 1 = violations listed on stderr.
