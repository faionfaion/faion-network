// vars/deployToK8s.groovy
// Shared library: kubectl set image + rollout status
def call(Map config = [:]) {
    def namespace  = config.namespace  ?: error('namespace is required')
    def deployment = config.deployment ?: error('deployment is required')
    def image      = config.image      ?: error('image is required')
    def timeout    = config.timeout    ?: '5m'
    def credId     = config.credId     ?: 'kubeconfig'

    withCredentials([file(credentialsId: credId, variable: 'KUBECONFIG')]) {
        sh """
            kubectl set image deployment/${deployment} ${deployment}=${image} -n ${namespace}
            kubectl rollout status deployment/${deployment} -n ${namespace} --timeout=${timeout}
        """
    }

    echo "Deployed ${image} to ${namespace}/${deployment}"
}
