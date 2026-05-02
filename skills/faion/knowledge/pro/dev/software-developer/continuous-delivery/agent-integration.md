# Agent Integration — Continuous Delivery

## When to use
- Web/SaaS products with user-facing changes that benefit from short feedback loops (multiple deploys per day).
- Teams already on CI with green-on-main as a hard rule and looking for the next maturity step.
- Microservices with independent deploy cadence; each service owning its pipeline.
- Mobile/desktop apps backed by app-store review — CD to TestFlight / Play internal track is still valuable.
- Regulated environments where audited, automated, repeatable releases beat manual change-control toil.
- DORA elite targets (deploy daily+, lead-time <1h, change-fail <15%, MTTR <1h).

## When NOT to use
- Truly batched/manual release contexts (firmware on shipped hardware, embedded in vehicles, regulated medical devices with formal validation per release). The pipeline still applies, but "every commit deployable" is a misframing.
- Teams without comprehensive automated tests or with flaky suites. CD on top of <50% coverage just ships bugs faster. Fix tests first.
- Pre-MVP / pre-product-market-fit when the deploy cost is a `git push` to one VM. The CD machinery costs more than the wins.
- Solo project with one production environment and zero customers — daily local push is sufficient.
- Schema changes that aren't backward-compatible-by-construction. Without expand/contract discipline, CD turns a bad migration into a 30-second outage.

## Where it fails / limitations
- **Test pyramid inversion.** Teams write E2E tests because "they cover the whole flow" → CI is 30 min, flaky, and the CD button is feared. Inverted pyramid kills CD before it starts.
- **Migrations that aren't backward-compatible.** README's expand/contract is the right pattern; agents skip step 1 and ship `NOT NULL` directly, breaking the previous version still running.
- **Feature flags rot.** Flags ship code, ship behaviour, then live forever. Without a kill-by-date the codebase has 200 stale flags and nobody knows what's live.
- **Smoke tests are too thin.** A `200 OK /health` doesn't prove checkout works. CD passes, bug ships.
- **Rollback that doesn't roll back state.** App rolls back, schema migration doesn't — now the previous version reads against a future schema and crashes.
- **Canary signals are noisy.** 10% canary, 5xx rate looks fine because the 10% saw the broken UI and never reached the API. Need user-facing metrics in the gate.
- **Deploy != release confusion.** Without flags, deploy IS release; "ship dark" doesn't exist; risk of every deploy stays high.
- **Pipeline-as-bottleneck.** Single shared pipeline serializes deploys; the org backs up at peak. Per-service pipelines + concurrency control needed.
- **DORA gaming.** Counting CI runs as "deploys"; counting partial rollbacks as "no failure." Numbers go up, reality doesn't.

## Agentic workflow
Drive CD adoption as a six-stage pipeline: (1) a baseline agent scores the current pipeline against the README's phase 1–5 maturity ladder; (2) a CI agent fixes the unit/integration test base (parallelisation, flake quarantine, coverage gates); (3) a deploy agent codifies environments (staging mirrors prod, IaC, secrets out of code); (4) a strategy agent picks blue-green / canary / rolling per service and writes the manifests; (5) a flag agent installs feature flags + a kill-date convention; (6) a metrics agent wires DORA + business metrics into the canary gate. Use `faion-sdd-executor-agent` to land each phase as an SDD task; persist the maturity matrix in `.aidocs/product_docs/cd-maturity.md` so progress is visible and auditable. Pair tightly with `pro/infra/cicd-engineer/` skill methodologies for pipeline mechanics.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one task per CD-phase upgrade (e.g., "add staging smoke tests," "wire automatic rollback"). Sonnet for routine pipeline edits; opus for deploy-strategy redesign.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — pipelines move secrets (deploy keys, registry tokens, webhook URLs); scrub workflows + Helm values pre-commit.
- A **cd-review-agent** (worth adding under `agents/`): scans CI YAML for missing rollback step, missing smoke test, branch trigger != main on a "production" job, secrets in plaintext, migrations applied before app deploy, no concurrency lock.
- `feature-executor` skill — sequential mode for a feature whose deploy spans migration → app deploy → flag flip → bake → flag remove; out-of-order = outage.

### Prompt pattern
Maturity assessment:
```
You are a CD coach. Read the repo's CI/CD config (.github/workflows,
.gitlab-ci.yml, Helm/Kustomize manifests, scripts/deploy*). Score
against the 5 phases in continuous-delivery/README.md. For each phase,
report: status (done/partial/missing), evidence (file:line),
next-task list (≤3 items, smallest viable). Output as a markdown
table; do not propose architecture overhauls.
```

