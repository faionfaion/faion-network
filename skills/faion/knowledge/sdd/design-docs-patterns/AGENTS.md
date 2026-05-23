# Design Docs Patterns

## Summary

**One-sentence:** Produces a design-doc spec (format selection rule + required sections + non-goals + ≥2 genuine alternatives + review deadline) so any feature >1 engineering day ships with a doc that captures the why.

**Ефективно для:** Solo devs whose 'I'll just code it' decisions keep getting re-debated three months later when someone asks why.

**One-paragraph:** Design docs collapse to no-doc or boilerplate copy when patterns aren't pinned. This methodology pins the format-selection rule (lightweight Google-style for team-scoped, heavier 6-pager / RFC for cross-org), required sections (context / goals / non-goals / proposed / alternatives / open questions), non-goals discipline, and the ≥2-genuine-alternatives bar. Output is consumed by ADR extraction and code-review-cycle.

## Applies If (ALL must hold)

- Feature implementation takes > 1 engineering day.
- Change has architectural or cross-cutting implications.
- Multiple alternatives genuinely exist.
- Decision will be revisited or questioned.

## Skip If (ANY kills it)

- Pure-copy changes with no logic.
- Trivial bug fixes with clear root cause.
- Decisions reversible inside a single PR.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| decision title | string | author |
| scope classification | small | team | cross-org | PM |
| alternatives shortlist | array | author |
| review audience list | array | PM |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/design-docs-big-tech` | Sibling — big-tech survey informs format selection. |
| `solo/sdd/sdd/architecture-decision-records` | Downstream — ADRs extract from accepted design docs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/design-docs-patterns.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/design-docs-patterns.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-design-docs-patterns.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[design-docs-big-tech]] — related methodology.
- [[architecture-decision-records]] — related methodology.
- [[code-review-cycle]] — related methodology.
- [[living-documentation]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
