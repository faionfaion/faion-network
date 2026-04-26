# Agent Integration — LLM-Friendly Architecture

## When to use
- Planning a new codebase that will rely heavily on Claude Code or similar AI tools for ongoing development.
- Refactoring an existing repo where AI-assisted edits frequently produce wrong line numbers or missed imports.
- Code review stage: auditing a PR to check file sizes exceed 300 lines before merging.
- After a team retrospective identifies "AI tool makes mistakes in large files" as a recurring problem.

## When NOT to use
- Generated code (protobuf outputs, ORM migrations, auto-generated clients) — file size limits don't apply to machine-generated files.
- Legacy monolith stabilization work where any structural change risks regressions; defer architecture until test coverage is in place.
- Performance-critical hot paths where splitting into smaller files increases import overhead (rare but real in Python startup-time-sensitive CLIs).

## Where it fails / limitations
- Flat structure works for small projects; beyond ~200 files, a flat `components/` directory becomes its own navigation problem.
- Data extraction pattern (separating data files) works for static data; it creates coupling problems for data that mutates frequently.
- "Max 300 lines per file" guidance breaks down for TypeScript `.d.ts` declaration files, SQL migration files, and test fixture files.
- LLM context window improvements (2M+ tokens in some models) may reduce urgency of file-size discipline — but edit accuracy still degrades with large files.
- Teams working without AI tooling may find the enforced decomposition overhead outweighs benefit.

## Agentic workflow
An agent can audit an existing codebase by globbing all source files, measuring line counts, then producing a prioritized refactoring plan ranked by file size and complexity. A second pass agent applies the decomposition. For new projects, the agent generates the directory skeleton from the template in README.md before writing any code, ensuring all conventions are in place from commit one.

### Recommended subagents
- `faion-sdd-executor-agent` — executes the refactoring tasks sequentially with quality gates that re-measure file sizes after each split.

### Prompt pattern
```
Glob all .ts and .tsx files in src/. List any file exceeding 250 lines. For each, suggest how to split it (what to extract, where to move it) following the LLM-friendly architecture principles: flat structure, explicit imports, data extraction, single responsibility.
```

```
Refactor <filename>: extract all static data arrays to src/data/<domain>.ts, extract custom hook logic to src/hooks/use-<feature>.ts. Keep the component under 100 lines. Update all import paths.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `wc -l` / `find` | Count lines per file for audit | system |
| `cloc` | Count lines of code by language, excluding blanks/comments | https://github.com/AlDanial/cloc |
| `rg` (ripgrep) | Find barrel re-exports (`export * from`) that hide file locations | https://github.com/BurntSushi/ripgrep |
| `madge` | Visualize JS/TS import dependency graph to spot circular deps after restructuring | https://github.com/pahen/madge |
| `knip` | Dead code and unused exports detector for TS projects | https://knip.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarQube / SonarCloud | SaaS/OSS | Yes — API + CLI | Enforces file complexity limits; can block PRs with files over threshold |
| CodeClimate | SaaS | Partial | "File complexity" metric catches god components |
| ESLint `max-lines` rule | OSS (config) | Yes — CLI | Enforce per-file line limit in CI; set to 250 for TS components |
| Danger JS | OSS | Yes — CI step | Warn in PRs when file line count exceeds limit |

## Templates & scripts
Inline audit script (≤50 lines):

```bash
#!/usr/bin/env bash
# llm-arch-audit.sh
# Usage: bash llm-arch-audit.sh src/ 250
DIR=${1:-src}
LIMIT=${2:-250}

echo "=== Files exceeding ${LIMIT} lines in ${DIR} ==="
find "$DIR" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.py" \) \
  | while read -r f; do
      lines=$(wc -l < "$f")
      if [ "$lines" -gt "$LIMIT" ]; then
        echo "$lines  $f"
      fi
    done \
  | sort -rn

echo ""
echo "=== Barrel re-exports (potential navigation traps) ==="
rg --glob "*.ts" "^export \* from" "$DIR" -l
```

## Best practices
- Apply the "Optimal File Size" rule (100-300 lines) to component and utility files only; test files and data files may exceed 300 lines legitimately.
- Name files after what they do, not where they live: `price-calculator.ts` not `utils.ts`. Agents grep by filename to find code; ambiguous names cause wrong-file edits.
- Enforce the flat structure with ESLint `no-restricted-imports` to ban imports deeper than 3 levels from component files.
- Extract data to `src/data/` as the first step in any AI-assisted refactor — it yields the biggest file-size reduction for the least logic risk.
- When decomposing a god component, keep the original filename as the orchestrator importing the new sub-components; this avoids breaking all existing import sites.
- Add a `# LLM note:` comment at the top of complex utility functions explaining intent; LLMs read doc comments before implementation when planning edits.
- Run `madge --circular` in CI to catch circular dependencies introduced when splitting files.

## AI-agent gotchas
- Agents editing large files (800+ lines) frequently produce edits with off-by-one line numbers due to context truncation. This is the primary failure mode; smaller files are not just style — they are accuracy requirements.
- When splitting a file, an agent may create the new files but forget to remove the original code, leaving duplicates. The review pass must diff the original against the new files.
- Barrel re-exports (`export * from './Button'`) cause agents to misidentify source locations; the agent edits the barrel file thinking it is the implementation. Explicit imports are mandatory for agentic projects.
- After a large restructure, TypeScript path aliases (`@/components`) may still resolve to old file locations if `tsconfig.json` is not updated. Agents often miss tsconfig changes.
- Auto-refactoring via agent can introduce inconsistent naming (e.g., mixing `useAuth` hook filename with `use-auth.ts` convention); enforce naming via ESLint plugin `check-file`.

## References
- https://www.anthropic.com/research/building-effective-agents — Anthropic guidance on context-aware code generation
- https://github.com/microsoft/vscode/issues (search "large file performance") — VSCode team discussions on file-size limits for tooling
- https://eslint.org/docs/latest/rules/max-lines — ESLint max-lines rule documentation
- https://knip.dev/guides/handling-issues — Knip unused exports guide
- https://github.com/pahen/madge — Madge dependency graph tool
