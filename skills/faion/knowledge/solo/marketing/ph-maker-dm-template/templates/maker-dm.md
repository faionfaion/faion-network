<!-- purpose: Markdown DM spec: hook line, ask line, evidence line, follow-up cadence, anti-spam guardrails. -->
<!-- consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml -->
<!-- produces: a spec artefact validating against scripts/validate-ph-maker-dm-template.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~400-1500 tokens once filled -->

# PH Maker DM Template — Artefact Skeleton

## Metadata

- `artefact_id`: <slug>-<context>-<YYYY-MM-DD>
- `owner`: <Full Name> <email>
- `version`: 1.0.0
- `last_reviewed`: 2026-05-23

## Sections

Fill against the schema in `content/02-output-contract.xml`. Each section below maps to a required JSON field for `produces: spec`.

- inputs_used — list every input with `name` + `source` (path or URL).
- decision / findings / sections / items — see schema for which applies.
- rationale (when present) — cite at least one entry from `inputs_used` by name.

## Validation

Run `python scripts/validate-ph-maker-dm-template.py --file <path-to-filled-json>`. Exit 0 = valid, exit 1 = violations listed on stderr.
