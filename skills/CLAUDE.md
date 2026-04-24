# Skills Directory

Claude Code skills for the faion-network framework.

## Active Skills

### Knowledge umbrella

| Skill | Description |
|-------|-------------|
| `faion-knowledge` | 52 domain knowledge bases, 1300+ methodologies. Load content from `faion-knowledge/knowledge/<group>/<name>/` on demand with Read. |

### Applied tools

| Skill | Description |
|-------|-------------|
| `faion-brainstorm` | Multi-agent diverge/converge/review for ideation |
| `faion-sdd-execution` | Quality gates, code review cycle, pattern/mistake memory |
| `faion-feature-executor` | Sequential SDD task execution with quality gates |
| `faion-improver` | Session-based audit/improve loop |
| `faion-media-ops` | Media pipeline templates |

### NERO-specific

| Skill | Description |
|-------|-------------|
| `nero-context` | NERO context loading |
| `nero-improve` | NERO improvement loop |
| `nero-tools` | NERO tooling |

## Knowledge Structure

All domain knowledge consolidated inside `faion-knowledge/knowledge/`:

```
faion-knowledge/
├── SKILL.md
├── CLAUDE.md
└── knowledge/
    ├── dev/          (13)  Python, JS, Go, Rust, Java, C#, backend, frontend, API, testing, architecture, automation, code quality
    ├── ai/            (7)  ML, agents, RAG, ML ops, multimodal, LLM integration, Claude Code
    ├── infra/         (4)  DevOps, CI/CD, infrastructure, server craft
    ├── product/       (3)  PM, planning, operations
    ├── pm/            (3)  Project, Agile, Traditional
    ├── ba/            (3)  BA, core, modeling
    ├── ux/            (5)  UX/UI, UI, UX research, user research, accessibility
    ├── marketing/     (8)  Marketing, GTM, content, growth, CRO, SEO, PPC, SMM
    ├── research/      (2)  Researcher, market research
    ├── comms/         (2)  Communicator, HR recruiter
    └── sdd/           (2)  SDD, SDD planning
```

Each skill folder: `SKILL.md` + methodology subfolders. Each methodology: 5-file pattern (`README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`).

## Statistics

| Metric | Count |
|--------|-------|
| User-invocable skills | 9 |
| Knowledge skills (inside faion-knowledge) | 52 |
| Methodologies | 1300+ |

## Related

- Umbrella skill: [faion-knowledge/SKILL.md](faion-knowledge/SKILL.md)
- Tier manifest: [tier-manifest.json](tier-manifest.json)
