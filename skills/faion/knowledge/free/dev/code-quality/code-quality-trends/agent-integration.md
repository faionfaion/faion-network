# Agent Integration — Code Quality Trends 2026

## When to use
- Setting up a new repo: agent generates lint/format/test/coverage configs aligned with current standards (TS strict, ruff/mypy strict, ESLint flat config, Lighthouse budget).
- Quarterly tech-debt audit: agent compares repo against the 2026 quality checklist; emits gap report with prioritized actions.
- Onboarding a stack the team hasn't used in 18+ months — agent surfaces what changed (React 19 RSC, Next 15 App Router, TS 5 features, Python 3.13 perf).
- Picking AI tooling per workflow: routing daily coding to Copilot, large refactors to Claude Code, flow-state to Cursor.
- Defining performance budgets and CI gates from the benchmarks table.

## When NOT to use
- Critical decisions that need human judgment about team skill, hiring, vendor lock-in. The trends doc is descriptive, not normative.
- Late-stage products where stack switch is prohibitively expensive — knowing TS adoption is 78% doesn't justify migrating Ruby.
- Niche stacks (Elixir, Clojure, Zig) — the trend doc is mainstream-biased.
- Real-time decisions during incidents — performance benchmarks are aspirational, not SLO replacements.

## Where it fails / limitations
- Trends data ages fast. The `2026-01-23` timestamp on the source means recommendations are <6mo old by mid-year and start drifting. Treat as snapshot, refresh quarterly.
- Statistics ("81% use AI tools") are headline-fragile and rarely audited. Don't cite as evidence to stakeholders without primary source.
- Tool routing table is opinionated; mileage varies wildly by codebase size, language, latency tolerance.
- The "Quality Checklist" mixes universal items (no `any`) with stack-specific ones (Server Components) — agent applying blindly produces nonsense lint configs.
- "Coverage >80%" without distinguishing line/branch/mutation is misleading; agent will check the easy metric.
- Performance benchmarks (FCP <1.8s) ignore p99/geography; agent flags green sites that fail in slow markets.

## Agentic workflow
Use as a configuration generator + audit checklist, not a knowledge oracle. On a new repo: a `setup` agent reads `package.json`/`pyproject.toml`, infers stack, applies the matched checklist row, generates configs (eslint.config.js, ruff.toml, tsconfig.json strict, pre-commit hooks, GH Actions workflow). On an existing repo: an `audit` agent runs the checklist, scores compliance, produces a prioritized gap list. Re-run audit quarterly via cron and diff scores. Always validate generated configs by running them — agent generates plausible-but-broken configs at non-trivial rate.

### Recommended subagents
- `stack-detector` — reads manifest files and outputs `{language, framework, version, build-tool}`.
- `quality-config-gen` — emits language/framework-matched configs from the checklist; sonnet.
- `quality-auditor` — runs the checklist as boolean checks against the live repo, scores 0-100, lists gaps.
- `perf-budget-watch` — Lighthouse/k6 runner per release; flags regressions vs the documented benchmarks.
- `dependency-freshness` — non-LLM (`npm outdated`, `pip list --outdated`) + agent triage of breaking-change risks.
- `faion-improver` (skill) — wraps the audit→fix loop as a session.

### Prompt pattern
Stack audit:
```
Audit this repo against the 2026 Code Quality Checklist for stack=<detected>.
Output JSON array of {item, status:"pass|fail|na", evidence, fix_command_if_fail}.
Cap items at 30; pick the highest-leverage from the matched stack list.
Do not invent configs that don't exist; if a tool isn't installed, mark "fail" and propose installation.
```

