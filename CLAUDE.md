# Claude Code Instructions

## Git Commits

- Keep commit messages concise (50 chars title, optional body)
- NO "Co-Authored-By: Claude" or any Claude mentions
- NO emojis in commits
- Format: `type: short description` (feat, fix, refactor, docs, chore)

## Language Rules

**User communication:** Ukrainian (користувач спілкується українською)

**Documentation & code:** English (saves ~30% tokens)

**Subagent context:** English — when calling Task tool, provide prompts in English for token efficiency

## Documentation Rules

**NO ASCII ART.** Save context.

### Allowed:
- Tables
- Numbered/bulleted lists
- Inline arrows: `A → B → C`
- Directory trees (├── format)

### Forbidden:
- Box diagrams (┌─────┐)
- ASCII flowcharts
- Unicode box-drawing for diagrams

## SDD Structure

```
aidocs/sdd/{project}/
├── constitution.md                  # Project principles
├── roadmap.md                       # Milestones, progress, risks
├── product_docs/                    # PRD, personas, etc.
├── tasks/                           # Standalone tasks (no feature)
│   └── {backlog,todo,in-progress,done}/
└── features/
    ├── backlog/                     # Features waiting for grooming
    │   └── {NN}-{feature}/
    │       └── spec.md              # Draft spec
    ├── todo/                        # Features ready for execution
    │   └── {NN}-{feature}/
    │       ├── spec.md
    │       ├── design.md
    │       ├── implementation-plan.md
    │       └── tasks/{backlog,todo,in-progress,done}/
    ├── in-progress/                 # Features being executed
    │   └── {NN}-{feature}/
    └── done/                        # Completed features
        └── {NN}-{feature}/
```

**Feature Lifecycle:**
`backlog/ → todo/ → in-progress/ → done/`

**Task Lifecycle:**
`tasks/backlog/ → tasks/todo/ → tasks/in-progress/ → tasks/done/`

## Token Efficiency

### Symbols (30-50% compression)
- `→` leads to | `⇒` transforms | `←` rollback
- `✅` done | `❌` failed | `⚠️` warning | `🔄` in progress
- `⚡` perf | `🛡️` security | `🏗️` architecture

### Abbreviations
`cfg` config | `impl` implementation | `perf` performance | `sec` security | `val` validation | `req` requirement | `dep` dependency

### Progressive Context Loading
- Layer 0: Bootstrap (50 tokens) - minimal start
- Layer 1: Intent (100 tokens) - what are we doing
- Layer 2: Selective (500-3K) - load what's needed
- Layer 3: Deep (10-20K) - full architecture
- Layer 4: External (20-50K) - docs, research

## SDD Memory System

```
~/.sdd/memory/
├── patterns_learned.jsonl    # Successful patterns
├── mistakes_learned.jsonl    # Errors + solutions
├── workflow_metrics.jsonl    # Execution metrics
└── session_context.md        # Current state
```

Use `/faion-reflexion` to record patterns and learn from mistakes.

## References

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Custom Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Private Skills](docs/PRIVATE_SKILLS.md) - how to add project-specific skills not synced to faion-network
