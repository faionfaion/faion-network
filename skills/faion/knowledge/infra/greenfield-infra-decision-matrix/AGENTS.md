# Greenfield Infra Decision Matrix

## Summary

**One-sentence:** Pre-build decision matrix for greenfield infra: self-host vs managed, EKS vs ECS vs Cloud Run, Terraform vs Pulumi, single-region vs multi-region, with weighting + red-flags + go/no-go criteria.

**One-paragraph:** DevOps engineers waste days re-deciding 'self-host vs managed', 'EKS vs ECS vs Cloud Run', 'Terraform vs Pulumi', 'single-region vs multi-region' on every greenfield engagement. The decisions look unique but follow the same axes: team-skill, compliance, scale-target, cost-curve, vendor-lock-in tolerance, recovery requirements. This methodology pins a decision matrix per axis with weighting + red-flag list (e.g. 'compliance requires data sovereignty → managed cloud out'). Outcome: a 1-page decision record with rationale per cell. Used at project kickoff + revisited yearly.

**Ефективно для:**

- Greenfield kickoff: 1 година матрицю → 1-page decision record.
- Уникнення re-deciding 'EKS vs ECS' на кожному проєкті.
- Red-flags: compliance / sovereignty switches off cells автоматично.
- Revisit yearly — capture коли decision стане stale.

## Applies If (ALL must hold)

- Greenfield infra (no legacy constraint that pre-decides)
- Multi-month commitment expected (decision matters)
- Team has authority to choose tech (not vendor-locked)
- Stakeholders (product, engineering, security) available for the kickoff session

## Skip If (ANY kills it)

- Brownfield with existing platform — extend, don't re-decide
- Trivial scope (single Lambda, single S3 bucket) — overhead exceeds value
- Compliance / contractual mandate already pre-decides (e.g. SaaS contract requires GCP)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stakeholder kickoff slot (2h block) | calendar | engineering leader |
| Workload sketch (scale, latency, compliance constraints) | product brief | product owner |
| Budget envelope (rough monthly cost ceiling) | finance input | finance |
| Team skill inventory | internal HR | engineering leader |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[terraform]] | Tool-choice axis references this |
| [[us-uk-eu-compliance-matrix]] | Compliance constraints feed red-flags |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `constraint_gathering` | sonnet | Facilitated structured intake |
| `scoring_session` | opus | Cross-tradeoff synthesis with team |
| `decision_record_draft` | sonnet | Bounded ADR writing |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-greenfield-infra-decision-matrix.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[headroom-cost-model]]
- [[edge-and-cdn-strategy]]
- [[terraform]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
