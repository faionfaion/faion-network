# Playbook: <Delivery Surface>

<One paragraph: what this surface is, when this playbook applies, what the canonical run looks like.>

## Trigger

<How a user typically asks for this batch (example phrasings or ticket shapes).>

## End-to-end flow

```
PHASE 1 — INTAKE & CLARIFY
  ├─ <surface-specific intake notes>
  └─ <surface-specific clarification themes>

PHASE 2 — PLAN
  └─ <where feature folders live for this surface>

PHASE 3 — SETUP LOCAL ENV
  ├─ <command(s) to bring the local stack up>
  └─ <data fixtures or env overrides typically needed>

PHASE 4 — BASELINE CAPTURE (optional, visual only)

PHASE 5 — WAVE EXECUTION
  └─ <wave-grouping heuristics for this surface>

PHASE 6 — VERIFY & REVIEW LOOP
  ├─ <build / test commands>
  └─ <review focus points specific to this surface>

PHASE 7 — RECAPTURE & DELIVER (visual only)

PHASE 8 — CLOSE & DEPLOY
  └─ <deploy mechanism for this surface>
```

## Parallelism heuristics

| Variant / area | Files typically touched |
|----------------|-------------------------|
| <area A> | `<file A>` |
| <area B> | `<file B>` |

## Pitfalls

1. <observed pitfall 1 + mitigation>
2. <observed pitfall 2 + mitigation>

## Checklist before declaring done

- [ ] All feature folders moved `todo/ → done/`.
- [ ] All task files moved through their lifecycle.
- [ ] Release notes updated with one entry per ticket under today's date.
- [ ] Visual evidence (before + after) delivered for every visual feature.
- [ ] Tracker statuses updated.
- [ ] Deploys / pushes performed only after explicit user authorization.
