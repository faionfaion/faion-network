---
type: change-request
cr_id: CR-006
title: "sdd/templates and sdd/templates-planning: one content_id, two different payloads"
priority: P2
created: 2026-08-15
status: proposed
affected_components: [faion-network/skills/faion/knowledge/sdd, skills/tier-manifest.json]
---

# Change Request: the `sdd/templates` pair

**This document proposes nothing be deleted today.** It is the evidence for a decision the repo
owner makes. Both directories are still on disk and both still resolve.

Surfaced while fixing `regen-domains-xml.py` (which had been swallowing `sdd/templates` whole
because the slug collides with the name of a structural subdirectory). Once the generator stopped
dropping it, the pair became visible.

## What they share

| | |
|---|---|
| `content_id` | `180a580e913ae900` — **identical** |
| `tier` · `status` · `produces` · `est_tokens` | `solo` · `draft` · `spec` · 2000 — identical |
| `content/01-core-rules.xml` | **byte-identical** |
| `content/02-output-contract.xml` | **byte-identical** |
| `content/03-failure-modes.xml` | differs (48 diff lines) |

So the XML bodies were copied. That is the whole of the overlap.

## What they do not share — and this is the reversal

The template payloads have nothing in common.

**`sdd/templates`** (40 files, 53 KB) carries the **pre-F-067 five-file Markdown pattern** —
`README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md`, repeated across
seven subdirectories (`constitution/`, `design/`, `implementation-plan/`, `memory/`, `roadmap/`,
`spec/`, `task/`). That is precisely the shape `docs/methodology-xml-schema.md` records as
superseded. It is migration residue that survived inside a methodology directory rather than a
payload anyone authored for the current corpus.

**`sdd/templates-planning`** (13 files, 15 KB) carries eight real artefacts in the current shape:
`constitution.md`, `roadmap.md`, `implementation-plan.md`, `backlog-item.md`,
`confidence-check.md`, `pattern-record.json`, `mistake-record.json`, `new-feature.sh`. Five of
those exist nowhere else in the corpus.

## The reference asymmetry cuts the other way

| Slug | `[[wikilinks]]` | `<ref slug=>` |
|---|---|---|
| `templates` | **62** | 1 |
| `templates-planning` | **0** | 1 |

The better payload is the one nothing points at.

Worth weighing before treating 62 as a mandate: every one of those inbound links is a bare
`- [[templates]]` bullet sitting at line 77-78 of a `## Related` block in a `dev/` methodology's
`AGENTS.md`. That is the signature of a bulk-generated boilerplate row, not 62 authors each
deciding this methodology was relevant. Sampling a handful before acting would settle it.

## Options

1. **Merge and retire.** Move the eight real artefacts into `sdd/templates`, delete the seven
   legacy five-file subdirectories, retire `templates-planning`. All 62 links keep resolving,
   nothing unique is lost, and the pre-F-067 residue leaves the corpus. Costs: one merged
   `03-failure-modes.xml`, and a `content_id` that must be re-derived because it currently
   describes neither result.
2. **Keep `templates-planning`, retire `templates`.** Better name, better payload, but 62
   inbound links break and would need repointing — cheap only if the boilerplate reading above
   holds.
3. **Split properly.** Give each a distinct contract and `content_id` and let both live. Honest
   only if someone can state what each is *for*; today neither `AGENTS.md` distinguishes them.

## Adjacent, and arguably the bigger question

Both are `status: "draft"`. Two other things follow from that and neither is settled:

- A `draft` methodology sits in `tier-manifest.json` exactly like an active one, so the CLI will
  serve it by path to any solo subscriber — while the retriever may never surface it. If `draft`
  is meant to mean "not ready to sell", the manifest is the place that has to know.
- These are the only two `draft` methodologies in a 2,601-slug corpus. If the status is not going
  to mean anything, it should not be in the vocabulary.

## Recommendation

Option 1, contingent on the wikilink sample confirming the links are generated boilerplate. It is
the only option that both preserves every unique artefact and removes migration residue, and it
is the one whose blast radius is a single directory.

Do not execute without the owner's approval — CR-005 set the precedent that corpus deletion
carries a re-verification pass against disk before anything is removed.
