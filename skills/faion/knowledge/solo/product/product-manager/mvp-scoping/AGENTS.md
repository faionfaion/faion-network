# MVP Scoping

## Summary

A six-step process for compressing a feature backlog into a minimum viable product:
define the core problem, identify the single job the product must do, categorise all
features with MoSCoW, validate scope fits the timeline, and define explicit "won't
have" and kill-signal criteria. The hard rules: Must-Haves capped at 5, total
Must+Should effort must fit the timebox (4-8 weeks), and every scope document requires
a learning goal and a failure criterion.

## Why

Founders build either too much (a 6-month "MVP" with 50 features) or too little to
deliver value. Without a framework, scope is determined by enthusiasm not evidence.
The MoSCoW + timebox combination forces trade-offs to be explicit; the kill-signal
requirement prevents the MVP from becoming an unfalsifiable experiment — if you
cannot say what evidence kills the idea, you will ship regardless of what you learn.

## When To Use

- Solo founder or small team turning a validated problem into a buildable first slice.
- Existing feature backlog has 30+ ideas and needs compression to a 4-8 week slice.
- Pivot: prior MVP failed, leaner re-scope with explicit "won't have" boundaries needed.
- New vertical or persona entry requiring an anchored smaller release.

## When NOT To Use

- Problem itself is unvalidated — run product-discovery and problem-validation first.
- Compliance/regulated products (medical, fintech KYC) where "minimum" violates statutory requirements.
- Feature parity migration of a production system — scope is dictated by parity, not learning.
- Mature product with a polished user base; "minimum" disappoints loyal users — use mlp-planning.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | MVP definition, MVP vs MLP distinction, MoSCoW priority table with scope percentages. |
| `content/02-process.xml` | Six-step scoping process: problem definition, core value identification, feature categorisation, MoSCoW application, scope validation, definition of done. |
| `content/03-examples.xml` | Time-tracking app and course platform worked examples with must/won't-have lists and learning goals. Antipatterns with fixes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mvp-scope-doc.md` | Full MVP scope document: problem statement, feature scope by MoSCoW category, constraints, learning goals, definition of done. |
| `templates/mvp-quick-check.md` | Five-question quick validator: solves one problem, delivers value today, minimum feature list, deferrals, timeline fit. |
| `templates/lint-scope.py` | Python validator: checks must-have count, learning goal, kill signal, wont-have list, and effort vs budget. |
