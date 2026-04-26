# Agent Integration — Jenkins Pipeline Patterns

## When to use
- Brownfield org running Jenkins controller (LTS) where migration to GitHub Actions / GitLab CI is not on the roadmap.
- You need a Groovy shared library to enforce conventions across 50+ pipelines (build/test/deploy/notify steps).
- Matrix or fan-out builds across multiple JDK / Node / OS axes that GitHub Actions matrices cannot express cheaply.
- Heavy on-prem / air-gapped scenarios with self-hosted agents and tight Vault / Artifactory integration.
- Existing investment in Jenkinsfile + plugin ecosystem (Blue Ocean, Configuration as Code, Job DSL).

## When NOT to use
- Greenfield repo on GitHub or GitLab — use native CI; Jenkins adds operator burden with no upside.
- Solo dev or small team — Jenkins controller maintenance (plugin upgrades, JVM tuning, agent provisioning) outweighs benefits.
- Workloads that fit cleanly into GitHub Actions reusable workflows or composite actions.
- Ephemeral / serverless CI requirements — Jenkins is stateful and assumes long-lived controllers.

## Where it fails / limitations
- CPS (Continuation-Passing Style) Groovy: any non-`Serializable` field inside a pipeline causes opaque `NotSerializableException` at random checkpoints. Agents must remember `@NonCPS` annotation rules.
- Plugin matrix instability: an LTS upgrade can silently break shared library steps. Pin plugin versions in `plugins.txt`.
- Sandbox / script approval: new Groovy methods require admin approval through `/scriptApproval` — blocks autonomous agents.
- Pipeline durability vs performance trade-off: `durability: PERFORMANCE_OPTIMIZED` loses state on controller crash.
- Parallel branches share the same workspace by default — non-obvious file races without `dir()` or `ws()`.

## Agentic workflow
Subagents are useful for three concrete jobs: (1) generating a fresh `Jenkinsfile` from a declarative template based on the repo's stack, (2) extracting recurring `sh` blocks into a shared library (`vars/buildApp.groovy`) and writing the JUnit-style test for it under `test/groovy/...`, (3) diagnosing a failing build by reading the console log + Stage View JSON via the Jenkins REST API. Keep the agent loop bounded: render Jenkinsfile → run `jenkins-cli declarative-linter` → fix → submit. Do not let the agent keep retrying live builds; that burns executor time and pollutes history.

### Recommended subagents
- `faion-sdd-executor` — drives Jenkinsfile changes through the SDD quality gate (lint → unit test → integration test).
- A purpose-built `jenkins-pipeline-author` subagent (define inline) — narrow scope: edit `Jenkinsfile` / `vars/*.groovy`, run linter, never push to `main`.
- `password-scrubber` — sweep generated Jenkinsfiles for credentials before commit (Jenkins encourages inline `withCredentials` blocks but secrets often leak into `echo`).

### Prompt pattern
```
You are editing Jenkinsfile in <repo>. Constraints:
- Declarative pipeline only (no scripted blocks at top level).
- Use shared library `@Library('platform@v1.4')`.
- Wrap any sh step that touches secrets in withCredentials().
- After edit, run: jenkins-cli -s $JENKINS_URL declarative-linter < Jenkinsfile.
- Do not push; output unified diff only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jenkins-cli.jar` | Linter, job CRUD, reload config | https://www.jenkins.io/doc/book/managing/cli/ |
| `jcasc-validator` | Validate Configuration-as-Code YAML | https://github.com/jenkinsci/configuration-as-code-plugin |
| `jenkinsfile-runner` | Run a Jenkinsfile in CLI / container without a controller | https://github.com/jenkinsci/jenkinsfile-runner |
| `jenkins-job-builder` (jjb) | Generate jobs from YAML (legacy XML jobs) | https://docs.openstack.org/infra/jenkins-job-builder/ |
| `gh` / `glab` | Pre-merge `Jenkinsfile` lint via webhook stub | https://cli.github.com/ |
| `groovy` | Validate `vars/*.groovy` syntax locally | https://groovy-lang.org/ |
| `jenkins.io` REST API | `curl $URL/job/<name>/wfapi/runs` for stage timing JSON | https://www.jenkins.io/doc/book/using/remote-access-api/ |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| CloudBees CI | SaaS / on-prem (commercial Jenkins) | Yes — REST API, RBAC | Multi-controller ops; `cbci` CLI |
| Jenkins X | OSS (k8s-native, GitOps) | Partial | Largely superseded by Tekton/ArgoCD; avoid for new projects |
| Tekton Pipelines | OSS (k8s-native) | Yes — `tkn` CLI, declarative YAML | Use as Jenkins replacement, not adjunct |
| Artifactory / Nexus | SaaS / OSS | Yes — REST API | Standard Jenkins artifact target; agents can publish/promote |
| HashiCorp Vault | SaaS / OSS | Yes | Use Vault plugin or `vault` CLI inside `sh` instead of credentials store |
| SonarQube | SaaS / OSS | Yes | `sonar-scanner` step; webhook back to PR |
| Selenoid / Sauce Labs | SaaS | Yes | For matrix browser tests inside parallel stages |

