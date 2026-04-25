# Agent Integration — Platform Engineering

## When to use
- 50+ engineer org where DevOps tickets become a queue and onboarding takes weeks.
- Multi-tenant infrastructure with shared Kubernetes / cloud accounts and inconsistent provisioning.
- When standardizing "golden paths" — opinionated app templates, CI workflows, observability defaults.
- Compliance environments (SOC2, HIPAA) where guardrails must be enforced, not documented.
- Migrating from Heroku/render-style PaaS to in-house cloud, while keeping developer ergonomics.
- AI-agent fleets that need RBAC, quota, and scope just like humans (2026 pattern).

## When NOT to use
- Solo or <10-person teams. Building an IDP for 5 devs is over-engineering; pick a managed PaaS.
- When the actual bottleneck is product/discovery, not infra friction. Platform won't fix unclear roadmaps.
- Greenfield with no production workloads — wait until you have ≥3 services and ≥10 deploys/week to learn what to abstract.
- Strict regulatory environments where central infra team must own every change (platform abstraction can hide compliance-relevant detail).

## Where it fails / limitations
- Backstage adoption fails when it's installed but not curated: empty catalog, dead links, no owner. Becomes a ghost portal in 6 months.
- Golden paths are too rigid: every team forks the template, abandons updates, and the platform team supports five forks instead of one.
- Internal "platform" without product mindset — no roadmap, no SLAs, no user research. Treat it like an external SaaS or it dies.
- Score / Humanitec abstractions are leaky: the moment a team needs a feature the spec doesn't cover, they bypass the orchestrator.
- Crossplane + Kubernetes-as-control-plane sounds elegant but complicates failure modes — when the K8s control plane is down, you can't provision K8s.
- AI agents with broad RBAC scopes silently consume cloud budget; without per-agent quotas the FinOps team gets a $40k surprise.

## Agentic workflow
Platform engineering with agents has two layers: agents that build the platform (IDP itself, Backstage scaffolds, golden-path templates) and agents that consume the platform (provisioning, deploys, drift checks via Score/Backstage actions). Have a planning agent decompose the IDP roadmap into "thinnest viable platform" increments — one self-service action per sprint. An implementation agent generates Backstage software-templates + Crossplane compositions; a reviewer agent (Opus) validates the composition matches the team's existing IaC conventions and that RBAC is least-privilege.

### Recommended subagents
- `faion-sdd-executor-agent` — drives self-service-action specs through quality gates.
- A custom `idp-rbac-auditor` (Opus, read-only) — given Backstage role bindings + Crossplane compositions, lists every permission an actor (human or agent) gains and flags excess scope.
- `password-scrubber-agent` — Backstage `app-config.yaml` and Humanitec env files inline tokens.

### Prompt pattern
```
Design a self-service action for "create new service".
Inputs: language (Go/Node/Python), traffic class (low/medium/high), data tier (none/postgres/s3).
Output: (1) Backstage software-template skeleton (cookiecutter vars, owner, lifecycle), (2) golden-path repo layout (CI, Dockerfile, k8s manifests), (3) Crossplane composition (env, namespace, IAM role, DB), (4) observability defaults (RED dashboard, baseline alerts), (5) FinOps gate (max monthly cost estimate before approval).
Forbid: hardcoded namespaces/owners, missing RBAC scope, no resource quota, broken golden-path README.
```

