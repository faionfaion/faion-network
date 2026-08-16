# IaC CI/CD Patterns

## Summary

**One-sentence:** Pipeline spec (config) for Terraform/Pulumi CI: plan-on-PR + apply-on-merge gates, WIF auth, drift detection, atlantis/spacelift mode, environment promotion.

**One-paragraph:** Pipeline spec (config) for Terraform/Pulumi CI: plan-on-PR + apply-on-merge gates, WIF auth, drift detection, atlantis/spacelift mode, environment promotion. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Adding CI to an existing IaC repo (Terraform/Pulumi/CDK).
- Splitting plan/apply into PR / merge stages with required reviewers.
- Adding nightly drift detection on production state.
- Promoting changes across dev → staging → prod with explicit gates.

## Skip If (ANY kills it)

- Solo repo where the same engineer plans and applies on a laptop with no audit trail.
- Repos that have no IaC yet — adopt `iac-basics` first.

**Ефективно для:**

- Teams з ≥ 2 engineers що пишуть infra.
- GitOps targets (Atlantis / Spacelift / Env0).
- Multi-env promotion з changeset preview.
- Drift detection як nightly task.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing IaC repo + tool choice | repo | team |
| CI provider (GitHub Actions / GitLab / Buildkite) | CI service | platform team |
| WIF/OIDC binding to cloud SA | GCP/AWS resource | security team |
| Required-reviewer policy | branch protection | platform team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/iac-basics` | Tool / state / secret choices made. |

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
| `scripts/validate-iac-patterns-cicd.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[iac-basics]]
- [[iac-patterns-testing]]
- [[iac-patterns-module-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config.json`

```json
{
  "repo": "acme/infra-terraform",
  "ci_provider": "github-actions",
  "auth": "wif",
  "stages": [
    {
      "name": "plan",
      "trigger": "pr",
      "approvers": 0
    },
    {
      "name": "apply-dev",
      "trigger": "merge",
      "approvers": 1
    },
    {
      "name": "apply-prod",
      "trigger": "manual",
      "approvers": 2
    }
  ],
  "drift_detection": {
    "enabled": true,
    "schedule": "0 3 * * *"
  },
  "promotion_order": [
    "dev",
    "staging",
    "prod"
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
  "repo": "acme/infra-terraform",
  "ci_provider": "github-actions",
  "auth": "wif",
  "stages": [
    {
      "name": "plan",
      "trigger": "pr",
      "approvers": 0
    },
    {
      "name": "apply-dev",
      "trigger": "merge",
      "approvers": 1
    },
    {
      "name": "apply-prod",
      "trigger": "manual",
      "approvers": 2
    }
  ],
  "drift_detection": {
    "enabled": true,
    "schedule": "0 3 * * *"
  },
  "owner": {
    "name": "Olha Petrenko",
    "role": "platform lead"
  },
  "produced_at": "2026-05-23T10:00:00Z"
}
```
