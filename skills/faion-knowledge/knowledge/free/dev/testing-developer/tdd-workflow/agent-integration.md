# Agent Integration — TDD Workflow

## When to use
- Bug-fix workflow: agent must reproduce the bug as a failing test before touching production code.
- Pure-function or business-logic implementation where requirements are precise (validators, calculators, parsers, state machines).
- API contract design — tests document the public surface before any handler exists.
- Library / SDK work where consumers depend on a stable interface.
- Onboarding a model into an unfamiliar codebase — writing tests first forces it to read the existing API.
- Specification-driven development (SDD) where ACs in `spec.md` map 1:1 to test cases.

## When NOT to use
- Exploratory spikes / research code — feedback loop is faster without tests; tests rot before commit.
- UI prototypes where the design changes hourly.
- Glue scripts and one-off migrations.
- Code that's intrinsically hard to unit-test (rendering, hardware drivers, framework internals) — invest in integration / characterization tests instead.
- Hot-fix under outage pressure — write the fix, then add the regression test in a follow-up PR (label clearly).
- Boilerplate code generation (proto, sqlc) — generated code shouldn't be TDD'd.

## Where it fails / limitations
- Agents skip the RED step: they write the implementation first, then "tests" that validate what they wrote (rationalization, not verification).
- Tests pin internal details (private methods, exact log strings) and break under any refactor.
- Mock-heavy unit tests pass while integration is broken — TDD without mutation testing can produce a false-confidence suite.
- Coverage % becomes the goal; agents game it with assertions on `True`.
- Refactor step is universally skipped — green tests + ugly code is "done" for an LLM unless the loop forces it.
- README presents TDD as universally applicable; reality is many domains (UI, infra, data engineering) do better with example-driven dev or property tests.

## Agentic workflow
Drive TDD as a loop subagent invocation **per behavior**, not per feature: prompt for ONE failing test, run, confirm RED, prompt for minimal pass, run, confirm GREEN, prompt for refactor, run, confirm still GREEN. The orchestrator enforces the cycle by parsing the test runner output between steps — if the model jumps ahead (writes both test and impl in one turn), reject the diff. Use a senior model for refactor decisions; cheaper models for GREEN-step boilerplate.

### Recommended subagents
- `faion-sdd-executor-agent` — already structured around quality gates; pair with explicit RED/GREEN/REFACTOR prompts.
- `faion-feature-executor` — sequential task execution mode is a natural fit for stepping through the cycle.
- A `tdd-cycle-enforcer` (custom) — single-purpose: parse `pytest -x` (or framework equivalent) output, decide RED vs GREEN, refuse to advance phase if state is wrong.
- `faion-test-agent` — emits the failing test only; no production code edits allowed.

### Prompt pattern
```
PHASE: RED. Behavior: <one sentence>.
Output ONLY a new test in <test file>. Do not modify implementation files.
After write, run `pytest path::test -x`. Expected: 1 failed, 0 passed.
Block if implementation files appear in the diff.
```

```
PHASE: GREEN. Implement the minimum code to make test <name> pass.
Do not change other tests. Do not add features not exercised by the failing test.
Run `pytest path::test -x`. Expected: 1 passed.
```

