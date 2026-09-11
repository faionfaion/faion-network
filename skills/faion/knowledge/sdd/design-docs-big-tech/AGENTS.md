# Design Docs at Big Tech Companies

## Summary

**One-sentence:** Produces a design-docs reference report (per-company format + trigger rules + LLM-assistance limits + common mistakes) so solo and small-team operators pick the right design-doc shape for their scope.

**Ефективно для:** Solo devs cargo-culting Amazon 6-pagers for one-day features because they read a blog post once.

**One-paragraph:** Big-tech design-doc practices differ widely by company; copying the wrong format wastes a week per doc. This methodology surveys Google, Amazon, Uber, Spotify, Stripe, Netflix, Microsoft, Airbnb, Shopify, and Atlassian — covering document names (RFC / ERD / 6-Pager / ADR), review formats, and trigger rules. The core rules: write before coding; match weight to scope; always include 'do nothing' as an alternative. Output is consumed by design-docs-patterns.

## Applies If (ALL must hold)

- Operator considering which design-doc format to use.
- Cross-team or cross-org decision needs heavyweight review.
- Solo operator wants a 1-2 page version of big-tech practice.
- Onboarding new devs to the team's doc culture.

## Skip If (ANY kills it)

- One-day features — use a 1-paragraph note.
- Pure-content changes — no design rationale needed.
- Single-person hobby project with no future readership.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| decision scope | small | team | cross-org | PM |
| audience list | array | PM |
| review deadline | date | operator |
| template library | folder | repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/design-docs-patterns` | Sibling — patterns reference this survey. |
| `solo/sdd/sdd/architecture-decision-records` | Sibling — ADRs extract from design docs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 10 testable rules with rationale + source; company practices (Google, Amazon, Uber, Spotify, Stripe, Meta, Microsoft, Shopify, Atlassian), when-to-write table, LLM effectiveness | ~2400 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 7 failure modes with detector + repair (incl. doc-as-spec, no alternatives, doc after code, >10 approvers) | ~1000 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching (incl. RFC/ADR split, LLM alternatives cap) to rule-id conclusions | ~550 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/design-docs-big-tech.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/design-docs-big-tech.md.j2` | Markdown skeleton with the required fields. |
| `templates/design-docs-big-tech.md` | Markdown skeleton with the required fields. Generated from `templates/design-docs-big-tech.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-design-docs-big-tech.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[design-docs-patterns]] — related methodology.
- [[architecture-decision-records]] — related methodology.
- [[living-documentation]] — related methodology.
- [[key-trends-summary]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
