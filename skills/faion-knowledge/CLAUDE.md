# Faion Knowledge

**Entry Point:** `/faion-knowledge`

Umbrella knowledge skill: 52 domain knowledge bases, 1300+ methodologies. Tier-partitioned. No sub-skill invocation — load content from `knowledge/<tier>/<group>/<name>/` on demand with Read.

## Structure

```
knowledge/
├── free/   8 skills   dev core + marketing-manager router
├── solo/  13 skills   frontend/API/architect/automation/SDD/product/UI/content/SEO/comms
├── pro/   24 skills   enterprise backend/DevOps/PM/BA/UX research/paid marketing/research/HR
└── geek/   7 skills   ml-engineer, ai-agents, rag-engineer, ml-ops, multimodal-ai, llm-integration, claude-code
```

Each tier → per-group subdirs (`dev/`, `infra/`, `marketing/`, etc.). Each skill = folder with `SKILL.md` + methodology subfolders. Each methodology = 5-file pattern (`README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`).

## How to Use

```
User task → Identify domain → Resolve tier → Read knowledge/<tier>/<group>/<name>/README.md → Apply
```

No `Skill(faion-X)` calls — sub-skills no longer exist as separate invocable skills.

Tier gating: free reads `free/`; solo reads `free/ + solo/`; pro reads `free/ + solo/ + pro/`; geek reads all four.

**Full routing:** [SKILL.md](SKILL.md) · **Tier manifest:** [../tier-manifest.json](../tier-manifest.json)

---

*Faion Network v4.1*
