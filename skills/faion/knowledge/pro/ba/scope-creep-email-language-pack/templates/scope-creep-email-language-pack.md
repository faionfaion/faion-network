<!-- purpose: working checklist skeleton for the Scope-Creep Email Language Pack methodology -->
<!-- consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml -->
<!-- produces: a checklist artefact validating against scripts/validate-scope-creep-email-language-pack.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~400-1200 tokens once filled -->

# Scope-Creep Email Language Pack — Artefact Skeleton

## Metadata

- `artefact_id`: <slug>-<client>-<YYYY-MM-DD>
- `owner`: Full Name <email>
- `version`: 1.0.0
- `last_reviewed`: 2026-05-23

## Body

Fill against the schema in `content/02-output-contract.xml`. Every section below maps to a required JSON field.

- `decision` / `summary` / `items` / `steps` — see schema for which applies to `produces: checklist`.
- `rationale` (when present) — cite at least one entry from `inputs_used` by name.
- `inputs_used` — list every input with `name` + `source` path/URL.

## Validation

Run `python scripts/validate-scope-creep-email-language-pack.py --file <path-to-filled-json>`. Exit 0 = valid, exit 1 = violations listed on stderr.
