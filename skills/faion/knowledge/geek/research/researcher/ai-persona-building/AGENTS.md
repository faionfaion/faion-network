# AI Persona Building (Automated Pipeline)

## Summary

Fully automated end-to-end persona generation for large user datasets (1,000+ users): Haiku ingests behavioral event exports via API, Opus validates cluster separability, Sonnet transforms clusters into JSON persona documents consumable by downstream agents. Human approval gate sits between Opus and Sonnet. Extends `ai-assisted-persona-building` with automation-specific schema, drift detection, and pipeline hardening rules.

## Why

At scale, manual review of clustering is infeasible. Automated pipelines enable monthly persona refresh but introduce new risks: silent schema breakage, weak-cluster propagation, and JTBD statements fabricated from behavioral data alone. Silhouette scoring, schema validation, and mandatory human gates prevent the most dangerous failure mode — confident wrong personas adopted without scrutiny.

## When To Use

- Automating persona generation as part of a recurring research pipeline (monthly cohort refresh).
- Building personas programmatically from large datasets where manual review of clustering is infeasible.
- Running JTBD map generation at scale across multiple product areas simultaneously.
- Integrating persona data into a downstream agent (copywriting, feature-priority) via stable JSON schema.

## When NOT To Use

- One-off persona creation for a single product decision — use `ai-assisted-persona-building` with direct team involvement.
- When data quality is unknown — run a data audit before feeding into the pipeline.
- When personas will be presented to external stakeholders without human review of the narrative layer.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline.xml` | Fully automated pipeline stages, schema requirements, drift detection rules. |
| `content/02-agent-workflow.xml` | Haiku/Opus/Sonnet roles, prompt patterns, silhouette gates, gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/validate-clusters.py` | Silhouette scoring across k range; recommends optimal k; flags weak clusters. |
| `templates/persona-schema-prompt.txt` | Prompt for generating structured persona JSON including data_confidence and assumptions fields. |
