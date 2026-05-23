<!-- purpose: Markdown skeleton for Indie Mini-CRM (Notion) indie-crm-spec artefact. -->
<!-- consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml -->
<!-- produces: a indie-crm-spec artefact validating against scripts/validate-indie-mini-crm-notion.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~400-1500 tokens once filled -->

# Indie Mini-CRM (Notion) — Artefact Skeleton

## Metadata

- `artefact_id`: <slug>-<client>-<YYYY-MM-DD>
- `owner`: <Full Name> <email>
- `version`: 1.0.0
- `last_reviewed`: 2026-05-23

## Sections

Fill against the schema in `content/02-output-contract.xml`. Each section below maps to a required JSON field.

- inputs_used — list every input with `name` + `source` (path or URL).
- findings — one item per rule-evidence pair, severity in [low, medium, high].
- decision / rationale — name the verdict and cite ≥1 input by name.

## Validation

Run `python scripts/validate-indie-mini-crm-notion.py --file <path-to-filled-json>`. Exit 0 = valid, exit 1 = violations listed on stderr.
