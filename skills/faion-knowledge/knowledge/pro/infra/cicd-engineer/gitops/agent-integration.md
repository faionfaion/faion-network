# Agent Integration — GitOps

## When to use
- Migrating a Kubernetes (or Helm/Kustomize-managed) workload off `kubectl apply` and CI-driven pushes onto a pull-based reconciler (Argo CD or Flux).
- Multi-cluster fleet management — single source of truth for 10+ clusters with environment promotion via PRs.
- Compliance / audit-heavy environments where every cluster change must be traceable to a Git commit and reviewer.
- Drift detection and self-healing of cluster state.
- Progressive delivery (canary, blue-green, automated rollback) layered on top of GitOps.

## When NOT to use
- Non-declarative workloads (one-off scripts, ad-hoc data jobs) — use a CI pipeline, not GitOps.
- Single small cluster with one developer and no compliance pressure — overhead exceeds benefit.
- Stateful migrations with manual data steps — GitOps tools won't orchestrate "drain, snapshot, restore" sequencing well; use a custom operator or runbook.
- Tight imperative sequencing (deploy A, wait for hook, then B, then C) where push-based pipelines are simpler.
- Branch-per-environment workflows — known anti-pattern; use folder-per-environment instead.

## Where it fails / limitations
- Secrets in Git: requires SOPS, Sealed Secrets, External Secrets Operator, or Vault — not free.
- Helm + ArgoCD: helm hooks (pre-install, post-install) don't always cooperate with reconciliation; sync waves and ignore-differences need careful tuning.
- Drift correction can fight with HPAs/cluster-autoscaler if `replicas` is templated; `ignoreDifferences` on `spec.replicas` is mandatory.
- Multi-cluster ApplicationSet at scale (hundreds of clusters) hits API rate limits and reconciliation lag.
- CRD upgrades: if a CRD removes fields, GitOps reconciliation can fail mid-rollout — staged CRD upgrades + `ServerSideApply` help.
- Webhooks vs polling: pull is great for security but can be slow without webhook push from Git provider — set webhooks.

## Agentic workflow
Use agents to author and review GitOps repos, never to bypass them. Pattern: developer (or agent) opens a PR against the config repo with a Kustomize overlay or Helm values change → CI runs `kustomize build` / `helm template` + policy checks (Kyverno/OPA Conftest) + diff preview against current cluster state → human reviews → merge → Argo CD/Flux reconciles. Agents can scaffold app manifests, run `argocd app diff` against a candidate branch, and post the diff to the PR. Auto-promotion between envs (dev → staging) happens via PR-bot agents that copy known-good versions; production promotion is human-gated.

### Recommended subagents
- `faion-sdd-executor-agent` — implement manifest/Helm chart changes with quality gates and review.
- Custom `gitops-pr-author` — generates Kustomize overlays / Helm values updates from a structured request.
- Custom `gitops-diff-reviewer` — runs `argocd app diff`/`flux diff` against PR branch and comments on dangerous changes (replica drops, image rollbacks, RBAC widening).
- Custom `kargo-promoter` — automates Kargo stage promotions with policy checks.

### Prompt pattern
"You are a GitOps PR author. Input: `{service: api, image: ghcr.io/org/api@sha256:xxx, env: staging}`. Modify only `clusters/staging/apps/api/kustomization.yaml` to bump the image tag. Do NOT touch `clusters/production/`. Return a unified diff and a PR title `chore(staging): bump api to <sha8>`."

