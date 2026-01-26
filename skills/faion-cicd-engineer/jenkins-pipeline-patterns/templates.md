# Jenkins Pipeline Templates

Copy-paste templates for common pipeline patterns.

---

## Basic Declarative Pipeline

```groovy
pipeline {
    agent any

    environment {
        APP_NAME = 'myapp'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
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
                    junit 'test-results/*.xml'
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy.sh'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            // Add notification here
            echo 'Build failed!'
        }
    }
}
```

---

## Kubernetes Agent Template

```groovy
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
                    command: [cat]
                    tty: true
                    resources:
                      requests:
                        memory: "512Mi"
                        cpu: "500m"
                      limits:
                        memory: "1Gi"
                        cpu: "1000m"
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
                sh 'npm ci && npm run build'
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

---

## Parallel Testing Template

```groovy
pipeline {
    agent any

    stages {
        stage('Install') {
            steps {
                sh 'npm ci'
            }
        }

        stage('Quality Gates') {
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
                stage('Lint') {
                    steps {
                        sh 'npm run lint'
                    }
                }
                stage('Security Scan') {
                    steps {
                        sh 'npm audit --audit-level=high'
                    }
                }
            }
        }
    }
}
```

---

## Multi-Environment Deployment Template

```groovy
pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'production'],
            description: 'Target environment'
        )
        booleanParam(
            name: 'SKIP_TESTS',
            defaultValue: false,
            description: 'Skip test stage'
        )
    }

    environment {
        KUBECONFIG_CRED = "kubeconfig-${params.ENVIRONMENT}"
        NAMESPACE = "${params.ENVIRONMENT}"
    }

    stages {
        stage('Build') {
            steps {
                sh 'npm ci && npm run build'
            }
        }

        stage('Test') {
            when {
                expression { !params.SKIP_TESTS }
            }
            steps {
                sh 'npm test'
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    expression { params.ENVIRONMENT == 'dev' }
                }
            }
            steps {
                withCredentials([file(credentialsId: env.KUBECONFIG_CRED, variable: 'KUBECONFIG')]) {
                    sh """
                        kubectl apply -f k8s/${params.ENVIRONMENT}/ -n ${NAMESPACE}
                        kubectl rollout status deployment/myapp -n ${NAMESPACE} --timeout=5m
                    """
                }
            }
        }

        stage('Production Approval') {
            when {
                expression { params.ENVIRONMENT == 'production' }
            }
            input {
                message "Deploy to production?"
                ok "Approve"
                submitter "admin,release-managers"
            }
            steps {
                echo 'Production deployment approved'
            }
        }
    }
}
```

---

## Shared Library Function Template

### vars/standardPipeline.groovy

```groovy
// vars/standardPipeline.groovy
def call(Map config = [:]) {
    def appName = config.appName ?: error('appName is required')
    def language = config.language ?: 'node'
    def deployEnabled = config.deploy ?: true

    pipeline {
        agent any

        environment {
            APP_NAME = "${appName}"
        }

        options {
            timeout(time: 30, unit: 'MINUTES')
            timestamps()
            buildDiscarder(logRotator(numToKeepStr: '10'))
        }

        stages {
            stage('Build') {
                steps {
                    script {
                        switch(language) {
                            case 'node':
                                sh 'npm ci && npm run build'
                                break
                            case 'python':
                                sh 'pip install -r requirements.txt'
                                break
                            case 'go':
                                sh 'go build -o app .'
                                break
                            default:
                                error("Unsupported language: ${language}")
                        }
                    }
                }
            }

            stage('Test') {
                steps {
                    script {
                        switch(language) {
                            case 'node':
                                sh 'npm test'
                                break
                            case 'python':
                                sh 'pytest'
                                break
                            case 'go':
                                sh 'go test ./...'
                                break
                        }
                    }
                }
            }

            stage('Deploy') {
                when {
                    expression { deployEnabled && env.BRANCH_NAME == 'main' }
                }
                steps {
                    sh "./deploy.sh ${appName}"
                }
            }
        }

        post {
            always {
                cleanWs()
            }
        }
    }
}
```

### Usage

```groovy
// Jenkinsfile
@Library('my-shared-library@v1.0.0') _

