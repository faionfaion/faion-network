# AWS Multi-Account Landing Zone

## Summary

**One-sentence:** AWS landing zone spec: OU hierarchy (Security, Workloads, Sandbox, Suspended), Control Tower or homegrown baseline, SCP guardrails, baseline IAM Identity Center permission sets, log + audit accounts, cross-account network hub.

**One-paragraph:** AWS landing zone spec: OU hierarchy (Security, Workloads, Sandbox, Suspended), Control Tower or homegrown baseline, SCP guardrails, baseline IAM Identity Center permission sets, log + audit accounts, cross-account network hub. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Org has ≥ 3 AWS accounts under AWS Organizations (or will, within 6 months).
- Named platform-lead has authority to define OU + baseline.
- Compliance or scaling pressure justifies the LZ overhead.

## Skip If (ANY kills it)

- Single-account team with no scaling pressure.
- Mature LZ already exists with Control Tower + drift detection.
- Org is < 12 months from a re-org / acquisition that will reshape accounts.

**Ефективно для:**

- Org з ≥ 3 AWS accounts (multi-account from day 1).
- Команди що рухаються до Control Tower / homegrown landing zone.
- Compliance (SOC2 / ISO27001) з вимогою account isolation.
- Стандартизація onboarding нових команд / продуктів через нові OU + account vending.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev` | Parent role context. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-multi-account-landing-zone.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
