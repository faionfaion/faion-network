# Gate Fail-Closed Rule

## Summary

**One-sentence:** Produces a Gate Failure Contract that forces every gate to answer one question — what do you report when you could not evaluate? — and routes every non-evaluating outcome to FAIL instead of the silent pass it defaults to today.

**One-paragraph:** A gate has three possible verdicts, PASS, FAIL and ERROR, and almost every gate written by hand has only two. The missing one leaks: an exception handler returns an empty result, a runner discards a sub-check's exit status, a configured checker is never invoked — and each of those renders as a clean build. The failure is silent by construction, because the symptom is absence, and it concentrates exactly where it hurts most: a judge fails when the provider is degraded, which is when volume is highest and attention is lowest. This methodology names the five non-evaluating modes, states the fix that actually ships (emit a synthetic finding at the gate's own blocking severity, do not raise into every caller), and requires a fault-injection proof so fail-closed is demonstrated rather than asserted. It costs zero tokens and catches a whole class of failure that no amount of better checking can reach.

**Ефективно для:**

- Any LLM-backed quality gate — judge, rubric scorer, classifier — where a bad reply currently parses to "nothing found".
- Aggregate runners that wrap several validators and report one status, especially shell scripts using pipes.
- Repositories where a linter, scanner or prose checker is configured but its output appears in no log.
- Anyone auditing why a gate that has been green for months finds nothing.

## Applies If (ALL must hold)

- A check exists whose verdict something downstream trusts — CI, a merge, a publish step, a batch driver.
- That check has at least one code path that terminates without producing a verdict.
- Nobody has yet broken the check on purpose and watched the build go red.

## Skip If (ANY kills it)

- The check's output is advisory and nothing branches on it — then it is a report, not a gate, and fail-open is its correct behaviour.
- The gate is a pure total function over bytes with no I/O, no subprocess and no parsing — there is no non-evaluating path to close.
- You have not decided what the gate should check yet. Instrument choice comes first — see `verification-rung-placement-rule`.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | R1 is the rule: a gate that cannot evaluate must not report pass. R2-R6 close the five doors it leaks through. |
| `content/02-output-contract.xml` | The Gate Failure Contract: every field, the per-instrument mandatory modes, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six production ways a gate reports pass without evaluating, with the live instance of each. |
| `content/06-decision-tree.xml` | Routing from the observed leak site to the fix. |
| `scripts/validate-gate-fail-closed-rule.py` | Validates a contract; enforces mandatory modes per instrument, severity floors, and the dated override. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gate-failure-contract.yaml` | Judge gate — the full five-mode case. Ships valid against the contract. |
| `templates/gate-failure-contract-static.yaml` | Rung-1 static gate — where the leak is the runner, not the model. Ships valid against the contract. |

## Related

- `verification-rung-placement-rule` — which instrument a check belongs on. That decides what the gate is; this decides what it does when it breaks.
- `lint-autofix-vs-flag-decision-rule` — what to do with a finding once the gate produced one. Same discipline, one step later.
- `ci-eval-gate-config` — the CI shape for eval gates; the fail-closed clause belongs in that config.
- `quality-gates-confidence` — phase-promotion gates; each of its levels needs a Gate Failure Contract of its own.
- `regression-eval-before-fix-rule` — the fault-injection proof is the same move applied to gates instead of to bugs.
