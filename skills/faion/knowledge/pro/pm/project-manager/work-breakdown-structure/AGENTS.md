# Work Breakdown Structure

## Summary

A deliverable-oriented hierarchical decomposition of project scope into work packages — noun-based nodes (outputs), not verbs (activities). Each level represents 100% of its parent (100% rule). Leaf nodes (work packages) satisfy the 8-80 hour rule and carry a Dictionary entry with acceptance criteria, owner, and dependencies. The WBS is the scope baseline; schedule and cost are derived from it, not contained in it.

## Why

Without a WBS, scope is ambiguous: team members build different things, estimates are guesses, and hidden dependencies surface too late. The deliverable orientation (nouns not verbs) keeps the structure stable when implementation changes. The 100% rule forces completeness — it eliminates forgotten work packages before scheduling or costing begins.

## When To Use

- Translating an approved scope statement or SOW into an estimable, assignable work-package tree before scheduling and costing
- Bidding on fixed-scope work requiring bottom-up estimation
- Validating the 100% rule on a hand-drafted plan: diff WBS against scope statement
- Re-baselining after a change request — mutate only the affected branch

## When NOT To Use

- Pure Scrum or Kanban teams where the product backlog is the decomposition — an extra WBS creates two sources of truth
- Discovery or research projects where less than 30% of scope is known — the WBS below level 2 will be fabricated
- Solo work on a feature under 2 weeks — a checklist is simpler
- Projects with emergent deliverables (innovation, R&D, platform exploration) — use rolling-wave planning instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-decomposition-rules.xml` | Deliverable orientation, 100% rule, 8/80 rule, ID stability, required overhead packages, depth limits |
| `content/02-wbs-dictionary.xml` | Dictionary entry structure, mandatory fields, antipatterns, two worked examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/wbs-template.md` | Hierarchical WBS outline with PM + all major branches |
| `templates/wbs-dict-entry.md` | Single work-package Dictionary card |
| `templates/wbs-validate.py` | Validator: weight_pct 100% rule + 8-80h leaf rule against wbs.yaml |
