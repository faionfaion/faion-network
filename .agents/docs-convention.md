# Documentation Convention

Applies to every directory in every project, not just repo roots. Canonical methodology:
`skills/faion/knowledge/claude-code/project-docs-convention/` (read `content/01-core-rules.xml`).

## Directory pattern

```
any-dir/
├── CLAUDE.md       # Always: @AGENTS.md (Claude Code entrypoint)
├── AGENTS.md       # Essential context for THIS dir (20-80 lines, auto-loaded)
├── .agents/        # Detailed reference docs (on-demand)
│   └── INDEX.md    # Full index of .agents/ contents
└── .aidocs/        # SDD lifecycle docs (project roots only)
    └── INDEX.md    # Full index of .aidocs/ contents
```

- `CLAUDE.md` = always `@AGENTS.md`, nothing else.
- `AGENTS.md` = what this dir IS + commands + gotchas. Mentions the `.agents/INDEX.md` path.
- `.agents/` = architecture, API refs, decisions, deep dives.
- `.product/` = per-project SDD + product docs (specs, designs, plans, roadmap).
- `.aidocs/` = workspace-level SDD (multi-repo projects like NERO).

## The five testable rules

1. **CLAUDE.md is just a ref** — exactly the line `@AGENTS.md` (plus at most a one-line note).
2. **Line budget** — `AGENTS.md` is 20-80 lines. Past 80, content moves to `.agents/<topic>.md` and `AGENTS.md` indexes it.
3. **Per-module coverage** — every directory containing source code carries the pair: subpackages, module folders, test dirs. Empty `__init__.py`-only dirs are the only exemption.
4. **Required sections** — one-line dir purpose, file table, key types / commands, gotchas.
5. **`.agents/` for deep content** — architecture, API references and decision records live there with an `INDEX.md`; `AGENTS.md` links by relative path.

## Cost constraint

Gloaguen et al. (ETH Zurich + LogicStar, arXiv, Feb 2026) is the only controlled study of these files:

- human-written context files: +4% task success at +19% inference cost
- machine-generated ones measurably hurt: -0.5% on SWE-bench Lite, worse in 5 of 8 settings
- every variant: +20-23% cost, 14-22% more reasoning tokens
- repository-overview sections specifically measured unhelpful — the agent derives them from the files anyway

Consequences:

- Never auto-generate prose for a submodule `AGENTS.md`. Where one is genuinely needed, write a stub of at most 30 lines carrying commands, conventions and boundaries only — no directory listing, no dependency list, no architecture overview.
- If a directory has nothing non-obvious to say, leave it without a pair. A missing file beats a generated one.

Full write-up: `skills/faion/knowledge/sdlc-ai/context-file-cost-budget/`.
