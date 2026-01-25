---
id: jenkins-basics
name: "Jenkins Basics"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Jenkins Basics

## Overview

Jenkins is an open-source automation server for building CI/CD pipelines. It uses Groovy-based Declarative or Scripted Pipeline syntax defined in Jenkinsfiles, supporting complex workflows, distributed builds, and extensive plugin ecosystem.

## When to Use

- Enterprise environments with existing Jenkins infrastructure
- Complex build requirements needing extensive customization
- On-premises deployments with strict security requirements
- Multi-branch projects with complex branching strategies
- Pipelines requiring custom plugins or integrations

## Key Concepts

| Concept | Description |
|---------|-------------|
| Pipeline | Automated workflow defined in Jenkinsfile |
| Stage | Logical division of pipeline (Build, Test, Deploy) |
| Step | Single task within a stage |
| Agent | Executor running pipeline (controller, node, docker) |
| Declarative | Structured pipeline syntax with predefined sections |
| Scripted | Flexible Groovy-based pipeline syntax |
| Shared Library | Reusable pipeline code |
| Blue Ocean | Modern pipeline visualization UI |

### Pipeline Types Comparison

| Feature | Declarative | Scripted |
|---------|-------------|----------|
| Syntax | Structured, predefined | Flexible Groovy |
| Error handling | Built-in post sections | try-catch blocks |
| Readability | Easier for beginners | More complex |
| Flexibility | Limited | Full Groovy power |
| Validation | Syntax validation | Runtime only |

## Basic Declarative Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        APP_NAME = 'myapp'
        VERSION = "${env.BUILD_NUMBER}"
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    triggers {
        pollSCM('H/5 * * * *')
        cron('H 2 * * *')
    }

    parameters {
        choice(
            name: 'DEPLOY_ENV',
            choices: ['staging', 'production'],
            description: 'Environment to deploy to'
        )
        booleanParam(
            name: 'SKIP_TESTS',
            defaultValue: false,
            description: 'Skip test stage'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }

        stage('Test') {
            when {
                not {
                    expression { params.SKIP_TESTS }
                }
            }
            steps {
                sh 'npm test'
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying to ${params.DEPLOY_ENV}"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Build succeeded'
        }
        failure {
            echo 'Build failed'
        }
    }
}
```

## Kubernetes Agent

```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: node
                    image: node:20-alpine
                    command:
                    - cat
                    tty: true
                  - name: docker
                    image: docker:24-dind
                    securityContext:
                      privileged: true
                    volumeMounts:
                    - name: docker-socket
                      mountPath: /var/run/docker.sock
                  volumes:
                  - name: docker-socket
                    emptyDir: {}
            '''
        }
    }

    stages {
        stage('Build') {
            steps {
                container('node') {
                    sh 'npm run build'
                }
            }
        }
    }
}
```

## Multibranch Pipeline

```groovy
// Jenkinsfile with branch-specific behavior
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }

        stage('Deploy Feature') {
            when {
                branch 'feature/*'
            }
            steps {
                echo "Deploying feature branch ${env.BRANCH_NAME}"
            }
        }

        stage('Deploy Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo "Deploying to staging"
            }
        }

        stage('Deploy Production') {
            when {
                branch 'main'
                beforeInput true
            }
            input {
                message "Deploy to production?"
                ok "Yes, deploy"
            }
            steps {
                echo "Deploying to production"
            }
        }
    }
}
```

## Best Practices

1. **Use Declarative Pipeline** - Prefer declarative syntax for readability and validation
2. **Implement Shared Libraries** - Centralize common pipeline code
3. **Use Kubernetes agents** - Dynamic, isolated build environments
4. **Parallelize stages** - Reduce build time with parallel execution
5. **Secure credentials** - Use Jenkins Credentials plugin, never hardcode
6. **Set timeouts** - Prevent stuck builds with stage/pipeline timeouts
7. **Clean workspace** - Always clean workspace in post section
8. **Use Blue Ocean** - Modern UI for better pipeline visualization
9. **Version Jenkinsfiles** - Store in source control with application
10. **Implement proper post sections** - Handle success, failure, always conditions

## Common Pitfalls

1. **Scripted for simple pipelines** - Declarative is simpler and validates syntax. Use scripted only when needed.

2. **No timeout limits** - Builds can hang indefinitely. Always set timeouts.

3. **Hardcoded credentials** - Security risk. Use Jenkins Credentials plugin.

4. **Missing post cleanup** - Resources leak without cleanup. Use `cleanWs()` in post always.

5. **Sequential when parallel is possible** - Wasted time. Use parallel stages for independent jobs.

6. **Ignoring agent scope** - Wrong agent for job. Specify agent per stage when needed.

## Sources

- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
- [Blue Ocean](https://www.jenkins.io/doc/book/blueocean/)
- [Jenkins Official Documentation](https://www.jenkins.io/doc/)
