# Verification Rung Placement Rule

## Summary

**One-sentence:** Produces a Rung Placement Record that routes every check to the cheapest instrument able to detect its defect — rung 1 static lint at zero tokens, rung 2 trigger evals scored mechanically, rung 3 a pairwise judge, rung H a person reading — and rejects any placement that cannot justify itself against the rung below.

**One-paragraph:** The whole of verification collapses into one operational question: for this specific failure, what is the cheapest instrument that can detect it? The rungs are not novel and they are not a maturity model — you do not graduate from rung 1 to rung 3. Their value is that they forbid the expensive mistake everyone makes, which is reaching for a model to catch a defect a regex would have caught for free. Our own live example: 528 broken reference slugs across 5,744 published files were being found by a review agent, at rung-3 prices, for a defect a twenty-line validator catches on every commit at zero cost. Placement also constrains what each rung is allowed to do once a check lands there — exact rules may block and heuristics may only flag, rung 3 is pairwise and capped at fifteen scenarios because the best debiased judge tested still only reaches κ=0.549, and rung H is a legitimate gate whose cost is founder-hours and whose job is to discover new checks rather than to repeat old ones.

**Ефективно для:**

- Deciding where a newly discovered defect class should be caught, before writing anything.
- Auditing an existing suite that is green and has never caught a real regression.
- Any team about to build an eval harness or a judge before it has a referential-integrity check.
- Solopreneurs deciding what to automate first when attention is the scarce resource.

## Applies If (ALL must hold)

- More than one verification instrument is available — at minimum, code and a person.
- Defects are recurring often enough that where they get caught matters.
- Someone is paying for the current instrument, in tokens, in wall-clock, or in their own hours.

## Skip If (ANY kills it)

- Only one instrument exists and there is nothing to route between.
- The question is what a gate should do when it breaks, not which gate to build — see `gate-fail-closed-rule`.
- The question is whether a phase may be promoted rather than which instrument verifies a check — see `quality-gates-confidence`.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | R1 places the check by three questions. R2 is the discipline: a check may live on a rung only if it cannot live on the rung below. R3-R6 govern blocking, judge shape, manual review, and cadence. |
| `content/02-output-contract.xml` | The Rung Placement Record: per-check fields, the answer-to-rung mapping, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six misplacement modes with the live instance of each, including plumbing suites that are green by construction. |
| `content/06-decision-tree.xml` | The three-question tree plus four overlays that constrain a check once it has landed. |
| `scripts/validate-verification-rung-placement-rule.py` | Validates a record; catches rung inflation mechanically by checking rung against the placement answer. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rung-placement-record.yaml` | Worked eight-check record over the faion corpus and CLI. Ships valid against the contract. |
| `templates/rung-placement-record-single-check.yaml` | Everyday one-check triage after a manual review catch. Ships valid against the contract. |

## Related

- `gate-fail-closed-rule` — what a gate must do when it cannot evaluate. Placement decides the instrument; that decides its behaviour on failure.
- `lint-autofix-vs-flag-decision-rule` — what to do with a finding once produced; this routes which instrument found it.
- `lint-precommit-floor` — the hook carries rung 1 only; this is the rule that says why.
- `eval-driven-development-tdd-for-ai` — when to write an eval; this decides whether an eval is the right tool at all.
- `agent-eval-cost-budget-policy` — cadence and spend inside rungs 2 and 3, once placement has put a check there.
- `judge-calibration-protocol` — rung 3's entry requirement: no judge without a measured κ.
- `quality-gates-confidence` — phase-promotion gates; orthogonal, and each of its levels still needs its checks placed.
