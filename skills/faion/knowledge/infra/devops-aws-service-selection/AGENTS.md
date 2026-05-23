# AWS Service Selection (Compute, Database, Architecture Decisions)

## Summary

**One-sentence:** Produces a decision-record for AWS compute + database service selection mapped against the 6 Well-Architected pillars, with rationale per pillar and Graviton-default for compute.

**One-paragraph:** AWS has 200+ services; the wrong compute/database choice at kickoff produces migration debt that compounds with scale. Compute heuristic: short tasks < 15 min → Lambda; container workloads → Fargate (unless EKS control needed); sustained CPU → Graviton EC2 Reserved. Database heuristic follows access patterns: key-value + global → DynamoDB; relational + ACID → Aurora Serverless v2; in-memory → ElastiCache. Output is a decision-record naming the chosen services + rationale tied to each of the 6 WA pillars + a gap list before the first production deployment.

**Ефективно для:**

- Новий AWS-проект — вибір core services.
- Огляд існуючої архітектури — cost / efficiency gaps.
- Migration on-prem → AWS, mapping legacy → equivalent.
- Well-Architected Review для 6 pillars.

## Applies If (ALL must hold)

- Decision is at design phase (not yet running in prod).
- WA framework is the chosen lens.
- Graviton (arm64) is acceptable (or constrained by binary deps).

## Skip If (ANY kills it)

- Architecture already in prod — apply cost-optimisation methodologies instead.
- Service-specific config details needed — see devops-aws-three-tier or devops-aws-serverless-api.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload profile | RPS / latency / state shape / batch vs interactive | product + perf team |
| Cost ceiling | $/month target | finance |
| Compliance scope | regulated workloads / data-residency | GRC |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[aws-well-architected-checklists]] | Decisions are evaluated against the 6 pillars |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: graviton-default, lambda-under-15min, ddb-key-value-only, evaluate-all-6-pillars, gap-list-before-prod, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for service-selection decision-record + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: lambda-for-long-task, ddb-for-relational, eks-when-fargate-suffices, x86-when-arm-fits | 800 |
| `content/04-procedure.xml` | essential | 5 steps: profile → compute → DB → WA-6-pillar evaluation → gap list | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree compute + DB → service | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-workload` | haiku | Bucket: short-task / container / sustained / batch. |
| `pick-services` | sonnet | Decision-tree application with cost trade-off. |
| `evaluate-pillars` | sonnet | Pillar-by-pillar gap list. |

## Templates

| File | Purpose |
|------|---------|
| `templates/service-selection.md` | Markdown skeleton for the AWS service-selection decision-record |
| `templates/service-selection.json` | JSON decision-record artefact (validator target) |
| `templates/_smoke-test.json` | Minimum decision-record used by validate-devops-aws-service-selection.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-aws-service-selection.py` | Validate the decision-record artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[aws-well-architected-checklists]]
- [[devops-aws-serverless-api]]
- [[devops-aws-three-tier]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it at project kickoff or migration scoping.
