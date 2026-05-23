pipeline {
    agent {
        kubernetes {
            yaml '''
                spec:
                  containers:
                  - name: node
                    image: node:20-alpine
                    command: [cat]
                    tty: true
                    resources:
                      requests:
                        cpu: 500m
                        memory: 512Mi
                  - name: docker
                    image: docker:24-dind
                    securityContext:
                      privileged: true
                    env:
                    - name: DOCKER_TLS_CERTDIR
                      value: ""
                  - name: kubectl
                    image: bitnami/kubectl:latest
                    command: [cat]
                    tty: true
            '''
        }
    }

    environment {
        VERSION = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
        REGISTRY = credentials('docker-registry-url')
    }

    options {
        timeout(time: 45, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Test') {
            parallel {
                stage('Unit') {
                    steps {
                        container('node') { sh 'npm ci && npm run test:unit' }
                    }
                }
                stage('Security') {
                    steps {
                        container('node') { sh 'npm audit --audit-level=high' }
                    }
                }
            }
        }

        stage('Build & Push') {
            steps {
                container('docker') {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-registry',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh """
                            echo "\$DOCKER_PASS" | docker login \$REGISTRY -u "\$DOCKER_USER" --password-stdin
                            docker build -t \$REGISTRY/myapp:\$VERSION .
                            docker push \$REGISTRY/myapp:\$VERSION
                        """
                    }
                }
            }
        }

        stage('Deploy Staging') {
            when { branch 'main' }
            steps {
                container('kubectl') {
                    withCredentials([file(credentialsId: 'kubeconfig-staging', variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl set image deployment/myapp myapp=\$REGISTRY/myapp:\$VERSION -n staging
                            kubectl rollout status deployment/myapp -n staging --timeout=5m
                        """
                    }
                }
            }
        }

        stage('Deploy Production') {
            when { branch 'main' }
            input { message "Deploy to production?"; submitter "admin,deployers" }
            steps {
                container('kubectl') {
                    withCredentials([file(credentialsId: 'kubeconfig-prod', variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl set image deployment/myapp myapp=\$REGISTRY/myapp:\$VERSION -n production
                            kubectl rollout status deployment/myapp -n production --timeout=5m
                        """
                    }
                }
            }
        }
    }

    post {
        always  { cleanWs() }
        failure { slackSend(color: 'danger', message: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}") }
    }
}
