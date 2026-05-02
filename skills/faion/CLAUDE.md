# Faion Knowledge

**Entry Point:** `/faion`

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

## Workflows

End-to-end orchestration patterns under [workflows/](workflows/AGENTS.md). The umbrella skill `/faion` auto-routes to one of these by context (see `description` in SKILL.md):

- `workflows/brainstorm/` — multi-agent diverge-converge-review (consent gate runs first if user did not request brainstorm)
- `workflows/sdd-batch-orchestrator/` — single-feature or multi-feature SDD batch (study → clarify → plan → wave-execute → verify → review → fix → close)
- `workflows/improver/` — session review + system audit + fix-apply-log-commit cycle
- `workflows/media-ops/` — AI media pipeline (interview → propose → scaffold → infra → content → register)
- `workflows/poll-agents/` — self-replenishing background-agent pool for long task queues

## Playbooks

Standalone how-to guides at [playbooks/](playbooks/AGENTS.md), parallel to `knowledge/`. Each playbook = one task at one tier (free/solo/pro/geek). Tier inheritance for citations is identical to knowledge: free playbook may only cite `knowledge/free/`; solo cites `free/ + solo/`; etc.

```
playbooks/
├── AGENTS.md
├── free/   tech-setup, hosting-infra, dev-fundamentals, business-discovery, mvp-essentials, marketing-fundamentals, cost-free-stack, ops-basics
├── solo/   sdd-workflow, frontend-launch, api-design, server-craft, automation, product-planning, product-ops, ui-design, content-marketing, seo-essentials, comms-stakeholder, launch-operations, solo-ops-finance
├── pro/    client-engagement, delivery-ops, team-management, business-analysis, product-management, devops-cicd, infra-engineering, backend-systems, ux-research, growth-marketing, paid-acquisition, smm-cro, market-research, hr-ops
└── geek/   rag-pipelines, ai-agents, llm-integration, prompt-engineering, context-engineering, mcp-protocol, claude-code-skills, evaluation, ai-safety, ml-ops, fine-tuning, multimodal, cost-optimization, ai-product-positioning, ai-consultancy-ops
```

Spec: `.aidocs/conventions/playbooks/playbook-spec.md`. Validator: `scripts/validate-tier-playbook.py`.

---

*Faion Network v4.1*
