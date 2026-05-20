---
slug: ai-story-truth-checklist
tier: geek
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "5eccf185523afd2e"
summary: A discrete BA checklist that vets AI-generated user stories for plausibility-but-wrong shapes — invented personas, conflated jobs, fabricated metrics, missing edge cases — before they enter the backlog.
tags: [user-stories, ba, ai-codegen, story-vetting, geek]
---
# AI Story Truth Checklist

## Summary

**One-sentence:** A discrete 8-point checklist the BA runs on every AI-generated user story to vet for the "plausible-but-wrong" failure mode — invented personas, conflated jobs, fabricated metrics, missing edge cases — before the story enters the team backlog.

**One-paragraph:** AI assistants generate user stories at velocity, but the dominant failure mode is "looks like a story, doesn't match reality": invented personas not in the actual user research, conflated jobs (login + onboarding lumped together), fabricated metrics ("25% of users want X" with no data), missing edge cases (no failure path, no offline mode, no privacy implication), missing acceptance criteria, story tense / voice violations, dependencies hand-waved, and out-of-scope features sneaking in. This methodology gives the BA an 8-point checklist they run on every AI-drafted story. Output: a per-story score and a `pass / revise / scrap` decision. Stories enter the backlog only after passing.

## Applies If (ALL must hold)

- BA owns the story-quality gate for the team's backlog.
- AI-generated stories are an active input (Claude, Cursor, ChatGPT, internal LLM).
- User research artefacts exist (personas, JTBD statements, interview notes) for cross-reference.
- A documented acceptance-criteria style guide exists in the repo.

## Skip If (ANY kills it)

- BA does not own the backlog gate — escalate to whoever does.
- Team has no user-research artefacts to validate against — the checklist's persona / metric checks have nothing to compare to.
- Stories are technical-only (e.g. tech debt) — different vetting applies.
- Process is in transition (e.g. story-mapping workshop in flight) — defer.

## Prerequisites

- Persona file or persona index (e.g. `personas.yaml`).
- JTBD statements or equivalent user-research artefact (`research/jtbd.md`).
- Acceptance-criteria style guide (`backlog/style-guide.md`).
- A `backlog/incoming/` folder where AI-drafted stories land before vetting.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/user-story-fundamentals` | Background on canonical story shape. |
| `solo/research/researcher/jtbd` (or pro variant) | JTBD statements are the truth anchor for the conflation check. |
| `geek/ba/business-analyst/ai-enabled-business-analysis` | Sibling: this checklist is the operational counterpart. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: persona-in-roster, JTBD-anchored, no fabricated stats, edge cases enumerated, AC traceable | ~1100 |
| `content/02-output-contract.xml` | essential | Story-vetting record schema, decision rule, traceability map | ~800 |
| `content/03-failure-modes.xml` | essential | 6 LLM-specific story failure modes with detectors | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `persona-match` | haiku | Mechanical: persona name lookup |
| `jtbd-conflation-check` | sonnet | Bounded judgement: does the story conflate two jobs? |
| `stat-verification` | sonnet | Bounded: trace claims to research artefacts |
| `vetting-aggregate` | opus | Cross-checklist synthesis; final pass / revise / scrap |

## Templates

| File | Purpose |
|------|---------|
| `templates/vetting-record.json` | Per-story vetting record |
| `templates/checklist.md` | The 8-point checklist with concrete prompts |
| `templates/style-guide.md` | Story / AC style reference |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/vet-story.py` | Run the checklist on a single story; emit vetting record | Per story in backlog/incoming |
| `scripts/batch-vet.py` | Run vetting on all incoming stories; produce daily summary | Daily |

## Related

- parent skill: `geek/ba/business-analyst/`
- peer methodologies: `ai-enabled-business-analysis`, `user-story-fundamentals`, `acceptance-criteria-writing`
- external: [Mike Cohn user-story guidance](https://www.mountaingoatsoftware.com/) · [INVEST criteria](https://en.wikipedia.org/wiki/INVEST_(mnemonic)) · [JTBD canonical: Christensen](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done)
