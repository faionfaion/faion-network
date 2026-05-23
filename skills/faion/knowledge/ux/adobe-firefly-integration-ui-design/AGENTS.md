# Adobe Firefly Integration

## Summary

**One-sentence:** Produces a Firefly Services REST client that batch-generates commercial-safe images, applies Generative Fill to placeholder regions, and audits prompts for brand compliance.

**One-paragraph:** Adobe Firefly Services exposes commercial-safe generative endpoints (text-to-image, generative-fill, generative-expand, vectorisation) trained only on Adobe Stock + public-domain. The agent surface is the REST API, not the desktop UI. This methodology produces a Firefly client that batch-generates assets from structured prompts, runs them through a brand-compliance audit (forbidden terms, style adherence, alt-text), and stores outputs with provenance metadata so downstream tools can prove commercial safety.

**Ефективно для:** design ops engineer, що масово генерує commercial-safe imagery (e-commerce, marketing) і потребує provenance + audit trail.

## Applies If (ALL must hold)

- Generating commercial-safe imagery at scale (≥10 assets per pipeline run).
- Brand compliance must be auditable (forbidden terms + style adherence).
- Output must carry provenance metadata (model version + prompt hash + Adobe content credentials).

## Skip If (ANY kills it)

- Single ad-hoc image — use the desktop UI.
- Output goes to a context that prohibits AI-generated imagery (some news / editorial).
- Commercial safety not required — cheaper open-source models suffice.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Adobe Firefly Services API credentials | secret | secrets manager |
| Brand prompt rules (forbidden + required terms) | YAML | brand team |
| Asset request batch | JSON array of prompt + dimensions + style | marketing |
| Output bucket + provenance metadata schema | config | ops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-plugin-ecosystem]] | Plugin vs REST API boundary. |
| [[figma-ai-ecosystem]] | Companion design-platform surfaces. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end. | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-code` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/firefly_client.py` | Python client: OAuth + batch submit + poll + provenance attach. |
| `templates/brand-rules.yaml` | Brand pre-filter rules skeleton (forbidden + required terms + style adherence). |
| `templates/_smoke-test.json` | Filled minimum-viable single-asset request. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-adobe-firefly-integration.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-plugin-ecosystem]]
- [[figma-ai-ecosystem]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the code; mis-routing leads to producing the wrong artefact shape.
