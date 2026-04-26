# Agent Integration — Best Practices 2026

## When to use
- Quick "is my stack current?" audit — agent reads the navigation hub and the three sub-docs (`ai-assisted-dev.md`, `modern-tooling-2026.md`, `code-quality-trends.md`), compares against the project, emits gap list.
- Choosing the right modern feature inside a stack: TS 5 strict flags, React 19 server actions, Next.js 15 caching, Python 3.13 features, Pydantic v2 patterns.
- Generating an "AI-assisted dev" playbook: tool selection (Copilot / Cursor / Claude Code), prompt patterns for code, AI test generation guardrails.
- Producing the standards section of a project's CONTRIBUTING.md or AGENTS.md.

## When NOT to use
- Deep, language-specific patterns (services/views/handlers) — see sibling `dev-methodologies-practices`.
- Architecture decisions (monolith vs microservice, sync vs async) — see `dev-methodologies-architecture` and `software-architect`.
- One-shot bug-fix or feature work; load only the specific section, not the umbrella.
- Anything where the project has a more recent or stricter house standard than the 2026 baseline.

## Where it fails / limitations
- This is a **navigation hub**, not content. Agent that reads only `README.md` gets a TOC and zero substance — must follow links to the sub-docs to be useful.
- "2026" snapshot ages quickly: TypeScript 5.x, React 19, Next.js 15, Python 3.13 are 2025-Q4 reality. New majors (React 20 / Python 3.14 / TS 6) will break section claims; cross-check release notes.
- AI-coding section conflates capabilities of Copilot, Cursor, Claude Code — recommendations may not reflect current pricing/UX.
- Sub-document sizes are estimated in tokens, not lines; agents using line-budget prompts mis-allocate context.
- "Quick reference" code-quality section is brief and presents thresholds without source — agents will quote them as if authoritative.
- Decomposed-doc pattern means the agent must do two reads to answer one question, increasing tool-call count.

## Agentic workflow
Two-phase load: (1) read the hub `README.md` to pick the relevant sub-doc(s); (2) read the sub-doc(s) and apply. For audits, pre-load all three; for targeted upgrades (e.g., "modernise TypeScript config"), load only `modern-tooling-2026.md`. Always cross-reference against the actual installed versions (`package.json`, `pyproject.toml`) before applying recommendations — the doc presumes current versions.

### Recommended subagents
- `faion-improver` — natural fit: it audits a system, finds gaps, proposes upgrades; this hub is its rubric.
- `faion-sdd-executor-agent` — executes the upgrade tasks once the gap list is produced.
- `review` skill — reviews the resulting modernisation PR.

### Prompt pattern
```
Step 1 — load:
- best-practices-2026/README.md
- best-practices-2026/code-quality-trends.md
- best-practices-2026/modern-tooling-2026.md (TypeScript section only)
Step 2 — audit ./apps/web (Next.js 14, TS 5.2, eslint-config-next):
- list deviations from "TypeScript 5 Strict Configuration"
- list missing React 19 / Next.js 15 features
- propose phased upgrade plan as SDD tasks
Output: markdown report. Do not edit files yet.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npm-check-updates` (`ncu`) | Detect outdated deps in JS/TS | `npm i -g npm-check-updates` |
| `pip-audit` / `pip list --outdated` | Python dep currency | `pip install pip-audit` |
| `cargo outdated` | Rust dep currency | `cargo install cargo-outdated` |
| `bun outdated` | Bun-native | bundled with bun |
| `tsc --noEmit` + `tsconfig-strict-defaults` | Validate TS strictness | bundled |
| `ruff` (Python) / `eslint` (JS) | 2026 default linters | `pip install ruff` / `npm i -D eslint` |
| Codemod runners (`jscodeshift`, `lib-cra-codemod`) | Automated migrations (e.g., React 19) | `npx @react-codemod` |
| `bunx` / `pnpm dlx` | One-shot tool runs | bundled |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Renovate / Dependabot | SaaS / OSS | Yes | Keeps the 2026 baseline current automatically. |
| GitHub Copilot | SaaS | Yes | The "AI Coding Tool Selection" matrix slot. |
| Cursor | SaaS | Yes — Composer + agents | Currently strongest IDE-native agent UX. |
| Claude Code | SaaS | Yes — first-party | Subagents, hooks, skills (this repo). |
| SonarCloud | SaaS | Yes — REST | Track code-quality trends over time. |
| Snyk / GitHub Security | SaaS | Yes — REST | Aligns with the Security Practices section. |
| Sentry | SaaS / self-host | Yes | Performance + error budgets baseline. |
| Vercel / Cloudflare Workers | SaaS | Yes | Targets for Next.js 15 / server actions. |

