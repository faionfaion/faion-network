# Agent Integration — Jenkins Basics

## When to use
- Brownfield enterprise CI: existing Jenkins controller, hundreds of Jenkinsfiles, plugin investments — migration cost > improvement payoff.
- Air-gapped / on-prem / strict-compliance environments where SaaS CI (GHA, GitLab.com) is not acceptable; Jenkins runs anywhere with a JVM.
- Pipelines that need long-running custom Groovy logic, deep filesystem access, or arbitrary plugin integrations (mainframe, legacy hardware).
- Multi-team shared library scenarios where a Groovy `@Library` is the unit of reuse across 50+ repos.
- Builds that need persistent agent state (caches, license files) across runs and don't fit the ephemeral-runner model.

## When NOT to use
- Greenfield projects on GitHub or GitLab — use the native CI; you avoid an entire ops surface (controller, plugins, agents, security CVEs).
- Teams that want declarative-only and dislike Groovy. Even "Declarative Pipeline" is Groovy under the hood, leaks at the edges.
- Cloud-native shops where ephemeral runners + OIDC + secret-less auth are the default — Jenkins requires extra plugins (oidc-provider, configuration-as-code) to match.
- Anyone unwilling to maintain plugins. Jenkins plugin CVE cadence is high; an unmaintained controller is a security liability.

## Where it fails / limitations
- **Plugin hell.** "It works on my Jenkins" because plugin versions diverge. Pin every plugin via `plugins.txt` + `jenkins-plugin-cli`, use Configuration-as-Code (JCasC) so the controller is reproducible.
- **Groovy sandbox approvals.** Agents write a `Jenkinsfile` with a method that's not whitelisted; first run requires manual admin approval. Agent stalls forever waiting for it.
- **Implicit `node {}` assumptions.** Scripted pipelines without explicit `node` blocks consume the controller's executor — single agent dies, all pipelines stall.
- **Workspace pollution.** `cleanWs()` is opt-in. Builds inherit dirty state from previous runs and produce phantom green/red.
- **Master/controller as build agent.** Default config in old installs lets jobs run on the controller — security disaster (full filesystem, secrets, kubeconfig).
- **Credentials binding leaks.** `withCredentials([string(credentialsId: 'X', variable: 'TOKEN')])` masks `$TOKEN` in logs but agents `echo $TOKEN | base64` and bypass masking.
- **Multibranch indexing storms.** A 5000-branch repo causes the controller to OOM on indexing; agents enable multibranch on a monorepo without thinking.
- **Shared libraries are global.** A breaking change to `vars/deploy.groovy` breaks every consumer pipeline at once. Versioning via Git tags is mandatory but rarely done.
- **Restart-from-stage** only works for Declarative pipelines, not Scripted; agents pick Scripted "for flexibility" and lose this.
- **Disk fills up.** Default workspace + build-history retention runs unbounded; controllers crash because `/var/jenkins_home` hits 100%.

