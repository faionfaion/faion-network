# GitHub Actions CI/CD Hardening

## Summary

**One-sentence:** Hardened GitHub Actions workflow config: SHA-pinned third-party actions, minimal permissions, OIDC to cloud, fork-safe pull_request_target gating.

**One-paragraph:** Hardened GitHub Actions workflow config: SHA-pinned third-party actions, minimal permissions, OIDC to cloud, fork-safe pull_request_target gating. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `config` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-github-actions-cicd.py` before publication.

**Ефективно для:**

- Hardening існуючого workflow.yml перед публікацією.
- Перехід з repo-secrets на OIDC до cloud-провайдера.
- Аудит pull_request_target use cases та fork-trust gating.

## Applies If (ALL must hold)

- Input matches the methodology scope (github-actions-cicd) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `config` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repository inventory | list of repos + visibility + trust level | platform team |
| Cloud OIDC trust | IAM role + audience config per cloud | security team |
| Third-party action audit | current actions + versions in workflows | ci team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[gitlab-cicd]] | upstream context likely already loaded when this methodology fires |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output/gate per step | ~800 |
| `content/06-decision-tree.xml` | essential | Root-question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| gather-and-validate-inputs | haiku | Mechanical inventory + freshness check. |
| apply-core-rules | sonnet | Rule-by-rule reasoning over the inputs. |
| draft-config-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/workflow.yml` | Annotated configuration skeleton with required keys + comments per knob |
| `templates/_smoke-test.json` | Minimum viable filled-in version of the template used by `--self-test` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-github-actions-cicd.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[gitlab-cicd]]
- [[jenkins-pipelines]]
- [[iac-pr-review-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `pin-actions-by-sha` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/workflow.yml`

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-24.04
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
        with:
          persist-credentials: false
      - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502  # v4.0.2
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gha-ci
          aws-region: us-east-1
      - name: build
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: ./scripts/build.sh
```

### `templates/_smoke-test.json`

```json
{
  "slug": "github-actions-cicd",
  "version": "1.0.0",
  "settings": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  },
  "applied_to": [
    "prod"
  ],
  "notes": "Generated by github-actions-cicd methodology."
}
```
