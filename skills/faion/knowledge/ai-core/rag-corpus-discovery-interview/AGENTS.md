# RAG Corpus Discovery Interview

## Summary

**One-sentence:** Structured SME interview that audits the corpus (sources, freshness, sensitivity, licensing) before any embedding choice — five-interview minimum before synthesis.

**One-paragraph:** Current rag-architecture methodology jumps to chunking + embedding without auditing the corpus. Wrong corpus → wrong embeddings → wrong retriever. This methodology produces a `corpus-discovery-report.json` based on ≥5 SME interviews (past-behaviour anchored, non-leading prompts) with full transcripts and tagged-quote evidence. Output: a versioned interview bundle the RAG engineer consumes before picking chunking strategy.

**Ефективно для:**

- Embed RAG в existing product — audit corpus state перед wiring.
- 5+ SME interviews для розуміння corpus realities.
- Non-leading prompts; past-behaviour anchored questions.
- Transcripts + tagged-quote evidence для synthesis.
- Bridge до downstream [[rag-bench-harness-template]] спеку.

## Applies If (ALL must hold)

- RAG project planning kickoff — pre-architecture phase.
- ≥5 SMEs available within the review window.
- Recording + transcript pipeline available.
- Named accountable owner.

## Skip If (ANY kills it)

- Corpus already documented in a recent (≤6mo) audit.
- &lt;5 SMEs available (would-be synthesis premature).
- One-shot prototype with no production stakes.
- No recording / transcript capability (notes-only is rejected).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| SME roster (≥5 names + roles) | YAML | platform |
| Interview guide template | Markdown | research repo |
| Recording + transcript tools | tool config | research repo |
| Consent forms | PDF | legal |
| Named accountable owner | string | ownership log |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[rag-bench-harness-template]]` | Downstream consumer of corpus audit findings. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for corpus-discovery-report + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns | ~900 |
| `content/04-procedure.xml` | essential | 5-step: roster → schedule → interview → transcribe → synthesise | ~700 |
| `content/05-examples.xml` | essential | Worked example: 7-SME KB audit | ~700 |
| `content/06-decision-tree.xml` | essential | Routes interview count + consent state to synthesis | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-guide` | sonnet | Anti-leading-question rewriting. |
| `tag-quotes` | sonnet | Per-quote evidence tagging. |
| `synthesise-findings` | opus | Cross-interview pattern detection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/corpus-discovery-report.json` | JSON skeleton matching 02-output-contract. |
| `templates/corpus-discovery-report.md.j2` | Narrative interview-bundle template. |
| `templates/corpus-discovery-report.md` | Narrative interview-bundle template. Generated from `templates/corpus-discovery-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-corpus-discovery-interview.py` | Validate corpus-discovery-report | Pre-commit + before rag-bench spec |

## Related

- [[rag-bench-harness-template]]
- [[production-trace-mining-for-training-data]]
- [[pii-scrubbing-recipe-for-eval-sets]]

## Decision tree

See `content/06-decision-tree.xml`. The tree blocks synthesis if interview count &lt;5 or consent missing; routes to rag-bench spec on green. Walk it before claiming "we know the corpus".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/corpus-discovery-report.json`

```json
{
  "artefact_id": "corpus-discovery-<project>-<period>",
  "owner": "<handle>@faion.net",
  "guide_prompts": [
    "Walk me through the last time you looked up <topic>.",
    "Show me where the answer actually lives in your tools.",
    "Tell me about a time the answer was wrong or stale.",
    "Describe how you decide which source to trust.",
    "Which document classes are licensed for embedding?"
  ],
  "interviews": [
    {
      "transcript_id": "t1",
      "recording_url": "s3://<bucket>/t1.m4a",
      "consent_recorded": true,
      "interviewee_role": "<role>"
    },
    {
      "transcript_id": "t2",
      "recording_url": "s3://<bucket>/t2.m4a",
      "consent_recorded": true,
      "interviewee_role": "<role>"
    },
    {
      "transcript_id": "t3",
      "recording_url": "s3://<bucket>/t3.m4a",
      "consent_recorded": true,
      "interviewee_role": "<role>"
    },
    {
      "transcript_id": "t4",
      "recording_url": "s3://<bucket>/t4.m4a",
      "consent_recorded": true,
      "interviewee_role": "<role>"
    },
    {
      "transcript_id": "t5",
      "recording_url": "s3://<bucket>/t5.m4a",
      "consent_recorded": true,
      "interviewee_role": "<role>"
    }
  ],
  "quotes": [
    {
      "transcript_id": "t1",
      "timestamp": "00:08:42",
      "text": "<verbatim quote>"
    },
    {
      "transcript_id": "t2",
      "timestamp": "00:12:10",
      "text": "<verbatim quote>"
    },
    {
      "transcript_id": "t3",
      "timestamp": "00:05:18",
      "text": "<verbatim quote>"
    },
    {
      "transcript_id": "t4",
      "timestamp": "00:21:33",
      "text": "<verbatim quote>"
    },
    {
      "transcript_id": "t5",
      "timestamp": "00:14:07",
      "text": "<verbatim quote>"
    }
  ],
  "findings": [
    {
      "id": "f1",
      "label": "finding",
      "evidence_quote_ids": [
        "t1@00:08:42",
        "t3@00:05:18"
      ]
    },
    {
      "id": "f2",
      "label": "hypothesis",
      "evidence_quote_ids": [
        "t2@00:12:10"
      ]
    }
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```
