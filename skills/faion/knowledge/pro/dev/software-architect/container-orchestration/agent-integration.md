# Agent Integration — Container Orchestration

## When to use
- Translating Docker Compose / VM deployments into Kubernetes manifests.
- Generating Helm charts / Kustomize overlays from a service spec.
- Reviewing pod specs for resource requests, probes, security context, RBAC, and netpols.
- Tuning HPA/KEDA/VPA policies from observed traffic profile.
- Drafting deployment strategy (rolling/blue-green/canary) per service with rollback playbook.
- Writing ADRs for cluster topology (multi-tenant vs single-tenant, namespace strategy).

## When NOT to use
- Single-VM apps where Kubernetes overhead dwarfs the value — use systemd or Docker.
- Stateful workloads requiring vendor-specific operators (Postgres HA, Cassandra) — operators encode best practices the agent cannot replicate.
- Hard-realtime workloads — Linux scheduler + K8s networking add jitter agent cannot diagnose.
- Edge/IoT with intermittent connectivity — K3s/MicroK8s may fit, but the design needs human cluster-arch input.

## Where it fails / limitations
- LLMs hallucinate apiVersions (e.g., `extensions/v1beta1` for Deployment in 2025) — pin K8s version.
- Resource requests/limits emitted are guesses; require profiling data.
- Probes use `/health` blindly without verifying the app exposes it; tune `initialDelaySeconds` based on real startup.
- Sidecar ordering: agents predate K8s 1.33 native sidecars and emit fragile init-container hacks.
- Network policies often default-allow because the agent lacks the namespace topology — verify intent.
- Storage class + access mode picks rarely match the workload (RWX requested where RWO suffices, or vice versa).

## Agentic workflow
Use a workload-profiler subagent to translate the app spec (RPS, memory profile, dependencies) into a sizing table; a manifest-coder to emit Helm/Kustomize; a security-reviewer to apply Pod Security Standards (Restricted), RBAC least-privilege, and NetworkPolicy default-deny; an autoscaling-tuner to pick HPA vs KEDA vs VPA. Run `kubeconform`, `kube-score`, `polaris`, `trivy` as automated gates before merge.

### Recommended subagents
- `k8s-architect` (Opus) — cluster topology, namespace/tenant model, ingress strategy.
- `manifest-coder` (Sonnet) — Helm charts, Kustomize overlays, raw manifests.
- `k8s-security-reviewer` (Sonnet) — PSS, RBAC, NetworkPolicy, secrets handling.
- `autoscaling-tuner` (Sonnet) — HPA/KEDA/VPA picks, scale-to-zero criteria.
- `rollout-planner` (Sonnet) — deployment strategy + rollback runbook (Argo Rollouts/Flagger).

### Prompt pattern
```
You are k8s-architect. App: <stack>. Target K8s version: 1.30. Cloud: EKS.
Output: namespace plan, ingress class, storage classes, autoscaling baseline,
node-pool taints, PSS profile per namespace, secrets backend (External Secrets),
observability stack (Prom/Loki/Tempo), and 3 cost-optimization picks.
No YAML yet.
```

