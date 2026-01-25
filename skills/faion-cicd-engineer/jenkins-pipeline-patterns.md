---
id: jenkins-pipeline-patterns
name: "Jenkins Pipeline Patterns"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Jenkins Pipeline Patterns

## Overview

Advanced Jenkins pipeline patterns including production-grade declarative pipelines, shared libraries, scripted pipelines, and reusable components. See [jenkins-basics.md](jenkins-basics.md) for fundamentals.

## Production-Grade Declarative Pipeline

```groovy
// Jenkinsfile
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
            '''
        }
    }

    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        APP_NAME = 'myapp'
        VERSION = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
        DOCKER_CREDENTIALS = credentials('docker-registry')
        KUBECONFIG = credentials('kubeconfig-staging')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        ansiColor('xterm')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_MSG = sh(
                        script: 'git log -1 --pretty=%B',
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                container('node') {
                    sh 'npm ci'
                }
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        container('node') {
                            sh 'npm run test:unit -- --coverage'
                        }
                    }
                    post {
                        always {
                            junit 'junit.xml'
                            publishHTML(target: [
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'coverage/lcov-report',
                                reportFiles: 'index.html',
                                reportName: 'Coverage Report'
                            ])
                        }
                    }
                }
                stage('Integration Tests') {
                    steps {
                        container('node') {
                            sh 'npm run test:integration'
                        }
                    }
                }
            }
        }

        stage('Security Scan') {
            parallel {
                stage('SAST') {
                    steps {
                        container('node') {
                            sh 'npm audit --audit-level=high'
                        }
                    }
                }
                stage('Container Scan') {
                    steps {
                        container('docker') {
                            sh '''
                                docker run --rm \
                                    -v /var/run/docker.sock:/var/run/docker.sock \
                                    aquasec/trivy:latest image \
                                    --severity HIGH,CRITICAL \
                                    --exit-code 1 \
                                    ${DOCKER_REGISTRY}/${APP_NAME}:${VERSION}
                            '''
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    script {
                        sh """
                            docker login -u ${DOCKER_CREDENTIALS_USR} -p ${DOCKER_CREDENTIALS_PSW} ${DOCKER_REGISTRY}
                            docker build -t ${DOCKER_REGISTRY}/${APP_NAME}:${VERSION} .
                            docker push ${DOCKER_REGISTRY}/${APP_NAME}:${VERSION}
                        """
                    }
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                container('kubectl') {
                    withCredentials([file(credentialsId: 'kubeconfig-staging', variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl set image deployment/${APP_NAME} \
                                ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${VERSION} \
                                -n staging
                            kubectl rollout status deployment/${APP_NAME} -n staging --timeout=5m
                        """
                    }
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            input {
                message "Deploy to production?"
                ok "Deploy"
                submitter "admin,deployers"
            }
            steps {
                container('kubectl') {
                    withCredentials([file(credentialsId: 'kubeconfig-prod', variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl set image deployment/${APP_NAME} \
                                ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${VERSION} \
                                -n production
                            kubectl rollout status deployment/${APP_NAME} -n production --timeout=10m
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            slackSend(
                color: 'good',
                message: "Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
            emailext(
                subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Commit: ${env.GIT_COMMIT}\nMessage: ${env.GIT_COMMIT_MSG}",
                recipientProviders: [culprits(), requestor()]
            )
        }
    }
}
```

## Shared Library Structure

```
vars/
├── buildApp.groovy          # Global variables/functions
├── deployToK8s.groovy
├── notifySlack.groovy
└── runTests.groovy
src/
└── com/
    └── example/
        ├── Docker.groovy    # Classes
        └── Kubernetes.groovy
resources/
└── templates/
    └── deployment.yaml      # Resource files
```

### Shared Library - vars/buildApp.groovy

```groovy
// vars/buildApp.groovy
def call(Map config = [:]) {
    def appName = config.appName ?: error('appName is required')
    def registry = config.registry ?: 'registry.example.com'
    def dockerfile = config.dockerfile ?: 'Dockerfile'
    def buildArgs = config.buildArgs ?: [:]

    def buildArgsString = buildArgs.collect { k, v -> "--build-arg ${k}=${v}" }.join(' ')

    pipeline {
        agent any

        stages {
            stage('Build') {
                steps {
                    script {
                        docker.withRegistry("https://${registry}", 'docker-credentials') {
                            def image = docker.build(
                                "${registry}/${appName}:${env.BUILD_NUMBER}",
                                "-f ${dockerfile} ${buildArgsString} ."
                            )
                            image.push()
                            image.push('latest')
                        }
                    }
                }
            }
        }
    }
}
```

### Shared Library - vars/deployToK8s.groovy

