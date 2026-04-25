# Agent Integration — Software Development Best Practices 2026

## When to use
- Choosing AI coding tooling (Claude Code, Cursor, Copilot) for a new project or workflow segment.
- Writing or updating a project's `.aidocs/constitution.md` to encode 2026-current standards (TS 5 strict, React 19 RSC, Python 3.12/3.13, AI testing).
- Bootstrapping a new TypeScript repo: pulling the strict `tsconfig.json` baseline.
- Designing a Next.js 15 App Router architecture and deciding the Server vs Client boundary.
- Adopting Server Actions / `useFormState` for forms instead of REST handlers.
- Modernizing Python codebases with PEP 742 (`TypeIs`), PEP 705 (`ReadOnly`), TaskGroups, async timeouts.
- Selecting AI-driven test tools (Katalon, mabl, testRigor, Virtuoso) and integrating their APIs into CI.
- Code review of agent-generated code: this README is the checklist of what "current" looks like.

## When NOT to use
- Legacy / LTS environments (Python 3.10, Node 18, React 17). The patterns here (TaskGroup, RSC, `verbatimModuleSyntax`) require newer runtimes.
- Embedded / WASM / extension contexts where Server Components or `pino` are irrelevant.
- Static-site generators (Astro, Hugo, Gatsby static) — the React 19 / Next.js 15 sections don't map.
- Solo experimentation where the strict tsconfig kills momentum — start strict on team projects, not on prototypes.
- Greenfield tasks better served by a more specific sibling: routing, Tailwind, server-architecture choice, etc.

## Where it fails / limitations
- **Time-bound by definition.** "2026" snapshot ages fast — JIT/no-GIL Python, RSC, AI testing tools all evolve quarterly. Treat as last-known-good.
- **Headline citations are blog-grade.** Many sources are Medium/DEV posts, not vendor docs. Use them as starting pointers, not authority.
- **Tool comparisons are marketing-shaped.** Katalon/mabl/testRigor table omits cost, lock-in, and on-prem availability. Validate before adoption.
- **AI risk numbers are unverified.** "AI can increase defect rates 4x" is provocative but uncited; do not quote in critical decisions.
- **Server Components: opinion as fact.** "38% faster initial load" is a single benchmark; real apps see 0–60% depending on hydration profile.
- **Python typing recommendations clash with library reality.** `from __future__ import annotations` + Pydantic v1 / Django < 5 still bites at runtime.
- **JIT / no-GIL CPython are experimental** as of 3.13; the README presents them as production-ready features. They are not.
- **No coverage of tooling for AI safety** (eval suites, red-teaming, CI checks for agent-generated code).
- **No section on package management 2026** (uv, pnpm 9, bun, deno 2) — the team-level decisions that drive the rest of the stack.

## Agentic workflow
Treat this README as a **constitutional source** for agents. (1) An **architect agent** reads it once per project, extracts the relevant section into `.aidocs/constitution.md`, and adds project-specific overrides. (2) A **scaffolder agent** uses the constitution (not this README) to bootstrap repos. (3) A **reviewer agent** runs against PRs and matches each change against the constitution clauses, citing this README only as a tertiary reference. (4) A **freshness agent** runs monthly: re-fetches each cited URL via WebFetch, flags broken links and superseded vendor docs, opens an SDD task to re-research. The agent never quotes this README verbatim into production code; it always projects through the project constitution.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts deltas between project state and the 2026 baseline into SDD tasks.
- A purpose-built **constitution-extractor agent** (worth creating): given a project repo + this README, produces `.aidocs/constitution.md` (TS, Python, React, testing sections) with explicit overrides documented.
- A purpose-built **freshness-checker agent** (worth creating): runs scheduled WebFetch against every reference URL, flags 404 / superseded content.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrubs example configs (`.env.example`, deploy scripts) before publishing internal copies of the constitution.

### Prompt pattern
Constitution extraction:
```
Read free/dev/software-developer/best-practices-2026/README.md and the
target repo's package.json/pyproject.toml. Produce
.aidocs/constitution.md with sections:
- AI Coding Stack (which tool for what)
- TypeScript Config (paste the strict baseline + project overrides)
- React/Next strategy (RSC boundary policy, Server Actions usage)
- Python (version, typing rules, async patterns)
- Testing (unit, integration, AI-assisted, AI test tools if any)
For each section: rule, rationale, override (if applicable), evidence URL.
```

