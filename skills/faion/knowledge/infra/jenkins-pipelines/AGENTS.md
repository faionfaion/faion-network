# Jenkins Declarative Pipelines

## Summary

**One-sentence:** Declarative Jenkinsfile scaffold: typed parameters, parallel stages, Kubernetes pod agents, shared-library pinning and post-build cleanup.

**One-paragraph:** Declarative Jenkinsfile scaffold: typed parameters, parallel stages, Kubernetes pod agents, shared-library pinning and post-build cleanup. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `code` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-jenkins-pipelines.py` before publication.

**Ефективно для:**

- Міграція FreeStyle job → declarative Jenkinsfile.
- Налаштування Kubernetes agent pool.
- Pinning shared-library версій.

## Applies If (ALL must hold)

- Input matches the methodology scope (jenkins-pipelines) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `code` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Jenkins controller version | LTS minor + plugin set | ci team |
| Agent topology | static vs Kubernetes vs cloud agents + labels | platform team |
| Shared-library catalogue | available globals + versions | ci team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[github-actions-cicd]] | upstream context likely already loaded when this methodology fires |

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
| draft-code-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Jenkinsfile` | Working scaffold (Chart.yaml / Jenkinsfile / nginx.conf depending on slug) |
| `templates/_smoke-test.yaml` | Minimum viable filled-in version of the template used by `--self-test` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-jenkins-pipelines.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[github-actions-cicd]]
- [[gitlab-cicd]]
- [[gitops]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `declarative-default` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Jenkinsfile`

```text
@Library('shared-lib@v1.2.3') _
pipeline {
  agent {
    kubernetes { yaml libraryResource('agents/standard.yaml') }
  }
  options {
    timeout(time: 30, unit: 'MINUTES')
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '50'))
    disableConcurrentBuilds()
  }
  stages {
    stage('Build') { steps { sh 'make build' } }
    stage('Test') {
      parallel {
        stage('unit') { steps { sh 'make test-unit' } }
        stage('integration') { steps { sh 'make test-int' } }
        stage('scan') { steps { sh 'make scan' } }
      }
    }
    stage('Deploy') {
      when { branch 'main' }
      input { message 'Promote to prod?'; ok 'Deploy'; submitter 'release-managers' }
      steps { sh 'make deploy ENV=prod' }
    }
  }
  post {
    always { cleanWs() }
    failure { slackSend channel: '#deploy', message: "FAIL: ${env.JOB_NAME} #${env.BUILD_NUMBER}" }
  }
}
```

### `templates/_smoke-test.yaml`

```yaml
# Minimum viable filled-in code scaffold; consumed by --self-test.
{
  "slug": "jenkins-pipelines",
  "language": "yaml",
  "entrypoint": "Chart.yaml",
  "files": [
    "Chart.yaml",
    "values.yaml",
    "templates/deployment.yaml"
  ],
  "build_command": "helm lint .",
  "test_command": "helm template . | kubeconform -"
}
```
