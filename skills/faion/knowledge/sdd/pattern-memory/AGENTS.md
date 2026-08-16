# Pattern Memory

## Summary

**One-sentence:** Produces a pattern-memory config (confidence-graduated entries + ≥2 distinct contexts to capture + CLAUDE.md sync at ≥0.8 confidence) so LLM agents apply consistent proven solutions across tasks and projects.

**Ефективно для:** Solo devs whose LLM agents keep re-inventing the same regex / retry / migration pattern in different ways because no memory layer carries the win forward.

**One-paragraph:** Patterns evaporate when not captured. This methodology pins .aidocs/memory/patterns.md with a confidence score (0.5 initial → 0.9+ proven), graduated by successful uses. Capture rule: solution works in ≥2 distinct contexts; obvious best-practices and one-off fixes rejected. High-confidence patterns (≥0.8) sync to CLAUDE.md for immediate availability in new sessions. Output is consumed by code-review-cycle and engagement-pattern-memory.

## Applies If (ALL must hold)

- Repo has .aidocs/memory/ directory.
- Operator uses an LLM agent with session-start context.
- Solutions recur across distinct contexts within the codebase.
- Confidence-graduation discipline is realistic at session end.

## Skip If (ANY kills it)

- One-shot scripts with no future reuse.
- Obvious best-practices already enforced by linter.
- Patterns that have worked exactly once — wait for the second context.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| .aidocs/memory/patterns.md | markdown | repo |
| CLAUDE.md sync target | markdown | repo |
| confidence-graduation rule | spec | team |
| session-start hook | tool config | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/mistake-memory` | Sibling — mistake memory captures failures; pattern memory captures successes. |
| `solo/sdd/sdd/engagement-pattern-memory` | Variant — per-client scoping for freelancers. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
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
| `templates/pattern-memory.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/pattern-memory.md.j2` | Markdown skeleton with the required fields. |
| `templates/pattern-memory.md` | Markdown skeleton with the required fields. Generated from `templates/pattern-memory.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |
| `templates/mistakes-file.md.j2` | .aidocs/memory/mistakes.md skeleton — recurring-error entries with frequency, root cause, fix, detection method, first/last seen. |
| `templates/mistakes-file.md` | .aidocs/memory/mistakes.md skeleton — recurring-error entries with frequency, root cause, fix, detection method, first/last seen. Generated from `templates/mistakes-file.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pattern-entry.md.j2` | Single pattern entry — confidence, category, context, pattern, code example, anti-pattern, rationale. |
| `templates/pattern-entry.md` | Single pattern entry — confidence, category, context, pattern, code example, anti-pattern, rationale. Generated from `templates/pattern-entry.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pattern-minimal.md.j2` | Minimal one-line pattern stub for low-confidence, newly observed patterns. |
| `templates/pattern-minimal.md` | Minimal one-line pattern stub for low-confidence, newly observed patterns. Generated from `templates/pattern-minimal.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/patterns-file.md.j2` | .aidocs/memory/patterns.md skeleton — category sections for pattern-entry.md inserts, CLAUDE.md-synced. |
| `templates/patterns-file.md` | .aidocs/memory/patterns.md skeleton — category sections for pattern-entry.md inserts, CLAUDE.md-synced. Generated from `templates/patterns-file.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-pattern-memory.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[mistake-memory]] — related methodology.
- [[engagement-pattern-memory]] — related methodology.
- [[code-review-cycle]] — related methodology.
- [[daily-ship-rubric]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pattern-memory.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/pattern-memory.json",
  "title": "Pattern Memory Output Contract",
  "type": "object",
  "required": [
    "pattern_id",
    "title",
    "confidence",
    "contexts_used",
    "rationale",
    "synced_to_claude_md",
    "occurrence_count",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "pattern_id": {
      "type": "string",
      "description": "stable id (PM-001..)"
    },
    "title": {
      "type": "string",
      "description": "pattern name"
    },
    "confidence": {
      "type": "number",
      "description": "0.5..0.95"
    },
    "contexts_used": {
      "type": "array",
      "description": "\u22652 with citation",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "rationale": {
      "type": "string",
      "description": "why it works"
    },
    "synced_to_claude_md": {
      "type": "boolean",
      "description": "true when confidence \u22650.8"
    },
    "occurrence_count": {
      "type": "integer",
      "description": "\u22652"
    },
    "owner": {
      "type": "string",
      "description": "named author"
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
  "pattern_id": "sample-pattern_id",
  "title": "sample-title",
  "confidence": 0.7,
  "contexts_used": [
    {
      "k": "v"
    }
  ],
  "rationale": "sample-rationale",
  "synced_to_claude_md": true,
  "occurrence_count": 3,
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
