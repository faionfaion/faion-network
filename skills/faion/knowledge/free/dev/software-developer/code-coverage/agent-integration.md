# Agent Integration — Code Coverage

Methodology covers line/branch/path coverage, tooling, thresholds, CI integration. Goal of this file: turn coverage from a vanity metric into an actionable signal an LLM agent can drive.

## When to use
- Setting a CI gate on new code coverage (diff coverage), not absolute repo coverage.
- Identifying critical untested paths in legacy code prior to refactor.
- Pre-release: surface modules below threshold, prioritize tests there.
- Onboarding tests for a third-party library wrapper before upgrading the dep.
- Justifying test budget — coverage diff PR-over-PR shows trend.

## When NOT to use
- As the primary quality metric. 100% coverage with no assertions is worse than 60% with rich assertions.
- Generated code (migrations, OpenAPI clients, protobuf stubs) — exclude in `.coveragerc` / `coverage.exclude`.
- UI smoke tests where flakiness > coverage value — coverage of E2E adds little signal vs unit tests.
- Performance-sensitive code where the coverage instrumentation overhead changes behavior (rare; coverage.py uses ~5-10% overhead, but C extensions sometimes blow up).
- Single-file scripts / spike code — overhead not justified.

## Where it fails / limitations
- README pushes "branch coverage > line coverage" but doesn't show how to assert each branch with `pytest --cov-branch` + `--cov-fail-under` on branch alone.
- Path coverage section warns "exponential complexity" but doesn't show that no mainstream Python tool actually does path coverage — agents may waste time looking.
- No diff-coverage tooling mentioned (`diff-cover`, `pytest-cov-context`) — leads to "100% on new files only" trick getting gamed.
- No mention of mutation testing (`mutmut`, `cosmic-ray`) — the real way to validate test *quality*, complementary to coverage.
- Excludes are easy to abuse: `# pragma: no cover` on the hot path zeros the metric without changing risk.
- Coverage on async / threading is unreliable in some runners (multiprocessing requires `coverage combine` with `--parallel-mode`).
- `pytest --cov` collected coverage of test files themselves unless `[tool.coverage.run] omit = ['tests/*']`.

## Agentic workflow
For coverage uplift: (1) run baseline `pytest --cov=src --cov-branch --cov-report=term-missing`, (2) parse the missing-lines report, (3) for each module below threshold, identify smallest set of new tests covering the largest contiguous miss block, (4) write tests with real assertions (not just `mod.func()`), (5) re-run coverage; require both line and branch deltas. CI: enforce `diff-cover --fail-under=90` on new code, soft warn on repo total.

### Recommended subagents
- `faion-test-agent` — Default for writing tests targeting uncovered lines/branches.
- `faion-code-agent` — Refactor untestable code (deep mocks needed) into smaller seams.
- `faion-software-architect` — Decides exclusions (generated code, migrations) and per-package thresholds.
- `faion-sdd-execution` — Wraps coverage uplift as a feature with milestones.
- `faion-devtools-developer` — Owns coverage CI, badge, history tracking.

### Prompt pattern
Per-module uplift:

```
Read coverage report for src/<module>. Identify the largest uncovered
branch (use --cov-report=term-missing). Write 2-4 pytest tests that:
  1) Cover the missed branches.
  2) Assert observable behavior (return value, side effect), not implementation detail.
  3) Reuse existing fixtures from tests/conftest.py.
Run: pytest tests/test_<module>.py --cov=src.<module> --cov-branch
--cov-report=term-missing --cov-fail-under=90.
```

Diff-coverage gate:

```
Generate scripts/diff-cover-ci.sh that:
1) Runs pytest --cov=src --cov-branch --cov-report=xml.
2) Calls diff-cover coverage.xml --compare-branch=origin/main --fail-under=90.
3) Returns exit non-zero on regression. Add to .github/workflows/ci.yml.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `coverage.py` | Python coverage measurement | https://coverage.readthedocs.io |
| `pytest-cov` | pytest plugin wrapper | https://pytest-cov.readthedocs.io |
| `diff-cover` | Coverage on diff vs base branch | https://github.com/Bachmann1234/diff_cover |
| `mutmut` | Mutation testing — validates test quality | https://mutmut.readthedocs.io |
| `cosmic-ray` | Mutation testing alt | https://cosmic-ray.readthedocs.io |
| `nyc` / `c8` | JS/TS coverage (V8 native via c8) | https://github.com/istanbuljs/nyc, https://github.com/bcoe/c8 |
| `vitest --coverage` | Vitest built-in (V8 or Istanbul) | https://vitest.dev/guide/coverage |
| `jest --coverage` | Jest built-in | https://jestjs.io |
| `go test -cover -coverprofile` | Go stdlib coverage | https://go.dev/blog/cover |
| `cargo tarpaulin` | Rust coverage | https://github.com/xd009642/tarpaulin |
| `genhtml` (lcov) | HTML report from lcov format | https://github.com/linux-test-project/lcov |
| `coverage combine` | Merge multi-process coverage data | bundled in coverage.py |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Codecov | SaaS | Yes — REST + GH App + CLI | Free for OSS, supports diff-cover comments on PRs |
| Coveralls | SaaS | Yes — `coveralls` CLI | Older, simpler than Codecov |
| SonarCloud / SonarQube | SaaS / OSS | Yes — `sonar-scanner` | Combines coverage + quality gates + duplication |
| Codacy | SaaS | Yes — REST | Less popular than Codecov |
| GitHub Actions | CI | Yes — `actions/upload-artifact` for `htmlcov/` | Cache coverage data between matrix jobs |
| Coverage gutters (VSCode ext) | IDE | Yes — reads `lcov.info` locally | Visualize missing branches inline |

## Templates & scripts
README provides snippets. Add this lcov-only flow that works across Python+JS+Go (≤45 lines):

```bash
#!/usr/bin/env bash
# scripts/coverage-all.sh — run coverage for each lang, merge into one lcov.
set -euo pipefail
out=coverage-merged.lcov
: > "$out"

