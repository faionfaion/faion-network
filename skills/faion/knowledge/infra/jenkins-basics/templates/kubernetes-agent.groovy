// purpose: Kubernetes pod template for dynamic Jenkins agents
// consumes: nodeImage, helmVersion, resource request/limit overrides
// produces: agent_kind=kubernetes container per content/02-output-contract.xml
// depends-on: content/01-core-rules.xml (kubernetes-agent, zero-controller-executors)
// token-budget-impact: ~500 tokens when loaded as context
// Copy into vars/ of your Shared Library.
// Usage: kubernetesAgent(nodeImage: 'node:20', helmVersion: '3.14') { ... }

def call(Map config = [:], Closure body) {
    def nodeImage  = config.get('nodeImage',  'node:20-alpine')
    def helmVersion = config.get('helmVersion', '3.14')
    def cpuRequest  = config.get('cpuRequest',  '500m')
    def memRequest  = config.get('memRequest',  '512Mi')
    def cpuLimit    = config.get('cpuLimit',    '2')
    def memLimit    = config.get('memLimit',    '2Gi')

    podTemplate(
        label: "jenkins-k8s-${UUID.randomUUID().toString()}",
        containers: [
            containerTemplate(
                name: 'jnlp',
                image: 'jenkins/inbound-agent:latest',
                resourceRequestCpu: '100m',
                resourceRequestMemory: '128Mi'
            ),
            containerTemplate(
                name: 'build',
                image: nodeImage,
                command: 'cat',
                ttyEnabled: true,
                resourceRequestCpu: cpuRequest,
                resourceRequestMemory: memRequest,
                resourceLimitCpu: cpuLimit,
                resourceLimitMemory: memLimit
            ),
            containerTemplate(
                name: 'helm',
                image: "alpine/helm:${helmVersion}",
                command: 'cat',
                ttyEnabled: true,
                resourceRequestCpu: '100m',
                resourceRequestMemory: '128Mi'
            ),
            containerTemplate(
                name: 'docker',
                image: 'docker:24-dind',
                privileged: true,
                resourceRequestCpu: '500m',
                resourceRequestMemory: '512Mi'
            )
        ],
        volumes: [
            emptyDirVolume(mountPath: '/var/lib/docker', memory: false)
        ]
    ) {
        node(POD_LABEL) {
            body()
        }
    }
}

// Example usage in a Jenkinsfile:
//
// @Library('my-shared-library@main') _
//
// kubernetesAgent(nodeImage: 'node:20-alpine', helmVersion: '3.14') {
//     stage('Build') {
//         container('build') {
//             sh 'npm ci && npm run build'
//         }
//     }
//     stage('Deploy') {
//         container('helm') {
//             withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
//                 sh 'helm upgrade --install myapp ./charts/myapp --wait'
//             }
//         }
//     }
// }
