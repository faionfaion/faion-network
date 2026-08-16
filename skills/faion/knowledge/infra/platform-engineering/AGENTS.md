# Platform Engineering

## Summary

**One-sentence:** Produces an Internal Developer Platform (IDP) spec: golden paths, service catalogue choice, DORA + platform metrics, RBAC + AI-agent citizenship model.

**One-paragraph:** Platform engineering is product management for the dev team. The output is not a tool list — it is an IDP spec: which golden path(s) we ship first, which service catalogue + portal we adopt, which DORA + platform-specific metrics the team is accountable to, which RBAC model spans humans and AI agents (2026 default), and what we explicitly will NOT abstract yet. Wrong order — building the portal UI before the orchestration backend — produces a hollow product the platform team cannot operate. This methodology forces the backend-first sequence, the one-golden-path rule, and the published-metrics gate.

**Ефективно для:**

- 50+ engineer org з queue на DevOps tickets, onboarding triває тижні.
- Multi-tenant K8s / cloud accounts з inconsistent provisioning.
- Standardizing 'golden paths' — opinionated app templates, CI workflows, observability defaults.
- Compliance (SOC2/HIPAA) — guardrails мають бути enforced, не documented.
- AI-agent fleet (2026): RBAC, quota, scope такі ж, як для людей.

## Applies If (ALL must hold)

- Engineering org size ≥ 50 (or growth path to 50 within 12 months).
- DevOps ticket queue is measurable + onboarding time is a real metric (not just gut feel).
- Multi-tenant infra exists (shared K8s / cloud account) OR is on the roadmap.

## Skip If (ANY kills it)

- Solo or <10-person team — managed PaaS (Render / Fly / Heroku) is cheaper than building a platform.
- The actual bottleneck is product / discovery, not infra friction — platform won't fix unclear roadmaps.
- Greenfield with no production workloads — wait until ≥3 services + ≥10 deploys/week to know what to abstract.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current-state survey | Markdown report — ticket volume, onboarding time, dev satisfaction (NPS) | internal survey + ticket-tracker query |
| Service inventory | list of services + their current deploy / CI / observability stack | service catalogue dump or manual census |
| Compliance scope | list of regulated environments (SOC2 / HIPAA / FedRAMP) | security / GRC team |
| Sponsor | named exec accountable for platform success + a budget envelope | leadership |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[dora-metrics]] | Platform success is measured on DORA + platform-specific metrics |
| [[argocd-gitops]] | Golden-path templates ship via GitOps to keep parity with cluster state |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: backend-first-then-portal, one-golden-path-at-start, version-templates, dora-plus-platform-metrics, ai-agents-are-citizens, skip-this-methodology | 1300 |
| `content/02-output-contract.xml` | essential | JSON Schema for IDP spec + valid/invalid + forbidden patterns | 1000 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: portal-first-no-backend, three-portals-concurrently, golden-path-mutation, no-metrics | 900 |
| `content/04-procedure.xml` | essential | 7 steps: survey → backend → 1 golden path → portal → metrics → AI-RBAC → publish | 900 |
| `content/05-examples.xml` | reference | Worked example: 80-dev SaaS adopting Backstage + Crossplane + Terraform stack | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on team size + maturity → portal + orchestration stack | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `baseline-survey` | sonnet | Read ticket history + survey responses, summarise the friction points. |
| `pick-golden-path` | opus | Strategic choice — depends on the dominant service shape + team appetite. |
| `draft-spec` | sonnet | Assemble the spec; structured writing, no novel decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/idp-spec.md.j2` | Markdown skeleton for the IDP spec |
| `templates/idp-spec.md` | Markdown skeleton for the IDP spec Generated from `templates/idp-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/golden-path-go-microservice.yaml` | Backstage scaffolder template for a Go microservice golden path |
| `templates/idp-spec.json` | JSON template for the IDP spec artefact (validator target) |
| `templates/_smoke-test.json` | Minimum filled IDP spec used by validate-platform-engineering.py --self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-platform-engineering.py` | Validate the spec artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[dora-metrics]]
- [[argocd-gitops]]
- [[security-policy-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when scoping a year-1 platform investment with a named sponsor.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/golden-path-go-microservice.yaml`

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: go-microservice
  title: Go Microservice Golden Path
  description: Production-ready Go service with CI/CD, observability, RBAC
spec:
  owner: platform-team
  type: service
  lifecycle: production
  parameters:
    - title: Service Details
      properties:
        serviceName:
          type: string
          pattern: "^[a-z][a-z0-9-]+$"
        owner:
          type: string
  steps:
    - id: fetch
      name: Fetch Skeleton
      action: fetch:template
      input:
        url: ./skeleton
        values:
          serviceName: ${{ parameters.serviceName }}
    - id: publish
      name: Publish to Git
      action: publish:github
      input:
        allowedHosts: [github.com]
        repoUrl: github.com?owner=acme&repo=${{ parameters.serviceName }}
    - id: register
      name: Register in Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml
```

### `templates/idp-spec.json`

```json
{
  "org": "",
  "current_state": {
    "devops_tickets_month": 0,
    "ttfd_days": 0,
    "dev_nps": 0,
    "service_count": 0
  },
  "decisions": {
    "portal": "backstage",
    "orchestrator": "crossplane",
    "iac": "terraform",
    "golden_path_first": "go-microservice",
    "rbac_includes_ai_agents": true
  },
  "metrics": {
    "dora": [
      "DF",
      "LT",
      "MTTR",
      "CFR"
    ],
    "platform": [
      "adoption_rate",
      "ttfd_new_dev",
      "ticket_trend",
      "nps"
    ]
  },
  "non_goals_year1": []
}
```

### `templates/_smoke-test.json`

```json
{
  "org": "acme",
  "current_state": {
    "devops_tickets_month": 220,
    "ttfd_days": 14,
    "dev_nps": -5,
    "service_count": 38
  },
  "decisions": {
    "portal": "backstage",
    "orchestrator": "crossplane",
    "iac": "terraform",
    "golden_path_first": "go-microservice",
    "rbac_includes_ai_agents": true
  },
  "metrics": {
    "dora": [
      "DF",
      "LT",
      "MTTR",
      "CFR"
    ],
    "platform": [
      "adoption_rate",
      "ttfd_new_dev",
      "ticket_trend",
      "nps"
    ]
  },
  "non_goals_year1": [
    "multi-cloud",
    "self-service databases"
  ]
}
```
