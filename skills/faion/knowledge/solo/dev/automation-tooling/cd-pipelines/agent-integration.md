# Agent Integration — CD Pipelines & Deployment Strategies

## When to use
- Authoring or refactoring a `.github/workflows/cd.yml` (or GitLab CI / CircleCI / Buildkite equivalent) for a single service.
- Adding deployment-strategy primitives: blue/green, canary, rolling, with proper readiness/liveness probes.
- Wiring smoke tests, rollback, deployment notifications, and DORA metric tracking into an existing pipeline.
- Replacing ad-hoc shell scripts (`deploy-gh.sh`) with a structured, observable pipeline.
- Diagnosing why a pipeline blocks: flaky integration tests, missing approvals, image-tag drift, race between rollout-status and smoke tests.

## When NOT to use
- For pure CI (build + test only) — see `cd-basics` and a CI-focused skill instead.
- For full platform engineering (multi-cluster, cross-region, GitOps with Argo/Flux). Use `pro/infra/cicd-engineer` and `argocd-gitops` knowledge.
- For serverless deploys with vendor-managed pipelines (Vercel, Netlify, Cloud Run "Continuous Deploy") — those mostly need build config, not workflow YAML.
- For monorepos with selective deploys per package — that needs Turborepo/Nx-aware pipelines that this methodology does not cover.
- For hand-off to humans only ("ops opens a ticket") — these patterns assume automation-first.

## Where it fails / limitations
- README's GitHub Actions YAML is illustrative: no caching, no concurrency control, no OIDC for cloud auth, no image-pull secrets — agents must add those.
- Canary example uses Istio; if the cluster runs Linkerd, NGINX-Ingress canary, or no service mesh, the YAML must be rewritten.
- Blue/green via label-swap is brittle for stateful services: db migrations + sticky sessions need extra orchestration.
- Rolling-update example has a single `maxSurge: 2 / maxUnavailable: 1` — ignores PDBs, topology spread, and zero-downtime requirements.
- Smoke tests are referenced via `./scripts/smoke-tests.sh` but the script is undefined — agents must author and pin it.
- Rollback strategy assumes `kubectl rollout undo` works; for canary/blue-green you actually want to swap traffic, not roll back the deployment object.
- Datadog DORA snippet is half-baked — change-failure-rate requires correlating to incidents, not just deploy outcome.

## Agentic workflow
Use a planner agent that reads `cd-basics` first, then this file, then drafts the pipeline as discrete jobs (build, integ, staging, e2e, prod). Each job becomes a small executor task: write YAML, validate with `actionlint`/`gitlab-ci-lint`, commit, watch the first run, fix failures. Force a human approval gate before any production deploy job is wired up. Capture the final pipeline run URL + DORA metric instrumentation as deliverables. Never let an autonomous agent push to a production environment that lacks an approval rule.

### Recommended subagents
- `general-purpose` — drafts the workflow YAML, runs lint, iterates on lint failures.
- `faion-sdd-executor-agent` — when the CD work is decomposed as SDD tasks under `.aidocs/in-progress/`.
- A narrow `pipeline-validator` task agent — only runs `actionlint`, `kubeval`, `kustomize build`, `helm template`; reports diffs.
- A `rollback-rehearsal` task agent — drives a staging-only intentional failure to prove the rollback path works.

