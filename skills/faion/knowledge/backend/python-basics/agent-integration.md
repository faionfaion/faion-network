# Agent Integration — Python Basics

## When to use
- Onboarding a new developer (or new agent persona) that needs Python fundamentals before tackling framework work.
- Code review where the issue is fundamentals (mutable defaults, EAFP vs LBYL, dict iteration, dataclass abuse) rather than framework-specific.
- Bootstrapping a fresh repo: `pyproject.toml` shape, `uv` commands, `ruff` config, basic module layout.
- Refactoring legacy 3.7/3.8 code to 3.12+ idioms: `list[int]` instead of `List[int]`, `X | Y` instead of `Union`, walrus, structural pattern matching, `match`/`case`.
- Generating beginner-grade examples or tutorial content where idiomatic Python matters more than performance.

## When NOT to use
- Inside a domain-specific feature (Django model, FastAPI route, ML model) — load the domain methodology, this overview is too generic.
- Performance optimization — covered briefly here; route to `python-overview/` or specialized tooling.
- Type-system depth (generics, ParamSpec, Protocol) — route to `python-typing/`.
- Async patterns — route to `python-async/`.
- Testing strategies — route to a pytest methodology.

## Where it fails / limitations
- README's "Pythonic (EAFP) vs LBYL" example uses `data["key"]` — but `dict.get(key, default)` is the actually idiomatic option for that exact case. Agents will write try/except where `.get()` is cleaner.
- "Walrus Operator" example doesn't warn that walrus inside comprehensions is allowed but reduces readability. Agents over-use it.
- Pattern matching example only covers list patterns; doesn't show class patterns, OR-patterns, or guard clauses — agents stay at the toy level.
- "Prefer keyword-only arguments" is correct but not always — agents make every parameter `*,` which breaks ergonomic APIs.
- "Use `__slots__` for memory optimization" — true but with caveats (no `__dict__`, no multiple-inheritance with non-slot bases, breaks `weakref` unless you add `__weakref__`). Agents apply blindly.
- "Use `@dataclass` for data containers" — agents reach for dataclass for everything, including cases where Pydantic, NamedTuple, or `attrs` would be better.
- `pyproject.toml` example uses `ruff line-length = 88` (Black's default) but the project AGENTS.md uses 100; agents will fight this drift.
- README mentions `uv add --dev pytest ruff mypy` then later shows `pyenv` and `poetry`; agents pick a different tool per file. Lock one stack per repo.
- "Modern Python (3.9+): Use `list[int]` instead of `typing.List[int]`" — agents will rewrite type stubs in libraries that must support 3.8 and break them.
- No mention of `enum` (StrEnum/IntEnum), `functools.cache`, `itertools.batched` (3.12+), `pathlib.Path.is_relative_to`, or `tomllib` — gaps agents fill from outdated training data.

## Agentic workflow
Use this methodology as a **style/idiom check** in code review and as a **bootstrap reference** at project start. Don't load it inside feature tasks. A reviewer subagent reads diffs and flags non-idiomatic patterns: mutable default args, raw `try: dict[k] except KeyError: ...` where `.get()` works, `from typing import List` in 3.10+ code, raw enum tuples instead of `StrEnum`, classes with two methods that should be functions. The bootstrap subagent generates `pyproject.toml`, `ruff` config, `mypy` config, and a starter test from a single template.

### Recommended subagents
- `python-style-reviewer` (sonnet) — read diff, flag non-idiomatic patterns; do NOT modify code.
- `python-bootstrap` (haiku) — emit `pyproject.toml`, `.python-version`, basic layout.
- `/faion` (sdd-batch-orchestrator workflow) — sequential gate; the basics methodology contributes the lint/format step.
- `password-scrubber-agent` — sweep before commit.

### Prompt pattern
```
Style review of this diff. Reference: skills/.../python-basics/README.md.
Flag (line, snippet, rule). Rules to apply:
- mutable default args
- `try: d[k] except KeyError` where `d.get(k, default)` works
- `typing.List/Dict/Optional/Union` in py>=3.10 code
- enum-by-tuple instead of StrEnum/IntEnum
- bare `except:` without exception type
- pattern-matchable if/elif chains over a single value
Output a numbered list. Do not edit files.
```

```
Bootstrap a Python 3.12 project named <name>. Use uv only.
Files to emit: pyproject.toml (with ruff line-length 100, mypy strict, pytest config),
.python-version (3.12), src/__init__.py, tests/test_smoke.py.
After: run `uv sync && uv run ruff check && uv run mypy src && uv run pytest`.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `uv` | Project + dep + Python version manager | https://docs.astral.sh/uv/ |
| `ruff` | Lint + format | https://docs.astral.sh/ruff/ |
| `mypy` / `pyright` | Type checking | https://mypy.readthedocs.io/ , https://github.com/microsoft/pyright |
| `pytest` (+ `pytest-cov`) | Testing | https://docs.pytest.org/ |
| `pyenv` | Python version manager (without uv) | https://github.com/pyenv/pyenv |
| `poetry` | Alternative dep manager | https://python-poetry.org/docs/ |
| `python -m venv` | Stdlib virtualenv | https://docs.python.org/3/library/venv.html |
| `python -m unittest` | Stdlib test runner (rarely preferred) | https://docs.python.org/3/library/unittest.html |
| `python -m timeit` / `cProfile` / `line_profiler` | Profile snippets | https://docs.python.org/3/library/timeit.html |
| `pre-commit` | Git hook framework | https://pre-commit.com/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PyPI | OSS | Yes | Default index. |
| Astral (uv, ruff) | OSS | Yes | Single org; consistent tooling. |
| Read the Docs | SaaS | Yes | Docs hosting. |
| GitHub Actions / GitLab CI | SaaS | Yes | `astral-sh/setup-uv` and `actions/setup-python`. |
| Codecov / Coveralls | SaaS | Yes | Coverage reports. |
| pre-commit.ci | SaaS | Yes | Free for public repos. |

## Templates & scripts
Minimal modern Python project bootstrap:

```bash
#!/usr/bin/env bash
# scripts/bootstrap-py-basics.sh PROJECT
set -euo pipefail
P=${1:?project name}
uv init "$P" --python 3.12
cd "$P"
uv add --dev ruff mypy pytest pytest-cov pre-commit
cat >> pyproject.toml <<'TOML'
[tool.ruff]
line-length = 100
target-version = "py312"
[tool.ruff.lint]
select = ["E","F","I","B","UP","SIM","T20","PT"]
[tool.mypy]
python_version = "3.12"
strict = true
[tool.pytest.ini_options]
addopts = "-q --strict-markers --strict-config"
TOML
mkdir -p src tests
echo 'def hello(name: str) -> str: return f"hello, {name}"' > src/__init__.py
echo 'from src import hello\n\ndef test_hello() -> None: assert hello("a") == "hello, a"' > tests/test_smoke.py
uv run ruff check . && uv run mypy src && uv run pytest -q
```

## Best practices
- Pin Python floor in `pyproject.toml` (`requires-python = ">=3.12"`) AND `.python-version`.
- One package manager per repo. If the repo started on `poetry`, agents must not switch to `uv` mid-feature.
- Use `ruff` for both lint and format; remove `black` and `isort`.
- Default to `pathlib.Path` over `os.path`; agents pattern-match the older API from training data.
- Use `dict.get(k, default)` over try/except KeyError for the simple case.
- Prefer `match`/`case` over `if x == "a": ... elif x == "b": ...` chains over a single value.
- Use `StrEnum`/`IntEnum` for closed sets, not raw tuples.
- Type-hint public functions; let internals stay loose if it speeds iteration.
- Write tests with `pytest` (not `unittest`) unless the project predates it.

## AI-agent gotchas
- Mutable default args (`def f(x=[]):`) — agents pattern-match Java/JS habits. Forbid in lint (`B006`).
- Bare `except:` clauses swallow `KeyboardInterrupt`/`SystemExit`. Force `except Exception:` minimum.
- Agents use `from typing import List, Dict, Optional, Union` in Python 3.10+ code. Use `list`, `dict`, `X | None`, `X | Y`.
- Agents reach for `dataclass` even where `NamedTuple` (immutable) or `Pydantic` (validated) is correct.
- Agents apply `__slots__` to all classes "for performance" without measuring; breaks subclasses and pickling.
- Agents replace `requirements.txt` with `pyproject.toml` without adjusting CI/Docker.
- Agents use `os.path.join`/`open(str_path)` instead of `pathlib.Path` despite the README example.
- Agents forget `encoding="utf-8"` on `open()` and break on non-UTF-8 systems.
- Agents enable `ruff` rule sets too aggressively (e.g., `ALL`) and waste a session fighting false positives.
- Agents write `print()` debug statements in production code; `T20` ruff rule should block them.
- Human-in-loop checkpoint: any change to `pyproject.toml [project]`, lockfile, or CI tooling.

## References
- https://docs.python.org/3/tutorial/index.html
- https://peps.python.org/pep-0008/
- https://peps.python.org/pep-0020/
- https://peps.python.org/pep-0636/
- https://docs.astral.sh/uv/
- https://docs.astral.sh/ruff/
- https://realpython.com/tutorials/best-practices/
- https://www.stuartellis.name/articles/python-modern-practices/