```
You are k8s-security-reviewer. Diff: <patch>. Reject if:
- containers run as root or without readOnlyRootFilesystem,
- no resource requests/limits,
- no NetworkPolicy in the namespace,
- secrets in env vars (not via External Secrets),
- privileged or hostNetwork: true,
- ServiceAccount automount left default-true.
Output a checklist with pass/fail and minimal-diff fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `kubectl` | Apply, debug, port-forward, exec | kubernetes.io/docs/tasks/tools/ |
| `helm` | Package, template, lint charts | helm.sh |
| `kustomize` | Overlays, patches | kustomize.io |
| `kubeconform` | Schema-validate manifests | github.com/yannh/kubeconform |
| `kube-score` | Best-practice linting | kube-score.com |
| `polaris` | Policy as code for K8s | polaris.docs.fairwinds.com |
| `kubectl-neat` | Strip server-side fluff | github.com/itaysk/kubectl-neat |
| `stern` | Multi-pod log tail | github.com/stern/stern |
| `k9s` | Terminal UI for clusters | k9scli.io |
| `trivy` | Image + manifest CVE / misconfig scan | aquasecurity.github.io/trivy/ |
| `argocd` / `flux` CLIs | GitOps reconcile | argoproj.github.io / fluxcd.io |
| `velero` CLI | Backup/restore | velero.io |
| `cosign` | Sign + verify images | sigstore.dev |
| `keda` CLI / CRDs | Event-driven autoscaling | keda.sh |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| EKS / AKS / GKE | SaaS | Yes | Provision via Terraform; agent handles HCL well. |
| Argo CD / Flux | OSS | Yes | GitOps reconciliation; agent edits Application/Kustomization CRs. |
| Argo Rollouts / Flagger | OSS | Yes | Progressive delivery (canary, blue-green). |
| Datadog / New Relic / Dynatrace | SaaS | Partial | Agent edits annotations/operators; alert tuning needs human. |
| External Secrets Operator | OSS | Yes | Bind cloud secret stores to K8s Secrets. |
| HashiCorp Vault | OSS + SaaS | Yes | Agent wires Vault Agent sidecars and policies. |
| Karpenter / Cluster Autoscaler | OSS | Yes | Node provisioning; provisioner CRs are template-friendly. |
| KEDA | OSS | Yes | ScaledObject CRs for queue/event scaling. |
| Falco / Tetragon | OSS | Partial | Runtime detection; rules need security-team review. |
| Velero | OSS | Yes | Backup schedules + restores. |
| Crossplane | OSS | Partial | Cloud resource CRs; complex compositions need human design. |

## Templates & scripts
See `templates.md` for full Deployment/Service/Ingress/HPA examples. Inline gate to enforce baseline rules on every manifest PR:

```bash
#!/usr/bin/env bash
# k8s-pr-gate.sh
set -euo pipefail
DIRS="${1:-charts/ kustomize/}"
helm lint $DIRS/* 2>/dev/null || true
find $DIRS -name '*.yaml' -print0 |
  xargs -0 kubeconform -strict -summary -kubernetes-version 1.30
find $DIRS -name '*.yaml' -print0 | xargs -0 kube-score score --output-format ci
trivy config --severity HIGH,CRITICAL --exit-code 1 $DIRS
# require requests/limits everywhere
! grep -RIn --include='*.yaml' -E '^\s*containers:' $DIRS | while read -r line; do
  f=${line%%:*}
  grep -q 'resources:' "$f" || { echo "missing resources in $f"; exit 1; }
done
# default-deny netpol per namespace
for ns in $(yq '.metadata.namespace' $DIRS/**/*.yaml 2>/dev/null | sort -u); do
  grep -RIn "name: default-deny" $DIRS >/dev/null || {
    echo "ERROR: no default-deny netpol for $ns"; exit 1; }
done
echo "k8s gate OK"
```

## Best practices
- Always pin `apiVersion` to the cluster's K8s version in the prompt; otherwise the agent picks deprecated APIs.
- Pin image tags by digest, not `:latest`; agents default to floating tags.
- Set `requests` close to observed usage; `limits` ≥ 1.5× requests for memory; CPU limits are optional and usually harmful.
- Use `topologySpreadConstraints` for HA across zones — agent rarely emits this unless asked.
- Probe `/livez` and `/readyz` separately; the same endpoint causes flapping under load.
- Default-deny NetworkPolicy per namespace, then allowlist; never trust the agent's "permissive" defaults.
- Use ExternalSecrets for any sensitive value; never accept `Secret` with cleartext in PR.
- Generate signed images (`cosign sign`) and verify with admission policy (Kyverno/OPA).
- Argo Rollouts > raw Deployment for prod traffic shifting; the agent should default to it.

## AI-agent gotchas
- Models pick `RWX` PVCs reflexively for "shared" data; on EBS/Persistent Disk that is unsupported.
- HPA targets averaged CPU; for spiky workloads use KEDA on queue depth.
- `terminationGracePeriodSeconds` defaults of 30s break long-running connection-draining.
- `podAntiAffinity` left as `preferredDuringScheduling…` instead of `required…` — colocated replicas defeat HA.
- Human checkpoint REQUIRED before: applying CRD changes, raising cluster-autoscaler max nodes, modifying admission policies, rotating cluster CA, draining nodes in prod.
- `imagePullPolicy: Always` plus `:latest` tags burn registry quotas and break airgapped clusters.
- Agent forgets `PodDisruptionBudget` during rolling updates — voluntary disruptions take down full replicas.
- KEDA's `cooldownPeriod` left default — services flap to zero mid-batch.

## References
- Kubernetes docs: https://kubernetes.io/docs/.
- Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/.
- KEDA: https://keda.sh/.
- Argo Rollouts: https://argoproj.github.io/argo-rollouts/.
- "Kubernetes Patterns" by Bilgin Ibryam & Roland Huss.
- "Production Kubernetes" by Josh Rosso et al.
- CIS Kubernetes Benchmark.
- Kyverno / OPA Gatekeeper policies.