### Prompt pattern
```
Read solo/dev/automation-tooling/cd-pipelines/README.md and cd-basics/README.md.
Author .github/workflows/cd.yml for service <name> targeting <cluster> with
strategy=<canary|blue-green|rolling>. Add: concurrency group, OIDC to <cloud>,
image cache, smoke-test script, automatic rollback on smoke fail, Slack notify.
Validate with `actionlint -shellcheck`. Open a draft PR — DO NOT enable the
prod job; leave it commented with a TODO for human approval.
```
```
Given an existing pipeline at <path>, audit against DORA metrics. Add
instrumentation that emits deploy_started / deploy_succeeded / deploy_failed
events with version+sha+duration to <metrics-backend>.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `actionlint` | Static lint for GitHub Actions YAML | rhysd/actionlint |
| `gitlab-ci-lint` (`glab ci lint`) | Lint GitLab CI YAML | glab CLI |
| `gh workflow run` / `gh run watch` | Trigger + tail GHA runs from CLI | GitHub CLI |
| `kubectl rollout status` / `undo` | Wait/observe rollouts; manual rollback | kubernetes/kubectl |
| `kubeval` / `kubeconform` | Validate K8s manifests against schema | github.com/yannh/kubeconform |
| `helm template` / `helm lint` / `helm diff` | Render + diff charts before apply | helm.sh |
| `kustomize build` | Render overlays | kustomize.io |
| `argocd app sync` / `argocd app rollback` | GitOps deploy/rollback | argo-cd CLI |
| `flagger` | Progressive delivery operator (canary, blue/green, A/B) | flagger.app |
| `kayenta` / `spinnaker` | Canary analysis | spinnaker.io |
| `dora-metrics` (Google) / `four-keys` | Compute DORA from event stream | github.com/dora-team/fourkeys |
| `cosign` / `syft` / `grype` | Sign images + SBOM + vuln scan in pipeline | sigstore.dev |
| `kubectl-tree` / `stern` | Inspect rollout tree + tail logs | krew |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes | Best agent ergonomics: `gh` CLI + actionlint + reusable workflows. |
| GitLab CI/CD | SaaS + OSS | Yes | Pipeline-as-code; environments + manual approvals built-in. |
| Argo CD | OSS | Yes | GitOps; agents commit manifests, controller deploys. |
| Flux CD | OSS | Yes | GitOps alternative; image-policy auto-bumps tags. |
| Argo Rollouts | OSS | Yes | Canary + blue/green CRDs; pairs cleanly with Argo CD. |
| Flagger | OSS | Yes | Automated canary + analysis on Linkerd/Istio/NGINX. |
| Spinnaker | OSS | Partial | Heavy install; powerful canary. |
| AWS CodeDeploy | SaaS | Yes | Built-in blue/green for ECS/EC2/Lambda. |
| Google Cloud Deploy | SaaS | Yes | Skaffold-driven progressive delivery. |
| Octopus Deploy | SaaS | Partial | Strong UI, less agent-friendly than YAML-first tools. |
| LaunchDarkly / Unleash / Flagsmith | SaaS / OSS | Yes | Decouples deploy from release — feature flags as canary substitute. |
| Datadog / Honeycomb / Grafana | SaaS / OSS | Yes | Pipeline emits deploy markers; SLO burn-rate gates rollout. |
| PagerDuty / Opsgenie | SaaS | Yes | Wire `deploy_failed` to incident; track time-to-restore. |
| Slack / Discord / Telegram | SaaS | Yes | Notify channels via webhook in final pipeline step. |

## Templates & scripts
See `templates.md` and `examples.md` for full pipeline. Minimum smoke + auto-rollback wrapper:

```bash
#!/usr/bin/env bash
# scripts/deploy-with-rollback.sh
set -euo pipefail
NS="${1:?namespace}"
DEP="${2:?deployment}"
IMAGE="${3:?image:tag}"
URL="${4:?smoke-url}"

PREV=$(kubectl -n "$NS" get deploy "$DEP" -o jsonpath='{.spec.template.spec.containers[0].image}')
kubectl -n "$NS" set image "deploy/$DEP" "$DEP=$IMAGE"
if ! kubectl -n "$NS" rollout status "deploy/$DEP" --timeout=5m; then
  kubectl -n "$NS" rollout undo "deploy/$DEP"
  exit 1
fi
if ! curl -fsS --max-time 10 --retry 6 --retry-delay 5 "$URL/health/ready" >/dev/null; then
  echo "Smoke failed — rolling back to $PREV"
  kubectl -n "$NS" set image "deploy/$DEP" "$DEP=$PREV"
  kubectl -n "$NS" rollout status "deploy/$DEP" --timeout=5m
  exit 1
fi
echo "Deploy ok: $IMAGE"
```

## Best practices
- Add `concurrency: { group: deploy-${{ github.ref }}, cancel-in-progress: false }` so two pushes don't deploy in parallel.
- Use OIDC federation (GitHub → AWS/GCP/Azure) instead of long-lived secrets in repo.
- Pin every action by SHA, not tag (`actions/checkout@<sha>`); supply-chain hygiene.
- Image tag = commit SHA (immutable), not `latest`. Required for rollback determinism.
- Smoke tests must be the same script in staging and prod, parameterized by base URL.
- For canary, gate promotion on SLO burn rate (Honeycomb / Datadog / Prometheus alert), not just HTTP status.
- Run schema migrations in a dedicated job before the deploy job, with its own rollback (or expand-contract pattern) — never inline in the app deploy.
- Emit DORA events to a single sink so the metric pipeline survives tool changes.
- Keep the prod job behind GitHub `environment: production` with required reviewers; agents cannot bypass.

## AI-agent gotchas
- Agents tend to copy the README's `kubectl set image` snippet verbatim, missing image digest pinning and namespace scoping.
- Don't let an agent generate `--force` or `--grace-period=0` flags — they bypass safety nets.
- Agents misuse `continue-on-error: true` — they will hide a real failure to make the pipeline "pass."
- Secrets: agents will paste tokens into workflow YAML during debugging. Require a pre-commit secret scanner (`gitleaks`, `trufflehog`).
- Canary: agents will set `weight: 50` on first deploy. Force a 5%/15min initial step.
- Rollback: agents may rollback the K8s deployment but forget to roll back the schema. Couple them.
- DORA: agents will compute deploy frequency without de-duplicating retries — instrument once at the gate, not per attempt.
- Rolling: agents drop readiness probes when the app starts slow; mandate `initialDelaySeconds` calibrated to real boot time.
- Approval gates: agents will helpfully "remove the manual approval to make CI green." Block this in code review.

## References
- Jez Humble & David Farley, Continuous Delivery (Pearson).
- Forsgren et al., Accelerate (IT Revolution) — DORA metrics origin.
- Argo Rollouts: https://argo-rollouts.readthedocs.io/
- Flagger: https://flagger.app/
- GitHub Actions security hardening: https://docs.github.com/actions/security-guides
- Kubernetes Deployment strategies: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Sibling: `solo/dev/automation-tooling/cd-basics/`, `feature-flags/`, `continuous-delivery/`.
