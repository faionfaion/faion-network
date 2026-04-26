# uv as the Python Lockfile Floor

## Summary

Standardize every Python project on Astral's `uv` for environment management, dependency resolution, lockfile, and Python version installation. The committed `uv.lock` is the single source of truth for reproducible installs; AI coding agents must invoke commands through `uv run <cmd>` (never bare `pytest` / `python`) so the right virtualenv and the right Python version are guaranteed for every tool call.

## Why

Pre-each-command lockfile re-verification (`uv sync` / `uv run`) closes the silent-drift gap that `pip install -r requirements.txt` leaves open: an agent cannot mutate the env without uv noticing on the next call. uv is implemented in Rust and resolves ~10x faster than pip-tools or Poetry, so the cost of "always sync before run" is small enough to keep an agentic inner loop viable. After OpenAI's March 2026 acquisition of Astral, Codex bundles uv natively — the de facto Python contract between coding agents and repos in 2026.

## When To Use

- Every new Python project (Python 3.10+).
- Migrating Poetry / pip-tools / requirements.txt projects when the team can switch lockfile formats.
- Multi-Python-version repos (uv installs and pins interpreter versions per project).
- Any repo where AI agents will run `pytest`, type-checkers, or scripts.

## When NOT To Use

- Conda / scientific stacks needing CUDA, GDAL, or other binary deps from conda-forge — `pixi` handles that subset better.
- Repos pinned to legacy Python (2.7) or to a private registry that uv's resolver does not understand.
- Single-file scripts where a venv is more ceremony than the script is worth.
- Projects that must keep `requirements.txt` for an external consumer (pull request agents, security scanners) until those consumers learn `uv.lock`.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | The lockfile-floor rule, why bare `pytest` is forbidden, and what `uv run` guarantees. |
| `content/02-workflow.xml` | The init/add/sync/lock/run command set; `uv tool install` for global tools; `--frozen` in CI. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | Minimal PEP-621 project skeleton wired up for uv with dev-dep group. |
| `templates/agents-md-snippet.md` | Drop-in `AGENTS.md` block telling agents to use `uv run` and never edit `uv.lock` by hand. |
