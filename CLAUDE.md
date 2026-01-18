# Claude Code Instructions

## Git Commits

- 50 chars title, optional body
- NO "Co-Authored-By: Claude"
- NO emojis
- Format: `type: short description`

## Language

- **User:** Ukrainian
- **Docs/code:** English (saves ~30% tokens)
- **Subagent prompts:** English

## Documentation

**NO ASCII ART.** Allowed: tables, lists, arrows (`→`), directory trees.

## Directory Structure

**Full documentation:** [docs/directory-structure.md](docs/directory-structure.md)

```
~/.claude/                    # Global framework (faion-network)
├── skills/faion-*-skill/
├── agents/faion-*-agent.md
└── docs/

{project}/                    # Project root
├── .claude/                  # Project-specific config
│   └── {project}-*-skill/   # Project skills (gitignored)
└── aidocs/sdd/{project}/    # SDD documentation
    ├── constitution.md
    ├── features/{status}/{NN}-{feature}/
    └── tasks/{status}/
```

**Lifecycle:** `backlog/ → todo/ → in-progress/ → done/`

## Token Efficiency

**Symbols:** `→` leads to | `⇒` transforms | `✅` done | `❌` failed | `⚠️` warning

**Abbrev:** `cfg` config | `impl` impl | `perf` perf | `sec` security | `dep` dependency

## SDD Memory

```
~/.sdd/memory/
├── patterns_learned.jsonl
├── mistakes_learned.jsonl
└── session_context.md
```

## References

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