Reviewer pass:
```
Review the diff. For each file changed, evaluate against
.aidocs/constitution.md. Cite the rule and the section.
Reject changes that:
- Use deprecated TS options (esModuleInterop without verbatimModuleSyntax)
- Add `any` types without `// eslint-disable-next-line` justification
- Write `useState` in a Server Component
- Add async functions without explicit timeout/Semaphore in Python I/O
- Use `Optional[X]` in new Python code (prefer `X | None`)
Output: pass/fail per file with rule citation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` (Claude Code) | Agentic CLI for refactor / docs / tests | https://docs.anthropic.com/en/docs/claude-code |
| `cursor-agent` | Cursor's CLI for batch edits | https://cursor.com |
| `gh copilot` | Copilot CLI for command suggestions | `gh extension install github/gh-copilot` |
| `pnpm` v9 / `bun` v1.x | Modern Node package managers | https://pnpm.io , https://bun.sh |
| `uv` | Modern Python package + venv tool | `pipx install uv` ; https://docs.astral.sh/uv/ |
| `ruff` | Python lint + format (replaces black/isort/flake8) | `uv tool install ruff` ; https://docs.astral.sh/ruff/ |
| `mypy` / `pyright` | Static typing | `uv tool install mypy` |
| `tsc --noEmit` | TypeScript type-check in CI | bundled with `typescript` |
| `eslint` + `@typescript-eslint` | Linter | https://typescript-eslint.io |
| `vitest` / `jest` | JS/TS test runners | https://vitest.dev |
| `pytest` + `pytest-asyncio` | Python testing | https://pytest.org |
| `playwright` | E2E (works with mabl, testRigor exports) | https://playwright.dev |
| `lychee` | Link-check the README's reference URLs | https://github.com/lycheeverse/lychee |
| `npm-check-updates` (`ncu`) / `uv pip compile --upgrade` | Dependency freshness | https://github.com/raineorshine/npm-check-updates |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude Code | SaaS CLI | yes | First-class agentic; primary in this stack. |
| Cursor | SaaS IDE | partial | Editor-bound; not headless-agent-friendly. |
| GitHub Copilot | SaaS IDE+CLI | yes (CLI) | Inline best; CLI suits scripting. |
| Vercel / Netlify | SaaS PaaS | yes | Required RSC validation happens at build; flags incompatible CSS-in-JS, Edge runtime. |
| Sentry / Datadog / Honeycomb | SaaS APM | yes | OTel SDKs across Node/Python/Go align with the README's logging recommendations. |
| Katalon / mabl / testRigor / Virtuoso | SaaS AI testing | partial | Each has REST API; check on-prem and pricing before adopting. |
| LambdaTest KaneAI | SaaS cross-browser | yes (API) | LLM-driven flows; pair with Playwright for fallback. |
| Linear / GitHub Issues | SaaS | yes | Track per-clause adoption (each constitution rule = a task). |
| pyright Language Server (via VS Code or `pyright`) | OSS | yes | Strict typing across the codebase. |
| Renovate / Dependabot | SaaS | yes | Automate freshness; the constitution dictates accept/reject policy. |

## Templates & scripts

The README is heavy on patterns; the missing piece is a **drift checker** that compares a repo against the 2026 baseline. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# bp2026-drift.sh — detect drift from the 2026 baseline.
# Usage: bp2026-drift.sh path/to/repo
set -euo pipefail
root="${1:-.}"
fail=0
note() { echo "- $*"; fail=1; }
if [ -f "$root/tsconfig.json" ]; then
  for k in '"strict": true' '"noUncheckedIndexedAccess": true' '"verbatimModuleSyntax": true'; do
    grep -q "$k" "$root/tsconfig.json" || note "tsconfig missing: $k"
  done
fi
if [ -f "$root/package.json" ]; then
  node -e '
    const p=require(process.argv[1]);
    const dep={...(p.dependencies||{}),...(p.devDependencies||{})};
    const want={typescript:"^5",react:"^19",next:"^15"};
    for (const [k,v] of Object.entries(want)) {
      if (k in dep && !new RegExp(v).test(dep[k]))
        console.log("- "+k+" pinned at "+dep[k]+", want "+v);
    }
  ' "$root/package.json"
fi
if [ -f "$root/pyproject.toml" ]; then
  grep -E "python = \"\\^?3\\.(12|13)" "$root/pyproject.toml" >/dev/null || note "Python <3.12"
  grep -q "ruff" "$root/pyproject.toml" || note "ruff not configured"
fi
exit $fail
```

Wire into CI; opens a `chore: bp2026-drift` task whenever something rots.