standardPipeline(
    appName: 'my-service',
    language: 'node',
    deploy: true
)
```

---

## Notification Template

```groovy
// vars/notifyBuild.groovy
def call(String status = 'STARTED') {
    def colorMap = [
        'STARTED': '#FFFF00',
        'SUCCESS': '#00FF00',
        'FAILURE': '#FF0000',
        'UNSTABLE': '#FFFF00'
    ]

    def color = colorMap[status] ?: '#808080'
    def summary = "${status}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"

    // Slack
    slackSend(
        color: color,
        message: summary,
        channel: '#builds'
    )

    // Email (on failure only)
    if (status == 'FAILURE') {
        emailext(
            subject: "Build ${status}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: """
                <p>Build ${status}</p>
                <p>Job: ${env.JOB_NAME}</p>
                <p>Build: ${env.BUILD_NUMBER}</p>
                <p>URL: ${env.BUILD_URL}</p>
            """,
            mimeType: 'text/html',
            recipientProviders: [
                culprits(),
                developers(),
                requestor()
            ]
        )
    }
}
```

---

## Docker Build and Push Template

```groovy
// vars/dockerBuildPush.groovy
def call(Map config = [:]) {
    def imageName = config.imageName ?: error('imageName is required')
    def registry = config.registry ?: 'docker.io'
    def credentialsId = config.credentials ?: 'docker-hub'
    def dockerfile = config.dockerfile ?: 'Dockerfile'
    def tags = config.tags ?: [env.BUILD_NUMBER, 'latest']
    def buildArgs = config.buildArgs ?: [:]

    def buildArgsString = buildArgs.collect { k, v -> "--build-arg ${k}=${v}" }.join(' ')
    def fullImageName = "${registry}/${imageName}"

    docker.withRegistry("https://${registry}", credentialsId) {
        def image = docker.build(
            "${fullImageName}:${env.BUILD_NUMBER}",
            "-f ${dockerfile} ${buildArgsString} ."
        )

        tags.each { tag ->
            image.push(tag)
        }
    }

    return fullImageName
}
```

---

## Helm Deployment Template

```groovy
// vars/helmDeploy.groovy
def call(Map config = [:]) {
    def releaseName = config.release ?: error('release is required')
    def chart = config.chart ?: error('chart is required')
    def namespace = config.namespace ?: 'default'
    def values = config.values ?: [:]
    def timeout = config.timeout ?: '5m'
    def kubeconfig = config.kubeconfig ?: 'kubeconfig'

    def setValues = values.collect { k, v -> "--set ${k}=${v}" }.join(' ')

    withCredentials([file(credentialsId: kubeconfig, variable: 'KUBECONFIG')]) {
        sh """
            helm upgrade --install ${releaseName} ${chart} \
                --namespace ${namespace} \
                --create-namespace \
                --wait \
                --timeout ${timeout} \
                ${setValues}
        """
    }
}
```

---

## Cleanup Template

```groovy
// vars/cleanupOldBuilds.groovy
def call(Map config = [:]) {
    def registry = config.registry ?: error('registry is required')
    def repository = config.repository ?: error('repository is required')
    def keepLast = config.keepLast ?: 10
    def dryRun = config.dryRun ?: false

    sh """
        # List all tags, sort by date, keep last N
        TAGS=\$(curl -s "https://${registry}/v2/${repository}/tags/list" | jq -r '.tags[]' | sort -r)
        COUNT=0

        for TAG in \$TAGS; do
            COUNT=\$((COUNT + 1))
            if [ \$COUNT -gt ${keepLast} ]; then
                echo "Deleting: ${registry}/${repository}:\$TAG"
                ${dryRun ? 'echo "[DRY RUN]"' : "curl -X DELETE https://${registry}/v2/${repository}/manifests/\$TAG"}
            fi
        done
    """
}
```
