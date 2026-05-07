# Skills Directory

Claude Code skills for the `faion` plugin (repo: faion-network).

## Active Skills

### Knowledge umbrella

| Skill | Description |
|-------|-------------|
| `faion` | 52 domain knowledge bases, 1300+ methodologies. Tier-partitioned. Load content from `faion/knowledge/<tier>/<group>/<name>/` on demand with Read. |
| `faion/playbooks` | Standalone how-to guides at `faion/playbooks/<tier>/<group>/<slug>/playbook.md`. Tier-gated parallel to knowledge. Spec: `.aidocs/conventions/playbooks/playbook-spec.md`. |

### Applied tools

All applied workflows are accessed via the `/faion` umbrella — auto-routed by context. Sub-folders under `faion/workflows/`: `brainstorm`, `improver`, `media-ops`, `poll-agents`, `sdd-batch-orchestrator`. SDD execution theory lives in `faion/knowledge/solo/sdd/sdd/`.

### NERO-specific

| Skill | Description |
|-------|-------------|
| `nero-context` | NERO context loading |
| `nero-improve` | NERO improvement loop |
| `nero-tools` | NERO tooling |

## Knowledge Structure

All domain knowledge consolidated inside `faion/knowledge/`, partitioned by pricing tier:

```
faion/
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
    └── geek/   (8)   AI agent-builder stack + SDLC+AI
        ├── ai/         ml-engineer, ai-agents (84), rag-engineer, ml-ops, multimodal-ai, llm-integration, claude-code
        └── sdlc-ai/    (52) lang/lint/test/tracker/kb/task/mr/inc/sec/gov methodologies wiring AI agents into the SDLC floor
```

Each skill folder: `SKILL.md` + methodology subfolders. Each methodology: 5-file pattern (`README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`).

## Statistics

| Metric | Count |
|--------|-------|
| User-invocable skills | 9 |
| Knowledge skills (inside faion) | 52 |
| Methodologies | 1300+ |
| Tiers | 4 (free / solo / pro / geek) |

## Related

- Umbrella skill: [faion/SKILL.md](faion/SKILL.md)
- Tier manifest: [tier-manifest.json](tier-manifest.json)
