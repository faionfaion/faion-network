<!--
purpose: Terraform Modules — Prompts - spec skeleton matching `produces=spec`
consumes: typed inputs from AGENTS.md Prerequisites table
produces: filled spec artefact validated by scripts/validate-terraform-modules-prompts.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~600 tokens for a typical instance
-->
# Terraform Modules — Prompts — {artefact_id}

| Field | Value |
|-------|-------|
| artefact_id | {artefact_id} |
| produces | spec |
| owner | {owner} |
| version | {version} |
| last_reviewed | {YYYY-MM-DD} |
| status | draft \| active \| review \| deprecated |

## Inputs used

- {input-name} — {source-uri-or-path}

## Decision

{one-line decision the artefact records}

## Rationale

{>=40 chars; must cite at least one item from "Inputs used"}

## Trace refs

- {ticket / commit / transcript id}