Config generation:
```
Generate <eslint.config.js | ruff.toml | tsconfig.json | .pre-commit-config.yaml> for:
stack=<...>, package_manager=<...>, target_node_or_python=<...>.
Strict mode on. No deprecated rules. Reference the 2026 Code Quality Checklist for required items.
Do not include rules that conflict with the project's existing Prettier/Black config.
After emitting, output a one-line command to validate the config.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` | Python lint + format (replaces black, isort, flake8) | `pip install ruff` |
| `mypy --strict` | Python static types | `pip install mypy` |
| `eslint` (flat config) | JS/TS lint | `npm i -D eslint` |
| `prettier` | JS/TS/CSS/MD format | `npm i -D prettier` |
| `tsc --noEmit` | TypeScript type-check in CI | tsc |
| `pytest --cov` | Python coverage | `pip install pytest-cov` |
| `vitest run --coverage` | JS/TS coverage | `npm i -D vitest` |
| `lighthouse-ci` | Lighthouse score gate in CI | `npm i -g @lhci/cli` |
| `k6` / `wrk` | Load testing for backend benchmarks | https://k6.io |
| `axe-core` | a11y check matching the React-checklist row | `npm i -g @axe-core/cli` |
| `npm-check-updates` / `pip-tools` | Dependency freshness | `npm i -g npm-check-updates` |
| `semgrep` | Rule-based security scan | `pip install semgrep` |
| `gitleaks` / `trufflehog` | Secret scan | github releases |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Copilot | SaaS | IDE-native | "Daily coding" lane in the routing table. |
| Cursor / Windsurf | SaaS | Yes | "Flow-state" lane. |
| Claude Code | SaaS | Yes — primary | "Large refactor / test gen / review" lane. |
| Snyk / GitHub Advanced Security | SaaS | Yes — APIs | Dependency + SAST. |
| Renovate / Dependabot | SaaS/OSS | Yes — config-driven | Autonomous dep updates. |
| Sentry | SaaS | Yes — APIs | Backs the "<0.1% error rate" benchmark. |
| Datadog / Grafana Cloud | SaaS | Yes — APIs | p95 API latency monitoring. |
| Codecov / Coveralls | SaaS | Yes | Coverage gates. |
| Sonar / SonarCloud | SaaS/OSS | Yes — issues API | Maintainability rating. |
| Lighthouse CI Server | OSS | Yes — REST | Self-hosted perf history. |

## Templates & scripts
See `templates.md` (sibling files in this dir) and the trend doc's checklists. Tier-detection one-liner:

```bash
#!/usr/bin/env bash
# detect-stack.sh — coarse stack classifier for the audit agent
set -euo pipefail
[ -f package.json ]       && jq -r '.engines.node // "node?"' package.json   > /dev/null
[ -f pyproject.toml ]     && grep -m1 'requires-python' pyproject.toml      || true
[ -f tsconfig.json ]      && echo "lang:ts" || ([ -f package.json ] && echo "lang:js")
[ -f pyproject.toml ] || [ -f requirements.txt ] && echo "lang:py"
[ -f next.config.* ]      && echo "fw:next"
[ -f remix.config.* ]     && echo "fw:remix"
[ -f svelte.config.* ]    && echo "fw:svelte"
[ -f manage.py ]          && echo "fw:django"
grep -ql '"react"' package.json 2>/dev/null && echo "lib:react"
```

## Best practices
- Use the trends doc as a checklist generator, not a source of truth. Cite primary sources (TC39, PEP, framework changelogs) in actual ADRs.
- Pin tool versions in CI; "latest" creates non-reproducible audits.
- Run quality audit as a cron-scheduled agent job, store score history. Trends matter more than single-point compliance.
- Distinguish line/branch/mutation coverage in any "80%" gate. Mutation kill rate >75% is a meaningful target; line coverage is a vanity number.
- Tie performance budgets to user-impacting metrics (FCP, LCP, INP) — not bundle size in isolation.
- Always pair AI tool routing with kill-switches: every Copilot/Cursor/Claude Code change must pass the same lint/test/coverage gates as human-written.
- Refresh the trends doc itself quarterly; agent-generated configs from a stale trends doc accumulate drift.

## AI-agent gotchas
- Stale-trend hallucination: agent cites benchmarks the doc doesn't contain (older training data leaking in). Quote-only mode in prompt: "Use only the attached trend doc; do not cite from memory."
- Generated configs reference non-existent rules (`@typescript-eslint/no-unsafe-narrowing` in versions where it doesn't exist). Always run the linter once on emit; auto-revert if it errors.
- Coverage gates without test infra produce false greens — agent sets `--cov-fail-under=80` while no tests exist. Verify >0 tests before enforcing.
- "AI Tool Selection" routing: agent picks the most expensive tier for everything ("opus everywhere"). Add cost-per-task constraint in prompt.
- Stats parroting: agent quotes "81% of teams use AI" to justify decisions. Filter statistical claims out of decision contexts.
- Performance benchmarks are global; agent flags regional regressions invisible without geo-distributed testing. Add explicit geography to the budget.
- Security checklist items ("CSRF tokens", "input validation") agent treats as binary; the real check needs threat modeling, not a tickbox. Pair with `security-review` skill.
- Documentation checklist: agent generates `README.md` and `ARCHITECTURE.md` that look polished but are wrong. Force "cite a file:line for every claim" rule.

## References
- React 19 release notes — https://react.dev/blog/2024/12/05/react-19
- Python 3.13 What's New — https://docs.python.org/3/whatsnew/3.13.html
- TypeScript 5 release docs — https://www.typescriptlang.org/docs/handbook/release-notes
- Next.js 15 — https://nextjs.org/blog/next-15
- Lighthouse CI — https://github.com/GoogleChrome/lighthouse-ci
- Stack Overflow Developer Survey 2024/2025 (audit before quoting stats)
- Anthropic — Claude Code Best Practices
