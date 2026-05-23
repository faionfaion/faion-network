# Test Pyramid Policy Enforcement

## Summary

**One-sentence:** Generates a policy-enforcement record — 'no new e2e without justification' rule + PR template + budget tracker — so the pyramid rebalance does not regress.

**One-paragraph:** Generates a policy-enforcement record — 'no new e2e without justification' rule + PR template + budget tracker — so the pyramid rebalance does not regress.

**Ефективно для:**

- Solo team that has rebalanced from e2e-heavy to contract+unit and needs to hold the gain.
- Repo where PR reviews keep slipping new e2e tests through.
- Quarterly enforcement check after the rebalance landed.

## Applies If (ALL must hold)

- Team has completed a test-pyramid rebalance (qa-test-pyramid-vs-trophy-decision applied).
- PR template exists and can be amended.
- Code-review process exists where the policy can be enforced.
- Named owner is willing to sign off on every e2e addition.

## Skip If (ANY kills it)

- No prior rebalance — enforce after the policy is set, not before.
- Greenfield prototype with no production users.
- Regulatory mandate forces e2e — defer to legal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prior pyramid decision record | yaml | qa-test-pyramid-vs-trophy-decision output |
| Current e2e count per module | json | test-runtime breakdown |
| PR template path | path | repo workflow |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| qa-test-pyramid-vs-trophy-decision | Provides the per-module shape this policy enforces. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-no-new-e2e-without-justification, r2-budget-per-module, r3-named-owner, r4-quarterly-review, r5-pr-template-amended | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Test Pyramid Policy Enforcement artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: policy-without-pr-template, budget-not-tracked, override-without-trace | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-test-pyramid-policy-enforcement` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-test-pyramid-policy-enforcement` | sonnet | Bounded structural check against the output contract. |
| `review-test-pyramid-policy-enforcement` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-pyramid-policy-enforcement.json` | JSON skeleton matching the output contract. |
| `templates/test-pyramid-policy-enforcement.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-pyramid-policy-enforcement.py` | Validate Test Pyramid Policy Enforcement output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[qa-test-pyramid-vs-trophy-decision]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
