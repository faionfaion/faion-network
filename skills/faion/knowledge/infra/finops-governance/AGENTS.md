# FinOps OPERATE Phase — Governance and Cost Gates

## Summary

**One-sentence:** Generates an OPERATE-phase config (automated policies + tiered budget alerts + dev/test auto-stop + CI/CD cost gates via Infracost) that sustains optimization without manual policing.

**One-paragraph:** Generates an OPERATE-phase config (automated policies + tiered budget alerts + dev/test auto-stop + CI/CD cost gates via Infracost) that sustains optimization without manual policing. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Sustain phase після optimize-sprint: автомат не дає waste re-accumulate.
- Pre-merge cost gates: Infracost блокує PR з cost-blowup.
- Tiered budget alerts: 50% notify, 80% warn, 100% page on-call.
- Compliance audit: показати automated policies замість ручних audit-loops.

## Applies If (ALL must hold)

- INFORM + OPTIMIZE phases complete (tag coverage ≥80%, waste rate ≤25%).
- Budgets per team / product exist with named owners.
- CI/CD pipeline reaches IaC (Terraform / Pulumi / CloudFormation).
- Automation runtime (Lambda / GitHub Actions / Azure Function) available.

## Skip If (ANY kills it)

- INFORM not done — automated gates fire on noisy data; fix tagging first.
- No IaC — pre-merge cost gates have nothing to evaluate.
- No budget owners — alerts go unanswered.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-team budget allocation | YAML (team, monthly_budget_usd) | Finance |
| IaC repos list | JSON | Platform team |
| Alert channel registry | YAML (team → channel) | FinOps Lead |
| Automation runtime | Lambda / Actions setup | Platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

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
| `draft-finops-governance` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finops-governance.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
