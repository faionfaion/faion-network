# Error Budget Policy and Freeze Rules

## Summary

**One-sentence:** Error-budget policy that converts SLO burn into deterministic actions (canary halt, ship freeze, focus shift, accept) with named owner, revert criteria, and stakeholder comms.

**One-paragraph:** An SLO without a policy is a dashboard. The policy turns burn into action: 'when budget burns at fast-rate AND service-class is user-facing critical, halt canary deploys'. Without a written policy, on-call debates 'what does this mean for us' every time. This methodology pins the policy text + freeze rules: who is authorized to declare a freeze, what actions a freeze allows (security patches, rollbacks) and forbids (new features), how revert criteria are met, who signs off on lift. Output: error-budget-policy.md per portfolio + freeze-rules.yaml machine-readable. Pairs with slo-burn-decision-matrix (the matrix is the lookup, the policy is the doctrine).

**Ефективно для:**

- Freeze не дебатний — policy визначає коли + хто + що дозволено.
- Stakeholder comms: product team знає, що означає 'freeze' (security only).
- Revert criteria: freeze автоматично знімається коли budget регенеровано.
- Doctrine: lift signed by engineering leader + product (no unilateral lift).

## Applies If (ALL must hold)

- SLOs defined per service
- Error-budget burn alerting in place
- Engineering team commits to act on budget burn (not observe)
- Product + engineering aligned on the doctrine (freeze stops feature shipping)

## Skip If (ANY kills it)

- SLOs aspirational and never trigger burn — fix SLO calibration first
- Org culture treats freezes as unacceptable — policy will be ignored

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| SLO definitions per service | slo.yaml | service owners |
| Burn-rate alerting | alert rules | SRE |
| Decision matrix (slo-burn-decision-matrix) | matrix.yaml | platform team |
| Stakeholder sign-off (product, engineering leader) | policy review meeting | VP eng |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[slo-burn-decision-matrix]] | Matrix is the lookup table this policy authorizes |
| [[slo-definition-template-per-service-class]] | SLOs the policy references |

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
| `doctrine_draft` | opus | Cross-stakeholder policy synthesis |
| `freeze_rules_yaml` | haiku | Mechanical YAML fill from doctrine |
| `comms_message_draft` | sonnet | Compose freeze announcement |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-error-budget-policy-and-freeze-rules.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[slo-burn-decision-matrix]]
- [[fast-vs-slow-burn-rule]]
- [[slo-definition-template-per-service-class]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