## Templates & scripts
See `templates.md` for full Jenkinsfile and shared-library skeleton. Inline minimum to lint a Jenkinsfile from an agent without a Jenkins controller:

```bash
#!/usr/bin/env bash
set -euo pipefail
JENKINSFILE="${1:-Jenkinsfile}"
docker run --rm -v "$PWD":/work -w /work \
  jenkins/jenkinsfile-runner:latest \
  --file "$JENKINSFILE" --runWorkspace /tmp/ws --no-sandbox \
  > /tmp/jfr.log 2>&1
grep -E "^(ERROR|FAILED)" /tmp/jfr.log && exit 1 || echo "OK"
```

## Best practices
- One `vars/*.groovy` step = one verb. `buildApp`, `deployToK8s`, `notifySlack`. Never `doEverything`.
- Pin shared library by tag in production: `@Library('platform@v1.4.2') _`. Floating `@main` causes non-deterministic builds.
- Always declare `options { timeout(time: 30, unit: 'MINUTES'); buildDiscarder(logRotator(numToKeepStr: '50')) }`. Stuck builds and unbounded log retention are the top two operator pain points.
- Use `lock(resource: 'shared-db')` instead of disabling concurrent builds globally.
- Prefer Kubernetes plugin pod templates over static node labels for parallel stages — eliminates resource exhaustion.
- Treat `Jenkinsfile` as application code: PR review, unit tests via `JenkinsPipelineUnit`, integration tests via `jenkinsfile-runner`.
- Configuration-as-Code (JCasC) for the controller itself — agents read/edit YAML, never click through UI.
- Mirror Jenkinsfile syntax updates into a doc snippet repo so agents have ground truth, not stale examples.

## AI-agent gotchas
- Groovy CPS rules trip LLMs: closures over non-serializable objects (`Pattern`, `Matcher`, `JsonSlurperResult`) compile fine but explode at runtime. Force agent to wrap such logic in `@NonCPS def helper() { ... }` returning primitives.
- LLMs over-use scripted blocks (`script { ... }`) inside declarative pipelines because that is what training data shows. Add an explicit constraint in the system prompt: "no `script` blocks unless declarative cannot express it; explain why in a comment."
- Jenkins error messages reference internal class names (`org.jenkinsci.plugins.workflow.cps.CpsThread`); agents misinterpret these as application errors. Pre-process logs with a known-error rewrite table before feeding to the agent.
- Plugin install is global state mutation — never let an agent run `jenkins-cli install-plugin` on a shared controller. Require human approval gate.
- Credentials binding via `withCredentials` masks values in console — but `set -x` in a `sh` block leaks them. Add a lint rule that bans `set -x` inside `withCredentials`.
- Webhook-triggered builds + LLM authoring loops can fork-bomb the queue if a generated Jenkinsfile triggers itself. Always include `triggers { }` review in agent checklist.
- Long-running builds break agent context windows when the agent tails the log. Use Stage View JSON (`/wfapi/runs`) for compact status.

## References
- Jenkins Pipeline Syntax — https://www.jenkins.io/doc/book/pipeline/syntax/
- Shared Libraries — https://www.jenkins.io/doc/book/pipeline/shared-libraries/
- Jenkins Configuration as Code — https://github.com/jenkinsci/configuration-as-code-plugin
- Jenkinsfile Runner — https://github.com/jenkinsci/jenkinsfile-runner
- JenkinsPipelineUnit — https://github.com/jenkinsci/JenkinsPipelineUnit
- CPS / `@NonCPS` reference — https://www.jenkins.io/doc/book/pipeline/cps-method-mismatches/
- CloudBees CI — https://docs.cloudbees.com/docs/cloudbees-ci/latest/
