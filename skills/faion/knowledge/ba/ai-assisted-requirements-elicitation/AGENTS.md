# AI-Assisted Requirements Elicitation

## Summary

**One-sentence:** BABOK-grounded methodology for BAs to draft user stories + AC from elicitation artifacts via LLM with hallucination guards (compliance-domain rules, evidence per claim).

**One-paragraph:** BABOK-grounded methodology for BAs to draft user stories + AC from elicitation artifacts via LLM with hallucination guards (compliance-domain rules, evidence per claim). Captured as a versioned artefact downstream agents and reviewers consume without re-deriving rationale. Mechanism: typed input → bounded transformation → contract-checked output.

**Ефективно для:**

- Bulk drafting stories + AC з interview transcripts.
- Compliance domains (banking, healthcare, legal) — hallucination guards critical.
- Multi-source synthesis (interviews + docs + tickets).
- Acceleration BA коли team scaled до agents+humans.

## Applies If (ALL must hold)

- Elicitation artifacts exist (transcripts, docs, interview notes).
- Output reviewed by named BA before merge.
- Compliance-domain hallucination guards required.
- Output schema (stories + AC) known.

## Skip If (ANY kills it)

- No elicitation artifacts collected yet — interview first.
- Single-conversation greenfield discovery — human-led is faster.
- Domain agents are not trusted for the regulatory class (defer to human-only).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent task context (30 days) | Markdown / tracker | BA |
| Write access to artefact store | repo / wiki | engagement manager |
| Named downstream owner | stakeholder list | BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-elicitation-prompt-patterns]] | Companion / upstream methodology |
| [[acceptance-criteria]] | Sibling artefact in the same lifecycle |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + examples | 800 |
| `content/03-failure-modes.xml` | essential | Antipatterns | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Mechanical template fill. |
| `synthesize_decision` | sonnet | Per-instance bounded judgment. |
| `review_for_compliance` | opus | Cross-input synthesis on high-stakes outputs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-assisted-requirements-elicitation.json` | Skeleton artefact with required fields |
| `templates/_smoke-test.json` | Minimum viable filled artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-assisted-requirements-elicitation.py` | Validate artefact against output-contract | After subagent returns; pre-commit |

## Related

- [[ai-elicitation-prompt-patterns]]
- [[acceptance-criteria]]
- [[ai-acceptance-criteria-generator-reviewer]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on artefact-state signal to the active rule.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ai-assisted-requirements-elicitation.json`

```json
{
  "elicitation_id": "REPLACE",
  "version_tag": "REPLACE",
  "ba_reviewer": "REPLACE",
  "stories": []
}
```

### `templates/_smoke-test.json`

```json
{
  "elicitation_id": "kyc-2026",
  "version_tag": "v1.0.0",
  "ba_reviewer": "Ana Rodrigues",
  "stories": [
    {
      "story_id": "STORY-101",
      "title": "ID verification step",
      "source_refs": [
        "interview-ana#08:14",
        "compliance-doc.md#L40"
      ],
      "ac_count": 5
    }
  ]
}
```