## Best practices
- **Project constitution > README.** Always copy the relevant clauses into `.aidocs/constitution.md` with explicit overrides; never have agents read this file at runtime to make decisions — the constitution is the contract.
- **Pin language/runtime versions** (`engines.node`, `python_requires`) to match the baseline. Drift is silent otherwise.
- **Adopt strict tsconfig in one PR.** Flip `strict: true` and friends together; piecemeal adoption produces inconsistent enforcement.
- **Use `satisfies` over assertion casts.** It validates without widening — exactly what you want for config objects.
- **Keep `'use client'` boundaries minimal.** Push interactivity to leaves; default to Server Components for everything possible.
- **Validate Server Action input with Zod.** Returning `{ error }` shapes is fine, but never trust `formData` directly.
- **Log structured JSON, request_id everywhere.** Both Node (`pino`) and Python (`structlog`) sections deserve uniform shape across services.
- **Replace `Optional[X]` with `X | None`** in new Python code. Old style is fine in legacy code; mixing creates noise.
- **Cap async fan-out with `asyncio.Semaphore`.** TaskGroups without bounds DDOS your downstream.
- **Treat AI test generators as a starting draft.** The "AI generates first draft, human reviews" rule is non-negotiable — never auto-merge AI-generated tests.
- **Cite vendor docs over blog posts.** When your constitution clauses cite `react.dev` or `python.org`, agents have a stable source. Medium URLs rot.
- **Run `lychee` on this README and the constitution monthly.** Dead links signal stale guidance.

## AI-agent gotchas
- **Outdated React patterns inherited from training data.** Agents emit `React.FC`, `useEffect` for data fetching in App Router pages, or wrap server components with `useState`. Reject and re-prompt with the RSC boundary explicit.
- **Server Action without `'use server'` directive.** Agents copy README snippets and skip the directive — function silently runs as a normal client function. Lint for the directive on every export named `*Action` or in `actions.ts`.
- **`use client` cascading.** Adding `'use client'` to a layout flips the entire subtree. Agents do this to "just make it work"; reviewer must catch.
- **`any` slips back in.** Default LLM output reaches for `any` under TypeScript pressure. Forbid via ESLint `@typescript-eslint/no-explicit-any` and reject PRs that disable it inline without a reason.
- **`Optional`/`Union` regressions.** Agents alternate between `int | None` and `Optional[int]` within a file. Pick one (preferably the modern syntax) and lint.
- **No-GIL / JIT presented as stable.** Agents read the README and recommend `python -X nogil` for production. It is experimental in 3.13. Block this in the constitution.
- **TaskGroup without timeouts.** Agents create unbounded TaskGroups; in production they hang on a slow downstream. Mandate `async with asyncio.timeout(...)` around groups.
- **AI testing tool selection by recency bias.** Agents echo whichever tool was most recently mentioned in their context. Force a comparison across 3+ tools with on-prem/cost columns.
- **Citing this file as authority.** Agents quote `best-practices-2026/README.md` in PRs as if it were a vendor doc. Force agents to cite the underlying source URL or, better, the project constitution clause.
- **`generateMetadata` over-fetching.** Agents call `getProduct(params.id)` twice (once in metadata, once in page). Memoize via `cache(...)` or shared module-level promise.
- **`useFormState` import path drift.** Renamed to `useActionState` in newer React; agents flip-flop. Pin React version + the matching API name in the constitution.
- **Snippet-level test generation.** AI test tools generate flaky XPath-anchored tests that break on first UI change. Always wrap with self-healing locators or migrate to role-based queries.
- **Stale dep pins from training cut-off.** Agents pin `next: "13.x"` because that was current in training. Force `ncu` post-generation and reject training-anchored versions.

## References
- React 19. https://react.dev/blog/2024/12/05/react-19
- Server Components. https://react.dev/reference/rsc/server-components
- Next.js 15. https://nextjs.org/blog/next-15
- TypeScript 5 release notes. https://devblogs.microsoft.com/typescript/
- Python 3.13 What's New. https://docs.python.org/3/whatsnew/3.13.html
- PEP 742 — `TypeIs`. https://peps.python.org/pep-0742/
- PEP 705 — `ReadOnly` for TypedDict. https://peps.python.org/pep-0705/
- PEP 703 — Free-threaded CPython. https://peps.python.org/pep-0703/
- ruff. https://docs.astral.sh/ruff/
- uv. https://docs.astral.sh/uv/
- Anthropic Claude Code. https://docs.anthropic.com/en/docs/claude-code
- OpenTelemetry. https://opentelemetry.io
- "How AI changes software engineering" — Stack Overflow Dev Survey 2024. https://survey.stackoverflow.co/2024
- Sibling methodologies in this repo: `free/dev/software-developer/best-practices-2026/`'s neighbours (`error-handling/`, `documentation/`, etc.); `geek/ai/claude-code/`; `solo/dev/software-architect/`.
