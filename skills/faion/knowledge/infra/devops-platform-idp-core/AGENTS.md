# Internal Developer Platform (IDP) Core Model

## Summary

**One-sentence:** Generates an IDP charter: platform mission, target personas, capability inventory (provisioning / observability / cost / security), success metrics, and product-team ownership model.

**One-paragraph:** Generates an IDP charter: platform mission, target personas, capability inventory (provisioning / observability / cost / security), success metrics, and product-team ownership model. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Перший рік platform team — від "shared SRE" до product team.
- Capability map: provisioning, observability, secrets, cost, dev experience.
- Persona-driven roadmap (dev / SRE / Sec / Finance).
- DORA + platform-adoption metrics як north star.

## Applies If (ALL must hold)

- Org has ≥50 engineers OR ≥20 services and infra cognitive load is rising.
- Leadership is willing to fund a dedicated platform team (≥3 engineers).
- Product mindset (PM / metrics / roadmap) can be applied to the platform.

## Skip If (ANY kills it)

- Org <20 engineers — informal SRE rotation is cheaper.
- No leadership commitment to fund a platform team — IDP rots without funding.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Persona research | table (persona, top pains) | Platform PM |
| Capability gap matrix | list (capability, today, target) | Platform PM |
| Success metrics | DORA + adoption + NPS | Platform PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | upstream context not required |

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
| `draft-devops-platform-idp-core` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-platform-idp-core.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-platform-backstage]]
- [[devops-platform-golden-paths]]
- [[devops-platform-policy-finops]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
