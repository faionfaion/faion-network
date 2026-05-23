# Vision Language Model Provider Selection

## Summary

**One-sentence:** Picks the cheapest VLM whose capability matrix covers the task (OCR accuracy, structured output, context length, doc-image throughput) before any integration is started.

**One-paragraph:** Modern VLMs (GPT-4o vision, Claude 3.5 Sonnet vision, Gemini 2.x, Llava-Onevision, Qwen-VL) trade off accuracy, latency, structured-output reliability, and cost differently. This methodology selects a VLM by hard-matching task needs (OCR vs scene understanding vs charts) against the 2026 matrix, then ships an adapter so a swap takes one config flip, not a refactor.

**Ефективно для:**

- Greenfield vision pipeline build: prevents 2-week rewrites when picked VLM lacks structured output.
- Cost re-evaluation after pilot: re-scores against capability matrix with real volume.
- Multi-VLM abstraction: decides which 2-3 VLMs deserve an adapter.
- Compliance vendor briefing: defensible scoring rubric.

## Applies If (ALL must hold)

- Selecting a VLM before integration code is written.
- Re-evaluating VLM choice under cost or quality pressure.
- Building a VLM-agnostic adapter and choosing which models to include.

## Skip If (ANY kills it)

- VLM already selected and integration is shipped — refer to vision-agentic-pipeline.
- Task is text-only — pick a non-vision LLM instead.
- Self-hosted required and budget < $5k/mo — open VLMs need GPU infra; revisit when budget grows.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task spec | markdown | Capability list: OCR? structured output? long context? |
| Expected volume | images/month | Pipeline estimate |
| Budget cap | USD/month | Hard ceiling |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `requirements_extract` | sonnet | Brief → capability matrix. |
| `matrix_scoring` | haiku | Deterministic capability lookup. |
| `decision_record` | sonnet | Narrative justification + cost table. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vlm-matrix.md` | Capability matrix scoring sheet |
| `templates/decision-record.md` | Filled-in decision record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vision-provider-selection.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[video-generation-provider-selection]]
- [[vision-document-extraction]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Does the task require >200K-token context (long video, multi-doc) ? Branches route to a rule id from `content/01-core-rules.xml` (gemini-when, gpt4o-when, claude-when, ...) so every leaf is traceable to a testable statement.
