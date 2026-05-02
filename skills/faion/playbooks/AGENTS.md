# Tier Playbooks

Standalone how-to guides organized by pricing tier. Parallel to `../knowledge/`.

```
playbooks/
├── free/   tech-setup, hosting-infra, dev-fundamentals, business-discovery, mvp-essentials, marketing-fundamentals, cost-free-stack, ops-basics
├── solo/   sdd-workflow, frontend-launch, api-design, server-craft, automation, product-planning, product-ops, ui-design, content-marketing, seo-essentials, comms-stakeholder, launch-operations, solo-ops-finance
├── pro/    client-engagement, delivery-ops, team-management, business-analysis, product-management, devops-cicd, infra-engineering, backend-systems, ux-research, growth-marketing, paid-acquisition, smm-cro, market-research, hr-ops
└── geek/   rag-pipelines, ai-agents, llm-integration, prompt-engineering, context-engineering, mcp-protocol, claude-code-skills, evaluation, ai-safety, ml-ops, fine-tuning, multimodal, cost-optimization, ai-product-positioning, ai-consultancy-ops
```

## File shape

Each playbook is `<tier>/<group>/<slug>/playbook.md` (+ optional `checklist.md`, `templates.md`, `examples.md`, `references.md`).

8 front-matter keys (name, description, tier, group, status, owner, last_verified, version) + 7 H2 sections in fixed order: `Goal`, `Prerequisites`, `Steps`, `Verify`, `Troubleshooting`, `Next`, `References`.

## Tier inheritance for citations

Same boundary as `../knowledge/`:

| Playbook tier | May cite from |
|---------------|---------------|
| free | `knowledge/free/` only |
| solo | `knowledge/free/ + solo/` |
| pro | `knowledge/free/ + solo/ + pro/` |
| geek | all four tiers |

Slugs are unique across tiers.

## Authoring

- Spec: `.aidocs/conventions/playbooks/playbook-spec.md`
- Validator: `python3 scripts/validate-tier-playbook.py <path>` (exits 0 on success)
- Author prompt template: `.aidocs/conventions/playbooks/author-prompt.md`
- Catalog: `.aidocs/in-progress/feature-048-tier-playbooks/catalog/priority-120.md`

## Boundary vs. workflow playbook

| | Tier playbook (here) | Workflow playbook |
|--|---------------------|-------------------|
| Path | `skills/faion/playbooks/<tier>/<group>/<slug>/` | `skills/faion/workflows/<wf>/playbooks/<surface>.md` |
| Bound to | tier + topic | workflow + surface |
| Spec | `.aidocs/conventions/playbooks/playbook-spec.md` | `.aidocs/conventions/workflows/playbook-spec.md` |

## Related

- `../SKILL.md` § Playbooks — entry point
- `../../tier-manifest.json` — `playbook_root`/`playbook_paths` per tier
