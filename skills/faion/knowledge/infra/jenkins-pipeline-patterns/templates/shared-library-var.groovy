// purpose: vars/buildApp.groovy — CPS-safe Shared Library function with @NonCPS escape hatch
// consumes: language + buildCommand params; runs inside any Declarative pipeline
// produces: shared_libraries entry in 02-output-contract.xml artefact (version_pinned=true)
// depends-on: content/01-core-rules.xml (shared-lib-dedicated-repo, library-version-pinned)
// token-budget-impact: ~400 tokens when loaded as context

import java.util.regex.Pattern

def call(Map config = [:]) {
    String language = config.get('language')
    String buildCommand = config.get('buildCommand')
    Integer timeoutMin = config.get('timeoutMin', 15)

    if (!language || !buildCommand) {
        error("buildApp requires language + buildCommand")
    }

    // Pipeline scope — only primitives and Serializable types
    try {
        timeout(time: timeoutMin, unit: 'MINUTES') {
            sh buildCommand
        }
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        notifyFailure(language: language, error: e.message)
        throw e
    }
}

// Pattern is NOT Serializable — must run inside @NonCPS so it never crosses a CPS checkpoint.
@NonCPS
boolean matchesPolicy(String text, String regex) {
    Pattern p = Pattern.compile(regex)
    return p.matcher(text).find()
}

def notifyFailure(Map cfg) {
    // Delegate to another vars/ function so the message lives in one place across the org.
    notifySlack(
        channel: '#ci-alerts',
        message: "buildApp[${cfg.language}] failed: ${cfg.error}"
    )
}
