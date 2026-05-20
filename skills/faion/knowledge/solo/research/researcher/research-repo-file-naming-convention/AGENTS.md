---
slug: research-repo-file-naming-convention
tier: solo
group: researcher
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "08ffd119d5509cd4"
summary: Filename and folder convention for a user-research repository so AI-assisted synthesis (RAG, agent tools, LLM tagging) can locate, group, and cite artefacts deterministically.
tags: [research-ops, user-research, naming-convention, taxonomy, ai-friendly]
---

# Research Repo File-Naming Convention

## Summary

**One-sentence:** Filename and folder convention for a personal-scale user-research repository (≤1 researcher, ≤300 artefacts) so AI synthesis tools find, group, and cite the right files deterministically.

**One-paragraph:** Solo researchers and UX-of-one founders accumulate transcripts, notes, screenshots, recordings, survey exports, and synthesis docs faster than they can organise them. Synthesis playbooks assume retrievable artefacts but the corpus is silent on how to make them retrievable for AI assistance. This methodology pins a single, slug-based file convention covering: project-prefix, study-type, participant-id (anonymised), date, asset-type, and language. Mechanism: every artefact carries enough metadata in the filename that a vector store, grep, or LLM agent can recover it without reading the body; folder structure mirrors study lifecycle (recruit → run → tag → synthesise → archive) so progress is visible from `ls`. Primary output: a `research/` tree that survives one researcher's memory and is RAG-readable.

## Applies If (ALL must hold)

- solo researcher OR small team (≤3 people) with a single research repo
- AI-assisted synthesis is in use OR planned (vector store, LLM tagger, transcript clusterer)
- artefacts include text, audio, video, and exports (Notion, Dovetail, Google Docs) AND ≥50 artefacts will accumulate per quarter
- repository is the canonical store (not just a backup; researchers will search it directly)

## Skip If (ANY kills it)

- enterprise research-ops with a dedicated platform (Dovetail, EnjoyHQ, Marvin) that already enforces taxonomy
- single-shot validation interview with &lt;10 artefacts total — convention overhead exceeds the value
- the team disagrees on every naming decision — convention works only with single-source authority

## Prerequisites

- a target repo location chosen (Git, Drive, Notion, S3 — convention is portable)
- participant anonymisation policy decided (e.g. P001, P002... not real names)
- list of study types you currently or will run (interview, usability, survey, diary, intercept)
- export format from your recording tool (transcript-only vs audio+video+transcript)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/user-interviews` | This methodology organises the artefacts that user-interviews produces |
| `solo/research/researcher/research-ethics-and-consent` | Anonymisation rule feeds participant-id format |
| `pro/ba/business-analyst/research-tagging-taxonomy` | Tag set used at the body level; this convention covers the filename level |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: slug-only filenames, date-prefix, participant anonymisation, study-type tag, language suffix | ~1000 |
| `content/02-output-contract.xml` | essential | Filename grammar, folder tree, manifest.json schema | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: name collision, PII leak, lost language, scattered transcripts, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `rename_legacy_files_to_convention` | sonnet | Pattern-matching old filenames to the new grammar |
| `extract_metadata_from_transcript` | sonnet | Recover date/type/participant from the body when the filename is missing |
| `manifest_generator` | haiku | Build manifest.json from folder scan |
| `pii_scrub_check` | sonnet | Detect real names / emails in filenames before commit |

## Templates

| File | Purpose |
|------|---------|
| `templates/folder-tree.md` | The canonical folder layout to copy into a new repo |
| `templates/manifest.schema.json` | Schema for the manifest the synthesis layer reads |
| `templates/filename-grammar.md` | Cheat-sheet for the filename pattern |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/lint-research-repo.py` | Verify all files match the grammar; surface PII leaks and collisions | Pre-commit hook + nightly cron |
| `scripts/build-manifest.py` | Walk the tree, produce manifest.json with hashes + tags | After every new artefact is committed |

## Related

- parent skill: `solo/research/researcher/`
- peer methodologies: `user-interviews`, `research-tagging-taxonomy`, `research-ethics-and-consent`
- external: [ResearchOps Community Naming Patterns](https://researchops.community/) · [Dovetail Tagging Best Practices](https://dovetail.com/customers/) · [Atomic Research](https://www.nngroup.com/articles/atomic-research/)
