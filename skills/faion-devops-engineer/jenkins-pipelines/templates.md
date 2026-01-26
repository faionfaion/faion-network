# Jenkins Pipeline Templates

Reusable templates for common pipeline scenarios.

## Shared Library Structure

```
jenkins-shared-library/
├── vars/
│   ├── buildApp.groovy          # Global variables/functions
│   ├── deployToK8s.groovy
│   ├── notifySlack.groovy
│   └── runTests.groovy
├── src/
│   └── com/
│       └── example/
│           ├── Docker.groovy    # Classes
│           └── Kubernetes.groovy
└── resources/
    └── templates/
        └── deployment.yaml      # Resource files
```

## vars/buildApp.groovy

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

## vars/deployToK8s.groovy

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

## vars/notifySlack.groovy

```groovy
// vars/notifySlack.groovy
def call(Map config = [:]) {
    def channel = config.channel ?: '#builds'
    def status = config.status ?: currentBuild.result ?: 'SUCCESS'
    def message = config.message ?: "${env.JOB_NAME} #${env.BUILD_NUMBER}"

    def color = status == 'SUCCESS' ? 'good' :
                status == 'FAILURE' ? 'danger' :
                'warning'

    slackSend(
        channel: channel,
        color: color,
        message: "${status}: ${message}\n${env.BUILD_URL}"
    )
}
```

## vars/runTests.groovy

```groovy
// vars/runTests.groovy
def call(Map config = [:]) {
    def testCommand = config.command ?: 'npm test'
    def coverage = config.coverage ?: true
    def junitReport = config.junitReport ?: 'junit.xml'
    def coverageDir = config.coverageDir ?: 'coverage/lcov-report'

    sh coverage ? "${testCommand} -- --coverage" : testCommand

    if (fileExists(junitReport)) {
        junit junitReport
    }

    if (coverage && fileExists(coverageDir)) {
        publishHTML(target: [
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: coverageDir,
            reportFiles: 'index.html',
            reportName: 'Coverage Report'
        ])
    }
}
```

## vars/securityScan.groovy

```groovy
// vars/securityScan.groovy
def call(Map config = [:]) {
    def image = config.image ?: error('image is required')
    def severity = config.severity ?: 'HIGH,CRITICAL'
    def failOnVulnerability = config.failOnVulnerability ?: true
    def exitCode = failOnVulnerability ? 1 : 0

    sh """
        docker run --rm \
            -v /var/run/docker.sock:/var/run/docker.sock \
            aquasec/trivy:latest image \
            --severity ${severity} \
            --exit-code ${exitCode} \
            ${image}
    """
}
```

## src/com/example/Docker.groovy

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

## src/com/example/Kubernetes.groovy

```groovy
// src/com/example/Kubernetes.groovy
package com.example

class Kubernetes implements Serializable {
    def steps
    def kubeconfig

    Kubernetes(steps, String kubeconfigCredentialId = 'kubeconfig') {
        this.steps = steps
        this.kubeconfig = kubeconfigCredentialId
    }

    def deploy(String namespace, String deployment, String image, String timeout = '5m') {
        steps.withCredentials([steps.file(credentialsId: kubeconfig, variable: 'KUBECONFIG')]) {
            steps.sh """
                kubectl set image deployment/${deployment} \
                    ${deployment}=${image} \
                    -n ${namespace}
                kubectl rollout status deployment/${deployment} \
                    -n ${namespace} \
                    --timeout=${timeout}
            """
        }
    }

    def rollback(String namespace, String deployment) {
        steps.withCredentials([steps.file(credentialsId: kubeconfig, variable: 'KUBECONFIG')]) {
            steps.sh """
                kubectl rollout undo deployment/${deployment} -n ${namespace}
                kubectl rollout status deployment/${deployment} -n ${namespace} --timeout=5m
            """
        }
    }

    def getStatus(String namespace, String deployment) {
        steps.withCredentials([steps.file(credentialsId: kubeconfig, variable: 'KUBECONFIG')]) {
            return steps.sh(
                script: "kubectl get deployment/${deployment} -n ${namespace} -o jsonpath='{.status.availableReplicas}'",
                returnStdout: true
            ).trim()
        }
    }
}
```

## Basic Jenkinsfile Template

```groovy
// Jenkinsfile - Basic Template
pipeline {
    agent any

    environment {
        APP_NAME = 'myapp'
        DOCKER_REGISTRY = 'registry.example.com'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'npm ci'
                sh 'npm run build'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
            post {
                always {
                    junit '**/junit.xml'
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying...'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
```

## Kubernetes Agent Template

```groovy
// Jenkinsfile - Kubernetes Agent Template
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                metadata:
                  labels:
                    jenkins: agent
                spec:
                  containers:
                  - name: node
                    image: node:20-alpine
                    command:
                    - cat
                    tty: true
                    resources:
                      limits:
                        memory: "2Gi"
                        cpu: "1"
                      requests:
                        memory: "1Gi"
                        cpu: "500m"
                  - name: docker
                    image: docker:24-dind
                    securityContext:
                      privileged: true
                    volumeMounts:
                    - name: docker-graph-storage
                      mountPath: /var/lib/docker
                  - name: kubectl
                    image: bitnami/kubectl:latest
                    command:
                    - cat
                    tty: true
                  volumes:
                  - name: docker-graph-storage
                    emptyDir: {}
            '''
        }
    }

    stages {
        stage('Node Tasks') {
            steps {
                container('node') {
                    sh 'npm ci && npm test'
                }
            }
        }

        stage('Docker Tasks') {
            steps {
                container('docker') {
                    sh 'docker build -t myapp .'
                }
            }
        }

        stage('Kubectl Tasks') {
            steps {
                container('kubectl') {
                    sh 'kubectl get pods'
                }
            }
        }
    }
}
```