# Python
if [[ -f pyproject.toml ]]; then
  pytest --cov=src --cov-branch --cov-report=lcov:python.lcov || true
  cat python.lcov >> "$out"
fi

# Node
if [[ -f package.json ]]; then
  npx --yes c8 --reporter=lcov --reports-dir=coverage-node \
    npm test || true
  cat coverage-node/lcov.info >> "$out"
fi

# Go
if [[ -f go.mod ]]; then
  go test ./... -coverprofile=go.cover
  # convert go.cover to lcov
  go install github.com/jandelgado/gcov2lcov@latest
  gcov2lcov -infile=go.cover -outfile=go.lcov
  cat go.lcov >> "$out"
fi

genhtml -o htmlcov-merged "$out"
echo "Open htmlcov-merged/index.html"
```

## Best practices
- **Use diff coverage as the gate, repo total as the trend.** Diff fail-under 90, repo soft target 75. Locks new code while allowing legacy uplift to pace itself.
- **Branch coverage required.** Line coverage misses unreached `else` branches; `--cov-branch` (Python) / `--branches` (nyc) / `-covermode=atomic` (Go).
- **Exclude generated code explicitly.** `[tool.coverage.run] omit = ["**/migrations/*", "**/proto/*", "**/_generated/*"]`. Audit `omit` in code review — easy to abuse.
- **Never `# pragma: no cover` defensive `if False`-like guards** without comment justifying. Reviewers miss it.
- **Pair with mutation testing on critical modules.** mutmut on the 5 most business-critical files; high coverage with surviving mutants = bad assertions.
- **Separate test types in CI**: unit coverage required, integration coverage informational. Mixing inflates the number without validating units.
- **Cache `.coverage`** across pytest-xdist workers + `coverage combine` at the end. Without combine, parallel runs lose data.
- **Fail-fast on threshold regression**, not just absolute. Codecov's "patch coverage" = the right metric; "project coverage" trend is secondary.
- **Don't compute coverage in production builds.** Always a separate CI step / matrix job.
- **Track coverage by package**, not just total. Set per-package thresholds in `pyproject.toml` (`[tool.coverage.report] fail_under` is global; use `diff-cover` for granularity).
- **Stop chasing 100%.** Set 80-90 as practical ceiling; remaining 10-20% is glue/error paths better validated by integration tests.

## AI-agent gotchas
- **`pytest --cov` measures the package, not test files** — but only if `omit` is set. Otherwise tests count toward coverage and inflate the number.
- **Async coverage on `asyncio` works**, but on `multiprocessing` you need `concurrency = ["multiprocessing"]` in `.coveragerc` AND `coverage combine` after.
- **`--cov` rerunning resets data** unless you pass `--cov-append`. Agents running test subsets repeatedly will lose coverage from prior runs.
- **`--cov-fail-under` works on total only**. To gate per-module, use diff-cover or write a custom checker parsing `coverage.json`.
- **Branch counts in coverage.py**: a `try/except` is one branch (entered or not), not two. README's "test all conditions" assumes if/elif which doesn't apply.
- **Parametrized tests with `pytest.mark.parametrize`** inflate coverage if they exercise many code paths but assert nothing. Reviewers must check assertions, not just count.
- **`# pragma: no cover` on a function vs a line**: function-level skips entire body but coverage tool still counts the `def` line as covered. Misleading.
- **Generated TypedDicts / Pydantic models** appear uncovered because their `__init__` isn't called. Exclude or instantiate in tests.
- **Coverage with `pytest-xdist`** (`-n auto`): each worker writes `.coverage.<pid>`. Without `pytest --cov-config` setting `parallel=True` and final `coverage combine`, you get partial reports.
- **C extensions / Cython** invisible to coverage.py. Need `cython --linetrace` and `CYTHON_TRACE=1` env at compile time.
- **Diff-cover false positive on renames**: file moves show as 100% changed, all uncovered. Use `diff-cover --src-roots=src` and exclude renames manually.
- **Coverage upload race condition** in matrix CI: parallel `codecov` uploads from py3.10/3.11/3.12 jobs can clobber each other unless given distinct flags (`-F unittests-py310`).
- **`coverage report --skip-empty`** hides files with 0 statements but counted in total — agent-friendly trick to clean reports.

## References
- README: `./README.md`
- Sibling: `../unit-testing/`, `../tdd-workflow/`, `../testing/`, `../mocking-strategies/`
- coverage.py: https://coverage.readthedocs.io/en/latest/
- pytest-cov: https://pytest-cov.readthedocs.io
- diff-cover: https://github.com/Bachmann1234/diff_cover
- Codecov docs: https://docs.codecov.com
- nyc / c8: https://github.com/istanbuljs/nyc, https://github.com/bcoe/c8
- Go cover: https://go.dev/blog/cover
- Tarpaulin (Rust): https://github.com/xd009642/tarpaulin
- mutmut: https://mutmut.readthedocs.io
- Martin Fowler on test coverage: https://martinfowler.com/bliki/TestCoverage.html
