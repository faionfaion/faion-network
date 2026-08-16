---
type: findings
title: "The 7,126 placeholders that are not variables, and why"
created: 2026-08-16
status: informational
affected_components: [faion-network/skills/faion/knowledge, faion-network/skills/faion/templates, faion-network/skills/faion/tools/template-builder]
companion_to: "skills/faion/templates/vars-dictionary.schema.json"
implements: ".aidocs/conventions/template-jinja-migration.md §3"
---

# What could not become a dictionary entry

Companion to `skills/faion/templates/vars-dictionary.schema.json` (66 entries). Measured across
all **2,919** Markdown templates under `skills/faion/knowledge/*/*/templates/` with
`skills/faion/tools/template-builder/scripts/tpl-migrate.py --report`, plus a driver over the same
`build_plan()` that keeps each placeholder's heading, row label and surrounding line.

**Headline: the migration's biggest obstacle is not prose, it is rows.** **5,543 placeholders across
731 templates** — 21.1% of every placeholder, 25.0% of every template — sit in a **repeating row
structure**: a Markdown table row, or a list bullet whose shape repeats inside the same file. §2.3
has no loops, so a repeating row cannot be a variable at any price. Prose is the larger *reported*
bucket (2,549) but it is a per-placeholder problem an author fixes by writing a sentence; repeating
rows are a structural problem that no dictionary entry can reach.

> **Definition, because the first draft of this file got it wrong and the whole of §1 rests on it.**
> The measure is *not* "a line repeating verbatim" — that is a much rarer degenerate case, **563
> placeholders in 102 templates**, and it would not support the recommendation below. What actually
> blocks the migration is a row **shape** recurring with different contents, which is precisely what
> a `{% for %}` exists to express. Reproducer, run from `skills/faion/knowledge/`: count placeholders
> on lines matching `^\|`, plus placeholders on `^[-*+] ` bullets whose text is identical after
> replacing every placeholder with a constant and every digit run with `#`.
>
> Denominators differ between this section and the table below on purpose: this one counts raw
> placeholder matches (26,224); the table counts `tpl-migrate.py`'s classified *candidates* (14,959),
> which exclude code spans and fenced blocks.

## The surface

| | count |
|---|--:|
| Templates walked | 2,919 |
| Templates whose header the parser refuses | 254 |
| Templates with no placeholders at all | 1,050 |
| Placeholder candidates | 14,959 |
| …nameable (`verdict: parameter`) | 7,833 |
| …**not** nameable | **7,126 (47.6%)** |
| Distinct names the tool proposed | 2,262 |
| Dictionary entries written | 66 |

The gap between 2,262 proposed names and 66 entries is not lossy compression. 1,491 of the proposed
names occur exactly once, and most of the rest are the cases below.

## 1. Per-row table placeholders — no loop, no variable

**4,188 placeholders sit inside a Markdown table row** (546 templates), and another **1,355 sit on a
repeated-shape list bullet** (318 templates) — 5,543 over 731 distinct files. The clearest specimens:

| Row | Templates | Why it cannot be a variable |
|---|--:|---|
| `\| [input-1] \| [format] \| [source] \|` | 76 | Three columns × N rows. `input_1` was proposed 77 times, `format` 78, `source` 116 — one name each for what is really an unbounded list of triples. |
| `\| d1 \| <topic> \| <choice> \| <why> \|` | ~15 (infra) | `d1`, `d2`, `d3` are the same row three times. Declaring `topic` binds all three to one value. |
| `\| [Name] \| Direct \| YYYY \| $X \| … \|` | competitor tables | The 375 `[Name]` occurrences in this shape are *the competitor on this row*, not *a name*. |
| `- <input-name-1> (<source path or URL>)` | 20 | Same list, written as bullets instead of a table. |
| `\| [Task] \| [Task] \| [Task] \| [Task] \|` | story maps | Four identical placeholders on one line. |

The corpus's own workaround is **numbered siblings**, and the converter faithfully reproduces it:
**161 numbered families over 864 occurrences** — `input_1..3`, `url_1..2`, `question_1..3`,
`requirement_1..2`, `check_1..2`, `task_1..5`, `role_1..5`, `slug_1..10`. None of these is in the
dictionary. `slug_1` through `slug_10` is the shape of a `for` loop written out by hand, and blessing
it would put ten near-identical entries in a file whose whole purpose is that a name means one thing.

**Where a section is one answer, the dictionary took the section, not the rows.** `out_of_scope` and
`open_questions` are `type: array` with `x-faion-compose`, so the author answers once and an LLM
writes the bullets. That is the only shape that survives the no-loops rule, and it only works where
the rows are homogeneous prose. It does not work for a table with typed columns.

