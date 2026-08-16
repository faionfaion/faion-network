# IaC Testing Patterns

## Summary

**One-sentence:** Test-pyramid spec (config) for IaC modules: validate/fmt/lint (unit), plan-diff (component), terratest/integration (real cloud), policy-as-code (OPA/Sentinel) gates.

**One-paragraph:** Test-pyramid spec (config) for IaC modules: validate/fmt/lint (unit), plan-diff (component), terratest/integration (real cloud), policy-as-code (OPA/Sentinel) gates. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Publishing a shared module that other teams will consume.
- Wiring CI checks for *.tf / Pulumi changes.
- Adding policy-as-code (OPA / Sentinel) gates on resource shape.
- Hardening a module against regressions caught only in production.

## Skip If (ANY kills it)

- Solo prototype with no consumers.
- Module already covered by an upstream test suite (registry-provided).

**Ефективно для:**

- Shared module з >= 3 consumers.
- Modules що ship з compliance constraints (CMEK / encryption).
- Pre-production environments що should mirror prod.
- Cost-impact resource changes (auto-scaling groups).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| IaC tool + module | repo | team |
| Test framework (terratest / kitchen-terraform / pulumi test) | lib | platform team |
| Sandbox cloud project / account | cloud env | platform team |
| Policy engine (OPA / Sentinel / Checkov) | binary | security team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/iac-patterns-module-design` | Module design rules. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Mechanical template fill from prerequisites table. |
| `populate-policy` | sonnet | Per-clause translation into config fields with judgment. |
| `review-breach-cases` | opus | Cross-engagement risk + failure-mode synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.json` | Config skeleton matching the output schema. |
| `templates/_smoke-test.json` | Minimum viable filled artefact. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-iac-patterns-testing.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[iac-patterns-module-design]]
- [[iac-patterns-cicd]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config.json`

```json
{
  "module_name": "vpc-network",
  "test_layers": {
    "unit": [
      "terraform fmt -check",
      "terraform validate",
      "tflint"
    ],
    "component": [
      "terraform plan -out plan.bin",
      "json-assert: resource_count==12"
    ],
    "integration": [
      "terratest examples/simple",
      "terratest examples/multi-region"
    ]
  },
  "policy_gates": [
    {
      "engine": "opa",
      "policies": [
        "no-public-buckets",
        "cmek-required",
        "no-primitive-roles"
      ]
    }
  ],
  "owner": {
    "name": "Olha Petrenko",
    "role": "platform lead"
  },
  "produced_at": "2026-05-23T10:00:00Z"
}
```

### `templates/_smoke-test.json`

```json
{
  "module_name": "vpc-network",
  "test_layers": {
    "unit": [
      "terraform fmt -check",
      "terraform validate",
      "tflint"
    ],
    "component": [
      "terraform plan -out plan.bin",
      "json-assert: resource_count==12"
    ],
    "integration": [
      "terratest examples/simple",
      "terratest examples/multi-region"
    ]
  },
  "policy_gates": [
    {
      "engine": "opa",
      "policies": [
        "no-public-buckets",
        "cmek-required",
        "no-primitive-roles"
      ]
    }
  ],
  "owner": {
    "name": "Olha Petrenko",
    "role": "platform lead"
  },
  "produced_at": "2026-05-23T10:00:00Z"
}
```
