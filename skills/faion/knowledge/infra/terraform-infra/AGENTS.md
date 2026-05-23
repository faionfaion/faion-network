# Terraform (Advanced)

## Summary

**One-sentence:** Production-grade Terraform project spec: directory layout, state architecture, CI/CD plan-then-apply gates, tfsec/checkov scanning, OIDC auth, Atlantis flow, drift detection.

**One-paragraph:** Production-grade Terraform project spec: directory layout, state architecture, CI/CD plan-then-apply gates, tfsec/checkov scanning, OIDC auth, Atlantis flow, drift detection. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Проєкт з >=2 env (dev/staging/prod) і >=2 компонентами (network/compute/db) — потрібна реальна blast-radius ізоляція.
- Команда вже мала інцидент через re-plan між review і apply або через VPA Auto без state lock.
- CI pipeline має включати tfsec/checkov і блокувати CRITICAL/HIGH без exception.
- OIDC-автентифікацію треба замінити статичні ключі в CI; static keys заборонені політикою.

## Applies If (ALL must hold)

- Designing multi-environment Terraform project layout (environments/dev|staging|prod + modules/)
- Setting up CI/CD pipelines (GitHub Actions, GitLab CI, Atlantis) with plan-then-apply gates
- Implementing security scanning (tfsec, Checkov) in the pipeline
- Deciding workspaces vs directory-per-environment isolation
- Implementing drift detection + tagging compliance

## Skip If (ANY kills it)

- HCL syntax basics or first Terraform project — use terraform-basics
- State backend configuration and import operations — use terraform-state
- Module development and versioning patterns — use terraform-modules-*

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
| `content/05-examples.xml` | essential | one worked end-to-end example with inputs and final artefact | ~700 |
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
| `templates/spec.md` | working skeleton matching the `produces=spec` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-terraform.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Is this a multi-environment Terraform project requiring isolated state + CI plan-apply gates?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
