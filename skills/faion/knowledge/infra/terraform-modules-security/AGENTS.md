# Terraform Modules — Security

## Summary

**One-sentence:** Per-module security checklist: sensitive var marking, no hardcoded secrets, encryption-by-default, least-privilege IAM, tfsec/checkov in module CI.

**One-paragraph:** Per-module security checklist: sensitive var marking, no hardcoded secrets, encryption-by-default, least-privilege IAM, tfsec/checkov in module CI. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Модуль має параметри типу db_password, api_key — потрібно явно sensitive = true.
- Модуль створює S3 / RDS / EBS — треба перевірити encryption at-rest за замовчуванням.
- tfsec / checkov ще не запускаються на модулі — публікація в registry без сканування заборонена.
- IAM policy у модулі має wildcard Action або Resource — треба урізати до least privilege.

## Applies If (ALL must hold)

- Module exposes resources that store data (S3, RDS, EBS, Secrets Manager)
- Module contains IAM policies or security group rules
- Module accepts sensitive input variables (DB passwords, API keys)
- Module is published to a registry consumed by external teams

## Skip If (ANY kills it)

- Module composition wiring — use terraform-modules-composition
- Module versioning + registry — use terraform-modules-versioning
- Module internal layout — use terraform-modules-structure

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trigger context | Markdown / ticket / transcript | upstream task |
| Named owner | string (handle, email, role) | team roster |
| Storage location | URL / repo path | artefact store |
| Prior cycle artefact (if any) | this methodology's output | last run |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/AGENTS.md` | parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/sdd` | SDD discipline for artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + run-the-checklist + skip-this-methodology conclusions | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid + invalid + forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom / root-cause / fix | ~700 |
| `content/04-procedure.xml` | essential | step-by-step procedure (input/action/output/decision-gate) | ~700 |
| `content/06-decision-tree.xml` | essential | root-question + branches + conclusion refs to 01-core-rules | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment over bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high or evidence chain is required |

## Templates

| File | Purpose |
|------|---------|
| `templates/checklist.md` | working skeleton matching the `produces=checklist` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-terraform-modules-security.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Does this module create data-at-rest resources, IAM policies, or accept sensitive variables?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
