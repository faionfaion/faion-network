# Agent Integration — ArgoCD GitOps

## When to use
- Kubernetes-first deployments where Git is the desired source of truth, with declarative reconciliation and drift detection out of the box.
- Multi-cluster fleets (5-500 clusters) — `ApplicationSet` with cluster generators is the cleanest fan-out story available today.
- Multi-tenant platforms where teams own namespaces and need RBAC-isolated apps without giving them cluster-admin.
- Progressive delivery: ArgoCD + Argo Rollouts (canary, blue/green, analysis templates) with metric-driven rollback.
- Audit-heavy environments — every cluster change traceable to a Git commit with author/SHA/CI run.

## When NOT to use
- Non-K8s workloads (VMs, serverless functions, on-prem bare metal). Use Flux for some of these or just Terraform/Pulumi.
- Tiny single-cluster deployments — `kubectl apply -k ./manifests` in CI is simpler and avoids running the ArgoCD control plane.
- Teams that want push-based deploys (`kubectl apply` from CI). ArgoCD is pull-based; mixing the two leads to constant fights.
- Workloads needing immediate sync from CI — pull interval (default 3 min) plus refresh latency means "deploy" is not instantaneous unless you wire webhooks correctly.

## Where it fails / limitations
- **App code + manifests in same repo.** Every code commit triggers a manifest sync; CI loop on the same repo causes infinite churn. Separate "app repo" from "config repo".
- **Branches per environment.** Hot-fix in prod-branch must be back-ported to dev-branch; merge conflicts forever. Use folder-per-env in one branch.
- **Raw YAML for everything.** Drift across `dev/`, `staging/`, `prod/` because someone hand-edited one. Use Helm or Kustomize with overlays.
- **`kubectl edit` in production.** ArgoCD detects drift and either reverts (auto-sync) or reports OutOfSync (manual sync). Either way the change is undocumented. Lock down with RBAC.
- **`automated.selfHeal: true` + flapping resources.** A Job that creates a TTL'd resource looks like drift; ArgoCD keeps re-creating. Use `ignoreDifferences` or annotate `argocd.argoproj.io/compare-options: IgnoreExtraneous`.
- **`ApplicationSet` template explosion.** Generators × clusters × envs = thousands of Applications; one bad template breaks them all simultaneously. Test with `--dry-run` and use progressive sync.
- **Sync waves misordered.** Agents add a wave to make CRDs deploy before CRs but forget that hooks (PreSync) run before all waves; result: hook fails on missing CRD.
- **Sharded controller misconfig.** With 100+ clusters, single controller OOMs; sharding via `replicas` requires correct `argocd-application-controller` env. Default config silently single-shards.
- **Helm + ArgoCD value precedence.** Values from `valueFiles`, `values`, `helm.parameters` merge in non-obvious order. Agents add a `parameters` block expecting override but `valueFiles` wins.
- **`syncPolicy.automated.prune: true`** mass-deletes resources when manifests are accidentally moved/renamed. Always pair with `prune: false` until tested, then enable behind feature-flag.
- **No sync windows.** Auto-sync at 3 AM Saturday during a security incident → uncontrolled changes. Configure `syncWindows` to block prod changes during business-hours-only or freeze periods.
- **Notifications missing.** Sync fails, no one sees it for hours. Configure `argocd-notifications` with Slack/Teams/PagerDuty and per-app subscriptions.

## Agentic workflow
GitOps inverts CI/CD: CI builds artifacts (images), agents must NOT `kubectl apply`. The agent's job ends at "image pushed + manifest PR opened in config repo". Have one planning agent design the repo layout (apps/<svc>/{base, overlays/{dev,stage,prod}}/, ApplicationSet generators, AppProjects) BEFORE writing any YAML. A second agent writes Kustomize/Helm + `Application` CRs. A reviewer agent runs `argocd app diff --revision <pr-sha>` against a draft `Application` and emits the impact summary on the PR. For prod changes, require manual sync (`syncPolicy.automated` disabled or sync window) so a human approves the actual rollout.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the spec → manifest → review loop; quality gate must include `argocd app diff` and `kustomize build` / `helm template` lint.
- `password-scrubber-agent` — config repos accumulate webhook secrets, registry pull creds, signing key references.
- A custom `argocd-drift-investigator` (Sonnet, read-only) — given an OutOfSync app, diffs live state vs. Git and classifies the drift cause (manual edit / controller / mutating webhook / CRD upgrade).
- A custom `applicationset-impact-modeler` — given an ApplicationSet change, lists every Application that would be created/updated/deleted before the change ships.

