# Agent Integration — Token Organization

## When to use
- Bootstrapping a new design system's token taxonomy (primitives → semantic → component).
- Auditing an existing token set for bloat, naming inconsistency, or aliasing depth.
- Renaming tokens across a large repo without breaking references.
- Reviewing PRs that add new tokens to enforce the lean-first principle.

## When NOT to use
- A 5-token brand palette for a single landing page — overhead exceeds benefit.
- Mid-rebrand chaos where the source of truth is in flux; stabilize visuals first.
- Pure component library without theming — token layer adds indirection without payoff.
- Brand-driven marketing assets that change weekly — naming churn kills ROI.

## Where it fails / limitations
- LLMs love symmetric naming and will invent token tiers (`color.brand.primary.light.hover.disabled`) that bloat the system.
- Renaming requires repo-wide refactor; agents may miss references in non-code files (Storybook MDX, Figma plugins, JSON config).
- Component tokens are easy to over-create; agent-suggested ones often duplicate semantic tokens.
- Aliasing depth > 3 levels makes debugging painful — visual diffs are the only check.
- Naming conventions vary by team (BEM-ish, dot-path, kebab); cross-team alignment is political, not technical.

## Agentic workflow
Use Claude as a "taxonomy linter + namer": it analyzes a token file, classifies each token into primitive / semantic / component, flags duplicates, suggests merge or rename, and produces a migration codemod. A separate naming pass enforces the project convention (`{category}.{property}.{variant}.{state}`). For renames, the agent emits a sed-able mapping table plus a Storybook + MDX scan to ensure references are caught everywhere.

### Recommended subagents
- `general-purpose` Claude subagent — taxonomy classification + bloat audit.
- `faion-sdd-executor-agent` — implement rename codemods as SDD task.
- A "naming-convention-validator" prompt — score each token name against the regex.

### Prompt pattern
```
Classify each token in tokens.json as primitive | semantic | component.
Flag tokens that look like duplicates (same value, different name) and
tokens whose name doesn't match `{category}.{property}.{variant}.{state}`.
Output: JSON {token, layer, issues[]}.
```

```
Propose a rename map from old names to new names matching convention X.
Ensure no two new names collide. Output sed-compatible mapping
plus a list of files to scan for references.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` v4+ | Native layered token model | `npm i -g style-dictionary@latest` |
| `jq` | Path-level inspection of token JSON | `apt install jq` |
| `comby` | Structural codemod for renames across many files | https://comby.dev/ |
| `ast-grep` | Grep with AST awareness for code references | `cargo install ast-grep` |
| `ripgrep` | Plain-text reference scan in MDX / Storybook | `apt install ripgrep` |
| `tokens-cli` (community) | Token-aware diff / merge | https://github.com/tokens-studio |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tokens Studio (Figma) | SaaS plugin | Partial | Designer authoring; alias support |
| Supernova | SaaS | Yes (REST + CLI) | Visual taxonomy explorer |
| Specify | SaaS | Yes (CLI) | Distribution-only, less authoring |
| zeroheight | SaaS | Limited | Documentation-first |
| Knapsack | SaaS | Yes (REST) | Token + component co-management |
| Storybook + tokens addon | OSS | Yes | In-repo visual docs |
| Penpot | OSS | Limited | Open-source Figma alternative |

## Templates & scripts
See `templates.md` for the layered taxonomy template. Inline naming linter:

```python
#!/usr/bin/env python3
# token_name_lint.py — flag bad names and duplicates
import json, re, sys
PATTERN = re.compile(r"^[a-z]+(\.[a-z][a-z0-9-]*){1,3}$")  # category.property[.variant[.state]]
data = json.load(sys.stdin)["tokens"]
seen = {}
issues = []
for t in data:
    name, val = t["name"], json.dumps(t["value"])
    if not PATTERN.match(name):
        issues.append(f"bad name: {name}")
    if val in seen and seen[val] != name:
        issues.append(f"duplicate value: {name} == {seen[val]}")
    seen[val] = name
sys.exit("\n".join(issues) or 0)
```

## Best practices
- Three layers, never four — primitives, semantic, component (use sparingly).
- Component tokens only when a single component needs an exception; otherwise stay semantic.
- Names describe purpose, not appearance — `color.surface.primary` beats `blue-500`.
- Add a `$description` to every semantic token; future maintainers (and LLMs) read it.
- Run a duplicate-value detector in CI; same value under two names is a smell.
- Pair every rename with a Storybook visual diff to catch unreferenced usages.

## AI-agent gotchas
- Claude generates dense, symmetric token trees (full Cartesian of state × variant) that nobody uses; cap depth in the prompt.
- Suggested component tokens often duplicate semantic ones; require justification per component token.
- Renames touch MDX, JSON, .storybook configs — agents miss these by default; explicitly include those globs.
- Aliasing more than 3 levels makes runtime debugging hellish; enforce a max-depth check.
- Don't let an agent "clean up unused tokens" — static analysis misses theming, runtime, and per-tenant overrides.
- LLMs invent fictional convention names ("Carbon style", "MUI v6 style") confidently; always pin the convention regex.

## References
- https://www.designsystems.com/token-naming/
- https://bradfrost.com/blog/post/design-token-hierarchy/
- https://www.nngroup.com/articles/design-token-architecture/
- https://css-tricks.com/organizing-design-tokens/
- https://styledictionary.com/info/architecture/
- Brad Frost, *Atomic Design* (2016)
