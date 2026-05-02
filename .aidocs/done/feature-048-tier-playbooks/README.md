# Feature 048: Tier Playbooks

**Status:** TODO
**Est. tokens:** ~650k (orchestrator + 4 authoring waves)
**Complexity:** High (volume-driven; 120 playbooks across 4 tiers)

## Summary

Introduce a new `tier-playbook` entity to the faion knowledge ecosystem. Tier playbooks are standalone, actionable how-to guides (e.g., "Buy a domain on Namecheap", "Build an MCP server", "First hire developer") organized by pricing tier and grouped by topic. They sit parallel to `knowledge/` (methodology corpus) and `workflows/` (orchestration patterns).

400-idea catalog generated via 4-tier multi-persona brainstorm; top 30 per tier (= 120) selected for the first implementation wave. Remaining 280 stay in catalog as TIER-2 backlog.

## Scope

| In | Out |
|----|-----|
| Convention spec at `.aidocs/conventions/playbooks/` | Workflow-bound playbooks (already specced under `workflows/playbook-spec.md`) |
| Folder structure under `skills/faion/playbooks/` | Authoring of TIER-2 catalog (remaining 280) |
| Updates to `faion/SKILL.md`, `faion/CLAUDE.md`, `skills/CLAUDE.md`, `tier-manifest.json` | Public site rendering of playbooks (separate FE feature) |
| Validator script `scripts/validate-tier-playbook.py` | Translation to UK/PL/DE |
| 120 playbooks (30 per tier) authored | Extending `/faion` retrieval to index playbooks (deferred) |

## Why Now

- Free + Solo audience needs concrete how-to content to convert preview → paid.
- Pro + Geek tiers need depth differentiators (USP moat = CLI integration + SDD).
- Knowledge corpus answers "what to know"; playbooks answer "what to do today".
- Direct revenue gating: Free playbooks honor 30% preview rule (hook); Solo+ unlocks lift conversion.

## Boundary vs. workflow-bound playbook

Two distinct entities share the term "playbook" intentionally — both are *actionable adaptations of underlying knowledge*, but they differ in axis of adaptation.

| Property | Workflow playbook | Tier playbook (this feature) |
|----------|-------------------|------------------------------|
| Spec | `.aidocs/conventions/workflows/playbook-spec.md` | `.aidocs/conventions/playbooks/playbook-spec.md` (NEW) |
| Path | `workflows/<slug>/playbooks/<surface>.md` | `skills/faion/playbooks/<tier>/<group>/<slug>/` |
| Bound to | one workflow + one surface | one tier + one topic |
| Audience | LLM agent executing workflow phases | Human or agent following standalone how-to |
| Required `## Methodologies` table | yes (surface-specific) | yes (tier-bound, all citations tier ≤ playbook tier) |
| Section count | 12 fixed | 8 fixed |

## Documents

- `spec.md` — requirements + acceptance criteria
- `design.md` — folder shape, file shape, citation rules, conventions, SKILL.md amendments
- `implementation-plan.md` — 7 phases (3 setup + 4 authoring waves), pool-based dispatch
- `test-plan.md` — drift sentinels, validator rules, wave + feature acceptance
- `catalog/all-400-ideas.md` — full brainstorm output (Free/Solo/Pro/Geek × 100)
- `catalog/priority-120.md` — top 30 per tier, implementation queue

## Brainstorm provenance

4-tier multi-persona brainstorm via /faion-brainstorm methodology. Per tier: 4 personas × ~25 ideas → cluster → rank → top 30. Outputs preserved verbatim in `catalog/all-400-ideas.md` (ranking + citation samples included).

## Related

- `.aidocs/conventions/workflows/playbook-spec.md` — sibling entity (workflow playbook)
- `skills/faion/CLAUDE.md` — umbrella entry point
- `skills/tier-manifest.json` — tier-to-path map (extends with playbook_paths in phase 2)
- `rules/skill-authoring.md` — mandatory pre-edit reading for any skill change