```
Audit Crossplane composition + Backstage role mapping. For each role (developer, platform-admin, ai-agent), list (action, resource, scope, justification, alternative_least_privilege). Flag any "*" verbs.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `backstage-cli` (`@backstage/cli`) | Scaffold + run Backstage app, plugins | https://backstage.io/docs/getting-started/ |
| `crossplane` CLI | Apply XRDs/Compositions, render | https://docs.crossplane.io/latest/cli/ |
| `humctl` | Humanitec orchestrator CLI | https://developer.humanitec.com/platform-orchestrator/cli/ |
| `score-compose` / `score-humanitec` / `score-k8s` | Convert Score spec to runtime manifests | https://docs.score.dev/ |
| `kratix` | Promise-based platform building | https://docs.kratix.io/ |
| `argocd` CLI | GitOps deploy of platform components | https://argo-cd.readthedocs.io/ |
| `pulumi` / `terraform` | IaC for platform substrate | https://www.pulumi.com / https://www.terraform.io |
| `bk` (Backstage CLI from community) | Bulk catalog operations | https://github.com/backstage |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Backstage (CNCF) | OSS | Yes | Catalog + Software Templates + TechDocs + Scaffolder. Plugins via npm. |
| Port | SaaS | Yes | API-first IDP; scorecards + actions; agents via Port API tokens. |
| Cortex | SaaS | Yes | Engineering intelligence; pulls from Git/CI/Pager. |
| Humanitec | SaaS | Yes | Platform orchestrator with Score; CLI + API for agents. |
| Crossplane | OSS | Yes | K8s-native composition model; agents apply XRs as YAML. |
| Kratix | OSS | Partial | Promises model; agent must understand Promise/Workshop schemas. |
| Roadie | SaaS | Yes | Hosted Backstage. |
| Spotify Portal | SaaS | Partial | Hosted Backstage with proprietary plugins. |
| OpsLevel | SaaS | Yes | Service ownership + scorecards. |

## Templates & scripts
See `templates.md` for full Backstage software-template + Crossplane composition pair. Minimal Score spec (`score.yaml`) the platform consumes (≤25 lines):

```yaml
apiVersion: score.dev/v1b1
metadata:
  name: orders-api
containers:
  app:
    image: ghcr.io/example/orders-api:${TAG}
    variables:
      DATABASE_URL: ${resources.db.uri}
      LOG_LEVEL: info
    resources:
      limits:
        memory: 512Mi
        cpu: "0.5"
service:
  ports:
    http:
      port: 80
      targetPort: 8080
resources:
  db:
    type: postgres
    params:
      version: "16"
      size: small
  dns:
    type: dns
    params:
      hostname: orders-api.example.com
```

## Best practices
- Run the platform as a product: have a PM, a roadmap, named users (other devs), NPS surveys, and SLOs (e.g. "self-service action P95 < 5 min").
- Start with one golden path (most-used stack) before generalizing. Three opinionated paths > one universal abstraction.
- Every self-service action emits an event the FinOps + audit dashboards consume. Without telemetry the platform is invisible.
- Version golden paths and let teams subscribe to updates; never silently mutate downstream repos.
- Use Score (or similar workload spec) as the developer interface — keep Crossplane / Terraform invisible to product devs.
- For AI-agent citizens: dedicated service accounts per agent, per-agent budget cap, per-agent action audit log, automatic shutdown on quota breach.
- Put DORA + platform-friction metrics on the same dashboard; the moment lead time degrades the platform team is on the hook.

## AI-agent gotchas
- Agents generate Backstage templates with broken `parameters → steps` wiring (variables undefined at template-render time). Always render template locally before merging.
- LLMs reach for "create one Crossplane Composition that handles all envs" — produces an unmaintainable monster. Force one Composition per concern (db, dns, queue) and compose at the XR level.
- Score's `resources` block is provider-agnostic on paper; in practice the runtime mapping (postgres → RDS vs CloudSQL vs in-cluster) leaks. Agents must declare the target runtime, not assume.
- Agents drop RBAC scope wide (`system:admin`) "to make it work" during scaffold tests; no one tightens it later. Force least-privilege from the first commit and have a reviewer agent enforce.
- Backstage catalog updates from agents must go through `catalog-info.yaml` PRs, never the API. API edits don't survive sync and produce silent drift.
- Human-in-loop checkpoint: every new self-service action gets a manual run-through by a non-platform engineer ("can a junior do this without Slack?"). If they need help → not yet golden.
- AI-agent budget gotcha: agents call `provision new env` in retry loops on transient errors → cloud bill explodes. Wrap every IaC apply with rate limit + idempotency token.

## References
- Team Topologies (Skelton, Pais) — https://teamtopologies.com/book
- Platform Engineering Maturity Model (CNCF) — https://github.com/cncf/tag-app-delivery/tree/main/platforms-maturity-model
- Backstage docs — https://backstage.io/docs
- Score spec — https://docs.score.dev/
- Crossplane docs — https://docs.crossplane.io/
- Humanitec resources — https://developer.humanitec.com/
- Internal Developer Platform Glossary — https://internaldeveloperplatform.org/
- "Thinnest Viable Platform" (Manuel Pais) — https://teamtopologies.com/key-concepts-content/what-is-a-thinnest-viable-platform-tvp
