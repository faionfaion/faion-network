# User Story Mapping

## Summary

A two-dimensional arrangement of user stories along a horizontal user-journey axis (activities → tasks) and a vertical priority axis (essential → nice-to-have), producing a story map that reveals the complete user experience and enables slice-based release planning. The BA owns scope definition: turning the map into formal artifacts (BRD, BPMN, traceability matrix, JIRA epics).

## Why

Flat backlogs lose journey context, making release planning a guessing game. Story mapping surfaces the walking skeleton — the thinnest vertical slice that delivers a coherent end-to-end experience — and lets a mixed business/IT audience agree on release scope using a single shared artifact. BABOK v3 §10.46 names it as the canonical technique for linking stories to process steps and traceability.

## When To Use

- Sprint-zero or pre-discovery session where the BA must convert a fuzzy idea into a stakeholder-signed release plan.
- Brownfield project with a flat 200+ ticket backlog needing journey context before re-prioritization.
- Compliance/regulated project where each story must trace to a process step, regulation clause, and acceptance criterion.
- Vendor migration: the existing journey is the backbone, gap analysis fills the cells.
- Stakeholder alignment with mixed business + IT audience who need to agree on a release slice.

## When NOT To Use

- Maintenance backlog of isolated bug fixes and tech debt — no journey, use WSJF or RICE instead.
- Pure API/platform product with no end-user persona — model with C4 + use cases.
- Team already on a stable release cadence with a healthy backlog and clear roadmap — rebuilding the map is sunk cost.
- One-off internal automation (single user, single happy path) — a 5-step checklist beats a wall map.
- Stakeholders cannot commit 2-4 contiguous hours — a half-attended map produces false consensus.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Story map structure, five-step mapping procedure, release-slicing strategies, and MVP definition. |
| `content/02-workshop.xml` | Workshop agenda, participant roles, common mistakes, and anti-patterns including agent-specific gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/story-map.md` | Story map document template with backbone, walking skeleton, and per-activity release tables. |
| `templates/user-story.md` | User story template with Given/When/Then acceptance criteria structure. |
| `templates/render-ba-package.py` | Script: story-map JSON → BRD.md + RTM.csv (BABOK Requirements Package). |