```
PHASE: REFACTOR. Improve <file> without changing public API or test outcomes.
Run full suite `pytest -q`. Expected: same pass count as before.
Block if any test now fails.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` + `pytest-watch` (`ptw`) | Auto re-run tests on save | https://docs.pytest.org / https://github.com/joeyespo/pytest-watch |
| `pytest-cov` | Coverage; pair with `--cov-fail-under` | https://pytest-cov.readthedocs.io |
| `mutmut` / `cosmic-ray` / `stryker` | Mutation testing — kills "fake" tests | https://mutmut.readthedocs.io |
| `vitest --watch` | JS/TS watch mode | https://vitest.dev |
| `jest --watch` / `--watchAll` | JS/TS watch mode | https://jestjs.io |
| `cargo test` + `cargo-watch` / `cargo nextest` | Rust runners | https://github.com/watchexec/cargo-watch |
| `go test ./... -count=1` | Disable cache for Go | go.dev |
| `entr` / `watchexec` | Re-run any command on file change | https://github.com/eradman/entr / https://watchexec.github.io/ |
| `pyflyby autoimport` / `ruff --fix` | Keep RED-phase tests compileable while iterating | https://docs.astral.sh/ruff/ |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions / GitLab CI | CI | Yes | Run `pytest --strict-markers --cov-fail-under=80` per PR |
| Codecov / Coveralls | SaaS | Yes | Block PR if coverage of changed lines drops |
| Pitest (Java) / Stryker (JS/TS/C#) | OSS | Yes — CLI integration | Mutation testing in CI to validate tests |
| Trunk Code Quality | SaaS | Yes — REST | Auto-quarantine flaky tests so RED-step signal stays clean |
| Reviewable / GitHub PR Review | SaaS | Yes | Enforce "test commit before impl commit" via commit-graph rule |

## Templates & scripts
See `templates.md` for the canonical loop. Inline orchestrator skeleton enforcing one-test-at-a-time:

```bash
#!/usr/bin/env bash
# scripts/tdd-cycle.sh — enforce RED → GREEN → REFACTOR for one test.
set -euo pipefail
TEST="$1"           # e.g. tests/billing/test_calc.py::test_zero_returns_zero
PHASE="${2:-red}"   # red | green | refactor

case "$PHASE" in
  red)
    pytest "$TEST" -x && { echo "Expected RED, got GREEN. Block."; exit 1; }
    echo "RED confirmed."
    ;;
  green)
    pytest "$TEST" -x || { echo "Still RED. Continue implementing."; exit 1; }
    echo "GREEN confirmed."
    ;;
  refactor)
    pytest -q || { echo "Refactor broke tests. Revert."; exit 1; }
    echo "Suite still GREEN after refactor."
    ;;
  *) echo "Unknown phase: $PHASE"; exit 1 ;;
esac
```

## Best practices
- **One test per cycle.** Resist writing the next test until current code is committed.
- **Commit RED → GREEN → REFACTOR as separate commits.** Easy to review, easy to revert.
- **Behavior names, not function names.** `test_returns_zero_when_quantity_is_zero` beats `test_calculate_total_v2`.
- **Run mutation tests on the new tests** before merging. If `mutmut`/`stryker` survives a mutation, your test is weak.
- **Don't refactor and add behavior in the same step.** Refactor moves code while keeping tests green; new behavior requires a new RED test first.
- **Tests must fail for the right reason in RED.** A test that fails because of an `ImportError` is not a real RED.
- **Resist the urge to design ahead.** TDD design emerges from tests; pre-designing leads to YAGNI features.
- **Pair TDD with property-based tests** for parsers/serializers — TDD covers happy + known edges; property tests find unknown unknowns.
- **For LLM-driven TDD, gate on test runner output, not on the LLM's claim of completion.** The runner is the source of truth.

## AI-agent gotchas
- **The LLM writes test + impl in one turn.** Reject diffs that touch both. Force one-or-the-other per turn.
- **"Fake" RED**: agent writes a test that asserts `False` to satisfy "must fail first". Detect by checking the failure was in an assertion related to the behavior, not a NameError / ImportError.
- **Skipping REFACTOR**: agent declares done at GREEN. Add an explicit refactor prompt in the loop, even if the answer is "no refactor needed".
- **Over-mocking in GREEN step** to make trivial impl pass — verifies the mock, not the code. Re-run with `mutmut` after merge.
- **Pinning private API in tests**: agent writes `assert obj._internal_state == ...`. Reject; refactor immediately or test through public API.
- **Wrong test framework**: agent uses `unittest.TestCase` style in a `pytest` codebase, breaking fixtures. Specify framework explicitly in prompt.
- **Async TDD in Python**: forgetting `@pytest.mark.asyncio` makes the test silently pass (coroutine returned, never awaited).
- **REFACTOR phase scope creep**: agent rewrites unrelated modules "for cleanliness". Constrain refactor to the file under test plus its direct dependents.
- **TDD with mocks for everything**: end up with a green suite that proves nothing. Mandatory mutation-test gate after every 5 cycles.
- **Human-in-loop checkpoint**: review the test name and assertion before letting the agent enter GREEN. The behavior contract is the most expensive thing to fix later.

## References
- README: `./README.md`
- Sibling: `../unit-testing/`, `../mocking-strategies/`, `../testing-patterns/`, `../test-fixtures/`
- "Test Driven Development: By Example" — Kent Beck
- "Growing Object-Oriented Software, Guided by Tests" — Freeman & Pryce
- https://martinfowler.com/bliki/TestDrivenDevelopment.html
- https://mutmut.readthedocs.io
- https://stryker-mutator.io
- https://docs.anthropic.com/en/docs/claude-code/sub-agents
