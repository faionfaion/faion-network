@Library('my-shared-library@v1.2.3') _

pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        APP_NAME    = 'myapp'
        REGISTRY    = 'registry.example.com'
        VERSION     = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'npm ci && npm run test:unit'
                    }
                    post {
                        always {
                            junit 'test-results/**/*.xml'
                        }
                    }
                }
                stage('Security Scan') {
                    steps {
                        sh 'npm audit --audit-level=high'
                    }
                }
            }
        }

        stage('Build') {
            steps {
                buildApp(
                    appName:  env.APP_NAME,
                    registry: env.REGISTRY,
                    version:  env.VERSION
                )
            }
        }

        stage('Deploy Staging') {
            when { branch 'main' }
            steps {
                deployToK8s(
                    namespace:  'staging',
                    deployment: env.APP_NAME,
                    image:      "${env.REGISTRY}/${env.APP_NAME}:${env.VERSION}"
                )
            }
        }

        stage('Deploy Production') {
            when { branch 'main' }
            input {
                message "Deploy ${env.VERSION} to production?"
                submitter "admin,deployers"
            }
            steps {
                deployToK8s(
                    namespace:  'production',
                    deployment: env.APP_NAME,
                    image:      "${env.REGISTRY}/${env.APP_NAME}:${env.VERSION}"
                )
            }
        }
    }

    post {
        always  { cleanWs() }
        success { notifySlack(channel: '#deployments', status: 'SUCCESS') }
        failure { notifySlack(channel: '#deployments', status: 'FAILURE') }
    }
}
