# Skills Directory

Claude Code skills for the faion-network framework.

## Active Skills

### Knowledge umbrella

| Skill | Description |
|-------|-------------|
| `faion-knowledge` | 52 domain knowledge bases, 1300+ methodologies. Tier-partitioned. Load content from `faion-knowledge/knowledge/<tier>/<group>/<name>/` on demand with Read. |

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

All domain knowledge consolidated inside `faion-knowledge/knowledge/`, partitioned by pricing tier:

```
faion-knowledge/
├── SKILL.md
├── CLAUDE.md
└── knowledge/
    ├── free/   (8)   dev core + marketing-manager
    │   ├── dev/        software-developer, python-developer, javascript-developer, testing-developer, code-quality, backend-developer, devtools-developer
    │   └── marketing/  marketing-manager
    ├── solo/  (13)   solopreneur essentials
    │   ├── dev/        frontend-developer, api-developer, software-architect, automation-tooling
    │   ├── infra/      server-craft
    │   ├── sdd/        sdd, sdd-planning
    │   ├── product/    product-planning, product-operations
    │   ├── ux/         ui-designer
    │   ├── marketing/  content-marketer, seo-manager
    │   └── comms/      communicator
    ├── pro/   (24)   enterprise / agency breadth
    │   ├── dev/        backend-systems, backend-enterprise
    │   ├── infra/      devops-engineer, cicd-engineer, infrastructure-engineer
    │   ├── pm/         pm-agile, pm-traditional, project-manager
    │   ├── product/    product-manager
    │   ├── ba/         business-analyst, ba-core, ba-modeling
    │   ├── ux/         ux-ui-designer, ux-researcher, user-researcher, accessibility-specialist
    │   ├── marketing/  growth-marketer, gtm-strategist, ppc-manager, smm-manager, conversion-optimizer
    │   ├── research/   market-researcher, researcher
    │   └── comms/      hr-recruiter
    └── geek/   (7)   AI agent-builder stack
        └── ai/         ml-engineer, ai-agents, rag-engineer, ml-ops, multimodal-ai, llm-integration, claude-code
```

Each skill folder: `SKILL.md` + methodology subfolders. Each methodology: 5-file pattern (`README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`).

## Statistics

| Metric | Count |
|--------|-------|
| User-invocable skills | 9 |
| Knowledge skills (inside faion-knowledge) | 52 |
| Methodologies | 1300+ |
| Tiers | 4 (free / solo / pro / geek) |

## Related

- Umbrella skill: [faion-knowledge/SKILL.md](faion-knowledge/SKILL.md)
- Tier manifest: [tier-manifest.json](tier-manifest.json)
