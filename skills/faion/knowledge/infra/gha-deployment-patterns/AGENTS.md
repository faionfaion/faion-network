# GitHub Actions — Deployment Patterns

## Summary

**One-sentence:** Generates a CD config (staged deploys with environment protection + reusable workflows + composite actions + canary/blue-green choice + release automation with changelog).

**One-paragraph:** Generates a CD config (staged deploys with environment protection + reusable workflows + composite actions + canary/blue-green choice + release automation with changelog). The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Multi-env deploys (dev → staging → prod) з environment protection.
- Canary / blue-green rollouts з metric-based rollback.
- Centralized reusable workflows для DRY-up CD pipelines.
- Release automation: changelog generation + git tag + GitHub Release.

## Applies If (ALL must hold)

- Repository deploys to ≥2 environments (e.g. staging + prod).
- Deployment is automatable (no manual UI clicks required).
- Health metrics exist for the deployed service (HTTP 2xx ratio, P95 latency, error rate).
- Release cadence is at least weekly — automation overhead pays back.

## Skip If (ANY kills it)

- Single-env deploy without progression (a personal project).
- Deployments require manual UI steps that cannot be scripted — fix tooling first.
- No service health metrics — rollback gates have no signal to act on.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Environment list | YAML (name, url, approvers) | Platform team |
| Service health metrics | Prometheus / Datadog query refs | SRE |
| Reusable workflow library | repo + path | CI team |
| Release notes template | MD template | PM / engineering |

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
| `draft-gha-deployment-patterns` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-instance.json` | JSON instance of a filled config artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gha-deployment-patterns.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config-instance.json`

```json
{
  "environments": [
    {
      "name": "staging",
      "url": "https://staging.acme.io",
      "approvers": [],
      "branch_filter": "main"
    },
    {
      "name": "production",
      "url": "https://acme.io",
      "approvers": [
        "release-captain@team.io"
      ],
      "branch_filter": "main"
    }
  ],
  "reusable_workflow_ref": {
    "uses": "acme/cd-library/.github/workflows/deploy.yml",
    "version_tag": "v2.4.0"
  },
  "strategy": {
    "type": "canary",
    "rollout_steps": [
      "10%",
      "50%",
      "100%"
    ],
    "rollback_gate": {
      "metric": "http_5xx_ratio",
      "threshold": 0.02,
      "window_minutes": 5
    }
  },
  "release_automation": {
    "tag_pattern": "v{major}.{minor}.{patch}",
    "changelog_generator": "release-drafter",
    "release_artifacts": [
      "binary",
      "sbom"
    ]
  },
  "owner": "cd-lead@team.io",
  "last_reviewed": "2026-05-23"
}
```
