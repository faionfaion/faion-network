# Jenkins Pipeline Examples

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
            defaultContainer 'node'
        }
    }

    stages {
        stage('Build') {
            steps {
                container('node') {
                    sh 'npm ci'
                    sh 'npm run build'
                }
            }
        }

        stage('Docker Build') {
            steps {
                container('docker') {
                    sh 'docker build -t myapp:${BUILD_NUMBER} .'
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

        stage('Test') {
            steps {
                sh 'npm test'
            }
        }

        stage('Deploy Feature') {
            when {
                branch 'feature/*'
            }
            steps {
                echo "Deploying feature branch ${env.BRANCH_NAME}"
                sh './deploy.sh feature'
            }
        }

        stage('Deploy Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo 'Deploying to staging'
                sh './deploy.sh staging'
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
                submitter "admin,release-managers"
            }
            steps {
                echo 'Deploying to production'
                sh './deploy.sh production'
            }
        }
    }
}
```

## Parallel Stages

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'npm ci'
                sh 'npm run build'
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'npm run test:unit'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh 'npm run test:integration'
                    }
                }
                stage('E2E Tests') {
                    steps {
                        sh 'npm run test:e2e'
                    }
                }
                stage('Lint') {
                    steps {
                        sh 'npm run lint'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh './deploy.sh'
            }
        }
    }
}
```

## Docker Agent

```groovy
pipeline {
    agent {
        docker {
            image 'node:20-alpine'
            args '-v $HOME/.npm:/root/.npm'
        }
    }

    stages {
        stage('Install') {
            steps {
                sh 'npm ci'
            }
        }

        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
    }
}
```

## Credentials Usage

```groovy
pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('docker-hub-creds')
        AWS_CREDENTIALS = credentials('aws-credentials')
    }

    stages {
        stage('Login to Docker Hub') {
            steps {
                sh '''
                    echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin
                '''
            }
        }

        stage('Push Image') {
            steps {
                sh 'docker push myapp:${BUILD_NUMBER}'
            }
        }

        stage('Deploy to AWS') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh 'kubectl apply -f k8s/'
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
}
```

## Shared Library Usage

```groovy
// Jenkinsfile using shared library
@Library('my-shared-library@main') _

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                buildApp()
            }
        }

        stage('Test') {
            steps {
                runTests()
            }
        }

        stage('Deploy') {
            steps {
                deployToEnvironment(env: 'staging')
            }
        }
    }

    post {
        failure {
            notifySlack(channel: '#builds', status: 'FAILURE')
        }
    }
}
```

## Shared Library Structure

```
vars/
├── buildApp.groovy
├── runTests.groovy
├── deployToEnvironment.groovy
└── notifySlack.groovy
src/
└── org/
    └── mycompany/
        └── PipelineUtils.groovy
resources/
└── templates/
    └── deployment.yaml
```

### vars/buildApp.groovy

```groovy
def call(Map config = [:]) {
    def buildTool = config.get('tool', 'npm')

    if (buildTool == 'npm') {
        sh 'npm ci'
        sh 'npm run build'
    } else if (buildTool == 'maven') {
        sh 'mvn clean package -DskipTests'
    }
}
```

### vars/deployToEnvironment.groovy

```groovy
def call(Map config) {
    def environment = config.env ?: 'staging'

    echo "Deploying to ${environment}"

    switch(environment) {
        case 'staging':
            sh './deploy.sh staging'
            break
        case 'production':
            input message: "Deploy to production?"
            sh './deploy.sh production'
            break
        default:
            error "Unknown environment: ${environment}"
    }
}
```

## Matrix Build

```groovy
pipeline {
    agent none

    stages {
        stage('Test') {
            matrix {
                axes {
                    axis {
                        name 'NODE_VERSION'
                        values '18', '20', '22'
                    }
                    axis {
                        name 'OS'
                        values 'linux', 'windows'
                    }
                }
                excludes {
                    exclude {
                        axis {
                            name 'NODE_VERSION'
                            values '18'
                        }
                        axis {
                            name 'OS'
                            values 'windows'
                        }
                    }
                }
                stages {
                    stage('Test on Node') {
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

## Stash and Unstash

```groovy
pipeline {
    agent none

    stages {
        stage('Build') {
            agent { label 'linux' }
            steps {
                sh 'npm ci'
                sh 'npm run build'
                stash includes: 'dist/**', name: 'build-artifacts'
            }
        }

        stage('Deploy to Multiple Servers') {
            parallel {
                stage('Deploy Server 1') {
                    agent { label 'deploy-1' }
                    steps {
                        unstash 'build-artifacts'
                        sh './deploy.sh server1'
                    }
                }
                stage('Deploy Server 2') {
                    agent { label 'deploy-2' }
                    steps {
                        unstash 'build-artifacts'
                        sh './deploy.sh server2'
                    }
                }
            }
        }
    }
}
```

## Error Handling

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }

        stage('Test') {
            steps {
                script {
                    try {
                        sh 'npm test'
                    } catch (Exception e) {
                        echo "Tests failed: ${e.message}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.result != 'FAILURE' }
            }
            steps {
                retry(3) {
                    sh './deploy.sh'
                }
            }
        }
    }

    post {
        failure {
            emailext(
                subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Check console output at ${env.BUILD_URL}",
                to: 'team@example.com'
            )
        }
        unstable {
            slackSend(
                channel: '#builds',
                color: 'warning',
                message: "Build unstable: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}
```

## Common Pitfalls and Solutions

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Scripted for simple pipelines | Harder to maintain, no syntax validation | Use Declarative syntax |
| No timeout limits | Builds hang indefinitely | Set `timeout()` option |
| Hardcoded credentials | Security risk | Use Credentials plugin |
| Missing post cleanup | Resource leaks | Use `cleanWs()` in post-always |
| Sequential independent stages | Wasted time | Use `parallel` stages |
| Builds on controller | Security risk, resource contention | Set controller executors to 0 |
| Using script block excessively | Defeats purpose of Declarative | Move logic to Shared Library |
| Ignoring agent scope | Wrong environment for tasks | Specify agent per stage |
