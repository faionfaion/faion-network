<!-- purpose: Markdown snippet enforcing `uv run` for all Python tool calls in AGENTS.md. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-1200 tokens when loaded as context -->

# AGENTS.md — Python / uv block (drop-in)

## Stack

- Python managed by `uv` (uv.lock committed).
- Python version pinned in `pyproject.toml` `requires-python`.

## Rules for agents

1. Run all project commands through `uv run <cmd>`. Bare `python` / `pytest` / `mypy` is forbidden.
2. Add deps via `uv add <pkg>` (runtime) or `uv add --dev <pkg>` (dev). Never edit `uv.lock` by hand.
3. Bump versions via `uv lock --upgrade-package <name>`; never delete and recreate `uv.lock`.
4. Install global tools (ruff, ty, mutmut, pre-commit) via `uv tool install <name>`, not into the project env.
5. CI installs with `uv sync --frozen --all-extras`. If that fails, fix `pyproject.toml` and re-lock locally before re-pushing.
