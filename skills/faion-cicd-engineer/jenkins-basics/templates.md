# Jenkins Pipeline Templates

## Node.js Application

```groovy
// Jenkinsfile - Node.js Application
pipeline {
    agent {
        docker {
            image 'node:20-alpine'
            args '-v $HOME/.npm:/root/.npm'
        }
    }

    environment {
        CI = 'true'
        NODE_ENV = 'test'
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
                sh 'npm ci'
            }
        }

        stage('Lint') {
            steps {
                sh 'npm run lint'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
            post {
                always {
                    junit 'junit.xml'
                }
            }
        }

        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }

        stage('Deploy Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh 'npm run deploy:staging'
            }
        }

        stage('Deploy Production') {
            when {
                branch 'main'
            }
            input {
                message "Deploy to production?"
                ok "Deploy"
            }
            steps {
                sh 'npm run deploy:production'
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

## Python Application

```groovy
// Jenkinsfile - Python Application
pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
        }
    }

    environment {
        PYTHONDONTWRITEBYTECODE = '1'
        PYTHONUNBUFFERED = '1'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    ruff check .
                    mypy src/
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --cov=src --cov-report=xml --junitxml=junit.xml
                '''
            }
            post {
                always {
                    junit 'junit.xml'
                    cobertura coberturaReportFile: 'coverage.xml'
                }
            }
        }

        stage('Build') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m build
                '''
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

## Docker Build and Push

```groovy
// Jenkinsfile - Docker Build and Push
pipeline {
    agent any

    environment {
        REGISTRY = 'docker.io'
        IMAGE_NAME = 'myorg/myapp'
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                script {
                    def imageTag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
                    sh "docker build -t ${REGISTRY}/${IMAGE_NAME}:${imageTag} ."

                    if (env.BRANCH_NAME == 'main') {
                        sh "docker tag ${REGISTRY}/${IMAGE_NAME}:${imageTag} ${REGISTRY}/${IMAGE_NAME}:latest"
                    }
                }
            }
        }

        stage('Security Scan') {
            steps {
                sh "trivy image ${REGISTRY}/${IMAGE_NAME}:${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
            }
        }

        stage('Push Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                sh '''
                    echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin
                    docker push ${REGISTRY}/${IMAGE_NAME}:${BRANCH_NAME}-${BUILD_NUMBER}
                '''
                script {
                    if (env.BRANCH_NAME == 'main') {
                        sh "docker push ${REGISTRY}/${IMAGE_NAME}:latest"
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
            cleanWs()
        }
    }
}
```

## Kubernetes Deployment

```groovy
// Jenkinsfile - Kubernetes Deployment
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: kubectl
                    image: bitnami/kubectl:latest
                    command:
                    - cat
                    tty: true
                  - name: helm
                    image: alpine/helm:latest
                    command:
                    - cat
                    tty: true
            '''
        }
    }

    environment {
        NAMESPACE = 'myapp'
        RELEASE_NAME = 'myapp'
    }

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['staging', 'production'],
            description: 'Target environment'
        )
        string(
            name: 'IMAGE_TAG',
            defaultValue: 'latest',
            description: 'Docker image tag to deploy'
        )
    }

    stages {
        stage('Validate') {
            steps {
                container('helm') {
                    sh 'helm lint ./charts/myapp'
                }
            }
        }

        stage('Dry Run') {
            steps {
                container('helm') {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh """
                            helm upgrade --install ${RELEASE_NAME} ./charts/myapp \
                                --namespace ${NAMESPACE} \
                                --values ./charts/myapp/values-${params.ENVIRONMENT}.yaml \
                                --set image.tag=${params.IMAGE_TAG} \
                                --dry-run
                        """
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                expression { params.ENVIRONMENT == 'staging' || input(message: 'Deploy to production?', ok: 'Deploy') }
            }
            steps {
                container('helm') {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh """
                            helm upgrade --install ${RELEASE_NAME} ./charts/myapp \
                                --namespace ${NAMESPACE} \
                                --values ./charts/myapp/values-${params.ENVIRONMENT}.yaml \
                                --set image.tag=${params.IMAGE_TAG} \
                                --wait \
                                --timeout 5m
                        """
                    }
                }
            }
        }

        stage('Verify') {
            steps {
                container('kubectl') {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl rollout status deployment/${RELEASE_NAME} -n ${NAMESPACE}
                            kubectl get pods -n ${NAMESPACE} -l app=${RELEASE_NAME}
                        """
                    }
                }
            }
        }
    }
}
```

## Microservices Monorepo

```groovy
// Jenkinsfile - Monorepo with Multiple Services
pipeline {
    agent any

    options {
        timeout(time: 60, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Detect Changes') {
            steps {
                script {
                    def changes = sh(
                        script: 'git diff --name-only HEAD~1',
                        returnStdout: true
                    ).trim().split('\n')

                    env.BUILD_API = changes.any { it.startsWith('services/api/') } ? 'true' : 'false'
                    env.BUILD_WEB = changes.any { it.startsWith('services/web/') } ? 'true' : 'false'
                    env.BUILD_WORKER = changes.any { it.startsWith('services/worker/') } ? 'true' : 'false'
                }
            }
        }

        stage('Build Services') {
            parallel {
                stage('API Service') {
                    when {
                        expression { env.BUILD_API == 'true' }
                    }
                    steps {
                        dir('services/api') {
                            sh 'docker build -t api:${BUILD_NUMBER} .'
                        }
                    }
                }
                stage('Web Service') {
                    when {
                        expression { env.BUILD_WEB == 'true' }
                    }
                    steps {
                        dir('services/web') {
                            sh 'docker build -t web:${BUILD_NUMBER} .'
                        }
                    }
                }
                stage('Worker Service') {
                    when {
                        expression { env.BUILD_WORKER == 'true' }
                    }
                    steps {
                        dir('services/worker') {
                            sh 'docker build -t worker:${BUILD_NUMBER} .'
                        }
                    }
                }
            }
        }

        stage('Test Services') {
            parallel {
                stage('API Tests') {
                    when {
                        expression { env.BUILD_API == 'true' }
                    }
                    steps {
                        dir('services/api') {
                            sh 'npm test'
                        }
                    }
                }
                stage('Web Tests') {
                    when {
                        expression { env.BUILD_WEB == 'true' }
                    }
                    steps {
                        dir('services/web') {
                            sh 'npm test'
                        }
                    }
                }
                stage('Worker Tests') {
                    when {
                        expression { env.BUILD_WORKER == 'true' }
                    }
                    steps {
                        dir('services/worker') {
                            sh 'npm test'
                        }
                    }
                }
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

## Shared Library Template

### vars/standardPipeline.groovy

```groovy
// Shared Library: vars/standardPipeline.groovy
def call(Map config) {
    pipeline {
        agent {
            docker {
                image config.get('dockerImage', 'node:20-alpine')
            }
        }

        options {
            timeout(time: config.get('timeout', 30), unit: 'MINUTES')
            timestamps()
            buildDiscarder(logRotator(numToKeepStr: '10'))
            disableConcurrentBuilds()
        }

        stages {
            stage('Install') {
                steps {
                    sh config.get('installCommand', 'npm ci')
                }
            }

            stage('Lint') {
                when {
                    expression { config.get('runLint', true) }
                }
                steps {
                    sh config.get('lintCommand', 'npm run lint')
                }
            }

            stage('Test') {
                when {
                    expression { config.get('runTests', true) }
                }
                steps {
                    sh config.get('testCommand', 'npm test')
                }
            }

            stage('Build') {
                steps {
                    sh config.get('buildCommand', 'npm run build')
                }
            }

            stage('Deploy') {
                when {
                    branch config.get('deployBranch', 'main')
                }
                steps {
                    sh config.get('deployCommand', 'npm run deploy')
                }
            }
        }

        post {
            always {
                cleanWs()
            }
            failure {
                script {
                    if (config.get('slackChannel')) {
                        slackSend(
                            channel: config.slackChannel,
                            color: 'danger',
                            message: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
                        )
                    }
                }
            }
        }
    }
}
```

### Usage in Jenkinsfile

```groovy
// Jenkinsfile using shared library
@Library('my-shared-library@main') _

standardPipeline(
    dockerImage: 'node:20-alpine',
    installCommand: 'npm ci',
    lintCommand: 'npm run lint',
    testCommand: 'npm run test:coverage',
    buildCommand: 'npm run build',
    deployCommand: './deploy.sh production',
    deployBranch: 'main',
    slackChannel: '#deployments',
    timeout: 45
)
```

## Configuration as Code (JCasC) Template

```yaml
# jenkins.yaml - Configuration as Code
jenkins:
  systemMessage: "Jenkins configured via JCasC"

  securityRealm:
    local:
      allowsSignup: false
      users:
        - id: "admin"
          password: "${ADMIN_PASSWORD}"

  authorizationStrategy:
    roleBased:
      roles:
        global:
          - name: "admin"
            permissions:
              - "Overall/Administer"
            assignments:
              - "admin"
          - name: "developer"
            permissions:
              - "Overall/Read"
              - "Job/Build"
              - "Job/Read"
            assignments:
              - "developers"

  nodes:
    - permanent:
        name: "linux-agent-1"
        labelString: "linux docker"
        remoteFS: "/var/jenkins"
        launcher:
          ssh:
            host: "agent1.example.com"
            credentialsId: "ssh-agent-key"

unclassified:
  location:
    url: "https://jenkins.example.com/"
    adminAddress: "admin@example.com"

  globalLibraries:
    libraries:
      - name: "my-shared-library"
        defaultVersion: "main"
        retriever:
          modernSCM:
            scm:
              git:
                remote: "https://github.com/myorg/jenkins-shared-library.git"
                credentialsId: "github-token"

credentials:
  system:
    domainCredentials:
      - credentials:
          - usernamePassword:
              scope: GLOBAL
              id: "docker-hub-credentials"
              username: "${DOCKER_USERNAME}"
              password: "${DOCKER_PASSWORD}"
          - string:
              scope: GLOBAL
              id: "github-token"
              secret: "${GITHUB_TOKEN}"
```
