// vars/buildApp.groovy
// Shared library: build Docker image and push to registry
def call(Map config = [:]) {
    def appName  = config.appName  ?: error('appName is required')
    def registry = config.registry ?: error('registry is required')
    def version  = config.version  ?: env.BUILD_NUMBER
    def context  = config.context  ?: '.'
    def dockerfile = config.dockerfile ?: 'Dockerfile'

    withCredentials([usernamePassword(
        credentialsId: config.registryCredId ?: 'docker-registry',
        usernameVariable: 'DOCKER_USER',
        passwordVariable: 'DOCKER_PASS'
    )]) {
        sh """
            echo "\$DOCKER_PASS" | docker login ${registry} -u "\$DOCKER_USER" --password-stdin
            docker build -f ${dockerfile} -t ${registry}/${appName}:${version} ${context}
            docker push ${registry}/${appName}:${version}
            docker tag  ${registry}/${appName}:${version} ${registry}/${appName}:latest
            docker push ${registry}/${appName}:latest
        """
    }

    echo "Built and pushed ${registry}/${appName}:${version}"
    return "${registry}/${appName}:${version}"
}
