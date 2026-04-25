# AGENT-02 — Python Tooling for AI-Augmented SDLC

State of the art as of April 2026. Focus: deterministic floor (lint/format/type/test/security) + how AI agents (Claude Code, aider, Codex) wire into it. Astral's Rust toolchain (ruff, uv, ty) plus Meta's pyrefly now form the "fast feedback" backbone that makes agentic loops viable — sub-10ms validation lets an agent iterate hundreds of times per task without melting the wall clock.

Important April 2026 context: **OpenAI acquired Astral in March 2026**; uv/ruff/ty are being integrated directly into Codex. Astral's `rye` is deprecated and folded into `uv`. ty is in beta (released Dec 16 2025), targeting 1.0 in 2026. Pyrefly (Meta) is in beta at v0.62, passing 90% of the Python typing conformance suite as of April 2026.

---

## M01 — `lint-ruff-as-agent-floor`  (lint-)

**Rule.** Use `ruff check` + `ruff format` as the single source of truth for lint/format/import-sorting. One tool replaces flake8 + black + isort + pydocstyle + pyupgrade + autoflake. Configure in `pyproject.toml` under `[tool.ruff]`. AI agents MUST run `ruff check --fix && ruff format` after every edit before claiming task complete.

**Why for AI.** Ruff processes <10 ms/file. An agent that iterates 200x in a session pays ~2 s of lint overhead total — the loop stays viable. At 2 s/file with legacy tools, the same loop is 400 s = unusable.

**URL.** https://docs.astral.sh/ruff/ · https://github.com/astral-sh/ruff · 2026 style guide changes: https://docs.astral.sh/ruff/formatter/

**When-to.** Every Python project, no exceptions. Default rule pack: `E,W,F,I,B,C4,UP,SIM,RUF`. Add `T20` (no-print), `DJ` (Django), `S` (Bandit subset) when applicable.

**When-NOT.** Don't use ruff when you need a deeper semantic linter that ruff hasn't ported (e.g., dead-code class graphs from `vulture`) — keep ruff plus the niche tool, not ruff alone.

**Snippet.**
```toml
# pyproject.toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "SIM", "RUF", "T20"]
ignore = ["E501"]  # handled by formatter
fixable = ["ALL"]

[tool.ruff.format]
quote-style = "double"
docstring-code-format = true
```

---

## M02 — `lang-uv-lockfile-floor`  (lang-)

**Rule.** Standardize on `uv` for env, deps, lockfile, Python install. One Rust binary handles `pip`, `pip-tools`, `virtualenv`, `pyenv`, and project workflow. Lockfile is `uv.lock`, committed. Use `uv sync` at session start, `uv add <pkg>` to mutate deps. AI agents call `uv run pytest`, never bare `pytest` — guarantees the right venv.

**Why for AI.** Reproducible env per agent task; `uv sync` is ~10x faster than `pip install -r requirements.txt`. Before each `uv run`, uv re-verifies lockfile vs `pyproject.toml` so the agent can't drift the env silently.

**URL.** https://docs.astral.sh/uv/ · https://github.com/astral-sh/uv · 2026 OpenAI/Astral integration: https://astral.sh/blog (Codex bundles uv)

**When-to.** All new projects. Migrate Poetry/pip-tools projects when feasible — `uv` reads `[project]` table directly, so PEP 621 metadata is portable.

