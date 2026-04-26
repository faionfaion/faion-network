# Project Closure

## Summary

Formal termination process for a project: obtain written deliverable acceptance, release resources, close contracts, capture lessons learned, archive documents, and transition to operations. Without a closure event, projects fade without official acceptance, resources stay allocated to finished work, and knowledge walks out with the team.

## Why

Informal endings leave ambiguous completion status, open vendor contracts (ongoing costs, liabilities), unarchived documentation, and no knowledge transfer. Formal closure enforces a hard boundary that unlocks people for new work, triggers financial reconciliation, and seeds future projects with lessons. Get acceptance in writing — verbal "looks good" does not hold at invoice time.

## When To Use

- End of any contracted or fixed-bid engagement requiring formal acceptance.
- Cancelled or descoped projects (closure must capture salvage value and lessons).
- Phase-gated programs at major milestone transitions (Phase 1 → Phase 2 closure).
- Internal projects transitioning from build to operate (handover to ops/support).

## When NOT To Use

- Continuous-flow or product teams — no closure event; only release boundaries.
- Solo throwaway prototypes — a `DONE.md` line is enough.
- Projects still in execution; premature closure loses incomplete deliverables.

## Content

| File | What's inside |
|------|---------------|
| `content/01-closure-process.xml` | Seven-step closure process: deliverable acceptance, admin closure, lessons, archiving, final report, ops transition, recognition. |
| `content/02-examples-antipatterns.xml` | Worked examples (normal and cancelled closure); antipatterns for skipping acceptance, resources, lessons, and celebration. |

## Templates

| File | Purpose |
|------|---------|
| `templates/closure-checklist.md` | Signed-off checklist covering acceptance, admin, resource release, knowledge, transition, and communication. |
| `templates/acceptance-form.md` | Per-deliverable acceptance form with criteria table, outstanding items, and signature block. |
| `templates/handover-doc.md` | Operations handover template: system overview, docs index, support tiers, known issues, monitoring, scheduled maintenance. |
| `templates/final-report.md` | Final project report skeleton: executive summary, deliverables, schedule/budget/scope/quality performance, lessons, transition info. |
| `templates/closeout-archive.sh` | Shell script to bundle project archive with per-category folders and SHA-256 manifest. |