```groovy
// vars/deployToK8s.groovy
def call(Map config = [:]) {
    def namespace = config.namespace ?: error('namespace is required')
    def deployment = config.deployment ?: error('deployment is required')
    def image = config.image ?: error('image is required')
    def kubeconfig = config.kubeconfig ?: 'kubeconfig'
    def timeout = config.timeout ?: '5m'

    withCredentials([file(credentialsId: kubeconfig, variable: 'KUBECONFIG')]) {
        sh """
            kubectl set image deployment/${deployment} \
                ${deployment}=${image} \
                -n ${namespace}
            kubectl rollout status deployment/${deployment} \
                -n ${namespace} \
                --timeout=${timeout}
        """
    }
}
```

### Shared Library - src/com/example/Docker.groovy

```groovy
// src/com/example/Docker.groovy
package com.example

class Docker implements Serializable {
    def steps

    Docker(steps) {
        this.steps = steps
    }

    def build(String imageName, String dockerfile = 'Dockerfile', Map buildArgs = [:]) {
        def buildArgsString = buildArgs.collect { k, v -> "--build-arg ${k}=${v}" }.join(' ')

        steps.sh """
            docker build \
                -t ${imageName} \
                -f ${dockerfile} \
                ${buildArgsString} \
                .
        """

        return imageName
    }

    def push(String imageName, String registry, String credentialsId) {
        steps.withCredentials([
            steps.usernamePassword(
                credentialsId: credentialsId,
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASS'
            )
        ]) {
            steps.sh """
                echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin ${registry}
                docker push ${imageName}
            """
        }
    }

    def scan(String imageName, String severity = 'HIGH,CRITICAL') {
        def result = steps.sh(
            script: """
                docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    aquasec/trivy:latest image \
                    --severity ${severity} \
                    --exit-code 1 \
                    ${imageName}
            """,
            returnStatus: true
        )

        if (result != 0) {
            steps.error("Security vulnerabilities found in ${imageName}")
        }
    }
}
```

### Using Shared Library

```groovy
// Jenkinsfile using shared library
@Library('my-shared-library@main') _

import com.example.Docker

pipeline {
    agent any

    stages {
        stage('Build and Deploy') {
            steps {
                script {
                    def docker = new Docker(this)

                    def imageName = docker.build(
                        'registry.example.com/myapp:latest',
                        'Dockerfile',
                        [VERSION: env.BUILD_NUMBER]
                    )

                    docker.scan(imageName)

                    docker.push(imageName, 'registry.example.com', 'docker-creds')

                    deployToK8s(
                        namespace: 'staging',
                        deployment: 'myapp',
                        image: imageName
                    )
                }
            }
        }
    }
}
```

## Scripted Pipeline (Complex Logic)

```groovy
// Jenkinsfile - Scripted Pipeline
node('docker') {
    def services = ['api', 'web', 'worker']
    def parallelStages = [:]

    try {
        stage('Checkout') {
            checkout scm
        }

        stage('Detect Changes') {
            def changedFiles = sh(
                script: "git diff --name-only HEAD~1",
                returnStdout: true
            ).trim().split('\n')

            services = services.findAll { service ->
                changedFiles.any { it.startsWith("services/${service}/") }
            }

            if (services.isEmpty()) {
                currentBuild.result = 'SUCCESS'
                return
            }

            echo "Building services: ${services.join(', ')}"
        }

        stage('Build Services') {
            services.each { service ->
                parallelStages["Build ${service}"] = {
                    node('docker') {
                        checkout scm
                        dir("services/${service}") {
                            sh 'docker build -t ${service}:${BUILD_NUMBER} .'
                        }
                    }
                }
            }
            parallel parallelStages
        }

        stage('Test Services') {
            parallelStages = [:]
            services.each { service ->
                parallelStages["Test ${service}"] = {
                    node('docker') {
                        checkout scm
                        dir("services/${service}") {
                            sh 'npm test'
                        }
                    }
                }
            }
            parallel parallelStages
        }

        stage('Deploy') {
            services.each { service ->
                deployService(service, env.BUILD_NUMBER)
            }
        }

    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        slackSend(color: 'danger', message: "Build failed: ${e.message}")
        throw e

    } finally {
        cleanWs()
    }
}

def deployService(String service, String version) {
    timeout(time: 5, unit: 'MINUTES') {
        sh """
            kubectl set image deployment/${service} ${service}=${service}:${version}
            kubectl rollout status deployment/${service} --timeout=5m
        """
    }
}
```

## Best Practices

1. **Use shared libraries** - Centralize common pipeline code for reusability
2. **Implement proper error handling** - Use try-catch in scripted pipelines
3. **Parallelize independent stages** - Reduce build time
4. **Use credentials plugin** - Never hardcode secrets
5. **Set timeouts** - Prevent stuck builds
6. **Clean workspace** - Always clean in post section
7. **Use Blue Ocean** - Better visualization
8. **Version shared libraries** - Pin to specific versions for stability

## Sources

- [Jenkins Basics](jenkins-basics.md)
- [Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins Best Practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
- [Kubernetes Plugin](https://plugins.jenkins.io/kubernetes/)