Pipeline review:
```
You are reviewing a CD pipeline PR. Flag:
(1) production deploy job triggered by anything other than main (or
    explicit release tag),
(2) deploy step without rollback step on failure,
(3) migration applied at the same step as app deploy (must be a
    separate, expand-only migration ahead of deploy),
(4) smoke-test job that only checks /health and not a business path,
(5) no concurrency: group on the production environment,
(6) secrets referenced as plaintext, not env vars from a vault,
(7) feature-flag added without a kill-date or owner.
Cite file:line. No fixes — only flags.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Trigger / inspect Actions runs from agents | https://cli.github.com |
| `glab` (GitLab CLI) | GitLab pipelines / MR review | https://gitlab.com/gitlab-org/cli |
| `act` | Run GitHub Actions locally for fast iteration | https://github.com/nektos/act |
| `kubectl` + `helm` + `kustomize` | Apply manifests, rollouts, rollbacks | https://kubernetes.io |
| `argocd` CLI | GitOps sync / app-of-apps / progressive delivery | https://argo-cd.readthedocs.io |
| `flux` CLI | Alt GitOps toolkit | https://fluxcd.io |
| `argo rollouts` plugin | Canary / blue-green CRDs with analysis templates | https://argoproj.github.io/argo-rollouts |
| `flagger` | Progressive delivery on Istio/NGINX/Linkerd | https://flagger.app |
| `flyway` / `liquibase` | Schema migrations driven by CI | https://flywaydb.org |
| `sqitch` / `dbmate` / `goose` | Lightweight migration alts | https://sqitch.org |
| `gitleaks` / `trufflehog` | Secret-leak scan in pipeline | https://github.com/gitleaks/gitleaks |
| `cosign` / `syft` / `grype` | Sign images, generate SBOM, scan CVEs | https://www.sigstore.dev |
| `k6` / `vegeta` | Synthetic load as a deploy gate | https://k6.io |
| `dora` toolkits | Compute DORA metrics from VCS + CI logs | https://github.com/dora-team |
| `rollout` (LaunchDarkly/Statsig/Unleash CLIs) | Manage feature flags from pipelines | varies |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | yes | Default for most teams; agents own `.github/workflows/*.yml`. |
| GitLab CI/CD | SaaS / OSS | yes | Strong built-in environments + manual approvals. |
| CircleCI / Buildkite / Drone | SaaS / OSS | yes | Alternatives if Actions/GitLab not available. |
| Argo CD / Argo Rollouts | OSS | yes | GitOps + canary CRDs; agents declare desired state. |
| Flux + Flagger | OSS | yes | Alt GitOps + progressive delivery on mesh. |
| Spinnaker | OSS | partially | Powerful, heavy; agents struggle with the UI-driven config. |
| Harness | SaaS | yes | Pipeline-as-code with built-in deployment verification (canary analysis). |
| LaunchDarkly / Statsig / Unleash / Flagsmith | SaaS / OSS | yes | Feature flags + experimentation; APIs for agents to manage flags. |
| Datadog / New Relic / Honeycomb | SaaS | yes | Deploy markers, SLO burn alerts, canary analysis. |
| Sentry | SaaS | yes | Release tracking + crash-rate gates per release. |
| Snyk / Trivy / Grype | SaaS / OSS | yes | Image scan as deploy gate. |
| Cloudflare / Fastly | SaaS | yes | Instant cache purge + atomic config rollouts as part of deploy. |
| AWS CodeDeploy / CodePipeline | SaaS | yes | If already on AWS; deploy hooks for canary analysis. |
| Kamal | OSS | yes | Single-binary container deploys for non-K8s shops. |
| PagerDuty / Opsgenie | SaaS | yes | Incident response wired to deploy events; auto-rollback hooks. |

## Templates & scripts
README ships GitHub Actions, Istio canary, blue-green, rolling deploys, and rollback. Add a per-service `release-checklist.md` (migration plan, flag plan, owner, kill-date). Inline pipeline lint:

```bash
#!/usr/bin/env bash
# cd-lint.sh — flag CD anti-patterns in GitHub Actions YAML.
set -euo pipefail
root="${1:-.github/workflows}"
fail=0
echo "## Production jobs missing rollback step"
for f in "$root"/*.yml; do
  if grep -qE 'environment:\s*production' "$f"; then
    grep -qE 'rollback|rollout undo' "$f" || { echo "no rollback: $f"; fail=1; }
  fi
done
echo "## Production deploy on non-main branch"
grep -rEnA 5 'environment:\s*production' "$root" \
  | grep -E 'branches:.*(develop|feature)' && fail=1 || true
echo "## Smoke test only checks /health"
grep -rEn 'smoke' "$root" -A 2 | grep -E '/health' \
  | grep -v -E '/api/.*|/checkout|/orders|/users' \
  | tee /tmp/cd.smoke || true
[[ -s /tmp/cd.smoke ]] && fail=1
echo "## Plaintext secret references"
grep -rEn 'password:\s*[a-zA-Z0-9]{6,}' "$root" \
  | grep -vE '\$\{\{\s*secrets\.' && fail=1 || true
echo "## Missing concurrency on prod"
grep -rEnB 2 'environment:\s*production' "$root" \
  | grep -qE 'concurrency:' || { echo "no concurrency lock"; fail=1; }
exit "$fail"
```

## Best practices
- **Trunk-based development.** Short-lived branches (<1 day), merged behind flags. Long-lived release branches and CD don't co-exist.
- **Expand/contract migrations.** Always two deploys: add nullable column → backfill → require → drop old. Never one-shot.
- **Smoke tests hit business paths.** Login, place order, view dashboard — not just `/health`.
- **Canary gate on user-facing metrics.** 5xx rate, p99 latency, conversion delta. Health-check pass alone is not a gate.
- **Per-service concurrency.** `concurrency: deploy-orders-prod`, cancel-in-progress: false. Prevents overlapping deploys.
- **Feature flags own a kill-date and an owner.** Without expiry, flags become permanent dark code paths.
- **Deploy != Release.** Code goes to prod hidden behind a flag; product owner enables when the rollout window opens. Decouples engineering from product timing.
- **Automated rollback on signal.** SLO burn → rollout undo. Don't rely on a human paged at 3 a.m.
- **DORA tracking from VCS + deploy events.** Don't self-report; pull from Actions/CI + observability.
- **One artifact, many environments.** Build once on main, promote the same image hash through staging → prod. No "rebuild for prod."
- **Secrets in vaults, refs in pipelines.** GitHub OIDC → cloud roles → Vault dynamic creds. No long-lived static keys.
- **Database changes have their own pipeline.** Migrations are deployable independently and tested with both old and new app versions running simultaneously.

## AI-agent gotchas
- **Hallucinated YAML schemas.** Agents invent Actions / Argo fields. Pin to a recent schema version and validate via `actionlint` / `kubeconform`.
- **Coupled migration + app deploy.** Agents put `flyway migrate` and `kubectl set image` in one job. Force two jobs with the migration first, app second, and the migration backward-compatible.
- **Skipped rollback step.** Agents emit a deploy job and stop. Always require the `if: failure() → rollback` step or the `argo rollouts undo` equivalent.
- **Smoke test = `/health`.** Agents reach for the easy probe. Provide a list of business paths and require at least one.
- **Hardcoded secrets in workflow.** Agents paste a token "for now"; they forget to remove it. Lint workflow YAML with `gitleaks` pre-commit.
- **No concurrency.** Two PRs merge to main, two deploys race. Force `concurrency: group` on prod jobs.
- **Feature-flag debt.** Agents add flags freely; force a registry file (`flags.yaml`) with `owner` + `kill_date` per entry; CI fails on missing fields.
- **Canary analysis stub.** Agents wire 10/90 split, no analysis template. Require a metrics-based promotion criterion (`prometheus-query`) before scaling to 100%.
- **Image tag drift.** `latest` floats; agents use it. Force immutable digests (`@sha256:...`) in production manifests.
- **Human-in-loop on deploy strategy change.** Switching from rolling to canary, or production to continuous-deploy (no manual approval) is a one-way door. Stop and ask.
- **DORA-metric self-reporting.** Agents will compute "we deploy 50x/day" by counting CI runs. Pull from real deploy events; verify against incident logs.

## References
- Humble, J. & Farley, D. "Continuous Delivery." Addison-Wesley, 2010. https://continuousdelivery.com
- Forsgren, N., Humble, J., Kim, G. "Accelerate." IT Revolution, 2018. (DORA findings.)
- Kim, G., Debois, P., Willis, J., Humble, J. "The DevOps Handbook," 2nd ed.
- Fowler, M. "Continuous Delivery." https://martinfowler.com/bliki/ContinuousDelivery.html
- Fowler, M. "Feature Toggles." https://martinfowler.com/articles/feature-toggles.html
- Fowler, M. "Blue-Green Deployment." https://martinfowler.com/bliki/BlueGreenDeployment.html
- DORA research. https://dora.dev
- Argo Rollouts docs. https://argoproj.github.io/argo-rollouts
- Flagger docs. https://flagger.app
- LaunchDarkly — Feature management guide. https://launchdarkly.com
- 12-Factor App. https://12factor.net
- Sibling methodologies in this repo: `pro/dev/software-developer/microservices-design/`, `pro/infra/cicd-engineer/`, `pro/infra/devops-engineer/`, `pro/infra/infrastructure-engineer/`.
