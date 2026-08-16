# Jenkins Basics

## Summary

**One-sentence:** Generates a Declarative Jenkinsfile + JCasC YAML with K8s/Docker agents, zero-executor controller, pinned plugins, withCredentials secrets, and post cleanup.

**One-paragraph:** Jenkins is an open-source automation server with Groovy-based Declarative (recommended) and Scripted pipeline syntax defined in Jenkinsfiles. Use Declarative pipelines for all new pipelines — they support restart-from-stage and syntax validation at load time. Use Shared Libraries to share pipeline code across projects. Use the Kubernetes agent for dynamic build agents — never run builds on the controller node. Manage controller configuration via the JCasC plugin from a YAML file in source control.

**Ефективно для:**

- Brownfield enterprise з існуючою Jenkins-інфраструктурою + plugin-екосистемою.
- On-prem або air-gapped CI з суворими compliance + network isolation вимогами.
- Multibranch / Organization Folder для багатобренчевих репозиторіїв.
- Migration: ad-hoc Jenkins config UI → reproducible JCasC YAML + plugins.txt.
- Dynamic K8s агенти замість long-lived VMs (scale-to-zero, ізольоване середовище build).

## Applies If (ALL must hold)

- Enterprise environments with existing Jenkins infrastructure and established pipelines.
- On-premises deployments with strict network isolation or compliance requirements.
- Pipelines requiring heavy customization via plugins not available in GitLab CI or GitHub Actions.
- Multi-branch projects with complex branching strategies (Organization Folder + Multibranch Pipeline).

## Skip If (ANY kills it)

- New projects on GitHub — GitHub Actions is simpler and has zero infrastructure cost.
- New projects on GitLab — GitLab CI is integrated and eliminates a separate server.
- Small teams or solo projects — Jenkins administration overhead is not justified.
- Projects that need serverless / ephemeral CI — prefer cloud-native CI tools.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repository tree | filesystem path | git repo |
| Build language + toolchain | name + version | project README / package manifest |
| Deploy target | env name + branch mapping | release plan |
| Secrets inventory | list of credentialsId | Jenkins Credentials store |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[github-actions-basics]] | Comparator surface; decide whether Jenkins is even the right tool. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: declarative-default, zero-controller-executors, jcasc-config, withCredentials-only, options-timeout-buildDiscarder, kubernetes-agent | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-agent-type` | sonnet | Light decision: K8s vs Docker vs label-based. |
| `write-jenkinsfile` | sonnet | Structured Declarative authoring. |
| `lint-jenkinsfile` | haiku | Mechanical pipeline-linter REST call. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Jenkinsfile` | Declarative pipeline skeleton with build/test/deploy + post-actions |
| `templates/kubernetes-agent.groovy` | Kubernetes pod template for dynamic Jenkins agents |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-jenkins-basics.py` | Validate the Jenkinsfile artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[jenkins-pipeline-patterns]]
- [[github-actions-basics]]
- [[gitlab-cicd]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (project host, infra ownership, build complexity, agent strategy) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the Jenkins methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Jenkinsfile`

```text
// Replace: DOCKER_IMAGE, DEPLOY_CMD, SLACK_CHANNEL, branch names

pipeline {
    agent {
        docker {
            image 'node:20-alpine'
            args '-v $HOME/.npm:/root/.npm'
        }
    }

    environment {
        CI = 'true'
        // Add credentials here, e.g.:
        // DEPLOY_KEY = credentials('deploy-ssh-key')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Install') {
            steps {
                sh 'npm ci --cache .npm --prefer-offline'
            }
        }

        stage('Validate') {
            parallel {
                stage('Lint') {
                    steps { sh 'npm run lint' }
                }
                stage('Type Check') {
                    steps { sh 'npm run typecheck' }
                }
            }
        }

        stage('Test') {
            steps {
                sh 'npm test -- --coverage'
            }
            post {
                always {
                    junit testResults: 'junit.xml', allowEmptyResults: true
                }
            }
        }

        stage('Build') {
            steps {
                sh 'npm run build'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'dist/**', fingerprint: true
                }
            }
        }

        stage('Deploy Staging') {
            when {
                branch 'develop'
                not { changeRequest() }
            }
            steps {
                sh './scripts/deploy.sh staging'
            }
            post {
                success {
                    echo "Deployed to staging: https://staging.example.com"
                }
            }
        }

        stage('Deploy Production') {
            when {
                branch 'main'
                not { changeRequest() }
            }
            input {
                message 'Deploy to production?'
                ok 'Deploy'
                submitter 'release-team'
            }
            steps {
                sh './scripts/deploy.sh production'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            slackSend(
                channel: '#ci-alerts',
                color: 'danger',
                message: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
            )
        }
        success {
            script {
                if (env.BRANCH_NAME == 'main') {
                    slackSend(
                        channel: '#deployments',
                        color: 'good',
                        message: "DEPLOYED: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
                    )
                }
            }
        }
    }
}
```

### `templates/kubernetes-agent.groovy`

```groovy
// Copy into vars/ of your Shared Library.
// Usage: kubernetesAgent(nodeImage: 'node:20', helmVersion: '3.14') { ... }

def call(Map config = [:], Closure body) {
    def nodeImage  = config.get('nodeImage',  'node:20-alpine')
    def helmVersion = config.get('helmVersion', '3.14')
    def cpuRequest  = config.get('cpuRequest',  '500m')
    def memRequest  = config.get('memRequest',  '512Mi')
    def cpuLimit    = config.get('cpuLimit',    '2')
    def memLimit    = config.get('memLimit',    '2Gi')

    podTemplate(
        label: "jenkins-k8s-${UUID.randomUUID().toString()}",
        containers: [
            containerTemplate(
                name: 'jnlp',
                image: 'jenkins/inbound-agent:latest',
                resourceRequestCpu: '100m',
                resourceRequestMemory: '128Mi'
            ),
            containerTemplate(
                name: 'build',
                image: nodeImage,
                command: 'cat',
                ttyEnabled: true,
                resourceRequestCpu: cpuRequest,
                resourceRequestMemory: memRequest,
                resourceLimitCpu: cpuLimit,
                resourceLimitMemory: memLimit
            ),
            containerTemplate(
                name: 'helm',
                image: "alpine/helm:${helmVersion}",
                command: 'cat',
                ttyEnabled: true,
                resourceRequestCpu: '100m',
                resourceRequestMemory: '128Mi'
            ),
            containerTemplate(
                name: 'docker',
                image: 'docker:24-dind',
                privileged: true,
                resourceRequestCpu: '500m',
                resourceRequestMemory: '512Mi'
            )
        ],
        volumes: [
            emptyDirVolume(mountPath: '/var/lib/docker', memory: false)
        ]
    ) {
        node(POD_LABEL) {
            body()
        }
    }
}

// Example usage in a Jenkinsfile:
//
// @Library('my-shared-library@main') _
//
// kubernetesAgent(nodeImage: 'node:20-alpine', helmVersion: '3.14') {
//     stage('Build') {
//         container('build') {
//             sh 'npm ci && npm run build'
//         }
//     }
//     stage('Deploy') {
//         container('helm') {
//             withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
//                 sh 'helm upgrade --install myapp ./charts/myapp --wait'
//             }
//         }
//     }
// }
```
