---
slug: research-repo-file-naming-convention
tier: solo
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a research-repo filename + folder spec (slug grammar + manifest.json schema + lifecycle folders) so AI-assisted synthesis can locate, group, and cite artefacts deterministically."
content_id: "348e58871164216a"
complexity: light
produces: spec
est_tokens: 3400
tags: [research-ops, user-research, naming-convention, taxonomy, ai-friendly]
---

# Research Repo File-Naming Convention

## Summary

**One-sentence:** Produces a research-repo filename + folder spec (slug grammar + manifest.json schema + lifecycle folders) so AI-assisted synthesis can locate, group, and cite artefacts deterministically.

**Ефективно для:** Solo researchers whose transcript-and-screenshot pile outgrew Drive search and whose LLM synthesis can't find what it needs.

**One-paragraph:** Solo researchers accumulate transcripts, recordings, notes, and exports faster than they can organise them. This methodology pins a single, slug-based filename grammar (project-study-participant-date-type-language), a lifecycle folder tree (recruit → run → tag → synthesise → archive), and a manifest.json the synthesis layer reads. Output is consumed by user-interviews and downstream synthesis pipelines.

## Applies If (ALL must hold)

- Solo researcher OR small team (≤3 people) with a single research repo.
- AI-assisted synthesis is in use OR planned (vector store, LLM tagger, clusterer).
- Artefacts include text, audio, video, and exports AND ≥50 artefacts accumulate per quarter.
- Repository is the canonical store (not just a backup).

## Skip If (ANY kills it)

- Enterprise research-ops with a platform (Dovetail, EnjoyHQ, Marvin) that already enforces taxonomy.
- Single-shot validation with <10 artefacts total — convention overhead exceeds the value.
- Team disagrees on every naming decision — convention requires single-source authority.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| target repo location | path | operator |
| anonymisation policy | rule | researcher |
| study-type list | array | researcher |
| export format from recording tool | string | tool |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/research/researcher/user-interviews` | Produces the artefacts this convention organises. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
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
| `templates/research-repo-file-naming-convention.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/research-repo-file-naming-convention.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-research-repo-file-naming-convention.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[user-interviews]] — related methodology.
- [[problem-validation-2026]] — related methodology.
- [[single-interview-fast-loop-template]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
