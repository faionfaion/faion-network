# Agent Integration — TDD Workflow

## When to use
- Bug-fix workflow: agent must reproduce the bug as a failing test before touching production code.
- Pure-function or business-logic implementation where requirements are precise (validators, calculators, parsers, state machines).
- API contract design — tests document the public surface before any handler exists.
- Library / SDK work where consumers depend on a stable interface.
- Onboarding a model into an unfamiliar codebase — writing tests first forces it to read the existing API.

## When NOT to use
- Exploratory spikes / research code — feedback loop is faster without tests.
- UI prototypes where the design changes hourly.
- Glue scripts and one-off migrations.
- Code that is intrinsically hard to test (rendering, hardware drivers, framework internals) — invest in integration / characterization tests instead.
- Hot-fix under outage pressure — write the fix, then add the regression test in a follow-up PR (and label that PR clearly).

## Where it fails / limitations
- Agents skip the RED step: they write the implementation first, then "tests" that validate what they wrote (rationalization, not verification).
- Tests pin internal details (private methods, exact log strings) and break under any refactor.
- Mock-heavy unit tests pass while integration is broken.
- Coverage % becomes the goal; agents game it with assertions on `True`.
- Refactor step is universally skipped — green tests + ugly code is "done" for an LLM unless the loop forces it.

## Agentic workflow
Drive TDD as a loop subagent invocation per behavior, not per feature: prompt for ONE failing test, run, confirm RED, prompt for minimal pass, run, confirm GREEN, then prompt for refactor, run, confirm still GREEN. The orchestrating agent enforces the cycle by checking the test runner output between steps — if the model jumps ahead (writes both test and impl in one turn), reject the diff. A senior model handles refactor decisions; cheaper models handle GREEN-step boilerplate.

### Recommended subagents
- `faion-sdd-executor-agent` — already structured around quality gates; pair with explicit RED/GREEN/REFACTOR prompts.
- `faion-feature-executor` — sequential task execution mode is a natural fit for stepping through the cycle.
- A `tdd-cycle-enforcer` (custom) — single-purpose: parse `pytest -x` output, decide RED vs GREEN, refuse to advance phase if state is wrong.

### Prompt pattern
```
PHASE: RED. Behaviour: <one sentence>.
Output ONLY a new test in <test file>. Do not modify implementation files.
After write, run `pytest path::test -x`. Expected: 1 failed, 0 passed.
```

```
PHASE: GREEN. Implement minimum code to make test <name> pass. Do not change other tests. Do not add features not exercised by the failing test. Run `pytest path::test -x`. Expected: 1 passed.
```

```
PHASE: REFACTOR. Improve <file> without changing public API or test outcomes. Run full suite `pytest -q`. Expected: same pass count as before. Block if any test now fails.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` + `pytest-watch` (`ptw`) | Auto re-run tests on save | https://docs.pytest.org / https://github.com/joeyespo/pytest-watch |
| `pytest-cov` | Coverage; pair with `--cov-fail-under` | https://pytest-cov.readthedocs.io |
| `mutmut` / `cosmic-ray` | Mutation testing — kills "fake" tests that pass against any impl | https://mutmut.readthedocs.io |
| `vitest --watch` | JS/TS equivalent | https://vitest.dev |
| `jest --watch` | JS/TS equivalent | https://jestjs.io |
| `cargo test` + `cargo-watch` | Rust | https://github.com/watchexec/cargo-watch |
| `go test ./... -count=1` | Disable cache for Go | go.dev |
| `entr` / `watchexec` | Re-run any command on file change | https://github.com/eradman/entr |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | yes | Required: status check on each PR; agents read `gh pr checks` for failure detail. |
| Codecov / Coveralls | SaaS | yes | Coverage delta on PR — agent uses to flag uncovered branches. |
| Stryker (mutators) | OSS | partial | Agents can run, but interpreting surviving mutants needs human review. |
| Cursor / Aider TDD modes | SaaS/OSS | yes | Some IDEs have RED/GREEN modes baked in. |
| pytest-xdist (`-n auto`) | OSS | yes | Parallelism cuts feedback latency, critical for tight TDD loops. |

## Templates & scripts
See `templates.md` for full RED/GREEN/REFACTOR examples in Python and TypeScript. Inline single-behavior loop driver:

```bash
#!/usr/bin/env bash
# tdd.sh — usage: ./tdd.sh path/to/test_file.py::test_name
set -e
TEST="$1"
echo "=== RED ==="
pytest "$TEST" -x && { echo "Expected fail; aborting"; exit 1; }
read -p "Now write minimal impl, then ENTER for GREEN... "
echo "=== GREEN ==="
pytest "$TEST" -x
read -p "Now refactor, then ENTER for full suite... "
echo "=== REFACTOR ==="
pytest -q
```

For agents, replace `read` prompts with explicit subagent invocations.

## Best practices
- One assertion concept per test, but multiple assert statements are fine if they describe the same behaviour.
- Test names: `test_<unit>_<scenario>_<expected>` e.g. `test_validator_rejects_short_password_with_clear_error`.
- Arrange-Act-Assert visual separation (blank lines), not comments.
- Use fakes (`FakeInventory`) over mocks when the dependency has logic; only mock when verifying interaction is the goal.
- Triangulate: write 2–3 input cases that force the implementation to generalize, otherwise GREEN tempts hardcoded returns.
- Tests live near code (`module.py` + `test_module.py`) for easy navigation; agents are bad at keeping mirrored `tests/` trees in sync.
- Run mutation testing weekly on critical modules — it's the only check that distinguishes "tests exist" from "tests would catch regressions".

## AI-agent gotchas
- The "skip RED" failure mode: agent writes a passing test against new code in one turn. Force RED by requiring failure output as part of the response.
- Agents over-mock: they'll mock `datetime.now`, file I/O, and the system under test. Restrict mocking to clearly external boundaries in the prompt.
- LLMs invent assertions that don't actually constrain behaviour: `assert result is not None` for a function that returns a fixed string. Reviewer subagent should flag weak assertions.
- Refactor phase is the highest-value, lowest-attention step for LLMs. Make it a separate agent invocation with the explicit goal "do not add features".
- Human-in-loop checkpoint: read the failing test before allowing GREEN. The test is the spec; if it's wrong, the implementation that satisfies it is also wrong.
- Coverage gating works against TDD when set too high — agents add `pragma: no cover` or write trivial tests to clear the bar. Pair coverage with mutation testing or branch coverage.
- For bug fixes, require the test to reference the issue ID in a docstring; auditing later proves the regression was actually pinned.

## References
- Kent Beck, "Test-Driven Development by Example" — https://www.amazon.com/dp/0321146530
- Steve Freeman & Nat Pryce, "Growing Object-Oriented Software, Guided by Tests" — http://www.growing-object-oriented-software.com/
- Robert C. Martin, "The Cycles of TDD" — https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html
- Martin Fowler, "Is TDD Dead?" series — https://martinfowler.com/articles/is-tdd-dead/
- https://mutmut.readthedocs.io — mutation testing for Python
- https://stryker-mutator.io — mutation testing for JS/TS/C#
