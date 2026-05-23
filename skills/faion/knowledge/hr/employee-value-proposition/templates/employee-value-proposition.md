<!-- purpose: working spec skeleton for the Employee Value Proposition (EVP) methodology -->
<!-- consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml -->
<!-- produces: a spec artefact validating against scripts/validate-employee-value-proposition.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~400-1200 tokens once filled -->

# Employee Value Proposition (EVP) — Artefact Skeleton

## Metadata

- `artefact_id`: <slug>-<client>-<YYYY-MM-DD>
- `owner`: Full Name <email>
- `version`: 1.0.0
- `last_reviewed`: 2026-05-23

## Body

Fill against the schema in `content/02-output-contract.xml`. Every section below maps to a required JSON field.

- `decision` / `summary` / `items` / `steps` — see schema for which applies to `produces: spec`.
- `rationale` (when present) — cite at least one entry from `inputs_used` by name.
- `inputs_used` — list every input with `name` + `source` path/URL.

## Validation

Run `python scripts/validate-employee-value-proposition.py --file <path-to-filled-json>`. Exit 0 = valid, exit 1 = violations listed on stderr.
