# Agent Integration — Code Coverage

## When to use
- Agent-authored test generation: feed coverage reports back to the LLM so it knows which branches still lack tests.
- CI gate: enforce minimum coverage on changed lines (diff coverage) for PRs touched by an agent.
- Targeted refactor planning — high-churn, low-coverage files become the first refactor candidates.
- Onboarding a new repo: an agent runs coverage once to map "what's tested" before suggesting changes.

## When NOT to use
- Tiny one-shot scripts with no test infra at all — wiring coverage costs more than it returns.
- UI/visual code where snapshot/visual tests give better signal than line coverage.
- Generated/migration code — exclude from coverage, don't try to test.
- As a single quality KPI for performance reviews — Goodhart's law applies; agents will write trivial tests to hit the number.

## Where it fails / limitations
- High line coverage with weak assertions: agents happily call functions and ignore return values. Coverage = 100%, behaviour untested.
- Branch coverage hides condition coverage: `if a and b:` reports two branches but four condition combos.
- Coverage tools' default exclusions (e.g., `__init__.py`, `if __name__ == "__main__"`) are correct for humans but agents need explicit reminders.
- Mutation testing reveals what coverage misses but is slow; agents must batch it.
- Async / multiprocess / native-extension code under-reports without `coverage.process_startup()` / `--cov-context`.

## Agentic workflow
Bake coverage into every test-writing loop. Step 1: run the suite with branch coverage and a machine-readable report (`coverage.xml`, Jest `lcov.info`). Step 2: feed the missing lines/branches to a test-author subagent with the source of the affected file pinned in context. Step 3: agent writes targeted tests, asserting behaviour (not just calling the function). Step 4: re-run coverage; if delta < expected, repeat or escalate to a human. Use `diff-cover` to enforce coverage only on changed lines so legacy gaps don't block PRs.

### Recommended subagents
- `faion-feature-executor` — sequential SDD task execution, naturally enforces test-coverage gates per task.
- `faion-sdd-executor-agent` — quality-gate-driven; coverage is one of the gates.
- Test-author subagent (Sonnet) — writes targeted tests for missing branches.
- Mutation-testing subagent (Opus, batch) — runs `mutmut`/`stryker` periodically to surface weak assertions.

### Prompt pattern
```
File: src/payments/processor.py
Coverage report (uncovered):
  lines 45-50  (network-error branch)
  lines 67     (refund early-return)

Write pytest tests covering exactly those branches.
Constraints:
- Each test must have at least one explicit `assert` on observable behaviour.
- Use existing fixtures from tests/conftest.py.
- No test that only exercises the line without asserting state.
Output: a single new file tests/test_processor_branches.py.
```
```
diff-coverage on this PR is 62% (target 90%).
Identify untested changed lines and propose tests, ranked by risk.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `coverage.py` / `pytest-cov` | Python line + branch coverage | https://coverage.readthedocs.io |
| `diff-cover` | Coverage for changed lines vs base branch | https://github.com/Bachmann1234/diff_cover |
| `mutmut` / `cosmic-ray` | Python mutation testing | https://mutmut.readthedocs.io |
| `jest --coverage` | JS/TS coverage with Istanbul | https://jestjs.io |
| `vitest --coverage` (`@vitest/coverage-v8`) | Modern Vite-based JS test coverage | https://vitest.dev |
| `c8` | Native V8 coverage for Node | https://github.com/bcoe/c8 |
| `nyc` | Istanbul CLI | https://github.com/istanbuljs/nyc |
| `stryker-mutator` | JS mutation testing | https://stryker-mutator.io |
| `go test -cover -coverprofile` | Go coverage | https://pkg.go.dev/cmd/go |
| `cargo-tarpaulin` / `grcov` | Rust coverage | https://github.com/xd009642/tarpaulin |
| `lcov` / `genhtml` | Format/merge LCOV reports | http://ltp.sourceforge.net/coverage/lcov.php |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Codecov | SaaS | Yes (REST API + CLI) | Per-PR diff coverage, components, flags |
| Coveralls | SaaS | Yes (API + CLI) | Simple LCOV uploader |
| SonarQube / SonarCloud | OSS + SaaS | Yes (API + scanner) | Coverage + quality gates, "new code" rules |
| GitHub Actions artifacts | SaaS | Yes | Cheap option: store HTML report as artifact, no SaaS dep |
| Codacy | SaaS | Yes | Per-language coverage trend |
| `coverage badge` services (Shields.io endpoint) | SaaS | Yes | Simple README badges |

## Templates & scripts
The methodology already ships pyproject + jest + GH Actions snippets in `templates.md`. Useful companion: a CI script that fails only on diff-coverage regression and emits a structured prompt for the agent.

```bash
#!/usr/bin/env bash
# diff-cov-report.sh — emit per-file uncovered changed lines for an agent.
# Usage: diff-cov-report.sh origin/main 90
set -euo pipefail
BASE="${1:-origin/main}"
TARGET="${2:-90}"

