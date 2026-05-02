# Feature 048: Tier Playbooks — Specification

## Goal

Introduce **tier-playbook** as a first-class content entity in faion-network: standalone, actionable how-to guides organized by pricing tier (free/solo/pro/geek), parallel to `knowledge/`. First wave delivers 120 playbooks (30 per tier).

## Non-Goals

- Workflow-bound playbooks (already specced)
- Authoring of TIER-2 catalog (remaining 280)
- Public site rendering
- Translations
- Extending `/faion` retrieval skill to index playbooks

## Functional Requirements

### F1 — Entity definition

A tier playbook is a self-contained how-to for one specific task / decision / setup. It MUST:
- Live at `skills/faion/playbooks/<tier>/<group>/<slug>/playbook.md`
- Have a kebab-case slug, ≤40 chars, regex `^[a-z][a-z0-9-]{2,40}$`
- Be unique-by-slug across all tiers (no duplicate slugs in different tiers)
- Cite ≥1 methodology from `skills/faion/knowledge/` (tier ≤ playbook tier)

### F2 — Tier inheritance for citations

| Playbook tier | May cite from |
|---------------|---------------|
| free | `knowledge/free/` only |
| solo | `knowledge/free/ + solo/` |
| pro | `knowledge/free/ + solo/ + pro/` |
| geek | all four tiers |

Cross-playbook citations follow the same `tier ≤` rule.

### F3 — Required playbook structure

`playbook.md` MUST contain in order:

1. Front-matter (YAML, 7 keys: `name`, `description`, `tier`, `group`, `status`, `owner`, `last_verified`, `version`)
2. `## Goal` — one-paragraph "what you will have after"
3. `## Prerequisites` — bullet list (assumed knowledge, accounts, tools, prior playbooks)
4. `## Steps` — numbered, action-leading verbs, real commands/snippets (no `foo`/`bar`)
5. `## Verify` — concrete confirmation of success
6. `## Troubleshooting` — known pitfalls + fixes
7. `## Next` — pointers to related playbooks/methodologies
8. `## References` — methodology citations with rationale

Optional companion files (same folder): `checklist.md`, `templates.md`, `examples.md`, `references.md`.

### F4 — Discovery surface

The following must be updated to expose playbooks:

| File | Change |
|------|--------|
| `skills/faion/SKILL.md` | Add "Playbooks" body section (no frontmatter change) |
| `skills/faion/CLAUDE.md` | Add playbooks tree parallel to knowledge tree |
| `skills/CLAUDE.md` | Add row to skills index pointing at `faion/playbooks/` |
| `skills/tier-manifest.json` | Add `playbook_root` + `playbook_paths` per tier |
| `skills/faion/playbooks/AGENTS.md` (NEW) | Orientation, ≤80 lines |
| `skills/faion/playbooks/<tier>/AGENTS.md` (NEW per tier) | Tier index, ≤80 lines |

### F5 — Validator

`scripts/validate-tier-playbook.py <playbook.md path>` MUST:

1. Parse front-matter; assert all 8 required keys present + valid values
2. Parse markdown; assert 7 `## ...` sections present in order
3. For each `## References` entry: parse citation path, assert resolves under `skills/faion/knowledge/`
4. Assert each citation tier ≤ playbook tier (tier order: free=0, solo=1, pro=2, geek=3)
5. Assert slug regex match
6. Exit 0 on success, 1 on failure with line-numbered errors

### F6 — Convention spec

Create `.aidocs/conventions/playbooks/`:
- `CLAUDE.md` (`@AGENTS.md`)
- `AGENTS.md` (boundary, when to author, validation, related; ≤80 lines)
- `playbook-spec.md` (full spec: front-matter schema, 8 sections, citation rules, drift sentinels, anti-patterns, inline template)

Update `.aidocs/conventions/workflows/AGENTS.md` to point at the new spec for the boundary clarification.

## Non-Functional Requirements

### NF1 — Authoring budget per playbook

- `playbook.md` body: ≤5k tokens
- AGENTS.md per group/tier: ≤80 lines
- Optional companion files: each ≤3k tokens

### NF2 — Cross-tier dedupe

Same slug must not exist in two tiers. Slugs reflect the audience-relevant scope; "vps-first-deploy" belongs in solo, not duplicated in pro. Topics that span tiers should be split into different slugs (free `buy-domain-namecheap` ≠ solo `cloudflare-dns-zones`).

### NF3 — Preview gating consistency

Free tier playbooks honor the existing 30% preview rule from `tier-manifest.json`. Higher tiers: 0% preview (full content visible to that tier or above).

### NF4 — Methodology citation specificity

Every citation rationale MUST be specific to the playbook (no generic "this methodology explains X"). Anti-pattern: empty rationale or boilerplate.

### NF5 — Action-leading language

Every step + section header uses imperative verbs. No theory paragraphs in the steps section.

## Success Criteria (Acceptance)

| # | Criterion | Verification |
|---|-----------|--------------|
| AC1 | Convention spec exists | `.aidocs/conventions/playbooks/playbook-spec.md` resolves; AGENTS.md ≤80 lines |
| AC2 | 120 playbooks authored (30 per tier) | `find skills/faion/playbooks -name playbook.md \| wc -l` = 120 |
| AC3 | All citations resolve, tier ≤ | Validator exits 0 on every playbook |
| AC4 | tier-manifest.json updated | `jq '.tiers.free.playbook_paths' tier-manifest.json` non-empty for each tier |
| AC5 | Discovery files updated | `faion/SKILL.md`, `faion/CLAUDE.md`, `skills/CLAUDE.md` mention playbooks section |
| AC6 | Catalog files complete | `catalog/all-400-ideas.md` lists 400; `priority-120.md` lists 120 |
| AC7 | No duplicate slugs cross-tier | Validator script checks |
| AC8 | Spec compliance | Random 5 playbooks per tier reviewed against `playbook-spec.md` |

## Risks

| Risk | Mitigation |
|------|------------|
| Subagent drift in playbook style | Tight prompt template with example + validator gate |
| Citation hallucination (paths don't exist) | Validator runs in-loop during authoring, not post-hoc |
| Slug collisions across tiers | Pre-check during dispatch; fail-fast |
| Volume causes context overload | Pool-based dispatch (5-8 parallel); each subagent handles 1-2 playbooks |
| Free-tier content trivial / not useful | Persona-mix in brainstorm (4 personas) ensures coverage; review pass on random 3 per wave |

## Dependencies

- `.aidocs/conventions/workflows/playbook-spec.md` (sibling, already exists; only updated for boundary cross-link)
- `skills/faion/knowledge/` corpus (citation targets must exist — validator checks)
- `skills/tier-manifest.json` (extended in phase 2)