## Templates & scripts
TS 5 strict baseline an agent can write to `tsconfig.base.json`:

```json
{
  "compilerOptions": {
    "target": "ES2023",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "skipLibCheck": true
  }
}
```

Python 3.13 `pyproject.toml` essentials:

```toml
[project]
requires-python = ">=3.13"
[tool.ruff]
target-version = "py313"
line-length = 100
[tool.ruff.lint]
select = ["E","F","I","B","UP","SIM","N","TCH","T20","ASYNC"]
[tool.mypy]
python_version = "3.13"
strict = true
plugins = ["pydantic.mypy"]
```

See `templates.md` for full, reusable variants.

## Best practices
- "Currentness" is a maintenance practice, not a snapshot. Schedule a quarterly review against this hub; treat it as a rubric, not a constitution.
- Adopt strict TS in new code first; convert legacy modules under `// @ts-strict-check` boundary or per-file pragmas; do not flip the global flag without budget.
- React 19 server components: don't sprinkle `'use server'` randomly; document a per-route policy (server-by-default, client-on-demand).
- Pin Python at minor (`>=3.13,<3.14`) until next LTS-equivalent stabilises; agents using `>=3.13` accept future majors and break compat.
- AI-assisted dev: require diff-review on every AI-generated change; reject anything > 200 lines unreviewed. The doc is permissive; the team must be stricter.
- For test generation by AI, run the original suite first to establish baseline; reject AI-added tests that don't fail when reverting the change (mutation-style sanity check).
- Track DORA metrics + a small "AI-effectiveness" panel (PR cycle time pre/post AI tooling) — the Best Practices hub should pay back, not just feel good.

## AI-agent gotchas
- Hub-only read: the agent confidently reports recommendations from the TOC alone. Always require both the hub and the relevant sub-doc.
- Stale "2026" claims: agent quotes "TS 5.x, React 19" as if frozen. After a Node/React major release, agent should consult release notes, not just the doc.
- Tool-recommendation drift: pricing and feature set of Copilot/Cursor/Claude Code change quickly. Rephrase agent output as "as of doc revision date" rather than absolute.
- AI test generation: agents asked to write tests for AI-generated code re-use the same model's blind spots; run an independent reviewer (different prompt or different model) on the test suite.
- Codemod application: agent runs codemods (e.g., React 19) on the entire repo unattended; failures pile up silently. Run per-package with a verification step.
- Python typing: agent mixes `typing.List` (legacy) with `list[T]` (PEP 585) in the same file; force `from __future__ import annotations` or commit fully to PEP 585.
- Human-in-loop checkpoint: any change to `tsconfig` global strictness flags, eslint root config, or `pyproject.toml` lint set; these have repo-wide blast radius.
- "Recent enough" trap: agent that hasn't been told the current date applies 2024 best practices to a 2026 codebase. Always anchor with `Today's date is YYYY-MM-DD` in the prompt.

## References
- https://www.typescriptlang.org/docs/handbook/release-notes/ — TS release notes
- https://react.dev/blog — React 19 announcements
- https://nextjs.org/docs — Next.js 15
- https://docs.python.org/3/whatsnew/3.13.html — Python 3.13
- https://docs.astral.sh/ruff/ — ruff (replaces black/isort/flake8)
- https://martinfowler.com/articles/exploring-gen-ai.html — AI-assisted dev patterns
- https://dora.dev/ — current DORA cohort thresholds
- https://owasp.org/www-project-top-ten/ — security baseline referenced in code-quality-trends