**Recommendation:** this is the strongest argument yet for revisiting §2.3's ban on loops, and it
should be argued on this evidence rather than on convenience. The SSTI reason for the ban is already
retired (`template-jinja-migration.md` §0); what remains is that a `{% for %}` over a value map is
not an injection surface either. Until then, 731 templates convert to a fixed number of rows or not
at all.

## 2. Prose masquerading as a variable — 2,549

The most common ones are instructions to a human wearing placeholder brackets:

| Text | Occurrences |
|---|--:|
| `[from AGENTS.md Applies If list]` | 78 |
| `<fill per the schema in \`content/02-output-contract.xml\`>` | 55 |
| `<fill per \`04-procedure.xml\` step outputs>` | 55 |
| `<TODO: list inputs per Prerequisites>` | 47 |
| `<TODO: produce artefact matching 02-output-contract>` | 47 |
| `<Optional: 'ready for owner review' or links to validator output.>` | 59 |

Declaring any of these produces a build that refuses by name for a parameter that should never have
existed — `template-jinja-migration.md` §5, and the converter is right to refuse them.

A subtler group is **directive text that reads like a value**: `<one paragraph>`, `<one sentence>`,
`<one-line>`, `[List variations]`, `[Describe variations]` (180 occurrences classified
`instruction`). These are not variables, but several of them *mark* one: `<one paragraph>` under
`## Scope summary` is why `scope_summary` exists with `x-faion-compose: true`. The rule that fell out:
**a length instruction is evidence of a composed field, never of a typed one.**

## 3. Placeholders that are examples, not slots — 2,061

1,947 sit in inline code spans and 114 inside fenced blocks. `<FILL>` appears 174 times inside
backticks; `<path-to-filled-json>` 74 times inside a `Run \`python scripts/validate-*.py --file
<path-to-filled-json>\`` line. Substituting there would change what the example demonstrates.

**504 templates contain at least one.** They are not blockers — the converter leaves them alone —
but they are why "template has placeholders" is not the same as "template needs parameters."

## 4. The 1,183 HTML-escaped placeholders — a prerequisite, not a finding

`&lt;artefact_id&gt;` (117), `&lt;source path or URL&gt;` (116), `&lt;ISO date&gt;` (62),
`&lt;handle or email — single named human, never "team"&gt;` (59), `&lt;kebab-case-slug&gt;` (58).
Concentrated in **133 templates**, heaviest in `ai-core` (234), `marketing` (218), `product` (216)
and `backend` (185).

Every one of these is a placeholder the dictionary *already covers* — `artefact_id`,
`evidence_source_ref`, `last_reviewed_date`, `owner_handle`, `artefact_slug`. They are unreachable
only because someone escaped them. `template-jinja-migration.md` §6 already books this as a
prerequisite; this measurement says how much it buys: **un-escaping 133 files converts 1,183
placeholders with no naming decisions at all**, the cheapest single step in the migration.

## 5. Names whose meaning genuinely varies by domain

These are the ones I could have written an entry for and deliberately did not, because no single
question fits every use. Each is absent from the dictionary on purpose.

