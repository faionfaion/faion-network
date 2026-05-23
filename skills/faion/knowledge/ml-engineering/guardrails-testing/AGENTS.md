# Guardrails Testing and Red-Teaming

## Summary

**One-sentence:** Builds three pytest suites — security (must-block payloads), accuracy (must-pass legit inputs), perf (latency p99 + throughput) — and the monthly red-team report.

**One-paragraph:** A guardrails layer that has not been red-teamed is theatre. This methodology produces the harness: parametrized unit tests per detector, integration tests with mocked LLM clients, an adversarial payload library (jailbreaks, encoded injection, role-play attacks, multi-turn chains), and a perf benchmark suite. Outputs a `guardrail-test-report.json` covering pass-rate per suite, false-positive rate, false-negative rate, and latency percentiles. Re-run pre-deploy + monthly + after model upgrade.

**Ефективно для:**

- Pre-deploy gate — без зеленого звіту guardrails-харнес не пускає реліз у прод.
- Monthly red-team — нові jailbreak-патерни зʼявляються щомісяця; стара захист тиха гниє.
- Model upgrade (gpt-4o → gpt-5) — non-deterministic поведінка змінюється, треба перевалідувати все.
- FP report investigation — користувачі скаржаться що legit input блокується; харнес ловить regress на конкретному patternі.

## Applies If (ALL must hold)

- Deployed or about-to-be-deployed guardrails layer (custom / NeMo / Guardrails AI).
- Python + pytest available; team can mock LLM clients in CI.
- Application owner accepts monthly red-team cadence (or pre-deploy gate only at minimum).

## Skip If (ANY kills it)

- Live prod traffic — tests must run in staging against prod-equivalent config.
- E2E with live LLM in CI — cost + flakiness explode; mock instead.
- Internal-only dev tooling with no security surface — harness ROI negative.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `guardrails_pipeline.py` or NeMo config | Python module / dir | `guardrails-custom-pipeline` / `guardrails-nemo` |
| Adversarial payload library | JSONL / YAML | this methodology produces it |
| pytest + pytest-benchmark | dev dep | dev requirements |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `guardrails-concepts` | Plan tells the harness which rails to test. |
| `guardrails-custom-pipeline` | Tested system under test. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: three-suite split, parametrize-detector, mock-llm-in-ci, payload-library-versioned, fp-budget, latency-p99-baseline | 1100 |
| `content/02-output-contract.xml` | essential | Schema for `guardrail-test-report.json` | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: live-llm-in-ci, no-fp-budget, single-payload-set, no-baseline | 800 |
| `content/04-procedure.xml` | essential | 6 steps: build payload lib → security suite → accuracy suite → perf suite → red-team → report | 800 |
| `content/05-examples.xml` | essential | Worked example: report for a custom pipeline | 600 |
| `content/06-decision-tree.xml` | essential | Test cadence decision tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold_suites` | haiku | Templated pytest layout. |
| `generate_payloads` | sonnet | Adversarial creativity needed. |
| `interpret_red_team` | opus | High-stakes reasoning over failure traces. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test_security.py` | Security suite skeleton with payload table |
| `templates/test_accuracy.py` | False-positive suite skeleton |
| `templates/test_perf.py` | Latency / throughput benchmark skeleton |
| `templates/_smoke-test.py` | Minimal runner |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-guardrails-testing.py` | Validate `guardrail-test-report.json` | After test run; pre-merge gate |

## Related

- [[guardrails-custom-pipeline]] — system under test
- [[guardrails-nemo]] — NeMo config under test
- [[prompt-injection-defense]] — source of adversarial patterns

## Decision tree

See `content/06-decision-tree.xml`. Branches on deploy stage (pre-deploy / monthly / on-incident) and on whether model was upgraded.
