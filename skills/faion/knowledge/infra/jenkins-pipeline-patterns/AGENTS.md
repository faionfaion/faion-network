# Jenkins Pipeline Patterns

## Summary

**One-sentence:** Generates production-grade Declarative Jenkinsfiles + version-pinned Shared Libraries + isolated parallel stages + K8s pod templates for brownfield orgs.

**One-paragraph:** Advanced Jenkins pipeline patterns for production-grade Declarative pipelines, Shared Libraries, scripted escapes, and reusable components across an organization. Covers Declarative-by-default with Scripted only inside `script { }`, Shared Library directory structure + CPS serialization rules, parallel stages with workspace isolation + lock(), Kubernetes pod templates with explicit resource requests/limits, and full pipeline options for timeout + buildDiscarder + concurrent-builds policy. Aimed at brownfield orgs with 50+ pipelines where standardisation matters more than raw speed.

**Ефективно для:**

- 50+ pipelines в одній організації, потребують shared library з єдиним стандартом.
- CPS-сериалізація: уникнути `NotSerializableException` на годинах робіт через `@NonCPS`.
- Parallel matrix builds (cross-OS / cross-JDK / cross-Node) з resource-aware агентами.
- Kubernetes pod templates з explicit requests/limits та dedicated service accounts.
- Migration: монолітні Jenkinsfile → модулярні `vars/`-функції з pinned `@Library('lib@v1.2.3')`.

## Applies If (ALL must hold)

- Brownfield organization running a Jenkins controller (LTS) with no migration off Jenkins on the roadmap.
- You need a Groovy Shared Library to enforce conventions across 50+ pipelines.
- Matrix or fan-out builds across multiple OS / JDK / Node axes.
- Heavy on-prem / air-gapped scenarios with Vault or Artifactory integration.
- Existing investment in Jenkinsfile + plugin ecosystem + team Groovy familiarity.

## Skip If (ANY kills it)

- Greenfield repo on GitHub or GitLab — use native CI; Jenkins adds operator burden with no upside.
- Solo dev or small team — controller maintenance outweighs benefits.
- Workloads that fit cleanly into GitHub Actions reusable workflows or composite actions.
- Ephemeral / serverless CI requirements — Jenkins is stateful and assumes a long-lived controller.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing Jenkinsfile or pipeline spec | Groovy / Markdown | repo / team |
| Shared Library repo URL | git URL | platform team |
| Library version tag | semver tag | release manager |
| Agent strategy | label / docker / kubernetes | infra |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[jenkins-basics]] | Declarative + JCasC + zero-controller-executors fundamentals. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: declarative-with-script-escape, shared-lib-dedicated-repo, library-version-pinned, parallel-workspace-isolation, pod-resources-required, options-required | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-pattern` | sonnet | Decision among shared-lib / parallel / matrix variants. |
| `write-shared-lib-var` | opus | CPS serialization + Groovy idiom judgement. |
| `lint-cps-issues` | haiku | Mechanical regex audit for `Pattern.compile`, `each {}`, `@NonCPS`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Jenkinsfile.declarative` | Declarative pipeline with parallel stages + options + post handlers |
| `templates/shared-library-var.groovy` | `vars/buildApp.groovy` skeleton enforcing CPS-safe patterns |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-jenkins-pipeline-patterns.py` | Validate the pipeline-pattern artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[jenkins-basics]]
- [[github-actions-basics]]
- [[gitlab-cicd]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (pipeline count, library presence, parallelism need, agent type) to a concrete pattern variant, each leaf referencing a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Jenkinsfile.declarative`

```text
@Library('platform@v1.4.2') _

pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-agent
  containers:
  - name: node
    image: node:20-alpine
    command: [cat]
    tty: true
    resources:
      requests: { cpu: "500m", memory: "512Mi" }
      limits:   { cpu: "1",    memory: "1Gi"   }
  - name: helm
    image: alpine/helm:3.14
    command: [cat]
    tty: true
    resources:
      requests: { cpu: "100m", memory: "128Mi" }
      limits:   { cpu: "500m", memory: "512Mi" }
'''
        }
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '50', artifactNumToKeepStr: '10'))
        disableConcurrentBuilds()
        timestamps()
        ansiColor('xterm')
    }

    stages {
        stage('Install') {
            steps {
                container('node') {
                    sh 'npm ci --cache .npm --prefer-offline'
                }
            }
        }

        stage('Validate') {
            parallel {
                stage('Lint') {
                    steps {
                        dir("branch-lint") {
                            container('node') {
                                sh 'npm run lint'
                            }
                        }
                    }
                }
                stage('Type Check') {
                    steps {
                        dir("branch-typecheck") {
                            container('node') {
                                sh 'npm run typecheck'
                            }
                        }
                    }
                }
            }
        }

        stage('Test') {
            steps {
                container('node') {
                    sh 'npm test -- --coverage'
                }
            }
            post {
                always { junit testResults: 'junit.xml', allowEmptyResults: true }
            }
        }

        stage('Deploy Prod') {
            when { branch 'main' }
            options { lock(resource: 'prod-deploy') }
            input { message 'Deploy to production?'; ok 'Deploy' }
            steps {
                container('helm') {
                    withCredentials([file(credentialsId: 'kubeconfig-prod', variable: 'KUBECONFIG')]) {
                        deployToK8s release: 'myapp', chart: './charts/myapp'
                    }
                }
            }
        }
    }

    post {
        always { cleanWs() }
        failure {
            notifySlack channel: '#ci-alerts', color: 'danger'
        }
    }
}
```

### `templates/shared-library-var.groovy`

```groovy
import java.util.regex.Pattern

def call(Map config = [:]) {
    String language = config.get('language')
    String buildCommand = config.get('buildCommand')
    Integer timeoutMin = config.get('timeoutMin', 15)

    if (!language || !buildCommand) {
        error("buildApp requires language + buildCommand")
    }

    // Pipeline scope — only primitives and Serializable types
    try {
        timeout(time: timeoutMin, unit: 'MINUTES') {
            sh buildCommand
        }
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        notifyFailure(language: language, error: e.message)
        throw e
    }
}

// Pattern is NOT Serializable — must run inside @NonCPS so it never crosses a CPS checkpoint.
@NonCPS
boolean matchesPolicy(String text, String regex) {
    Pattern p = Pattern.compile(regex)
    return p.matcher(text).find()
}

def notifyFailure(Map cfg) {
    // Delegate to another vars/ function so the message lives in one place across the org.
    notifySlack(
        channel: '#ci-alerts',
        message: "buildApp[${cfg.language}] failed: ${cfg.error}"
    )
}
```
