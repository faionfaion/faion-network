# Ruff for Python and Biome for JS/TS as the Sole Linter+Formatter

## Summary

For new Python projects, `ruff` is the SOLE linter and formatter — it replaces black, flake8, isort, pyupgrade, autoflake and pydocstyle, ships 900+ rules, and runs 10–100x faster than the previous Python toolchain. For new JavaScript/TypeScript/JSX/CSS/GraphQL projects, `biome` is the SOLE linter and formatter — it replaces ESLint and Prettier with 491 rules and a single config file. Both tools have `--fix` / `--write` flags that AI agents call after every code edit. The repository config concentrates ruff settings in `pyproject.toml` and biome settings in `biome.json`; no `.flake8`, no `.eslintrc`, no `setup.cfg`. Faion-network's backend already enforces this for ruff (see backend pre-commit hook); the same rule extends to dag and any new TypeScript package.

## Why

Both tools are single Rust binaries with no Node or Python plug-in chain — startup is sub-100ms even on cold cache, so they fit in pre-commit hooks and inside the agent's edit-test loop without slowing the inner cycle. Ruff covers 900+ rules including Django (`DJ`), bugbear (`B`), pyupgrade (`UP`), no-print (`T20`), pyflakes (`F`), pycodestyle (`E/W`), isort (`I`), simplify (`SIM`); biome v2 (Biotype, Feb 2026) added type-aware lints and multi-file project understanding and is in production at AWS, Google, Microsoft, Cloudflare, Coinbase, Discord, Slack and Vercel. Consolidating to one tool per language eliminates the "two formatters disagree" trap that produces no-op churn and confuses LLM agents during reflexion loops.

## When To Use

- Any new Python project — start with ruff in `pyproject.toml`, no other linter or formatter.
- Any new JS/TS project — start with biome in `biome.json`, no ESLint, no Prettier.
- Any agent-driven workflow where the inner loop is "edit → format → test"; both tools' speed makes the inner loop sub-second.
- Any monorepo migrating off black/flake8/isort or ESLint/Prettier — migrate one package at a time.

## When NOT To Use

- Legacy projects with deeply customized ESLint plug-ins that have no biome equivalent yet — migrate incrementally rather than mid-sprint.
- Projects that ship a public ESLint/Prettier config as a product (e.g., a shareable preset) — biome is not yet a drop-in replacement for that consumption pattern.
- One-off scripts not part of a package; running a formatter on a single ad-hoc file is overhead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-single-tool-rule.xml` | The "exactly one linter+formatter per language" rule and the agent's `--fix`/`--write` invocation contract. |
| `content/02-config-co-location.xml` | Where ruff and biome configs live (`pyproject.toml`, `biome.json`) and which legacy files to delete. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject-ruff.toml` | `[tool.ruff]` block with the rule groups faion-network enforces (E/W/F/I/B/C4/UP/SIM/DJ/T20). |
| `templates/biome.json` | Strict biome config with linter and formatter both enabled and recommended ruleset on. |
