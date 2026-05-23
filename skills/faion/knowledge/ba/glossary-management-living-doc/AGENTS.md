# Glossary Management (Living Doc)

## Summary

**One-sentence:** Living-doc glossary lifecycle (intake → definition → conflict resolution → deprecation → propagation) producing a single-source-of-truth term registry with audit-able conflict-resolution records and term-usage hooks across docs/code/tests.

**One-paragraph:** Solves the recurring BA pain where business terms drift between PRDs, code, tests, and support copy until the team debates which 'customer' the bug ticket means. Single intake channel for new terms, definition template (term, definition, scope, owner, status, examples, aliases, conflicts-with), resolution path (pick winner OR split into two terms), deprecation flow (mark term deprecated, route to replacement, track usage to zero), propagation hooks into product docs, code constants, test plans, support macros. Primary output: a glossary entry that travels with the term across every artifact.

**Ефективно для:**

- Команд із 3+ стейкхолдер-груп, де "customer" в білінгу і в support означає різне.
- DDD проєктів з bounded contexts, де scope визначення критичний.
- Підтримки PRD/spec linting: будь-який не-тривіальний noun лінкає на glossary.
- Onboarding new-hires — їх перше джерело істини щодо термінів.

## Applies If (ALL must hold)

- project has ≥3 distinct stakeholder groups (product, eng, support).
- ≥1 documented incident traceable to terminology drift.
- documentation surface exists (Confluence/Notion/internal wiki/repo /docs).
- BA or product owner willing to be the glossary maintainer (single owner, not committee).

## Skip If (ANY kills it)

- Single-person team — implicit shared vocabulary is sufficient.
- One-off project with no expected maintenance phase.
- Consumer-facing product with stable, well-known vocabulary.
- Team unwilling to update glossary as part of every PRD / spec.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Documentation tool with versioning | Notion / Confluence / repo | knowledge management |
| Terminology debt inventory | Markdown / CSV | BA |
| PRD template hook | Markdown | product / BA |
| Single glossary maintainer | named individual | team |
| Audit script venue | CI / cron | engineering |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/requirements-traceability` | Traceability consumes glossary entries linked to requirement IDs. |
| `pro/ba/business-analyst/elicitation-techniques` | Source new term proposals from sessions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `term_extraction_from_doc` | haiku | Scan PRD/spec, propose new terms not yet in glossary. |
| `definition_drafting` | sonnet | Synthesise candidate definition from usage contexts. |
| `conflict_resolution_proposal` | opus | Two definitions collide — deep cross-stakeholder synthesis. |
| `propagation_diff_check` | sonnet | Compare glossary entry vs code constants / tests / macros. |

## Templates

| File | Purpose |
|------|---------|
| `templates/glossary-entry.json` | JSON Schema for one term entry. |
| `templates/glossary-page.md` | Markdown page template for the maintained glossary surface. |
| `templates/conflict-resolution-record.md` | Record of a resolution: parties, dispute, decision, date. |
| `templates/_smoke-test.json` | Minimum viable filled-in entry. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-glossary-management-living-doc.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[requirements-traceability]]
- [[elicitation-techniques]]
- [[requirements-documentation]]
- [[modern-ba-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
