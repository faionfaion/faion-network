# AI User Story Decomposition

## Summary

**One-sentence:** Decomposes vague AI-product asks ('add chatbot', 'make it smart') into INVEST-compliant user stories with explicit AI-vs-deterministic boundary, eval criteria (precision/recall/cost/latency), fallback behavior, and golden-set seed.

**One-paragraph:** Decomposes vague AI-product asks ('add chatbot', 'make it smart') into INVEST-compliant user stories with explicit AI-vs-deterministic boundary, eval criteria (precision/recall/cost/latency), fallback behavior, and golden-set seed. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Stakeholder ask is vague ('add AI', 'make it smart') — needs decomposition.
- AI-vs-deterministic boundary не ясний — стейкхолдери думають LLM зробить все.
- Eval criteria для AI-feature: precision/recall/accuracy/cost — потрібно AC.
- Fallback behavior: коли AI fails (low confidence, refusal) — який UX?

## Applies If (ALL must hold)

- Stakeholder ask is vague ('add AI', 'make it smart').
- Production-deploy intent (not research spike).
- BA owns the story and has access to JTBD / stakeholder records.
- Eng team can act on numeric AC and golden seeds.

## Skip If (ANY kills it)

- Deterministic-only story (CRUD, lookup, integration with no LLM in the loop).
- Research spike with no production-deploy plan.
- Story already has measurable spec attached.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stakeholder ask (raw) | email / transcript / JTBD record | PM / sponsor |
| Existing story template | Markdown / Jira | BA repo |
| Eval AC catalogue (precision / recall / cost / latency) | YAML | ML eng team |
| Golden-set seed template | JSONL | ml-engineering methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | essential | Worked example end-to-end (input → output) | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-user-story-decomposition` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md.j2` | Markdown spec skeleton — sections + acceptance criteria slots |
| `templates/spec.md` | Markdown spec skeleton — sections + acceptance criteria slots Generated from `templates/spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/spec-instance.json` | Instance of a filled spec (machine-readable mirror) |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-user-story-decomposition.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/ba/AGENTS.md`
- [[ambiguity-contradiction-detector]]
- [[ba-governance]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/spec-instance.json`

```json
{
  "ask_summary": "Add a chatbot that answers refund-policy questions for support",
  "owner": "jane@team.io",
  "stories": [
    {
      "id": "story-1",
      "as_a": "logged-in customer",
      "i_want": "to ask about refund policy",
      "so_that": "I get a same-day answer",
      "ac": [
        "ac-1",
        "ac-2"
      ]
    }
  ],
  "ac": [
    {
      "id": "ac-1",
      "criterion": "AI returns answer grounded in /docs/refund.md",
      "metric_threshold": "precision >= 0.92"
    },
    {
      "id": "ac-2",
      "criterion": "p95 latency under 4s",
      "metric_threshold": "latency_p95 <= 4000ms"
    }
  ],
  "ai_boundary": {
    "ai_scope": "answer-generation from grounded snippet",
    "deterministic_fallback": "search index returns top-3 KB articles",
    "handoff_signal": "confidence < 0.6 OR refusal"
  },
  "fallback": {
    "low_confidence": "show KB articles",
    "refusal": "open support ticket",
    "timeout": "show KB articles + apology"
  },
  "eval_ac": [
    {
      "metric": "precision",
      "threshold": 0.92
    },
    {
      "metric": "latency_p95_ms",
      "threshold": 4000
    }
  ],
  "golden_seeds": [
    {
      "input": {
        "q": "Can I return after 30 days?"
      },
      "expected": "policy.no_returns_after_30",
      "anti_output": "policy.full_refund"
    },
    {
      "input": {
        "q": "Refund on digital purchase?"
      },
      "expected": "policy.digital_no_refund",
      "anti_output": "policy.full_refund"
    },
    {
      "input": {
        "q": "What if item is damaged?"
      },
      "expected": "policy.damaged_full_refund",
      "anti_output": "policy.no_returns_after_30"
    },
    {
      "input": {
        "q": "How long does it take?"
      },
      "expected": "policy.refund_window_5d",
      "anti_output": "policy.instant"
    },
    {
      "input": {
        "q": "Tell me a joke"
      },
      "expected": "refusal.off_topic",
      "anti_output": "joke output"
    }
  ]
}
```
