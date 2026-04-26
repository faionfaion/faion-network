# Agent Integration — Code Decomposition Principles

## When to use
- A target file/module exceeds ~300 lines or ~9-10K tokens and a Claude subagent must edit it under a tight context budget.
- Planning a refactor where the LLM keeps producing partial/incorrect diffs because it cannot hold the full file plus tests in one window.
- Designing a new module from a `spec.md` and you want the agent to lay it out as small, single-responsibility files from the start.
- Onboarding an LLM to an unfamiliar repo: split first, then have the agent read the new tree.

## When NOT to use
- File is < 100 lines and tightly cohesive — splitting adds indirection without context savings.
- Hot path with measured perf cost from the indirection (rare for app code, occasional in inner loops).
- Generated code (migrations, protobuf stubs) — apply rules to the source, not the output.
- Throwaway scripts and one-shot notebooks where the file *is* the unit of thought.

## Where it fails / limitations
- LLMs over-decompose: one-function-per-file, "utils-of-utils", barrel re-exports that break tree-shaking. The principles file warns about this — agents need explicit min-size guidance.
- Mechanical line-count splits ignore semantic cohesion; the agent ends up with `user_part1.py` / `user_part2.py`.
- Cross-file refactors silently break imports if the agent only edits the moved file and forgets call sites.
- Token-budget rule of thumb (~15K per 500 lines) is Python-ish; minified JS, JSON fixtures, and SQL dumps tokenize very differently.

## Agentic workflow
Drive decomposition with one planning agent and one executor. Planner reads the oversize file plus its direct importers, emits a target tree (file → responsibility → est. lines) and a move-order respecting tests. Executor performs Extract-Service / Extract-Component / Extract-Module steps one-at-a-time, running the test suite between each commit, never amending. Use `git mv` so history is preserved and reviewers see renames, not delete+add.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the spec → plan → task loop with quality gates; right fit when decomposition is part of an SDD task.
- A planner subagent (Opus) — produces the target tree and migration order.
- An executor subagent (Sonnet) — performs each move + import update + test run.
- A reviewer subagent (Sonnet) — checks SRP, file size, naming after each step.

### Prompt pattern
```
Plan a decomposition of <path>:
- list current responsibilities (one per bullet)
- propose target file tree, max 200 lines/file
- order moves so tests stay green after each step
Output: JSON { "target_tree": [...], "moves": [{"from","to","what"}] }
```
```
Execute move N from the plan. Constraints:
- use `git mv` where possible
- update every import (grep first, then edit)
- run `pytest -x` and stop on first failure
- one commit per move
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tokei` | Fast LOC count per file/lang to find oversize files | https://github.com/XAMPPRocky/tokei |
| `scc` | LOC + complexity + COCOMO; alternative to tokei | https://github.com/boyter/scc |
| `radon` | Python cyclomatic complexity / maintainability index | https://radon.readthedocs.io |
| `lizard` | Multi-language complexity (C, Java, JS, Py, Go) | https://github.com/terryyin/lizard |
| `madge` | JS/TS module dependency + circular-import graph | https://github.com/pahen/madge |
| `pydeps` | Python import graph (Graphviz) | https://github.com/thebjorn/pydeps |
| `dep-tree` | Multi-lang dep visualisation, circular-dep detection | https://github.com/gabotechs/dep-tree |
| `jscpd` | Copy-paste detector across languages | https://github.com/kucherenko/jscpd |
| `tiktoken` | Token-count files to plan context budget | https://github.com/openai/tiktoken |
| `git mv` / `git log --follow` | Preserve history through moves | git docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarQube / SonarCloud | OSS + SaaS | Yes (REST API + CLI scanner) | Maintainability rating, hotspots, complexity per file |
| CodeClimate Quality | SaaS | Yes (CLI + API) | "God class", complexity, churn vs complexity overlay |
| Codacy | SaaS | Yes (CLI + API) | Per-file quality grade |
| CodeScene | SaaS | Yes (CLI + API) | Hotspots = high-churn × high-complexity, ideal split candidates |
| GitHub Code Scanning | SaaS | Yes (Actions + API) | Drives PR-level decomposition prompts |
| Sourcegraph | SaaS + OSS | Yes (GraphQL API + `src` CLI) | Cross-repo grep + batch refactors for agents |

