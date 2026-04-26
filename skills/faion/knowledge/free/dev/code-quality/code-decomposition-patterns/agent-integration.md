# Agent Integration — Code Decomposition Patterns

## When to use
- Agent must apply a *named* pattern (Extract Service, Extract Component, Extract Module, Extract Configuration, Extract Types) — pattern catalog gives crisp prompts and acceptance criteria.
- Refactoring a fat controller / 400-line React component / 500-line settings file — the README already has before/after templates the agent can mimic.
- New feature scaffolding: agent lays out files using language-specific tree (Python/Django, TS/React, Go) before writing code.
- Migration from flat → modular structure (Pattern 3) where the agent has to plan moves and update imports.

## When NOT to use
- Tiny features (≤200 lines total) where applying a pattern adds more files than logic.
- Code with strong runtime coupling that the patterns assume away (e.g., framework-mandated single file like Django `urls.py`).
- Generated code or ORM migrations.
- Performance-critical hot loops where indirection has measured cost.

## Where it fails / limitations
- "Extract Service" leaks framework concepts (request/response objects) into the service layer if the agent isn't explicit about purity.
- "Extract Component" → too many small components reduce readability and break React reconciliation; pattern doesn't define a min-size rule.
- Barrel `index.ts` re-exports (warned in the principles file, not here) regularly slip back in when applying Extract Module.
- Configuration extraction without a config-loader strategy creates import cycles (`base.py` ← `production.py` ← `database.py`).
- Type extraction across many files makes "go to definition" worse, not better, when not paired with editor/IDE indexes.

## Agentic workflow
Pattern application is a deterministic transform with verifiable post-conditions; ideal for an agent. Step 1: classify which pattern fits (often via a planner agent reading the principles + this patterns file). Step 2: for the chosen pattern, the agent reads the current file plus its direct importers, drafts the new tree using the language-specific layout from this README, and emits a sequence of `git mv` + edit commands. Step 3: executor agent performs each step in its own commit; runs tests after every step. Step 4: a verifier agent checks the after-tree matches the pattern's invariants (file sizes, naming, no circular imports). Use the SDD task flow so each pattern application is one task with a green-test acceptance gate.

### Recommended subagents
- `faion-sdd-executor-agent` — pattern application as an SDD task with quality gates.
- `faion-feature-executor` — sequential step execution with test validation.
- Planner subagent (Opus) — picks the pattern and emits the move plan.
- Executor subagent (Sonnet) — applies one step at a time.
- Reviewer subagent (Sonnet) — verifies against pattern invariants.
- See sibling `code-decomposition-principles/agent-integration.md` for the broader principles workflow this layers on top of.

### Prompt pattern
```
Pattern: Extract Service.
Source: src/views/order_view.py (180 lines).
Importers: $(grep -rl 'order_view' src/).

Plan:
1. List business logic vs HTTP-handling lines.
2. Propose service file path + signature.
3. Propose validator/notifier files if logic > 50 lines.

Output JSON:
{ "files": [{"path","responsibilities","est_lines"}],
  "moves": [{"from","to","what"}],
  "notes": "" }
```
```
Apply Extract Component to src/Dashboard.tsx.
Constraints:
- Keep top-level component < 50 lines, only composition.
- Each extracted child < 100 lines.
- Co-locate child components in src/components/dashboard/<Name>/.
- Hooks for data go to src/hooks/useDashboardData.ts.
After each extraction, run `pnpm test` and `pnpm typecheck`.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tokei` / `scc` | Confirm before/after line counts per file | https://github.com/XAMPPRocky/tokei |
| `madge` | JS/TS dependency graph + circular-import detection post-extract | https://github.com/pahen/madge |
| `pydeps` | Python import graph after Extract Module | https://github.com/thebjorn/pydeps |
| `ts-morph` | Programmatic TS refactors (rename/move/extract) | https://ts-morph.com |
| `rope` / `pyrefactor` | Python rename/extract refactors | https://github.com/python-rope/rope |
| `gopls` / `gomvpkg` | Go package moves | https://pkg.go.dev/golang.org/x/tools |
| `git mv` + `git log --follow` | Preserve history through moves | git docs |
| `jscodeshift` / `ast-grep` | Codemod engines for bulk transforms | https://github.com/facebook/jscodeshift / https://ast-grep.github.io |
| `comby` | Language-aware structural rewrites | https://comby.dev |
| `eslint --fix` / `ruff check --fix` | Clean up after each move | tool docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Code Search | SaaS | Yes (REST) | Find all callers before a move |
| Sourcegraph | OSS + SaaS | Yes (`src` CLI + GraphQL) | Cross-repo callers / batch refactor |
| OpenRewrite | OSS | Yes (CLI) | Recipe-based Java/Kotlin/Groovy refactors |
| `comby-server` / Glean | OSS | Yes | Indexed code search for large monorepos |
| GitHub Actions | SaaS | Yes | Run tests + dep-graph checks per pattern application |
| `pre-commit` | OSS | Yes | Block PRs that introduce circular imports |