## Agentic workflow
Treat Jenkins as a programmable platform with a real ops surface. Have one agent generate the Jenkinsfile (always Declarative unless there's a documented reason for Scripted), with `agent { kubernetes { ... } }` or `agent { docker { ... } }` — never `agent any`. A second agent maintains JCasC + `plugins.txt` + Dockerfile for the controller. A reviewer agent runs `jenkins-pipeline-linter` against the Jenkinsfile and `groovy:checkstyle` against shared library code. For shared library changes, force a versioned `@Library('mylib@v1.4.2')` ref and tag the library — agents must never use `@Library('mylib@main')` in production pipelines.

### Recommended subagents
- `faion-sdd-executor-agent` — quality gate: linter + dry-run against a parallel "review" controller (or a `jenkinsfile-runner` container).
- `password-scrubber-agent` — Jenkinsfiles attract `withCredentials` plus inline `curl -u user:pass` patterns.
- A custom `jcasc-validator` (Sonnet, read-only) — diffs proposed JCasC against running controller via API and lists destructive changes.
- A custom `plugin-cve-watcher` — pulls Jenkins security advisories, flags any installed plugin with open CVE.

### Prompt pattern
```
Generate a Declarative Jenkinsfile for <repo>. Inputs: language, build/test/deploy steps, target envs, agents available (k8s pod template name OR docker image), credentials needed (by ID), shared library ref.
Output: (1) full Jenkinsfile using `agent { kubernetes }` OR `agent { docker }`, (2) explicit `options { timeout, ansiColor, buildDiscarder, disableConcurrentBuilds, retry }`, (3) `parameters {}` for any human inputs, (4) `post { always cleanWs(); failure notifySlack() }`, (5) credentialsId list separately.
Forbid: `agent any` on master/controller, scripted blocks for trivial logic, shared library refs without an explicit version tag, secrets via env vars set outside withCredentials.
```

```
Lint: run `curl -X POST -F "jenkinsfile=<Jenkinsfile" $JENKINS_URL/pipeline-model-converter/validate`. Then parse, emit JSON {stages[], parallel_branches[], agents[], credentials_used[], post_actions[]}. Reject if any stage runs on built-in node OR uses credentialsId not declared in JCasC.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jenkins-cli.jar` | Run jobs, get logs, install plugins from CLI | `$JENKINS_URL/jnlpJars/jenkins-cli.jar` |
| `jenkins-plugin-cli` | Install plugins from `plugins.txt` reproducibly | https://github.com/jenkinsci/plugin-installation-manager-tool |
| `jenkinsfile-runner` | Run a Jenkinsfile locally without a server | https://github.com/jenkinsci/jenkinsfile-runner |
| Pipeline Linter (REST) | `POST /pipeline-model-converter/validate` validates Declarative syntax | built-in |
| `jcasc-export` (REST) | Dump current config as YAML for diff | https://www.jenkins.io/projects/jcasc/ |
| `jenkinsapi` (Python) / `python-jenkins` | Programmatic SDK | https://python-jenkins.readthedocs.io |
| `groovylint` / `npm-groovy-lint` | Lint Jenkinsfile + shared lib Groovy | https://nvuillam.github.io/npm-groovy-lint/ |
| `hadolint` | Lint controller/agent Dockerfiles | https://github.com/hadolint/hadolint |
| `trivy` / `grype` | Scan controller image for plugin/JVM CVEs | https://github.com/aquasecurity/trivy |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jenkins (self-hosted) | OSS | Partial | Programmable, but plugin churn + restart cycles slow agentic loops. |
| CloudBees CI | Commercial | Yes | Multi-controller, RBAC, bundled JCasC; agents get a stable target. |
| Jenkins X | OSS | Limited | Declarative, K8s-native — but largely superseded by Tekton/Argo. |
| Kubernetes plugin | OSS | Yes | Pod-per-build agents; the only sane way to run Jenkins at scale. |
| Configuration-as-Code (JCasC) plugin | OSS | Yes | Controller config in YAML; agents diff/apply via Git. |
| Job DSL plugin | OSS | Partial | Generate jobs from Groovy seed; agents prefer Multibranch + JCasC. |
| Blue Ocean | OSS | Partial | UI only; agents don't need it. |
| Tekton / Argo Workflows | OSS | Yes | Common K8s-native replacements when migrating off Jenkins. |
| HashiCorp Vault | OSS / SaaS | Yes | Vault plugin issues short-lived creds; replace static credentials. |
| Slack / PagerDuty plugins | SaaS | Yes | Standard `post { failure }` notifications. |

## Templates & scripts
See `templates.md` for shared library + Jenkinsfile starters. Reproducible controller image (≤40 lines) — agents should use this as the baseline and never hand-install plugins:

```dockerfile
# Dockerfile for a reproducible Jenkins controller
FROM jenkins/jenkins:2.452.3-lts-jdk17

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl jq git docker.io \
    && rm -rf /var/lib/apt/lists/*
USER jenkins

# Pin every plugin
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt --verbose

# JCasC: controller is pure config, no manual setup
COPY casc/ /var/jenkins_home/casc_configs/
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/casc_configs/

# Groovy init: disable build-on-controller, set executors=0 on master
COPY init.groovy.d/ /usr/share/jenkins/ref/init.groovy.d/

# Disable setup wizard, run-from-package config
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false -Dhudson.model.DirectoryBrowserSupport.CSP=\"\""
```

```groovy
// init.groovy.d/00-disable-master-builds.groovy
import jenkins.model.*
Jenkins.instance.setNumExecutors(0)
Jenkins.instance.save()
```

## Best practices
- Always Declarative over Scripted; reach for Scripted only inside a Shared Library `vars/*.groovy` if Declarative truly cannot express the logic.
- Pin plugin versions (`plugins.txt`), pin shared library versions (`@Library('lib@v1.2.3')`), pin agent images by digest.
- Controller has zero executors; all builds on labeled K8s pods or Docker agents.
- JCasC + Groovy `init.groovy.d` is the only way to mutate controller config. UI-driven changes are forbidden — they are unreviewable.
- Use `withCredentials` for every secret; never store plaintext in environment, NEVER `echo` secrets even masked.
- `options { timeout(time: 30, unit: 'MINUTES'); buildDiscarder(logRotator(numToKeepStr: '50')); disableConcurrentBuilds() }` on every pipeline. Unbounded pipelines = fillable disk + races.
- Multibranch with `excludeBranches` filter — never index a 5000-branch monorepo without filters.
- `cleanWs()` in `post { always }` everywhere.
- Audit `Authorize Project` plugin or equivalent: jobs run as a project-bound identity, not the global agent.
- Maintenance window: weekly controller restart + plugin update sweep; track CVE feed.

## AI-agent gotchas
- Groovy CPS sandbox: agents call `Files.list()` or `new URL(...).text` — these are not whitelisted; first run requires admin approval that never comes in CI. Always use plugin-provided steps (`readFile`, `httpRequest`) instead.
- Closures + iteration: `list.each { ... }` is non-CPS-friendly under heavy iteration; use plain `for` loops in shared libraries.
- `def` variables across stages disappear. Agents declare `def x = 1` in stage A and reference in stage B — fails with `MissingPropertyException`. Use environment block or `script { }` with explicit binding.
- Parallel + `failFast: true` plus `unstable` results — agents misread non-zero stage exits as build failures and trigger duplicate alerts.
- `try/catch` in Declarative requires a `script {}` block. Agents copy try/catch from Scripted samples; pipeline fails to parse.
- Shared library breaking change with no version pin → fleet-wide pipeline outage. Force tagged refs and a "library compat" check in the library's own pipeline.
- Human-in-loop checkpoints: any change to JCasC role assignments, credentialsId definitions, or controller plugin set MUST require human approval. These touch the trust boundary of every job on the controller.
- Plugin install mid-build occasionally restarts the controller; agents that auto-upgrade plugins during a deploy window cause production stalls.
- Groovy `String` interpolation inside `sh "..."` is a shell-injection footgun: agents emit `sh "echo ${userInput}"` — always use single-quoted `sh '''echo "$USER_INPUT"'''` + env var binding.

## References
- Pipeline best practices — https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/
- Declarative syntax reference — https://www.jenkins.io/doc/book/pipeline/syntax/
- Configuration-as-Code (JCasC) — https://www.jenkins.io/projects/jcasc/
- Kubernetes plugin — https://plugins.jenkins.io/kubernetes/
- jenkinsfile-runner — https://github.com/jenkinsci/jenkinsfile-runner
- Jenkins Security Advisories — https://www.jenkins.io/security/advisories/
- Shared libraries — https://www.jenkins.io/doc/book/pipeline/shared-libraries/
- Pipeline linter — https://www.jenkins.io/doc/book/pipeline/development/#linter