### Prompt pattern
```
Design a GitOps config repo for <platform>. Inputs: cluster list (name, region, env), services to deploy, secret backend (ESO/Sealed Secrets/SOPS), image registry, branching model preference.
Output: (1) directory tree (folders not branches per env), (2) AppProject definitions with RBAC + sourceRepos + destinations, (3) ApplicationSet using cluster generator + matrix generator, (4) sync policy per env (auto for dev, manual for prod, syncWindow for prod), (5) notifications subscriptions per AppProject.
Forbid: branches-per-env, Application without AppProject, automated prune+selfHeal in same env without testing, hardcoded cluster URLs (use generators), values override via Application parameters when a values file would do.
```

```
Pre-merge gate: for each changed Application, run `argocd app diff --local <kustomize_dir> <app-name>` and `kustomize build` / `helm template`. Emit JSON {app, kind_changes: {created[], updated[], deleted[]}, dangerous: bool, dangerous_reason}. Mark dangerous if: deletes > 0 OR Namespace/CRD/ClusterRole created OR PVC modified OR replicas decreased >50%. Reject if dangerous AND target is prod AND no human approver listed.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `argocd` | Official CLI: app/project/cluster CRUD, sync, diff, rollback | https://argo-cd.readthedocs.io/en/stable/cli_installation/ |
| `argocd app diff` | Compare live cluster state to manifests | https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_diff/ |
| `argocd app sync` / `--dry-run` | Trigger sync from CLI; agent loop friendly | https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_sync/ |
| `argocd-vault-plugin` | Inject Vault secrets into manifests at sync time | https://argocd-vault-plugin.readthedocs.io |
| `kustomize` | Build overlays; `kustomize build` is the canonical preview | https://kustomize.io |
| `helm` + `helm template` | Render Helm charts to plain YAML for diffing | https://helm.sh/docs/ |
| `kubectl-argo-rollouts` | Manage Argo Rollouts (canary/bluegreen) from CLI | https://argoproj.github.io/argo-rollouts/features/kubectl-plugin/ |
| `argocd app rollback` | Roll back to previous deployed Git revision | built-in |
| `kustomize build && conftest test` | Policy-as-code on rendered manifests | https://www.conftest.dev |
| `kubeconform` / `kube-linter` | Validate manifests against K8s schemas / best practices | https://github.com/yannh/kubeconform |
| `argo-cd-image-updater` | Auto-bump image tags via PR or write-back | https://argocd-image-updater.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Argo CD | OSS | Yes | Self-hosted on the K8s cluster it manages (or a separate "hub" cluster). |
| Argo CD on Akuity / Codefresh | SaaS | Yes | Hosted control plane; useful for multi-tenant orgs. |
| Argo Rollouts | OSS | Yes | Canary/blue-green/analysis with Prometheus/Datadog/CloudWatch checks. |
| Argo Workflows | OSS | Yes | DAG/pipeline runner; pairs with ArgoCD for CD-in-cluster patterns. |
| ApplicationSet generators (List, Cluster, Git, Matrix, Pull-Request) | OSS | Yes | Built-in; PR generator is killer for preview environments. |
| External Secrets Operator | OSS | Yes | Best secret-injection partner — keep secret material out of Git. |
| Sealed Secrets | OSS | Yes | Cluster-public-key encryption — secrets in Git but encrypted. |
| KSOPS / Helm-Secrets | OSS | Yes | SOPS-decrypt-at-render integration with ArgoCD via plugins. |
| Notifications (argocd-notifications) | OSS | Yes | Slack, Teams, Webhook, Email subscriptions per app/project. |
| OpenShift GitOps | Commercial | Yes | Red Hat distribution; same APIs, hardened defaults. |
| FluxCD | OSS | Yes | Alternative GitOps controller; sometimes preferred for SOPS-native flow. |

## Templates & scripts
See `templates.md` and `examples.md` for ApplicationSet + AppProject + Helm/Kustomize starters. Diff-and-comment helper for PR review (≤35 lines):

```bash
#!/usr/bin/env bash
# scripts/argocd-pr-diff.sh — emits per-app diff for a PR; meant for CI comment.
set -euo pipefail

