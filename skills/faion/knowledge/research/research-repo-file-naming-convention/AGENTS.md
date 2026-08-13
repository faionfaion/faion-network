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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/research-repo-file-naming-convention.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/research-repo-file-naming-convention.json",
  "title": "Research Repo File-Naming Convention Output Contract",
  "type": "object",
  "required": [
    "repo_root",
    "folder_tree",
    "filename_grammar",
    "manifest_schema",
    "anonymisation_policy",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "repo_root": {
      "type": "string",
      "description": "absolute path to research repo"
    },
    "folder_tree": {
      "type": "array",
      "description": "lifecycle folders: recruit/, run/, tag/, synthesise/, archive/",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "filename_grammar": {
      "type": "string",
      "description": "regex for valid filenames"
    },
    "manifest_schema": {
      "type": "object",
      "description": "JSON Schema for manifest.json"
    },
    "anonymisation_policy": {
      "type": "string",
      "description": "Pnnn rule + scrub regex"
    },
    "owner": {
      "type": "string",
      "description": "named researcher"
    },
    "version": {
      "type": "string",
      "description": "semver"
    },
    "last_reviewed": {
      "type": "string",
      "description": "ISO date",
      "format": "date"
    }
  },
  "additionalProperties": true
}
```

### `templates/_smoke-test.json`

```json
{
  "repo_root": "sample-repo_root",
  "folder_tree": [
    {
      "k": "v"
    }
  ],
  "filename_grammar": "sample-filename_grammar",
  "manifest_schema": {
    "k": "v"
  },
  "anonymisation_policy": "sample-anonymisation_policy",
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