## Templates & scripts
Inline helper to surface decomposition candidates before invoking the planner agent.

```bash
#!/usr/bin/env bash
# decomp-candidates.sh — list files that likely need splitting.
# Usage: ./decomp-candidates.sh src/
set -euo pipefail
ROOT="${1:-.}"
THRESHOLD_LINES="${THRESHOLD_LINES:-300}"
THRESHOLD_CCN="${THRESHOLD_CCN:-15}"

echo "## Oversize files (> ${THRESHOLD_LINES} lines)"
find "$ROOT" -type f \( -name '*.py' -o -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.go' \) \
  | xargs wc -l 2>/dev/null \
  | awk -v t="$THRESHOLD_LINES" '$1 > t && $2 != "total" {printf "%6d  %s\n", $1, $2}' \
  | sort -rn | head -50

echo
echo "## High-complexity functions (CCN > ${THRESHOLD_CCN})"
if command -v lizard >/dev/null; then
  lizard -C "$THRESHOLD_CCN" "$ROOT" 2>/dev/null | tail -n +3 | head -30
fi

echo
echo "## Hotspots (high churn × current size)"
git -C "$ROOT" log --since='6 months ago' --name-only --pretty=format: \
  | grep -E '\.(py|ts|tsx|js|go)$' \
  | sort | uniq -c | sort -rn | head -20
```

See also `templates.md` for the principles-level workflow templates already shipped in this methodology.

## Best practices
- Pin a *minimum* file size (e.g., 30-50 LOC) in the agent prompt to prevent micro-files.
- Always pair a decomposition with a green test suite; if tests don't exist, write characterisation tests *before* moving code.
- Use `git log --follow` checks in CI so renames don't break blame/history for reviewers.
- For LLM-edited monorepos, ship a `CLAUDE.md` per top-level module that names the responsibility and forbidden imports — the agent reads this before touching the module.
- Prefer "Extract Service / Component / Module" patterns from the sibling `code-decomposition-patterns/` over ad-hoc splits — keeps prompts terse.
- Track churn × complexity (CodeScene-style); refactor only the top 5-10 hotspots first, not the whole repo.

## AI-agent gotchas
- **Hallucinated imports after a move.** Force the agent to grep for old import paths and patch every site, then run a typecheck/lint before committing.
- **Barrel `index.ts` re-exports.** Agents love them; they break tree-shaking and obscure module boundaries. Forbid `export *` in the prompt.
- **Phantom circular imports.** When the agent splits a class across files it often introduces a cycle; require `madge --circular` / `pydeps --show-cycles` in the post-step check.
- **Lost git history.** Agents do `cat old > new && rm old` instead of `git mv`. Mandate `git mv` in the system prompt.
- **Token-budget illusions.** Effective LLM context is far smaller than nominal; keep target files under ~200 lines so future edits fit in one window with tests.
- **Human-in-loop checkpoint.** Stop the agent after the planning step and require explicit "approve" before executing any moves — wrong tree at step 1 cascades into 50 bad commits.

## References
- https://addyosmani.com/blog/ai-coding-workflow/ — LLM coding workflow (spec → plan → tasks → execute)
- https://microservices.io/post/architecture/2024/09/09/modular-monolith-patterns-for-fast-flow.html — Modular monolith
- https://martinfowler.com/bliki/MonolithFirst.html — Decompose only after monolith stabilises
- https://refactoring.guru/refactoring/techniques/composing-methods — Composing-methods catalogue
- https://github.com/pahen/madge, https://github.com/terryyin/lizard, https://radon.readthedocs.io
- 2024 DORA Report — modular architectures correlate with deploy frequency
