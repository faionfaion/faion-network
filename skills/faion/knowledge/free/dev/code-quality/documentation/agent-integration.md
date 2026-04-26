# Agent Integration — Documentation (CLAUDE.md / AGENTS.md)

## When to use
- Bootstrapping AI-readable docs in a new repo or sub-package: agent generates initial `CLAUDE.md`/`AGENTS.md` from code.
- Drift detection on existing docs after a refactor: agent diffs reality (file tree, exports) vs the doc and proposes patches.
- Multi-repo monorepo where each package needs a small, accurate `AGENTS.md` (20-80 lines) per the convention.
- Per-module rollout when adding the convention to a legacy codebase that has only a top-level README.

## When NOT to use
- Repos < ~200 lines with one obvious entry point — a README already does the job.
- Generated/derived directories (`dist/`, `build/`, `node_modules/`); doc would just repeat tooling output.
- Short-lived experiments — doc rots faster than the experiment iterates.
- Public-facing user docs (Docusaurus/Mintlify sites); this methodology is for *AI* readers, not customers.

## Where it fails / limitations
- LLMs hallucinate: invented files, wrong exports, fabricated commands. Without a verification step, docs become misinformation.
- Agent-written docs trend toward 200+ lines (LLMs love bullets); the methodology caps at 100-150. Enforce in the prompt.
- Type tables and entry-point lists drift quickly; without a regen pipeline they're stale within weeks.
- "Token efficiency" (English-only, no ASCII art) is repeatedly violated by LLMs that default to fancy boxes.
- Cross-references break when files move; agents rarely update upward `CLAUDE.md` references after a rename.

## Agentic workflow
Run docs generation as a two-pass pipeline. Pass 1: a discovery agent walks the directory, runs `tree`/`ls`, parses imports, extracts public API surface (exports, public classes, route declarations), and emits a JSON outline. Pass 2: a writer agent fills the template strictly from the outline (no invention). Pass 3 (verification): a checker agent re-reads the produced doc, opens every file/path mentioned, and reports broken references. Keep docs in git; CI runs a "doc-drift" check on every PR that touches the module.

### Recommended subagents
- `init` skill (built-in) — produces an initial `CLAUDE.md` for a repo; good first pass.
- `faion-sdd-executor-agent` — quality-gate-driven; doc creation can be a gate per the project convention.
- Discovery subagent (Sonnet) — extracts file list, public API.
- Writer subagent (Sonnet) — fills the template from JSON outline.
- Verifier subagent (Sonnet) — link/file-existence check.
- Periodic drift subagent (Haiku) — runs nightly to flag stale tables.

### Prompt pattern
```
Create AGENTS.md for <dir>. Strict rules:
- Length 20-80 lines.
- Use the universal template from documentation/README.md.
- Every entry in the file table must correspond to an actual file (verified by Read).
- No ASCII art. Tables, lists, arrows ('→'), directory trees only.
- English only.
- If a section has nothing real to say, omit it.
Input outline (JSON): <outline>
Output: contents of AGENTS.md only, no commentary.
```
```
Verify <path>/AGENTS.md against the actual directory.
For every file/symbol mentioned, Read or grep to confirm.
Output JSON: { "missing_refs": [...], "stale_tables": [...] }.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tree -L 2 -I 'node_modules|.git'` | File tree for the structure section | https://mama.indstate.edu/users/ice/tree/ |
| `eza --tree --git-ignore` | Modern `tree` with gitignore awareness | https://eza.rocks |
| `markdownlint-cli2` | Lint generated markdown | https://github.com/DavidAnson/markdownlint-cli2 |
| `vale` | Prose lint, kills filler the LLM loves | https://vale.sh |
| `lychee` | Markdown link checker, catches broken refs | https://github.com/lycheeverse/lychee |
| `cspell` | Spell-check generated docs | https://cspell.org |
| `tokei` | LOC counts for the structure table | https://github.com/XAMPPRocky/tokei |
| `tree-sitter` queries | Extract exports/public API for the outline | https://tree-sitter.github.io |
| `ts-morph` / `astroid` | Per-language API extraction | https://ts-morph.com / https://astroid.readthedocs.io |
| `git ls-files` | Source of truth for "what exists" | git docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes | Schedule nightly drift check; PR check on doc updates |
| GitHub Copilot Workspace | SaaS | Yes | Tasks the LLM with repo-aware doc updates |
| Mintlify Writer | SaaS | Yes | Auto-generate doc updates on PRs |
| Cursor / Zed | SaaS / OSS | Yes | Inline LLM doc generation while editing |
| Backstage TechDocs | OSS | Indirect | Different audience (humans), but agent can dual-emit |
| `markdownlint` GH Action | SaaS | Yes | Enforces structure rules on PRs |
| Vale (with custom style) | OSS | Yes | Encodes "no ASCII art / no filler" as enforceable rules |

