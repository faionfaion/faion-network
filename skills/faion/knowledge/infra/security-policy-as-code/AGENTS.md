# Policy as Code: OPA, Kyverno, and Admission Control

## Summary

**One-sentence:** Produces a Kyverno ClusterPolicy bundle (or OPA/Gatekeeper Rego pack) deployed via GitOps in audit-first mode, with kyverno test / conftest verify unit tests.

**One-paragraph:** Without admission control, any workload can land in the cluster with privileged containers, root users, untrusted-registry images, or no resource limits — defeating SAST + scanning earlier in the pipeline. Policy as Code closes the gap: every kubectl apply / helm install is evaluated against a versioned policy before it hits etcd. Output: a Kyverno ClusterPolicy bundle (or OPA/Gatekeeper Rego pack) with audit-first rollout, kyverno test (or conftest verify) unit tests, GitOps delivery (ArgoCD / Flux), and a documented promotion gate from audit → enforce.

**Ефективно для:**

- Multi-tenant K8s cluster — security baselines не повинні бути overridden per-team.
- Compliance mandates (SOC2 / HIPAA): no-privileged / no-root / trusted-registries / resource-limits.
- Multi-system policy: OPA + Terraform / API gateway / CI gates via Conftest.
- Image signing verification (Kyverno verifyImages → Sigstore cosign).

## Applies If (ALL must hold)

- Cluster is Kubernetes (any flavour) AND admission webhooks are reachable.
- Security baseline exists OR is being authored (Pod Security Standards baseline+).
- GitOps tool (ArgoCD / Flux) is in place OR being adopted concurrently.

## Skip If (ANY kills it)

- Non-Kubernetes workloads — use native IAM / network ACLs / Terraform Sentinel instead.
- Trying to replace application-level authz with admission control — admission controls the platform, not the app's RBAC.
- Enforcing before audit-mode review — blocks all teams' pending workloads simultaneously.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cluster baseline | PSS profile (baseline / restricted) | security team |
| Trusted registry list | list of allowed image hosts | platform team |
| GitOps repo | ArgoCD app or Flux Kustomization | GitOps controller |
| Cosign verification keys / OIDC issuer | key or issuer URL | Sigstore / internal CA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[security-container-scanning]] | Cosign signatures from the scan pipeline are what verifyImages validates |
| [[argocd-gitops]] | Policies must reach the cluster via GitOps sync, not kubectl apply |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: audit-first-then-enforce, unit-tests-required, gitops-only-delivery, version-control-policies, skip-this-methodology | 1300 |
| `content/02-output-contract.xml` | essential | JSON Schema for policy bundle + valid/invalid + forbidden | 1000 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: enforce-without-audit, untested-policy, kubectl-apply-drift, deny-all-fallback-missing | 900 |
| `content/04-procedure.xml` | essential | 6 steps: define baseline → write Kyverno YAML → kyverno test → GitOps sync audit-mode → review → enforce | 900 |
| `content/06-decision-tree.xml` | essential | Decision tree on engine choice + audit phase → rule | 900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-engine` | haiku | Kyverno vs OPA/Gatekeeper — deterministic on multi-system reach. |
| `write-policy` | sonnet | Author YAML / Rego from baseline + sample manifests. |
| `write-tests` | sonnet | Compose kyverno test / conftest verify fixtures + assertions. |
| `review-audit-violations` | opus | Strategic — triage which violations to fix vs which require exemption. |

## Templates

| File | Purpose |
|------|---------|
| `templates/baseline-cluster-policy.yaml` | Kyverno ClusterPolicy: no-privileged + no-root + require-resource-limits + trusted-registries |
| `templates/kyverno-test.yaml` | Kyverno test harness — runs in CI alongside app tests |
| `templates/verify-images-policy.yaml` | Kyverno verifyImages policy — only accepts cosign-signed images |
| `templates/_smoke-test.json` | Minimum policy-bundle artefact used by validate-security-policy-as-code.py --self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-security-policy-as-code.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[security-container-scanning]]
- [[argocd-gitops]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when designing the admission-control layer for a new cluster or hardening an existing one.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/baseline-cluster-policy.yaml`

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: baseline-security
  annotations:
    policies.kyverno.io/title: Baseline Security Policy
    policies.kyverno.io/category: Pod Security
    policies.kyverno.io/severity: high
spec:
  validationFailureAction: Audit   # START IN AUDIT; flip to Enforce only after triage
  background: true
  rules:
    - name: deny-privileged
      match:
        any:
          - resources: { kinds: [Pod] }
      validate:
        message: "Privileged containers are not allowed."
        pattern:
          spec:
            =(initContainers):
              - securityContext: { privileged: "false" }
            containers:
              - securityContext: { privileged: "false" }
    - name: require-run-as-non-root
      match:
        any:
          - resources: { kinds: [Pod] }
      validate:
        message: "Containers must run as non-root user."
        pattern:
          spec:
            securityContext: { runAsNonRoot: true }
    - name: require-resource-limits
      match:
        any:
          - resources: { kinds: [Pod] }
      validate:
        message: "Containers must declare CPU + memory limits."
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    memory: "?*"
                    cpu: "?*"
    - name: trusted-registries
      match:
        any:
          - resources: { kinds: [Pod] }
      validate:
        message: "Images must come from a trusted registry (ghcr.io/acme/* | quay.io/acme/*)."
        pattern:
          spec:
            containers:
              - image: "ghcr.io/acme/* | quay.io/acme/*"
```

### `templates/kyverno-test.yaml`

```yaml
apiVersion: cli.kyverno.io/v1alpha1
kind: Test
name: baseline-security-test
policies:
  - ../baseline-cluster-policy.yaml
resources:
  - resources/pod-good.yaml
  - resources/pod-privileged-bad.yaml
  - resources/pod-root-bad.yaml
results:
  - policy: baseline-security
    rule: deny-privileged
    resource: pod-privileged-bad
    kind: Pod
    result: fail
  - policy: baseline-security
    rule: require-run-as-non-root
    resource: pod-root-bad
    kind: Pod
    result: fail
  - policy: baseline-security
    rule: deny-privileged
    resource: pod-good
    kind: Pod
    result: pass
```

### `templates/verify-images-policy.yaml`

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signatures
spec:
  validationFailureAction: Audit
  rules:
    - name: verify-cosign
      match:
        any:
          - resources: { kinds: [Pod] }
      verifyImages:
        - imageReferences: ["ghcr.io/acme/*"]
          attestors:
            - entries:
                - keyless:
                    issuer: "https://token.actions.githubusercontent.com"
                    subject: "https://github.com/acme/*/.github/workflows/*"
```

### `templates/_smoke-test.json`

```json
{
  "engine": "kyverno",
  "engine_version": "1.12.0",
  "policies": [
    "baseline-security",
    "verify-image-signatures"
  ],
  "rollout_phase": "audit",
  "unit_tests_present": true,
  "delivery_via_gitops": true,
  "trusted_registries": [
    "ghcr.io/acme/*",
    "quay.io/acme/*"
  ],
  "verify_images": true
}
```
