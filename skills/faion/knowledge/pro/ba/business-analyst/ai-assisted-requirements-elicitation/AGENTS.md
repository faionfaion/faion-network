---
slug: ai-assisted-requirements-elicitation
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "ce5752334a501363"
summary: BABOK-grounded methodology for BAs to use LLMs to draft user stories and acceptance criteria from elicitation artifacts, with hallucination guards for compliance domains.
tags: [business-analysis, llm, requirements, user-stories, babok, acceptance-criteria, compliance]
---
# AI-Assisted Requirements Elicitation

## Summary

**One-sentence:** BABOK-grounded methodology for BAs to use LLMs to draft user stories and acceptance criteria from elicitation artifacts, with hallucination guards for compliance domains.

**One-paragraph:** Existing `ai-enabled-business-analysis` is geek-tier and generic; BAs in regulated domains (fintech, healthcare, public sector) need a concrete recipe: which prompt patterns produce reliable user stories, how to enforce evidence-attribution to elicitation transcripts, how to add hallucination guards when stakes are compliance-relevant, where to put human-in-the-loop checkpoints. Mechanism: structured ingestion of elicitation artifacts (interview transcripts, workshop notes, existing process docs) → BABOK-style requirements draft (user stories + AC + traceability) → evidence-citation validation → human BA review pass → version-controlled publication. Each draft requirement carries a transcript citation; ungrounded drafts are rejected.

## Applies If (ALL must hold)

- BA running a discovery / requirements engagement in a regulated or high-stakes domain
- elicitation artifacts are written (transcripts, workshop notes, surveys) — required as inputs
- LLM API access available with a model that supports structured output + long context
- BA owns final responsibility for requirements quality (not the LLM)
- engagement uses BABOK-aligned process (user stories + AC + traceability matrix)

## Skip If (ANY kills it)

- pre-elicitation phase (no artifacts yet) — do the workshops first
- pure UX research output — use JTBD or persona-building methodologies instead
- code-first developer-driven projects with no BA — different workflow
- single-stakeholder project — overhead exceeds value; manual draft faster
- non-compliance domain with relaxed accuracy bar — geek/ai-enabled-business-analysis lighter version may fit

## Prerequisites (must be true before starting)

- elicitation transcripts / notes in text form with consistent attribution (who said what, when)
- stakeholder roster + their decision rights (some can sign off; others can only provide input)
- domain compliance constraints documented (HIPAA, PCI, SOX, GDPR, AML, etc.)
- BABOK v3-aligned story / AC template the team uses
- LLM-generated content review SLA (e.g., "every AI-drafted requirement reviewed by BA within 24h")

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/elicitation-techniques` | Source artifacts come from these techniques |
| `pro/ba/business-analyst/acceptance-criteria` | Format standard for the AI-generated outputs |
| `pro/ba/business-analyst/requirements-traceability` | Traceability matrix the citations feed |
| `geek/ba/business-analyst/<ai-enabled-business-analysis>` | Geek-tier reference; this is the pro-tier applied recipe |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: transcript-cited requirements, BABOK-format compliance, compliance-domain hallucination guards, human BA review, version-controlled drafts | ~950 |
| `content/02-output-contract.xml` | essential | Story + AC + citation schema, traceability matrix schema, forbidden patterns | ~750 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (compliance hallucination, missing citations, story bloat, regulatory misattribution, stakeholder consent leak, AC vague, traceability gap) | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `transcript_ingestion_and_dedup` | sonnet | Per-doc normalization |
| `story_draft_per_capability` | sonnet | Bounded template fill: Given/When/Then or As-a/I-want/So-that |
| `acceptance_criteria_from_story` | sonnet | Mechanical expansion of story into AC |
| `compliance_constraint_check` | opus | Cross-check requirement against compliance constraints |
| `traceability_matrix_update` | haiku | Append story id → transcript id mapping |

## Templates

| File | Purpose |
|------|---------|
| `templates/story-template.md` | BABOK-aligned story format with citation slot |
| `templates/ac-template.md` | Acceptance criteria template (Given/When/Then) |
| `templates/traceability-matrix.md` | Story id → transcript citation map |
| `templates/compliance-cross-check.md` | Per-requirement compliance constraint check |
| `templates/human-review-log.md` | BA review pass record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/ingest-elicitation.py` | Normalize transcripts + notes into a citable corpus | Engagement setup |
| `scripts/validate-requirement-citations.py` | Verify every requirement has a verifiable transcript citation | Pre-review |
| `scripts/compliance-cross-check.py` | Flag requirements that may conflict with compliance constraints | Per draft |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer methodologies: `acceptance-criteria`, `requirements-traceability`, `elicitation-techniques`
- external: [IIBA BABOK Guide v3](https://www.iiba.org/standards-and-resources/babok/) · [Anthropic - Tool use with citations](https://docs.anthropic.com/en/docs/build-with-claude/citations) · [Mike Cohn - User Stories Applied](https://www.mountaingoatsoftware.com/books/user-stories-applied)
