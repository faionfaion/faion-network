// vars/notifySlack.groovy
// Shared library: Slack notification with status color
def call(Map config = [:]) {
    def channel = config.channel ?: '#builds'
    def status  = config.status  ?: currentBuild.currentResult
    def message = config.message ?: "${env.JOB_NAME} #${env.BUILD_NUMBER} — ${status}"

    def colorMap = [
        'SUCCESS' : 'good',
        'FAILURE' : 'danger',
        'UNSTABLE': 'warning',
        'ABORTED' : '#808080',
    ]
    def color = colorMap[status] ?: '#808080'

    slackSend(
        channel: channel,
        color:   color,
        message: "${message} (<${env.BUILD_URL}|Open>)"
    )
}
