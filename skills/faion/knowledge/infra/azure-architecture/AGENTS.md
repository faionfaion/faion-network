# Azure Architecture (Well-Architected + Landing Zones)

## Summary

**One-sentence:** Produces an Azure architecture spec: 5-pillar WA evaluation + 8 Landing Zone design areas, with AVM+Bicep IaC and Zero-Trust identity model (ESLZ Terraform deprecated Aug 2026).

**One-paragraph:** Azure enterprise architecture is organised around two frameworks: Well-Architected (5 pillars — Reliability, Security, Cost, OpEx, Performance) and Landing Zones (8 design areas — Identity, Network, Mgmt-Group hierarchy, Policy, RBAC, Cost mgmt, Resource org, BCDR). The output is a spec naming the AVM+Bicep modules used, the policy initiative applied, the Entra-ID + Managed Identity model, the hub-spoke network shape, and the PIM-based privileged access pattern. Critical 2026 fact: legacy ESLZ Terraform module is deprecated — new deployments use AVM + Bicep only.

**Ефективно для:**

- Greenfield Azure workload with governance baseline.
- Org adopting Azure at scale (multiple subscriptions / teams).
- WA-pillar audit existing Azure deployment.
- Hub-spoke networking + Entra ID + PIM privileged access setup.
- On-prem migration following Cloud Adoption Framework patterns.

## Applies If (ALL must hold)

- Target cloud is Azure (any subscription tier).
- Multi-subscription OR compliance scope > basic.
- AVM + Bicep is an acceptable IaC choice (or org policy mandates Bicep).

## Skip If (ANY kills it)

- Single-subscription, single-team, no compliance — Landing Zone overhead is not justified.
- Non-Azure cloud (AWS, GCP).
- POC / sandbox env — apply minimal governance, not full LZ.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tenant + subscription map | list of mgmt groups + subs | Azure portal / az cli |
| Identity provider | Entra ID tenant + RBAC baseline | IT / IAM team |
| Compliance scope | SOC2 / GDPR / regional | GRC |
| Connectivity model | hub-spoke / VWAN / mesh | network team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[aws-well-architected-checklists]] | Cross-cloud pattern recognition; not directly used |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: avm-bicep-not-eslz-terraform, zero-trust-identity, policy-initiative-enforced, mg-hierarchy-3-levels-min, skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for Azure arch spec + valid/invalid + forbidden | 1000 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: eslz-terraform-still, network-perimeter-only, no-pim, no-policy | 900 |
| `content/04-procedure.xml` | essential | 6 steps: tenant model → MG hierarchy → policy → identity → network → BCDR | 900 |
| `content/05-examples.xml` | reference | Worked example: regulated SaaS adopting 3-MG hub-spoke | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on org size + compliance → LZ size | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-mg-hierarchy` | sonnet | Strategic — depends on compliance + org units. |
| `compose-spec` | sonnet | Assemble the doc from the canonical sections. |
| `validate-bicep` | haiku | Mechanical syntax + AVM-module-existence check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/azure-lz-spec.md` | Markdown skeleton for the Azure architecture spec |
| `templates/main.bicep` | Bicep skeleton using AVM modules (deployment-level) |
| `templates/policy-initiative.json` | Sample Azure Policy initiative JSON enforcing baseline controls |
| `templates/_smoke-test.json` | Minimum spec artefact used by validate-azure-architecture.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-azure-architecture.py` | Validate the spec artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[aws-well-architected-checklists]]
- [[backup-strategies]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when scoping a new Azure tenant or hardening an existing one.