# Run full coverage with branch
pytest --cov=src --cov-branch --cov-report=xml -q

# Diff-cover against base; markdown for humans, json for agent
diff-cover coverage.xml --compare-branch="$BASE" \
  --fail-under="$TARGET" \
  --markdown-report diff-cov.md \
  --json-report   diff-cov.json

# Emit agent-ready prompt fragments
jq -r '
  .src_stats | to_entries[]
  | "FILE: \(.key)\nUNCOVERED_LINES: \(.value.uncovered_lines | join(\",\"))\n"
' diff-cov.json
```

## Best practices
- Track **diff coverage** on PRs (target 80-95%) instead of repo-wide percentage. Legacy gaps shouldn't block new work.
- Always enable **branch coverage**, not just line. Set `branch = true` in `coverage.py`, `--branch` in `nyc`, `coverageProvider: 'v8'` for Vitest.
- Combine coverage with mutation testing on critical modules (auth, billing, data integrity) — coverage measures execution, mutation measures assertion strength.
- Exclude carefully: `pragma: no cover` is OK for genuine no-test code (CLI entry, type-checking-only blocks). Forbid the agent from adding it to silence failing thresholds.
- Per-directory thresholds beat a single global number (utility libs 90%, glue code 70%).
- Pin the coverage tool version; flaky/unreliable coverage tools cause "tests pass locally, fail in CI" loops that LLMs will keep retrying.
- Persist HTML reports as CI artifacts so the agent (or human) can drill into specific lines.

## AI-agent gotchas
- **Coverage gaming.** Agent writes `def test_x(): processor.run()` with no assertion. Require at least one `assert`/`expect` per test in the prompt; verify with a lint rule (`pytest-flake8-assertions`, `eslint-plugin-jest/expect-expect`).
- **Phantom imports for coverage.** Agent imports a module just to bump line coverage. Detect via mutation testing or by checking that each new test fails when the function under test is broken.
- **Threshold ratcheting trap.** Agent keeps adding `pragma: no cover` to pass thresholds. Fail the build if pragmas are added to changed files unless explicitly justified in the PR body.
- **Async coverage gaps.** Agent doesn't realise `pytest-asyncio` / Jest fake timers need extra config; coverage looks low even though tests run. Provide a coverage-config snippet in the prompt.
- **Big report context.** Don't paste the full XML/HTML report into the prompt — extract only uncovered lines per touched file.
- **Human-in-loop checkpoint.** Agent should not lower a coverage threshold to make CI green. Threshold changes go via a labelled PR with human sign-off.
- **Mutation cost.** Agents will run mutation tests on every commit if you let them. Schedule it nightly on changed packages only.

## References
- https://coverage.readthedocs.io/, https://pytest-cov.readthedocs.io/
- https://jestjs.io/docs/configuration#coveragethreshold-object
- https://martinfowler.com/bliki/TestCoverage.html — coverage is a tool, not a goal
- https://github.com/Bachmann1234/diff_cover — diff-coverage tool
- https://stryker-mutator.io/, https://mutmut.readthedocs.io/
- https://docs.codecov.com/docs/quick-start
