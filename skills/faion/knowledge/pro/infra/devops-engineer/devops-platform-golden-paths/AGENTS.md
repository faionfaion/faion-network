---
slug: devops-platform-golden-paths
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a golden-path catalogue: template inventory (new service / database / API), required guardrails (CI, observability, security scans), opt-out policy, and adoption metric.
content_id: "6bf55bb9f71d3753"
complexity: medium
produces: config
est_tokens: 4400
tags: [golden-paths, templates, platform, self-service, adoption]
---
# Golden Paths: Opinionated Self-Service Templates

## Summary

**One-sentence:** Generates a golden-path catalogue: template inventory (new service / database / API), required guardrails (CI, observability, security scans), opt-out policy, and adoption metric.

**One-paragraph:** Generates a golden-path catalogue: template inventory (new service / database / API), required guardrails (CI, observability, security scans), opt-out policy, and adoption metric. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Перший "new-service-in-15-minutes" experience через Backstage Software Template.
- Database / Cache provisioning as self-service з вбудованою observability.
- Standardized API scaffolders з OpenAPI + linting + auth defaults.
- Adoption tracking (golden-path use % vs ad-hoc).

## Applies If (ALL must hold)

- Org has ≥3 repeatable provisioning tasks (new service, new DB, new pipeline).
- Platform team can own the templates and respond to issues within 24h.
- Adoption can be measured (use vs ad-hoc).

## Skip If (ANY kills it)

- Templates would freeze pre-product-market-fit experimentation.
- Platform team capacity below 0.5 FTE — templates rot.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task inventory | list of repeatable provisioning tasks | Platform |
| Guardrail set | table (CI / obs / sec) | Platform / Security |
| Adoption metric | definition | Platform PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/devops-platform-idp-core/AGENTS.md` | IDP framing |
| `pro/infra/devops-engineer/devops-platform-backstage/AGENTS.md` | Template host |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-devops-platform-golden-paths` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-platform-golden-paths.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-platform-idp-core]]
- [[devops-platform-backstage]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