| Proposed name | Uses | Domains | Why it has no entry |
|---|--:|--:|---|
| `name` | 676 | 17 | The corpus's worst variable, and §3 says so. It resolves to `owner_full_name`, `reviewer_name`, `engagement_name`, `competitor_name` (per-row), `component_name`, `flow_name`, `persona_name` and `feature_name` depending on the line it sits on. There is no `name` entry and there must never be one. |
| `value` | 165 | 8 | **140 of the 165 are `ai-agents` writing `- \`<config_key>\`: <value>`** — the meaning lives in the backticked key beside it, which changes every line (`eval_budget_usd`, `agent_kind`, `loader`, `prompt_template`). The other 25 are business value in a benefits table. Two unrelated things, and the big one is a per-row slot. |
| `source` | 116 | 11 | Three meanings: a citation (`evidence_source_ref`), a table column in the `[input-1]` row, and a migration origin (`Migrate from [Source] to [Target]`, a `system_name`). |
| `date` | 267 | 10 | Five meanings — produced-on, last-reviewed, due, session, per-row event. All five are in the dictionary under their own names; `date` itself is not. |
| `action` | 89 | 10 | A next action (`next_action`), a procedure step, the `when [action]` clause of an acceptance criterion, and a per-row remediation cell. |
| `format` | 78 | 6 | 76 of them are the `[format]` column of the `[input-1]` row. Not a variable, a column. |
| `x`, `y` | 119 | 8 | `[X%]`, `[$X]`, `[X]`, `<±X>` — a value *shape*, never a name. 74 of the 200 collision refusals are these two. |
| `list` | 62 | 10 | The type of an answer, not the answer. Every use needs the label beside it to mean anything. |
| `description`, `title`, `type`, `id`, `item`, `who`, `why` | 185 | 4–9 each | Column headers. Each names its row's subject, and the row changes. |
| `role` | 65 | 8 | Split into `owner_role` and `user_role` — see the dictionary. A third sense (a channel's role in a funnel) is per-row and got nothing. |
| `target` | 25 | 6 | Split into `metric_target`, `target_audience` and `system_name`. Three questions, one spelling. |

## 6. Two smaller refusal classes worth naming

**Composite identifiers (`no-context`, 178).** `artefact_id: <slug>-<client>-<YYYY-MM-DD>` is one
line holding three variables plus punctuation. The converter names the *last* component
`artefact_id`, which is wrong — it is the date. The dictionary carries `artefact_id`,
`artefact_slug`, `client_slug` and `artefact_date` as four independent entries with a `$comment`
saying why nothing derives one from another: §2.3 has no expressions.

**Rating scales (`unnameable`, 130).** `[1-5]`, `[0-4]`, `[1-4]`, `<1-10>` — a range, in a cell,
under a heading like "Performance Ratings (1–5)". The range is the *type*; the meaning is the row.
`ux/heuristic-evaluation` alone carries 36 of them, one per heuristic. Per-row again, so no entry.

## 7. What this list is worth

The 66-entry dictionary covers the artefact **envelope** — identity, dates, the people, the client,
the evidence, the verdict — and that envelope is where the convergence money is. The single best
number in this whole exercise: **814 templates carry an `owner` slot, in roughly 30 distinct
spellings** (`<@handle>` 189, `<Full Name> <email>` 71, `&lt;handle or email — single named human,
never "team"&gt;` 59, `<name>` 55, `@name (role)` 42, `<named-human>` 21, `role:<handle>` 19,
`<single-named-handle>` 15, `<role:person>` 15, `<name @handle>` 15, and twenty more). One meaning,
thirty spellings, and after this file: four entries — `owner_full_name`, `owner_email`,
`owner_handle`, `owner_role` — with `reviewer_name`, `author_name`, `sponsor_name`,
`session_facilitator` and `next_action_owner` split off because they are genuinely other people.

The body of each artefact is a different problem. It is mostly tables, it is mostly per-row, and
**no dictionary fixes it.** Section 1 is the change request hiding in this document.

## 8. `sensitive` conflates two surfaces, and the dictionary is what exposed it

Nine entries are `x-faion-sensitive`, and eight of them are people: `owner_full_name`, `owner_email`,
`owner_handle`, `reviewer_name`, `author_name`, `sponsor_name`, `session_facilitator`,
`next_action_owner`, plus `candidate_name`. Every one is correct under `template-builder.md` §5a,
whose test is *"would this value identify a person, or open a door?"*

The consequence is only visible now that a dictionary exists. §5 says a sensitive parameter is
**never written to the project store** — verified in `tplcore.py`: `store_put()` records
`{"sensitive": true, "placeholder": …}` and nothing else, and `save_store()` raises outright if a
sensitive entry carries a value. So the field that **814 templates** carry, in roughly 30 spellings,
is the one field a project can never remember. Every artefact re-asks who the owner is.

**The rule is doing two jobs and only one of them holds here.** `sensitive` means both:

1. *the value must never reach the multi-tenant assembler* — §2.2's actual threat, and
2. *the value must never be cached in `<project>/.faion/template-params.json`* — a local file on the
   author's own disk.

For a **credential** both hold, and (2) is the stronger one: the rendered artefact contains only the
placeholder, so caching the secret locally would be a genuinely new exposure.

For **personal data** only (1) holds. The rendered artefact sits in the same project directory with
the owner's name in plaintext inside it — that is the entire point of rendering it. A store next to
it holding the same name is not a new exposure; refusing to hold it protects nothing and costs the
store its dominant use.

**Not changed here.** §5 and §5a are ratified, and this is an argument for splitting one flag into
two (`travels: false` / `cached: false`, or `sensitive` plus `personal`), which is a contract change
and belongs to whoever owns §2.2 — not to a findings file. Recorded with the evidence so the decision
can be made on it: **the first real use of `sensitive` at corpus scale made the project store useless
for the corpus's single most common field.**
