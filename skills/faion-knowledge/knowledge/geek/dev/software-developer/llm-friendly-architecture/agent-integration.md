# Agent Integration — LLM-Friendly Architecture (Software Developer Perspective)

## When to use
- Designing the initial structure of a new TypeScript/React/Python project that will use Claude Code for feature development.
- During code review: flagging god components, barrel re-exports, or files exceeding 300 lines before they merge.
- When an agent repeatedly makes wrong edits on a specific file — the root cause is almost always file size or ambiguous naming.
- Migrating a legacy codebase to LLM-friendly patterns in preparation for AI-assisted feature development.

## When NOT to use
- Auto-generated files (GraphQL schemas, protobuf, ORM migrations, locale bundles) — size limits do not apply.
- Highly stable, rarely-changed modules where the refactoring cost exceeds the benefit.
- Performance-sensitive Python CLI startup: many small files increase import time; profile before splitting.
- Projects without any AI-assisted development planned — the patterns add value but are not mandatory for human-only teams.

## Where it fails / limitations
- Flat component directories become search problems at 100+ components; a secondary grouping by feature (not deep nesting) is still needed.
- Data extraction to `src/data/` creates a coupling between component and data file that makes co-location refactors awkward.
- LLM context windows continue to grow (2M+ tokens in 2026 models); the urgency of strict file-size limits decreases, but edit precision still suffers on very large files.
- Barrel re-export prohibition conflicts with some library design patterns and published package APIs. Apply only to internal application code.
- "Self-documenting names" require agreement across the team; without a linter, naming drift reintroduces ambiguity over time.

## Agentic workflow
An agent audits existing files (glob + line count), scores each by LLM-friendliness (size, name clarity, barrel usage), and generates a prioritized refactor backlog as a markdown task list. A second agent implements each task sequentially, running TypeScript compilation and tests after each split to catch broken imports. The agent verifies no file exceeds the threshold after each commit before proceeding to the next.

### Recommended subagents
- `faion-sdd-executor-agent` — runs refactoring tasks sequentially with compile + test quality gates after each file split.

### Prompt pattern
```
Run the following audit on src/: (1) list all files over 250 lines, (2) list all files named utils.ts, helpers.ts, index.ts, or common.ts, (3) list all barrel re-export files (files containing "export * from"). Output as a JSON object with keys: large_files, ambiguous_names, barrel_exports.
```

```
Refactor the file src/features/user/UserProfile.tsx following LLM-friendly architecture principles:
- Extract any static data arrays to src/data/user-profile-data.ts
- Extract custom hook logic (useEffect, useState blocks) to src/hooks/use-user-profile.ts
- Keep the component under 120 lines
- Use explicit imports, not barrel re-exports
Run tsc --noEmit after refactoring to verify no type errors.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tsc --noEmit` | Verify TypeScript compiles after structural changes | https://www.typescriptlang.org/docs/handbook/compiler-options.html |
| `eslint --rule 'max-lines: [error, 250]'` | Enforce file size limit in CI | https://eslint.org/docs/latest/rules/max-lines |
| `knip` | Detect unused exports after splitting files | https://knip.dev |
| `madge` | Circular dependency detection after restructuring | https://github.com/pahen/madge |
| `cloc` | Count lines of code by file type for audit baseline | https://github.com/AlDanial/cloc |
| `check-file` (ESLint plugin) | Enforce naming conventions (kebab-case files, PascalCase components) | https://github.com/DukeLuo/eslint-plugin-check-file |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarCloud | SaaS | Yes — API + CLI | Cognitive complexity and file size metrics; gate PRs |
| CodeClimate | SaaS | Yes — REST API | "File complexity" maintainability checks |
| Danger JS | OSS | Yes — CI hook | Comment on PRs when file line count exceeds threshold |
| ESLint | OSS | Yes — CLI | `max-lines` rule enforces per-file limit in CI |

## Templates & scripts
ESLint config snippet to enforce LLM-friendly limits:

```json
{
  "rules": {
    "max-lines": ["error", { "max": 250, "skipComments": true, "skipBlankLines": true }],
    "no-restricted-imports": ["error", {
      "patterns": ["../../*", "../../../*"]
    }]
  }
}
```

Audit script:

```bash
#!/usr/bin/env bash
# llm-audit.sh <src_dir>
DIR=${1:-src}
echo "--- Files > 250 lines ---"
find "$DIR" -name "*.ts" -o -name "*.tsx" -o -name "*.py" \
  | xargs wc -l 2>/dev/null \
  | awk '$1 > 250 {print $1, $2}' | sort -rn

echo "--- Ambiguous file names ---"
find "$DIR" -name "utils.*" -o -name "helpers.*" -o -name "common.*" -o -name "misc.*"

echo "--- Barrel re-exports ---"
grep -rl "^export \* from" "$DIR" 2>/dev/null
```

## Best practices
- Apply the 100-300 line rule immediately at project start; retrofitting it on large codebases requires significant refactoring effort.
- Use self-documenting names aggressively: `price-calculator.ts` not `utils.ts`. The agent's first action is usually grepping for a file by name.
- Define the naming convention in CLAUDE.md so every agent working on the project applies it consistently.
- When splitting a large component, keep the original filename as the orchestrator; renaming the original breaks all existing import paths.
- Run `knip` after every significant refactor to detect dead exports left behind from splitting.
- Enforce explicit imports via ESLint `no-restricted-imports` — this single rule prevents the barrel re-export anti-pattern from creeping back in.
- Add JSDoc `@param` and `@returns` to complex utility functions so agents understand intent from the signature without reading the implementation.

## AI-agent gotchas
- An agent refactoring a 600-line file may split it correctly but leave the original 600-line file untouched (forgetting to delete or clear the source of truth). Always diff before and after.
- When extracting data to `src/data/`, an agent may create the file but not update the component's import. The TypeScript compiler catches this — run `tsc --noEmit` as a quality gate.
- Barrel re-exports (`export * from`) cause agents to look in the wrong file for implementations. The agent edits the barrel index, not the actual component, causing silent no-ops.
- After renaming a file to a descriptive name, the agent must update all import paths. Missing even one breaks the build; always run compile as the commit quality gate.
- Agents have been observed naming new hook files with PascalCase (`UseAuth.ts`) instead of the kebab-case convention (`use-auth.ts`). ESLint `check-file` plugin prevents this in CI.

## References
- https://eslint.org/docs/latest/rules/max-lines — ESLint max-lines rule
- https://knip.dev — Unused exports detector for TypeScript
- https://github.com/pahen/madge — Circular dependency graph for JS/TS
- https://github.com/DukeLuo/eslint-plugin-check-file — Filename convention enforcement
- https://www.typescriptlang.org/docs/handbook/compiler-options.html — TypeScript compiler options
