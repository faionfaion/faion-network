# Mutation Testing as the Agent Feedback Signal

## Summary

**One-sentence:** Replace coverage gates with diff-scoped mutation testing (Stryker / mutmut / PIT); feed surviving-mutants back to the agent's next iteration; gate merges on a mutation-score threshold.

**One-paragraph:** Coverage percent is a near-useless signal for AI-written tests — agents can hit 90% line coverage with assertions that never observe a mutation. Replace coverage gates with mutation testing (Stryker, mutmut, PIT) scoped to changed files, and feed the surviving-mutants report back into the agent's next iteration. The gate passes only when the mutation score on the diff clears a threshold (typical: 70 break / 80 high). Meta's ACH (FSE 2025) extended the pattern: an LLM both generates targeted mutants for a domain (privacy, compliance, payments) and writes the tests that kill them — 73% of ACH-suggested tests merged at Messenger and WhatsApp.

**Ефективно для:**

- Agent-written tests, де coverage% — фейковий сигнал.
- Stripe-like high-stakes domains: payments / privacy / compliance.
- FSE 2025 Meta ACH pattern: LLM генерує mutants + tests, що їх kill.
- CI що уже стабільний (flaky base = mutation noise).

## Applies If (ALL must hold)

- Project has a stable test suite and CI capacity for an extra slow job.
- Agent-written tests are common in the workflow.
- Critical domain (payments, privacy, compliance) where weak tests cost real money.

## Skip If (ANY kills it)

- Pure prototype or research code where test quality is not gated.
- Test suite is so flaky that mutation noise drowns out signal.
- Language without a viable mutation tool (rare in 2026 mainstream stacks).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stable test suite | code | repo |
| Mutation tool installed | Stryker / mutmut / PIT | dev environment |
| CI runner with slow-job budget | infra | CI provider |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stryker.conf.json` | Stryker config with diff scope + break/high thresholds. |
| `templates/mutation-prompt.txt` | Prompt feeding surviving mutants back to the coding agent for iteration 2. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-mutation-feedback-loop.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[test-tdd-red-green-split-agents]]
- [[test-property-based-llm-invariants]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
