# GitLab CI/CD

## Summary

**One-sentence:** Generates a GitLab pipeline config (stages + jobs DAG via needs + rules + protected/masked variables + sast/secret scanning + cache/artifact split) for DevSecOps pipelines.

**One-paragraph:** Generates a GitLab pipeline config (stages + jobs DAG via needs + rules + protected/masked variables + sast/secret scanning + cache/artifact split) for DevSecOps pipelines. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- GitLab-hosted repos з integrated DevSecOps (SAST/DAST/secret-detect).
- Pipeline-as-DAG: needs замість лінійних stages для паралелізму.
- Multi-environment deploys з manual gates і environment protection.
- Reusable include-style pipelines між teams.

## Applies If (ALL must hold)

- Repository hosted on GitLab (self-managed or .com).
- Pipeline complexity ≥3 jobs with dependencies.
- DevSecOps requirements (SAST, secret scanning, dependency check).
- Multi-environment deploys (dev/staging/prod) with promotion gates.

## Skip If (ANY kills it)

- Repo on GitHub / Bitbucket / etc. — use the platform-native methodology.
- Single-job pipeline — GitLab template default is sufficient.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pipeline job list | YAML (name, stage, needs) | Eng team |
| Variable inventory | list (name, scope, masked) | Platform team |
| Environments + URLs | YAML | Platform team |
| Security scanner choices | list | Security team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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
| `draft-gitlab-cicd` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-instance.json` | JSON instance of a filled config artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

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
  "stages": [
    "build",
    "test",
    "security",
    "deploy"
  ],
  "jobs": [
    {
      "name": "build",
      "stage": "build",
      "needs": [],
      "rules": [
        {
          "if": "$CI_PIPELINE_SOURCE == 'merge_request_event'"
        }
      ]
    },
    {
      "name": "test",
      "stage": "test",
      "needs": [
        "build"
      ],
      "rules": [
        {
          "if": "$CI_PIPELINE_SOURCE == 'merge_request_event'"
        }
      ]
    },
    {
      "name": "sast",
      "stage": "security",
      "needs": [],
      "rules": [
        {
          "if": "$CI_PIPELINE_SOURCE == 'merge_request_event'"
        }
      ]
    },
    {
      "name": "deploy-prod",
      "stage": "deploy",
      "needs": [
        "test",
        "sast"
      ],
      "rules": [
        {
          "if": "$CI_COMMIT_BRANCH == 'main'",
          "when": "manual"
        }
      ]
    }
  ],
  "variables_policy": {
    "all_protected": true,
    "all_masked_when_sensitive": true
  },
  "security_scanners": [
    "sast",
    "secret_detection",
    "dependency_scanning"
  ],
  "environments": [
    {
      "name": "production",
      "url": "https://acme.io",
      "deployment_tier": "production"
    }
  ],
  "owner": "platform@team.io",
  "last_reviewed": "2026-05-23"
}
```