PR_BRANCH="${1:?pr branch}"
ARGOCD_SERVER="${ARGOCD_SERVER:?}"
APPS=$(argocd app list -o json | jq -r '.[] | select(.spec.source.repoURL | contains("'"$REPO"'")) | .metadata.name')

for APP in $APPS; do
  echo "## ArgoCD diff: $APP"
  echo '```diff'
  argocd app diff "$APP" \
    --revision "$PR_BRANCH" \
    --loglevel error \
    || true
  echo '```'
  echo
done | tee diff-comment.md

# Flag dangerous changes
if grep -qE '^(- )?(kind: Namespace|kind: CustomResourceDefinition|kind: ClusterRole|kind: PersistentVolumeClaim)' diff-comment.md; then
  echo "::warning::Dangerous resource diff detected — manual approval required"
fi
```

## Best practices
- Two repos: `app-source` (code, Dockerfile, CI builds image) and `app-config` (manifests, ArgoCD CRs). CI in app-source updates an image tag via PR to app-config.
- Folders per env, never branches. Promote by PR from `dev/` overlay to `stage/` to `prod/`.
- Every Application belongs to an AppProject. Default project should be locked down (no `*` sourceRepos).
- Auto-sync ON in dev/stage; manual sync in prod with sync windows + required reviewers.
- `selfHeal: true` only after a quarter of stable operation; until then OutOfSync alerts surface drift for humans to triage.
- Use `ApplicationSet` cluster generator; never write 50 nearly identical Applications by hand.
- Notifications: subscribe to `on-deployed`, `on-health-degraded`, `on-sync-failed` per AppProject. Pipe to a single channel + page for prod.
- Limit RBAC: agents creating apps should use a service account scoped to one AppProject; never use admin tokens.
- Pin Helm chart versions; pin Kustomize builds via `kustomize build --enable-helm` with `--load-restrictor LoadRestrictionsRootOnly`.
- Backup ArgoCD: `argocd admin export` + secret backup; restore drill quarterly.

## AI-agent gotchas
- Agents commit a Helm chart bump that changes resource limits; auto-sync rolls it out cluster-wide before anyone sees the diff. Force prod manual sync.
- `kubectl apply -k` from a CI job "to fix something fast" — drift then erased on next ArgoCD sync. Agents do this in incidents and create cyclic outages. Hard rule: only ArgoCD writes to managed namespaces.
- ApplicationSet `goTemplate: true` vs default fasttemplate — agents copy templates that work in one mode and not the other. Force one mode org-wide.
- `revisionHistoryLimit` defaults to 10 — agents add a `selfHeal` flap that burns through history and rollback fails. Set to 50+.
- Image tag pinning: agents use `:latest` or floating tags; ArgoCD shows Healthy but cluster keeps pulling new images out-of-band. Always pin by digest or use Argo CD Image Updater with PR write-back.
- Multi-source apps (`spec.sources[]`, ArgoCD 2.6+) confuse agents trained on single-source examples. Default to single-source unless absolutely necessary.
- Project-wide destination clusters allow `*` — one compromised app can deploy to any cluster. Always scope destinations.
- Human-in-loop checkpoints (mandatory): creating new AppProject, adding a new cluster destination, granting `applications, sync, *, *, allow` policy, enabling `automated.selfHeal` + `automated.prune` together. These all expand blast radius.
- Webhook misconfig: agents wire GitHub/GitLab webhook to ArgoCD but don't verify signature → anyone can trigger a sync. Always set `webhook.github.secret` and validate.
- "Sync stuck": app shows OutOfSync forever; agents loop `argocd app sync` and burn rate limits. Check `argocd app get <app>` for `conditions` first — usually a CRD missing or RBAC denial.

## References
- ArgoCD docs — https://argo-cd.readthedocs.io
- Best practices — https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/
- ApplicationSet — https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/
- Argo Rollouts — https://argoproj.github.io/argo-rollouts/
- Anti-patterns — https://codefresh.io/blog/argo-cd-anti-patterns-for-gitops/
- Multi-cluster patterns — https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/
- OpenShift GitOps practices — https://developers.redhat.com/blog/2025/03/05/openshift-gitops-recommended-practices
