# Constitution.md

## Summary

**One-sentence:** Produces `constitution.md` — at most twenty standing rules, each surviving a four-part admission test and carrying a one-sentence why written *before* the rule — small enough that every phase can afford to load all of it, every time.

**One-paragraph:** Half a dozen agent-SDLC frameworks demand a "Constitution Gate" and none of them says what a constitution is, so the file gets written as a dumping ground: framework versions, API shapes, domain facts, aspirations. It grows past the point where any phase loads it, and an unread rule is not a rule. This methodology fixes the shape instead of the content. Admission is a four-part test — durable, cross-cutting, contestable, checkable — and everything failing it is routed somewhere it belongs, most often to `project-spec/`. The twenty-rule cap is not a style preference; it is the enabling constraint that keeps the file cheap enough to load into planning, execution, review and readiness alike. Stable `R-NN` ids make a rule citable in a review verdict. The one-sentence why is elicited before the rule is drafted, because a rule whose reason cannot be stated first is a preference, and preferences do not survive their first inconvenient sprint. What this methodology cannot do is enforce meaning: the bundled validator checks structure — count, cap, why present, ids sequential, footer parses — and nothing else. Semantic compliance is a review activity performed by a human or an agent that has read the diff.

**Ефективно для:**

- Any project where an agent writes code and keeps re-litigating a decision that was settled months ago.
- Repos where `decisions.md` has become an append-only log nobody reads, and the standing set has to be extracted from it.
- Bootstrap: the moment after the first architecture decisions lock and before the first feature is planned.
- Handover — to a contractor, a co-founder, or the next agent session.

## Applies If (ALL must hold)

- The project has made at least three decisions that will constrain future work and will otherwise be re-argued.
- Somebody or something reads project context at the start of a task, and paying for that context is a real cost.
- The decisions are contestable — a competent person could have chosen otherwise.

## Skip If (ANY kills it)

- No decision has been made yet. A constitution written before the first hard choice records aspirations, not constraints, and every aspiration in it will later be violated silently.
- The candidate rules are all domain facts, business rules, data model or deploy topology — those belong in `project-spec/`, and a constitution that absorbs them stops being loadable.
- The project is a throwaway spike. Its output is learning, and learning does not need standing rules.
- What is actually wanted is a decision *history*. That is `decisions.md` / ADRs — append-only, one entry per choice, never pruned. The constitution is the standing set; a stale rule there is amended, not appended to.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Seven testable rules: the admission test, the twenty cap, why-before-rule, stable ids, compliance, amendment and versioning, and the `project-spec/` delegation. |
| `content/02-output-contract.xml` | The exact file shape — Sync Impact Report, sections, `R-NN` blocks, footer — and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six ways a constitution dies, including the one this methodology cannot prevent: nothing checks that the code obeys it. |
| `content/06-decision-tree.xml` | Admission routing for one candidate rule: in, or to `project-spec/`, `roadmap.md`, `decisions.md`, or nowhere. |
| `scripts/validate-constitution-md.py` | Structural validator: rule count, word cap, why present, ids sequential, sections present, footer parses, no unresolved placeholders. `--draft` relaxes the placeholder check; `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/constitution.md.j2` | Deliberately empty. Every rule slot is a `TODO(...)` placeholder and the examples live in HTML comments, so the template can never pre-load somebody else's opinions into your project. |
| `templates/constitution.md` | Deliberately empty. Every rule slot is a `TODO(...)` placeholder and the examples live in HTML comments, so the template can never pre-load somebody else's opinions into your project. Generated from `templates/constitution.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

- `project-spec-structure` — where domain facts, business rules, data model and deploy topology go. The delegation pointer in the constitution's Scope section names this location; the two files fail together if either absorbs the other.
- `architecture-decision-records` — the history. One ADR per decision, append-only. The constitution holds the standing consequences of those decisions, and it is amended rather than appended.
- `client-conventions-as-code` — the next step for any rule that turns out to be mechanically checkable: move it into a linter and cite the linter from the rule.
- `quality-gates-confidence` — how a compliance statement becomes a gate that actually blocks something.
- `ai-convention-anchoring` — why an agent re-derives conventions it was told once, and what changes when the rules are short, numbered and always loaded.
