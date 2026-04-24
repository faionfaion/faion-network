# Jenkins Pipeline Examples

Production-grade pipeline examples for common scenarios.

## Production Declarative Pipeline

Complete pipeline with Kubernetes agents, parallel testing, security scanning, and multi-environment deployment.

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

## Shared Library Usage

Using shared library with declarative pipeline.

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

For dynamic service detection and parallel builds.

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

## Multibranch Pipeline

Pipeline adapting to different branch strategies.

```groovy
pipeline {
    agent any

    environment {
        DEPLOY_ENV = "${env.BRANCH_NAME == 'main' ? 'production' :
                       env.BRANCH_NAME == 'develop' ? 'staging' :
                       'development'}"
    }

    stages {
        stage('Build') {
            steps {
                sh 'npm ci && npm run build'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                    branch pattern: 'feature/*', comparator: 'GLOB'
                }
            }
            steps {
                echo "Deploying to ${DEPLOY_ENV}"
                sh "./deploy.sh ${DEPLOY_ENV}"
            }
        }
    }
}
```

## Matrix Build

Build across multiple configurations.

```groovy
pipeline {
    agent none

    stages {
        stage('Build Matrix') {
            matrix {
                axes {
                    axis {
                        name 'NODE_VERSION'
                        values '18', '20', '22'
                    }
                    axis {
                        name 'OS'
                        values 'linux', 'macos'
                    }
                }
                excludes {
                    exclude {
                        axis {
                            name 'OS'
                            values 'macos'
                        }
                        axis {
                            name 'NODE_VERSION'
                            values '18'
                        }
                    }
                }
                stages {
                    stage('Build') {
                        agent {
                            label "${OS}"
                        }
                        steps {
                            sh "nvm use ${NODE_VERSION} && npm ci && npm run build"
                        }
                    }
                    stage('Test') {
                        agent {
                            label "${OS}"
                        }
                        steps {
                            sh "nvm use ${NODE_VERSION} && npm test"
                        }
                    }
                }
            }
        }
    }
}
```

## Canary Deployment

Progressive rollout with validation.

```groovy
pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_TAG', description: 'Docker image tag')
        choice(name: 'CANARY_WEIGHT', choices: ['10', '25', '50', '100'])
    }

    stages {
        stage('Canary Deploy') {
            steps {
                sh """
                    kubectl set image deployment/myapp-canary \
                        myapp=${DOCKER_REGISTRY}/myapp:${params.IMAGE_TAG}

                    # Update Istio VirtualService weight
                    kubectl patch virtualservice myapp \
                        --type=json \
                        -p='[{"op": "replace", "path": "/spec/http/0/route/0/weight", "value": ${params.CANARY_WEIGHT}}]'
                """
            }
        }

        stage('Validate Canary') {
            steps {
                sh './scripts/validate-canary.sh'
            }
        }

        stage('Promote or Rollback') {
            input {
                message "Promote canary to production?"
                ok "Promote"
            }
            steps {
                sh """
                    kubectl set image deployment/myapp \
                        myapp=${DOCKER_REGISTRY}/myapp:${params.IMAGE_TAG}

                    # Reset canary weight
                    kubectl patch virtualservice myapp \
                        --type=json \
                        -p='[{"op": "replace", "path": "/spec/http/0/route/0/weight", "value": 0}]'
                """
            }
        }
    }

    post {
        failure {
            sh """
                # Rollback canary
                kubectl patch virtualservice myapp \
                    --type=json \
                    -p='[{"op": "replace", "path": "/spec/http/0/route/0/weight", "value": 0}]'
            """
        }
    }
}
```
