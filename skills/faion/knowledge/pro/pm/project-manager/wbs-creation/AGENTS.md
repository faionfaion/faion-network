# WBS Creation

## Summary

Hierarchical decomposition of project scope into deliverable-oriented work packages using the 100% rule. Each node in the tree is a noun (an output), not a verb (an activity). The lowest level items — work packages — are estimable (8-80 hours), assignable to one owner, and have explicit acceptance criteria documented in a WBS Dictionary.

## Why

Without a WBS, scope is ambiguous: estimates are guesses, dependencies are invisible, and forgotten work surfaces too late to recover. The 100% rule forces completeness at every level — if all children are done, the parent is done. Deliverable orientation (nouns not verbs) keeps the tree stable when implementation decisions change.

## When To Use

- Predictive/waterfall projects with fixed scope at kickoff (agency contracts, ERP rollouts, hardware launches)
- Hybrid delivery: WBS at program level, sprints underneath each work package
- Cost-loaded schedules and EVM tracking — WBS is the spine for cost accounts
- Migration projects (data, system, vendor) where every artefact must be enumerated
- Compliance projects (SOC2, HIPAA, ISO 27001) where 100% rule maps to control coverage

## When NOT To Use

- Pure-agile teams driven by a product backlog — WBS calcifies what should flex
- Discovery / R&D where deliverables are emergent — use a hypothesis backlog instead
- Fast-moving startup product work where scope changes weekly — overhead exceeds value
- Solo work on a feature under 2 weeks — a checklist beats a WBS

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | 100% rule, deliverable orientation, 8/80 rule, depth limits, required overhead packages |
| `content/02-wbs-dictionary.xml` | Dictionary entry structure, mandatory fields, acceptance criteria, examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/wbs-outline.md` | Hierarchical WBS outline skeleton with numbered levels |
| `templates/wbs-dictionary-entry.md` | Single work-package dictionary card with all required fields |
| `templates/wbs-validate.py` | Validator: 100% rule + 8-80h leaf check against wbs.yaml |
