---
slug: terraform-modules-versioning
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Semantic versioning spec for Terraform modules: when to bump major/minor/patch, registry publishing flow, version pinning rules in consumers, deprecation policy.
content_id: "38f2ebf32707a74c"
complexity: medium
produces: spec
est_tokens: 4300
tags: [terraform, modules, versioning, semver, iac]
---
# Terraform Modules — Versioning

## Summary

**One-sentence:** Semantic versioning spec for Terraform modules: when to bump major/minor/patch, registry publishing flow, version pinning rules in consumers, deprecation policy.

**One-paragraph:** Semantic versioning spec for Terraform modules: when to bump major/minor/patch, registry publishing flow, version pinning rules in consumers, deprecation policy. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Модуль вживають >=2 проєкти — треба явна semver схема замість git ref-only.
- Останній реліз додав required input — це BREAKING; команда випустила це як minor і зламала споживачів.
- Consumers пінять модуль через git ref або latest — треба перевести на ~> X.Y.
- Команда планує deprecation старої версії модуля — потрібен policy + timeline.

## Applies If (ALL must hold)

- Cutting a new release of a shared Terraform module
- Deciding whether a change is breaking (major bump) or backward-compatible
- Configuring consumer module references with pessimistic version constraints
- Publishing the module to a Terraform Registry (public or private)

## Skip If (ANY kills it)

- Module composition — use terraform-modules-composition
- Module security — use terraform-modules-security
- Module structure — use terraform-modules-structure

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
| `scripts/validate-terraform-modules-versioning.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Is the goal to release, version, or pin a shared Terraform module?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