## Templates & scripts
The methodology already ships a universal `CLAUDE.md` template plus type-specific sections (Backend / Frontend / Infra / Library) in `templates.md`. Useful agent companion: a discovery script that builds the JSON outline.

```bash
#!/usr/bin/env bash
# doc-outline.sh — emit a JSON outline for a directory the writer agent will fill.
# Usage: doc-outline.sh path/to/dir
set -euo pipefail
DIR="$1"

jq -n \
  --arg dir "$DIR" \
  --argjson files "$(git ls-files "$DIR" | jq -Rsc 'split("\n")|map(select(length>0))')" \
  --argjson lang "$(tokei -o json "$DIR" 2>/dev/null | jq '.. | objects | select(.language) | {(.language): .code}' 2>/dev/null || echo '{}')" \
  --arg type "$(test -f "$DIR/package.json" && echo frontend \
                || test -f "$DIR/manage.py" && echo backend-django \
                || test -f "$DIR/pyproject.toml" && echo backend-python \
                || test -d "$DIR/terraform" && echo infra \
                || echo library)" \
  '{dir:$dir, type:$type, files:$files, languages:$lang}'
```

## Best practices
- Cap `AGENTS.md` at 80 lines and `CLAUDE.md` at @AGENTS.md only — enforce with markdownlint custom rule.
- Always pair AGENTS.md with a verification step that opens every referenced file; LLMs invent paths confidently.
- Co-locate doc generation with code edits in the same PR; nightly drift jobs are a fallback, not the primary path.
- Use `tree-sitter` or language-native AST for the API extraction step — regex misses nested classes, decorators, JSX exports.
- Forbid ASCII art and emojis in the prompt; LLMs default to them.
- Add a "Last verified: <commit hash>" footer; if the hash is more than N commits behind HEAD, mark stale in CI.
- For monorepos, generate one `AGENTS.md` per package and a top-level `INDEX.md` linking them; the agent reads only what it needs.

## AI-agent gotchas
- **Hallucinated files.** Most common failure. Mitigation: pass `git ls-files` output as the *only* source of file truth, and run a post-write verification step.
- **Length creep.** Agent expands to 200+ lines with redundant prose. Enforce a hard cap; reject and retry if exceeded.
- **Stale tables.** "Endpoints" / "Models" tables go stale after every refactor. Regenerate from AST, don't hand-edit.
- **Forbidden formatting.** Agent inserts ASCII boxes, banners, emojis. Add explicit "REJECT" rules and a markdownlint check.
- **Self-referential loops.** Agent reads its own previous draft and treats hallucinations as fact. Always start from raw repo state, not previous doc.
- **Multi-language confusion.** In monorepos with Python + TS + Go, the agent picks one and ignores the others. Pass per-package outlines, not whole-repo.
- **Human-in-loop checkpoint.** First-time generation in a directory should always be human-reviewed. Subsequent updates can be agent-merged if drift checks pass.

## References
- https://docs.anthropic.com/en/docs/claude-code/memory — `CLAUDE.md` semantics
- https://agents.md — community AGENTS.md spec
- Project convention: `skills/faion-claude-code/project-docs-convention/README.md`
- https://vale.sh, https://github.com/DavidAnson/markdownlint-cli2
- https://tree-sitter.github.io, https://ts-morph.com
- https://docs.divio.com/documentation-system/ — Diátaxis (audience-aware doc structure, complementary)