## Templates & scripts
The README already ships before/after templates per pattern and language-specific layouts. Useful companion: a guard script that enforces pattern invariants in CI.

```bash
#!/usr/bin/env bash
# pattern-guard.sh — enforce decomposition pattern invariants post-refactor.
# Usage: ./pattern-guard.sh [path]
set -euo pipefail
ROOT="${1:-.}"
MAX_VIEW=120; MAX_COMPONENT=200; MAX_SERVICE=300; MAX_CONFIG=150

# Views must be thin (Extract Service)
find "$ROOT" -path '*/views/*' -name '*.py' \
  | xargs awk -v t="$MAX_VIEW" 'END{ if(NR>t) print FILENAME": "NR" lines (>",t,")" }'

# React components capped (Extract Component)
find "$ROOT/src/components" -name '*.tsx' 2>/dev/null \
  | while read -r f; do
      n=$(wc -l < "$f")
      [ "$n" -gt "$MAX_COMPONENT" ] && echo "$f: $n lines (> $MAX_COMPONENT)"
    done

# Settings split (Extract Configuration)
[ -f "$ROOT/settings.py" ] && {
  n=$(wc -l < "$ROOT/settings.py")
  [ "$n" -gt "$MAX_CONFIG" ] && echo "settings.py: $n lines (> $MAX_CONFIG) — extract per-env"
}

# Circular imports
command -v madge >/dev/null && madge --circular "$ROOT/src" 2>/dev/null || true
command -v pydeps >/dev/null && pydeps --show-cycles "$ROOT" 2>/dev/null || true
```

## Best practices
- Always name the pattern in the commit message: `refactor: extract OrderService (Extract Service)`. Reviewers and future agents can grep by pattern.
- Apply one pattern per PR. Mixing Extract Service + Extract Module = unreviewable diff.
- Pair Pattern 5 (Extract Types) with Pattern 3 (Extract Module): types follow the module they describe, not a global `types/` dump.
- After Extract Service, write at least one unit test that exercises the service without the HTTP layer — proves the abstraction actually decoupled them.
- After Extract Component, verify React render perf with the React DevTools profiler; over-decomposition can regress it.
- Use `git mv` for every move; preserve blame.
- Always update the directory's `AGENTS.md`/`CLAUDE.md` in the same PR — the structure changed, the doc must match.

## AI-agent gotchas
- **Pattern misapplication.** Agent applies "Extract Component" to a Vue/Svelte file using React conventions. Pin the language layout in the prompt.
- **Leaky service.** Agent leaves `request` / `response` parameters in the extracted service method. Forbid framework-typed params in the new service signature.
- **Over-extraction.** Agent creates `MicroService` for 5-line helpers. Set a min-size rule (≥40 lines or 3 callers).
- **Import update misses.** Agent edits the moved file but not the importers. Mandate a `grep` pass + post-step `tsc --noEmit` / `python -c 'import app'`.
- **Re-export sprawl.** Agent adds `export *` in `index.ts`. Forbid `export *`.
- **Settings cycle.** When applying Extract Configuration, agent imports `production.py` from `base.py` (cycle). Enforce one-way load: `__init__.py` decides which env file to import.
- **Doc drift.** Pattern application without `AGENTS.md` update lands stale docs. Block in pre-commit / CI.
- **Human-in-loop checkpoint.** Approve the *plan* (file tree + move list) before execution. Wrong plan at step 1 cascades.

## References
- https://refactoring.guru/refactoring/techniques/composing-methods, https://refactoring.guru/refactoring/techniques/moving-features-between-objects
- https://martinfowler.com/books/refactoring.html — Fowler's catalog (canonical names)
- https://addyosmani.com/blog/ai-coding-workflow/
- https://docs.openrewrite.org/, https://ast-grep.github.io/, https://comby.dev/
- https://ts-morph.com/, https://github.com/python-rope/rope
- Sibling: `code-decomposition-principles/agent-integration.md`, `refactoring-patterns/`