**When-NOT.** If you need conda packages with binary deps from conda-forge (CUDA, GDAL, scientific stack), prefer `pixi` over uv for that subset (https://pixi.sh).

**Snippet.**
```bash
uv init my-pkg --package
uv add fastapi pydantic
uv add --dev pytest ruff ty hypothesis pytest-cov
uv lock --upgrade
uv run pytest -x  # always via `uv run`
```

---

## M03 — `lint-type-checker-dual-track`  (lint-)

**Rule.** Pick exactly one type checker and run it in CI + pre-commit. As of April 2026 the credible options are: **mypy** (incumbent, strict mode), **pyright** (Microsoft, mature), **ty** (Astral beta, 10–60x faster than mypy/pyright), **pyrefly** (Meta, 1.85M LOC/sec on huge codebases). For AI-agent loops choose ty or pyrefly; for stable production strictness today, mypy `--strict` or pyright is still safer.

**Why for AI.** Type errors are the single best deterministic signal an agent can use to self-correct. Sub-second checking = the agent can re-run after every edit. ty in editor: 4.7 ms vs pyright 386 ms vs pyrefly 2.38 s on a PyTorch edit (per Astral's beta post).

**URL.** mypy: https://mypy.readthedocs.io/ · pyright: https://microsoft.github.io/pyright/ · ty: https://docs.astral.sh/ty/ + https://astral.sh/blog/ty · pyrefly: https://pyrefly.org · https://github.com/facebook/pyrefly · https://engineering.fb.com/2025/05/15/developer-tools/introducing-pyrefly-a-new-type-checker-and-ide-experience-for-python/

**When-to.** New project with type-aware AI workflow → ty (accept beta caveats) or pyrefly. Existing mypy codebase that already passes strict → keep mypy until ty hits 1.0.

**When-NOT.** Don't run two checkers in CI — pick one, document why. Don't run type checking only locally — agents lie about "I ran mypy"; CI must enforce.

**Snippet.**
```toml
# pyproject.toml — ty config
[tool.ty.environment]
python-version = "3.12"

[tool.ty.rules]
possibly-unresolved-reference = "error"
unused-ignore-comment = "warn"
```
```bash
uv tool install ty@latest
uv run ty check src/   # 10-60x faster than mypy
```

---

## M04 — `test-pytest-9-strict-config`  (test-)

**Rule.** pytest 9.x (released 2026) is the baseline. Enable native TOML config (`[tool.pytest.ini_options]`), `strict_parametrization_ids`, `strict_markers`, `--strict-config`, and `addopts = "-ra --tb=short"`. Run via `uv run pytest`. Coverage gate via `pytest-cov` with branch coverage and a per-PR fail threshold.

**Why for AI.** Strict mode turns silent tests-pass-but-don't-actually-run failures into errors — agents are notorious for renaming markers or fixtures and getting "passed" results. Sub-test support (new in 9.0) lets agents emit table-driven tests cleanly.

**URL.** https://docs.pytest.org/en/stable/changelog.html · https://lwn.net/Articles/1045923/ (pytest 9.0 release coverage) · pytest-cov: https://pytest-cov.readthedocs.io/

**When-to.** Every Python project; required for any AI-agent test loop.

**When-NOT.** Don't add pytest to a tiny one-shot script — `python -m unittest` is fine. Don't lower strictness "just to make the agent green"; that defeats the floor.

**Snippet.**
```toml
[tool.pytest.ini_options]
minversion = "9.0"
addopts = "-ra --strict-markers --strict-config --tb=short --cov=src --cov-branch --cov-fail-under=85"
testpaths = ["tests"]
xfail_strict = true
filterwarnings = ["error"]
strict_parametrization_ids = true
```

---

## M05 — `test-property-based-hypothesis`  (test-)

**Rule.** For any pure function or stateful machine where AI generates the implementation, add at least one Hypothesis property test alongside example tests. Use `@given`, `st.from_type` for typed inputs, and `.example()` only in REPL. For state machines, use `RuleBasedStateMachine`. Hypothesis 6.152+ as of April 2026.

**Why for AI.** Example tests are easy for an agent to overfit ("hardcode the constant the test expects"). Properties — round-trip, idempotency, monotonicity, invariance — force the implementation to actually generalize. Hypothesis shrinks failures into minimal repros the agent can fix.

**URL.** https://hypothesis.readthedocs.io/ · https://hypothesis.works/ · https://github.com/HypothesisWorks/hypothesis · 2026 stateful/metamorphic guide: https://www.marktechpost.com/2026/04/18/a-coding-guide-for-property-based-testing-using-hypothesis-with-stateful-differential-and-metamorphic-test-design/

**When-to.** Parsers, serializers, math, sort/search, schedulers, anything with algebraic invariants. Differential testing of "agent rewrote function, must match old behavior".

**When-NOT.** Pure I/O glue, framework wiring, throwaway notebooks — no useful properties to express, just noise.

**Snippet.**
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)

@given(st.text())
def test_roundtrip(s):
    assert decode(encode(s)) == s
```

---

## M06 — `test-mutmut-as-test-quality-gate`  (test-)

**Rule.** Once a module has ≥85% line coverage, run `mutmut` against it and require ≥80% mutants killed. Investigate every survivor — surviving mutants point at tests that pass without exercising the code. Use `cosmic-ray` for distributed/CI mutation runs on larger codebases.

**Why for AI.** Coverage is gameable — agents write tests that import a function and assert nothing meaningful, hitting 100% line coverage with zero behavioral checks. Mutation testing is the empirical answer to "does the test actually catch a bug?" Per 2026 benchmarks, mutmut hits 88.5% detection rate at ~1,200 mutants/min (AST-based, no JVM).

**URL.** mutmut: https://github.com/boxed/mutmut · cosmic-ray: https://github.com/sixty-north/cosmic-ray · 2026 comparison: https://reu.techconf.org/document/01-Publications/An_Analysis_and_Comparison_of_Mutation_Testing_Tools_for_Python.pdf

**When-to.** Critical-path business logic, anything safety/financial/security related. Run nightly on a subset, full sweep weekly.

**When-NOT.** Don't run mutation on every PR (too slow). Don't bother on glue/IO modules where mutants don't translate to bugs.

**Snippet.**
```toml
# pyproject.toml
[tool.mutmut]
paths_to_mutate = "src/"
runner = "uv run pytest -x -q"
tests_dir = "tests/"
```
```bash
uv tool run mutmut run
uv tool run mutmut results
```

---

## M07 — `sec-three-pronged-scanner-stack`  (sec-)

**Rule.** Run three security scanners in pre-commit + CI: **bandit** (code SAST — hardcoded creds, weak crypto, SQL injection patterns), **pip-audit** (deps vs PyPA Advisory DB — official PyPA tool), **safety** (deps vs Safety DB — broader CVE coverage). pip-audit and safety overlap; running both catches advisories that arrive in only one DB.

**Why for AI.** Agents pull dependencies aggressively to "solve" tasks (`uv add some-helper`) and sometimes generate insecure patterns (eval, shell=True, hardcoded tokens). Three scanners = three nets. Bandit's AST-level detection catches the agent's bad patterns; pip-audit + safety catch the bad packages it added.

**URL.** bandit: https://github.com/PyCQA/bandit · pip-audit: https://pypi.org/project/pip-audit/ · safety: https://pyup.io/safety/ · 2026 overview: https://www.helpnetsecurity.com/2026/01/21/bandit-open-source-tool-find-security-issues-python-code/

**When-to.** Every project, even internal tools. Wire into pre-commit + GitHub Actions; fail on HIGH severity.

**When-NOT.** Don't replace SCA with bandit (it's SAST only) or vice versa. Don't suppress findings without writing a `# nosec B101 — reason` justification.

**Snippet.**
```yaml
# .pre-commit-config.yaml (excerpt)
- repo: https://github.com/PyCQA/bandit
  rev: 1.8.0
  hooks: [{id: bandit, args: ["-c", "pyproject.toml", "-r", "src/"]}]
- repo: https://github.com/pypa/pip-audit
  rev: v2.7.3
  hooks: [{id: pip-audit, args: ["--strict"]}]
```

---

## M08 — `test-tdd-guard-claude-code`  (test-)

**Rule.** When Claude Code edits Python in a project that uses pytest, install **tdd-guard** as a Claude Code plugin. It hooks file-modification tools, captures pytest reporter output, and **blocks** commits that violate red-green-refactor (writing impl before failing test, over-implementing, batching multiple tests). Setup: `/plugin marketplace add nizos/tdd-guard && /plugin install tdd-guard@tdd-guard && /tdd-guard:setup`.

**Why for AI.** AI agents skip the Red phase by default — they pattern-match a known impl, write the test to match, and call it done. tdd-guard makes the harness enforce discipline the model won't enforce on itself. The pytest reporter feeds outcomes back to the guard for AST-level validation.

**URL.** https://github.com/nizos/tdd-guard · HN launch: https://news.ycombinator.com/item?id=44962913 · https://claudelog.com/claude-code-mcps/tdd-guard/

**When-to.** Any agent-driven feature dev where you actually want TDD. Especially valuable in green-field code where the agent has wide latitude to over-build.

**When-NOT.** Refactor-only sessions (no behavior change → no new test needed). Spike/throwaway code. When the project's test conventions are non-pytest.

**Snippet.**
```bash
# inside Claude Code session in your repo
/plugin marketplace add nizos/tdd-guard
/plugin install tdd-guard@tdd-guard
/tdd-guard:setup     # configures pytest reporter
# from now on, any Edit/Write that violates TDD is blocked with explanation
```

---

## M09 — `test-pytest-watcher-agent-loop`  (test-)

**Rule.** Run `pytest-watcher` (NOT the unmaintained `pytest-watch`) in a tmux pane next to the agent. Each Edit triggers re-run; agent (or human) reads the output without context-switching. For AI-only loops, pipe `pytest --tb=line -q` results back to the agent every cycle and stop iteration on first non-flaky failure.

**Why for AI.** Tight inner-loop feedback is the highest-leverage pattern in agentic dev (per Owain Lewis's 2026 "10x skill" post). Without it, the agent guesses; with it, the agent self-corrects. <500 ms test-cycle time = agent can run the loop dozens of times per minute.

**URL.** https://pypi.org/project/pytest-watcher/ · https://newsletter.owainlewis.com/p/the-10x-skill-for-ai-engineers-in · agent-test strategy: https://dagster.io/blog/pytest-for-agent-generated-code-concrete-testing-strategies-to-put-into-practice

**When-to.** Active dev sessions; TDD; bug-hunt loops where you want the agent to bisect.

**When-NOT.** CI/cron. Long-running integration suites (use markers and run a fast subset in the watcher).

**Snippet.**
```bash
uv tool run pytest-watcher . --runner "uv run pytest -x -q --tb=line"
# in another pane: claude / aider / cursor — each save retests in <1s
```

---

## M10 — `lint-pre-commit-orchestrator`  (lint-)

**Rule.** Every Python repo ships `.pre-commit-config.yaml` with: `ruff-check --fix` BEFORE `ruff-format` (fix can introduce changes the formatter must touch), then type-checker (ty/mypy/pyright), then bandit + pip-audit. Use `additional_dependencies` for type stubs. `pre-commit autoupdate` quarterly. **Never** bypass with `--no-verify`; if a hook fails, fix the root cause.

**Why for AI.** Pre-commit is the contract between agent and repo. The agent CAN run `git commit --no-verify` if you let it — most agent rule sets explicitly forbid this for that reason. With hooks enforced, the agent's commit either lands clean or it doesn't land at all.

**URL.** https://pre-commit.com/ · ruff hook: https://github.com/astral-sh/ruff-pre-commit · mypy mirror: https://github.com/pre-commit/mirrors-mypy · 2026 guide: https://gatlenculp.medium.com/effortless-code-quality-the-ultimate-pre-commit-hooks-guide-for-2025-57ca501d9835

**When-to.** Every repo. Run via `pre-commit run --all-files` in CI to mirror local checks.

**When-NOT.** Don't put slow tests in pre-commit (use `pre-push` or CI). Don't run mypy on full repo per-commit on huge codebases — scope to changed files.

**Snippet.**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.11
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/astral-sh/ty-pre-commit
    rev: 0.0.1a17
    hooks: [{id: ty}]
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.0
    hooks: [{id: bandit, args: ["-r", "src/"]}]
```

---

## M11 — `lang-pyproject-single-source`  (lang-)

**Rule.** All config lives in `pyproject.toml`: `[build-system]`, `[project]` (PEP 621), `[tool.uv]`, `[tool.ruff]`, `[tool.ty]` / `[tool.mypy]`, `[tool.pytest.ini_options]`, `[tool.coverage.run]`, `[tool.bandit]`, `[tool.mutmut]`. No `setup.py`, no `setup.cfg`, no `tox.ini` (use `nox` or `tox` configured inside pyproject), no `requirements*.txt` (use uv lockfile). Single file = single source of truth for both humans and agents.

**Why for AI.** Agents reason about config better when there's one file to read. Multi-file config (setup.cfg + tox.ini + .flake8 + requirements.txt) means the agent has to discover and stitch — common failure mode is the agent edits one and forgets the other, producing inconsistent state.

**URL.** PEP 621: https://peps.python.org/pep-0621/ · spec: https://packaging.python.org/en/latest/specifications/pyproject-toml/ · 2026 guide: https://www.hrekov.com/blog/pyproject-toml-guide

**When-to.** Every new project. Migrate legacy projects opportunistically; setuptools and hatchling both fully support pyproject-only.

**When-NOT.** A package with truly exotic build needs (custom C extensions, cython hooks) may still need `setup.py` for build-time logic — keep it minimal and put metadata in `[project]`.

**Snippet.**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-pkg"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115", "pydantic>=2.9"]

[project.optional-dependencies]
dev = ["pytest>=9.0", "ruff>=0.15", "ty", "hypothesis", "mutmut", "pytest-cov"]

[tool.uv]
dev-dependencies = ["pytest-watcher", "bandit", "pip-audit"]
```

---

## M12 — `test-pact-consumer-driven-contracts`  (test-)

**Rule.** For any service-to-service boundary in a Python microservice, write **consumer-driven contracts** with `pact-python`. Consumer side records expected interactions in `pytest` fixtures; provider side replays the contract via `verifier.verify_pacts()`. Pact 5.x (April 2026) ships a Rust FFI core, so feature parity with JS/Java/Go is real.

**Why for AI.** Agents implementing a provider can't easily know what consumers expect — contracts make that explicit, machine-readable, and testable in isolation. Stops the classic agent failure of "I changed the response shape, the unit tests pass, prod blows up because consumer X relied on a field I removed".

**URL.** https://github.com/pact-foundation/pact-python · https://docs.pact.io/implementation_guides/python/readme · consumer test guide: https://docs.pact.io/implementation_guides/python/docs/consumer

**When-to.** ≥2 services owned by ≥2 teams (or ≥2 agents). Replace fragile end-to-end stack tests at the service boundary.

**When-NOT.** Single-service monolith — overkill, just unit + integration. Public APIs with unknown consumers — use OpenAPI + schemathesis instead.

**Snippet.**
```python
# tests/contracts/test_user_consumer.py
from pact import Consumer, Provider

pact = Consumer("WebApp").has_pact_with(Provider("UserService"))

def test_get_user(pact):
    pact.given("user 42 exists") \
        .upon_receiving("a request for user 42") \
        .with_request("GET", "/users/42") \
        .will_respond_with(200, body={"id": 42, "name": "Ada"})
    with pact:
        assert client.get_user(42).name == "Ada"
```

---

## M13 — `test-pytest-bdd-living-spec`  (test-)

**Rule.** When SDD specs live in Gherkin (.feature files) — common in `.aidocs/` SDD lifecycles — bind them to executable tests with `pytest-bdd`. Each `Given/When/Then` step is a pytest fixture/function; the `.feature` file IS the spec, the test, and the documentation simultaneously. Run inside the same pytest session as unit tests for one report.

**Why for AI.** A Gherkin spec is a dense, structured prompt. Agents read it, generate impl, re-run pytest-bdd, get pass/fail keyed to specific scenarios. Far more legible to both humans and LLMs than free-form acceptance criteria.

**URL.** https://pytest-bdd.readthedocs.io/ · https://github.com/pytest-dev/pytest-bdd

**When-to.** Feature work with non-trivial business logic and multiple stakeholders (PM/QA/dev). SDD-style workflows where spec.md → test-plan.md → implementation lives as a chain.

**When-NOT.** Pure libraries. Internal infra. Anything where Gherkin overhead exceeds the value of the shared vocabulary.

**Snippet.**
```gherkin
# tests/features/checkout.feature
Scenario: cart with 3 items applies bulk discount
  Given a cart with 3 items at $10 each
  When the user checks out
  Then the total is $27 (10% bulk discount)
```
```python
# tests/test_checkout.py
from pytest_bdd import scenarios, given, when, then
scenarios("features/checkout.feature")
```

---

## M14 — `lang-codex-astral-stack-integration`  (lang-)

**Rule.** As of April 2026, OpenAI ships Codex with uv/ruff/ty bundled (post-Astral acquisition March 2026). Treat the Astral toolchain as the **default contract** between AI coding agents and Python repos: the agent assumes uv-managed env, ruff-clean code, ty-typed code. Provide an `AGENTS.md` at repo root telling the agent which Python version, which extras, which test command.

**Why for AI.** Convergence is real. Codex, Claude Code, and aider all preferentially invoke ruff + uv when present. A ruff-clean, uv-locked, ty-typed repo is "agent-native" — the agent's failure rate measurably drops because its tools agree with the repo's tools.

**URL.** OpenAI/Astral acquisition: https://blog.jetbrains.com/pycharm/2026/03/openai-acquires-astral-what-it-means-for-pycharm-users/ · https://creati.ai/ai-news/2026-03-21/openai-acquires-astral-python-developer-tools-codex-integration-2026/ · AGENTS.md spec: https://agents.md/

**When-to.** Any repo where ≥1 AI agent will touch code regularly. Standardize across the org so agents get consistent affordances.

**When-NOT.** Repo locked to legacy stack (e.g., Python 2.7, internal pip mirror only) — pick the closest viable subset.

**Snippet.**
```markdown
# AGENTS.md (repo root)
## Stack
- Python 3.12 via uv (uv.lock committed)
- Lint/format: ruff
- Types: ty (--strict)
- Test: pytest 9 + hypothesis, run via `uv run pytest`
## Required before commit
1. `uv run ruff check --fix && uv run ruff format`
2. `uv run ty check src/`
3. `uv run pytest -x`
4. `pre-commit run --all-files`
Never use `git commit --no-verify`.
```

---

## Summary

Python's 2026 SDLC floor is the Astral-Meta stack: ruff (lint/format <10ms/file), uv (env/deps), ty or pyrefly (type checking 10–60x faster than mypy), pytest 9 + hypothesis + mutmut for behavioral correctness, bandit + pip-audit + safety for security — all wired through pre-commit and a single `pyproject.toml`. AI integration sits on top: tdd-guard enforces red-green-refactor against Claude Code's edits, pytest-watcher closes the inner loop in sub-second time, AGENTS.md + Codex/Astral convergence makes repos "agent-native". The pattern is: deterministic floor must be FAST, because every AI iteration pays for it; if a check is slow, the agent will skip it or you will.

Sources:
- [Ruff docs](https://docs.astral.sh/ruff/) · [GitHub](https://github.com/astral-sh/ruff)
- [uv docs](https://docs.astral.sh/uv/) · [GitHub](https://github.com/astral-sh/uv)
- [ty docs](https://docs.astral.sh/ty/) · [ty beta announcement](https://astral.sh/blog/ty)
- [Pyrefly](https://pyrefly.org/) · [Meta engineering blog](https://engineering.fb.com/2025/05/15/developer-tools/introducing-pyrefly-a-new-type-checker-and-ide-experience-for-python/)
- [pytest changelog](https://docs.pytest.org/en/stable/changelog.html) · [pytest 9.0 release](https://lwn.net/Articles/1045923/)
- [Hypothesis](https://hypothesis.readthedocs.io/) · [hypothesis.works](https://hypothesis.works/)
- [mutmut](https://github.com/boxed/mutmut) · [cosmic-ray](https://github.com/sixty-north/cosmic-ray)
- [bandit](https://github.com/PyCQA/bandit) · [pip-audit](https://pypi.org/project/pip-audit/)
- [tdd-guard](https://github.com/nizos/tdd-guard)
- [pytest-watcher](https://pypi.org/project/pytest-watcher/) · [agent feedback loops](https://newsletter.owainlewis.com/p/the-10x-skill-for-ai-engineers-in)
- [pre-commit](https://pre-commit.com/) · [ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit)
- [PEP 621](https://peps.python.org/pep-0621/) · [pyproject.toml spec](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- [pact-python](https://github.com/pact-foundation/pact-python) · [pytest-bdd](https://pytest-bdd.readthedocs.io/)
- [OpenAI acquires Astral (PyCharm blog)](https://blog.jetbrains.com/pycharm/2026/03/openai-acquires-astral-what-it-means-for-pycharm-users/)
- [Dagster: pytest for agent code](https://dagster.io/blog/pytest-for-agent-generated-code-concrete-testing-strategies-to-put-into-practice)

Two-line summary: 14 Python SDLC methodologies covering deterministic floor (ruff, uv, ty/pyrefly/mypy, pytest 9, hypothesis, mutmut, bandit/pip-audit/safety, pre-commit, pyproject.toml, pact-python, pytest-bdd) and AI-agent integration layer (tdd-guard for Claude Code, pytest-watcher loops, Codex+Astral convergence). Tagged across `lang-`, `lint-`, `test-`, `sec-`; key 2026 inflection: Astral acquired by OpenAI, ty/pyrefly displacing mypy, sub-10ms feedback making agentic loops viable.