"You are a GitOps diff reviewer. Run `argocd app diff <app> --revision <pr-sha>`. If the diff includes any of: replica count decrease, removal of `resources.limits`, RBAC subject additions, or image tag downgrades — block with a comment listing each. Otherwise approve."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `argocd` | Argo CD CLI for apps, sync, diff | https://argo-cd.readthedocs.io/en/stable/cli_installation/ |
| `flux` | Flux CLI for sources, kustomizations, helm releases | https://fluxcd.io/flux/cmd/ |
| `kustomize` | Render Kustomize overlays | https://kustomize.io/ |
| `helm` + `helm diff` | Render and diff charts | https://helm.sh/ |
| `kubeconform` | Manifest schema validation | https://github.com/yannh/kubeconform |
| `conftest` | Policy testing with Rego | https://www.conftest.dev/ |
| `kyverno` CLI | Kyverno policy testing | https://kyverno.io/docs/kyverno-cli/ |
| `sops` | Encrypted secrets in Git | https://github.com/getsops/sops |
| `kargo` | Multi-stage promotions | https://kargo.akuity.io/ |
| `argocd-image-updater` | Automated image bumps in Git | https://argocd-image-updater.readthedocs.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Argo CD | OSS | Yes — full REST/gRPC API | Default choice 2025; ~60% market share |
| Flux | OSS | Yes — CRD-driven | Lightweight, multi-source, no UI by default |
| Akuity Platform | SaaS (Argo CD-as-a-service) | Yes | Hosted control plane + AI rollback |
| Weave GitOps | OSS/SaaS | Yes | Note: Weaveworks shut down; project moved to community |
| Kargo | OSS | Yes — promotion API | Stage promotions across envs |
| Flagger | OSS | Yes — CRDs | Progressive delivery on top of Argo/Flux |
| Argo Rollouts | OSS | Yes — CRDs | Canary/blue-green primitives |
| Sealed Secrets | OSS | Yes | Bitnami; secrets sealed to a cluster key |
| External Secrets Operator | OSS | Yes | Pull from Vault/AWS SM/GCP SM into K8s secrets |
| Crossplane + Argo | OSS | Yes | Manage cloud resources via GitOps too |

## Templates & scripts
See `templates.md` for repo layouts. Inline drift-aware sync helper:

```bash
#!/usr/bin/env bash
# argocd-safe-sync.sh — diff first, refuse on dangerous changes
set -euo pipefail
APP=${1:?app name}
DIFF=$(argocd app diff "$APP" --output json || true)
if echo "$DIFF" | jq -e '.[] | select(.kind=="Deployment") | .target.spec.replicas < .live.spec.replicas' >/dev/null; then
  echo "REFUSE: replica decrease detected"; exit 2
fi
if echo "$DIFF" | jq -e '.[] | select(.kind=="ClusterRoleBinding")' >/dev/null; then
  echo "REFUSE: RBAC change requires human approval"; exit 2
fi
argocd app sync "$APP" --prune --timeout 300
argocd app wait "$APP" --health --timeout 600
```

## Best practices
- Folder-per-environment, never branch-per-environment.
- Separate app repo (source code) from config repo (manifests) — or at least a clean boundary inside a monorepo.
- Render-test in CI: `kustomize build` / `helm template` + `kubeconform` + `conftest` on every PR.
- App-of-Apps or ApplicationSet for fleet-wide deployments; avoid hand-listing apps.
- Pin Helm chart versions; don't track `latest`.
- `ignoreDifferences` for HPA-managed `replicas`, KEDA-managed scale targets, cert-manager-rotated secrets.
- Sync waves and `argocd.argoproj.io/sync-options: ServerSideApply=true` to handle CRD ordering.
- Secrets via SOPS (with age/KMS) or External Secrets Operator — never plain in Git.
- Webhook from Git provider to reconciler so changes apply in seconds, not after the next poll.
- Backups of the Git repo + cluster ETCD; GitOps assumes Git is durable, but it isn't a backup of in-cluster state.

## AI-agent gotchas
- LLMs frequently emit `apiVersion: apps/v1beta1` or other deprecated APIs; pin a CRD/API inventory and validate with `kubeconform` against the target Kubernetes version.
- Image tag suggestions sometimes include `:latest` — explicitly disallow in policies and prompts.
- Helm values overrides: agents may set values that the chart doesn't expose; render and diff before commit.
- Multi-line YAML formatting: agents break indentation in nested overlays; always run `yamllint` and `kustomize build` on output.
- Cross-env contamination: an agent told to "bump api in staging" may also touch prod overlays if path patterns are loose — constrain the working directory in the prompt.
- Secret leakage: never let an agent commit a decrypted SOPS file or a `kubectl get secret -o yaml` dump; route through `password-scrubber-agent`.
- Auto-merge bots + Argo CD auto-sync = blast radius; require human approval at least at prod boundary.

## References
- Argo CD docs: https://argo-cd.readthedocs.io/
- Flux docs: https://fluxcd.io/flux/
- OpenGitOps principles: https://opengitops.dev/
- Akuity Best Practices Whitepaper: https://akuity.io/blog/gitops-best-practices-whitepaper
- Flux repo structure guide: https://fluxcd.io/flux/guides/repository-structure/
- Argo Rollouts: https://argoproj.github.io/argo-rollouts/
- Kargo: https://kargo.akuity.io/
- External Secrets Operator: https://external-secrets.io/
