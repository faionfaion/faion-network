# Problem Validation 2026

## Summary

**One-sentence:** Produces a quarterly problem-validation report (evidence ledger sorted on 5-level hierarchy + cold-respondent count + validated-or-hypothesis verdict) so problems are pinned to behavioral signals, not stated preferences.

**Ефективно для:** Solopreneur researchers who keep declaring problems 'validated' from warm-contact compliments and need a forced evidence-tier discipline.

**One-paragraph:** Survey-only validation and warm-contact interviews systematically over-report demand. This methodology pins all validation evidence onto a 5-level hierarchy (paid > committed > engaged-with-prototype > expressed-interest > stated-problem), requires ≥3 tier-1/tier-2 signals from cold, non-network respondents, and forces quarterly re-validation. Output is consumed by mvp-scoping and value-proposition-design.

## Applies If (ALL must hold)

- Pre-MVP: validate problem is real, painful, and worth paying for before writing code.
- Pivoting: re-validate problem assumptions when retention is low or engagement is sparse.
- Adjacent expansion: testing whether an existing segment has a related underserved problem.
- After a hypothesis breaks (low conversion, no upsell) to confirm the problem still holds.
- Discovery runs on a weekly cadence rather than as a single validation gate.
- The founder's interview style is drawing performance answers and the script needs the commitment-signal discipline.

## Skip If (ANY kills it)

- PMF is established with a paying user base — switch to feature-discovery and continuous-discovery.
- Incremental funnel optimization where A/B testing answers faster.
- Cannot reach the target segment within a week — you will over-rely on weak proxies.
- Commodity or undifferentiated problems where solution quality matters more than problem existence.
- No live discovery loop exists — the team can only interview once a quarter, so the iteration r4 schedules cannot happen.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| hypothesis statement | string | founder |
| interview transcripts (diarized) | files | recording tool |
| respondent network status | tag/cold|warm | researcher |
| prior quarter's evidence ledger | json | previous run |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/research/researcher/user-interviews` | Upstream — produces the transcripts this methodology scores. |
| `solo/research/researcher/value-proposition-design` | Downstream — consumes validated problem statements. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 9 testable rules with rationale + source, plus a skip-this-methodology fallback | ~1600 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 8 failure modes with detector + repair | ~1200 |
| `content/04-procedure.xml` | essential | 5 step procedure | ~700 |
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
| `templates/problem-validation-2026.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/problem-validation-2026.md.j2` | Markdown skeleton with the required fields. |
| `templates/problem-validation-2026.md` | Markdown skeleton with the required fields. Generated from `templates/problem-validation-2026.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-problem-validation-2026.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[user-interviews]] — related methodology.
- [[value-proposition-design]] — related methodology.
- [[single-interview-fast-loop-template]] — related methodology.
- [[validation-paralysis-breaker]] — related methodology.
- [[pain-point-research]] — upstream source of candidate problems to validate.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
