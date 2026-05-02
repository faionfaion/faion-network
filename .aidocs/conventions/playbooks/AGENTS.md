---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
applies_to: skills/faion/playbooks/
---

# Tier Playbooks Conventions

Authoritative spec for the **tier playbook** entity under `skills/faion/playbooks/<tier>/<group>/<slug>/`.

## What lives here

| File | Read when |
|------|-----------|
| `playbook-spec.md` | Authoring or auditing a tier playbook. Front-matter, 8 sections, citation rules, anti-patterns, inline template. |

## Boundary vs. workflow playbook

Two entities share the term "playbook" intentionally — both adapt underlying knowledge into actionable form. They differ in axis of adaptation.

| Property | Tier playbook (this spec) | Workflow playbook |
|----------|---------------------------|-------------------|
| Spec | this folder | `../workflows/playbook-spec.md` |
| Path | `skills/faion/playbooks/<tier>/<group>/<slug>/playbook.md` | `skills/faion/workflows/<workflow>/playbooks/<surface>.md` |
| Bound to | one **tier** + one **topic** | one **workflow** + one **surface** |
| Section count | 8 fixed | 12 fixed |
| Audience | human or agent following standalone how-to | LLM agent executing workflow phases |
| Citation table | `## References` (tier ≤ playbook tier) | `## Methodologies` (surface-specific) |

If your draft adapts *along surface* — author it as a workflow playbook. If it adapts *along topic + audience tier* — author it here.

## Tier inheritance for citations

| Playbook tier | May cite from |
|---------------|---------------|
| free | `knowledge/free/` only |
| solo | `knowledge/free/ + solo/` |
| pro | `knowledge/free/ + solo/ + pro/` |
| geek | all four tiers |

Slugs are unique across tiers.

## Validation

`scripts/validate-tier-playbook.py <playbook.md>` enforces:

- 8 front-matter keys present + valid
- 7 H2 sections present in order
- Citation paths resolve under `skills/faion/knowledge/`
- Citation tier ≤ playbook tier
- Slug regex `^[a-z][a-z0-9-]{2,40}$`
- Rationale ≥10 chars, non-generic
- No `foo`/`bar`/`example.com` placeholders in Steps

Run before every commit; CI re-runs on push.

## Related

- `../workflows/playbook-spec.md` — sibling spec (workflow-bound playbook)
- `../workflows/workflow-spec.md` — orchestration pattern spec
- `../../in-progress/feature-048-tier-playbooks/` — first wave (120 playbooks)
- `skills/tier-manifest.json` — tier-to-path map (drives validator tier ordering)

## When to author

Add a tier playbook when **all** apply:

- Topic is a self-contained how-to (one user goal, ≤90 minutes of work).
- Topic does not duplicate an existing playbook in the same tier or below.
- ≥1 methodology in `knowledge/` (at allowed tier) covers the underlying theory.
- The catalog `priority-120.md` lists it (or an explicit user request).

Otherwise, file an idea in `.aidocs/in-progress/feature-048-tier-playbooks/catalog/all-400-ideas.md` for future selection.
