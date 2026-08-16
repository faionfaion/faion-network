# Thumbs Down to Eval Pipeline

## Summary

**One-sentence:** Closes the loop from a user thumbs-down (or hallucination report) to a row in the regression eval set within 24h, with PII scrubbing, judgment voting, and deterministic eval-set growth caps.

**One-paragraph:** Most LLM products collect thumbs-up/down feedback but never funnel it into evals; the data dies in a Kafka topic. This methodology codifies a 4-stage pipeline (ingest → scrub → judge → admit) plus a stop-the-bleed escalation rule (3+ thumbs-down on same response pattern → human-on-call within 4h). Eval set growth is capped at 50 rows/week to keep CI runtime bounded. Output: `EvalCandidate` records routed to admit/reject + `EvalSet` with versioned rows. Built on OpenAI Evals, Anthropic AISI patterns, and the Lilian Weng "LLM ops" playbook.

**Ефективно для:**

- Продуктів із thumbs widget + регресійним eval suite — закриває loop між сигналом і регресією за 24h, не вручну.
- Hallucination-sensitive feature (legal, medical, support) — stop-the-bleed gate ловить кластер однотипних відмов за 4h.
- CI-budget-aware команд — cap 50 rows/week тримає eval runtime bounded; eval suite не вибухає.
- Privacy-strict пайплайнів — обовʼязковий PII-scrub gate перед admit оберігає eval-suite від витоків.

## Applies If (ALL must hold)

- production LLM feature with ≥ 1000 daily interactions
- user-facing feedback widget (thumbs / report) writes to a queryable store
- existing regression eval suite with at least 50 baseline rows
- model deployment uses a runner (Modal, Replicate, vLLM, OpenAI) that supports versioned evals

## Skip If (ANY kills it)

- product has &lt; 50 daily interactions — feedback volume too thin
- no eval suite exists yet — bootstrap that first (`eval-set-bootstrap` methodology)
- PII can leak in feedback content and no scrubbing infrastructure — fix scrubbing first
- team has no triage rotation — pipeline produces alerts no one reads

## Prerequisites

- feedback store with `(interaction_id, prompt, response, signal: enum {up, down, report}, comment, timestamp, user_hash)` rows
- PII scrubber (Presidio, AWS Comprehend, regex) integrated
- eval suite stored as code (Anthropic Evals format, OpenAI Evals format, or YAML)
- on-call rotation defined for hallucination incidents

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/regression-eval-set` | Defines the eval set structure this pipeline writes to |
| `geek/ai/ml-engineer/hallucination-incident-triage` | Downstream when stop-the-bleed fires |
| `geek/ai/ml-engineer/customer-ai-feedback-triage` | Sister methodology for weekly triage; this is automated daily |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 4-stage pipeline, PII scrub gate, judge voting, weekly cap, stop-the-bleed | 1000 |
| `content/02-output-contract.xml` | essential | `EvalCandidate` + admitted-row schema | 700 |
| `content/03-failure-modes.xml` | essential | 6 modes: noisy thumbs, PII leak, judge bias, etc. | 900 |
| `content/04-procedure.xml` | essential | 6 steps: ingest → scrub → cluster → judge vote → admit → ship | 800 |
| `content/05-examples.xml` | essential | Worked example: 3-thumbs-down cluster fires stop-the-bleed | 500 |
| `content/06-decision-tree.xml` | essential | Routes by cluster-size, judge-vote, PII-status, weekly-cap | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `feedback_ingest_normalise` | haiku | Field extraction from queue events |
| `pii_scrub` | sonnet | Presidio-like entity detection bounded by allow-list |
| `triple_judge_vote` | sonnet | 3-judge LLM voting on whether to admit |
| `cluster_for_stop_bleed` | sonnet | Embedding clustering of same-pattern failures |
| `eval_set_admit_pr` | sonnet | Compose PR adding rows to eval suite |

## Templates

| File | Purpose |
|------|---------|
| `templates/eval-candidate.schema.json` | EvalCandidate JSON schema |
| `templates/admitted-row.schema.json` | Eval-suite row schema |
| `templates/stop-bleed-alert.json` | PagerDuty-compatible alert payload |
| `templates/_smoke-test.json` | Minimum-viable EvalCandidate that validates clean |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-thumbs-down-to-eval-pipeline.py` | Lint EvalCandidate against schema, enforce PII-clean flag + weekly cap | Pre-commit + nightly batch |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[rag-feature-acceptance-contract]] — eval set referenced by the contract
- [[retrieval-drift-alerting-recipe]] — drift signal complements this signal-from-users feedback loop
- external: [Anthropic — Building Evals](https://docs.anthropic.com/claude/docs/evaluating-prompts) · [OpenAI Evals](https://github.com/openai/evals) · [Hamel Husain — Your AI product needs evals](https://hamel.dev/blog/posts/evals/)

## Decision tree

See `content/06-decision-tree.xml`. Routes a feedback row by: cluster-size (>3 → stop-the-bleed), PII-clean flag, judge-vote (≥2/3 admit), and weekly-cap remaining.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/eval-candidate.schema.json`

```json
{
  "_header": [
    "purpose: JSON Schema for EvalCandidate emitted by ingest stage",
    "consumes: feedback-store row",
    "produces: validation schema for validate-thumbs-down-to-eval-pipeline.py",
    "depends-on: jsonschema at validation time",
    "token-budget-impact: 0 at runtime"
  ],
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "interaction_id",
    "prompt",
    "response",
    "signal",
    "timestamp",
    "pii_clean",
    "judge_votes",
    "cluster_size",
    "admitted_this_week"
  ],
  "properties": {
    "interaction_id": {
      "type": "string",
      "minLength": 3
    },
    "prompt": {
      "type": "string",
      "minLength": 1
    },
    "response": {
      "type": "string",
      "minLength": 1
    },
    "signal": {
      "type": "string",
      "enum": [
        "down",
        "report"
      ]
    },
    "comment": {
      "type": "string"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "user_hash": {
      "type": "string"
    },
    "pii_clean": {
      "type": "boolean"
    },
    "judge_votes": {
      "type": "array",
      "minItems": 3,
      "maxItems": 3,
      "items": {
        "type": "string",
        "enum": [
          "ADMIT",
          "REJECT"
        ]
      }
    },
    "cluster_size": {
      "type": "integer",
      "minimum": 1
    },
    "admitted_this_week": {
      "type": "integer",
      "minimum": 0,
      "maximum": 50
    }
  }
}
```

### `templates/admitted-row.schema.json`

```json
{
  "_header": [
    "purpose: eval-suite row schema (final admitted form)",
    "consumes: EvalCandidate (admit_decision=ADMIT)",
    "produces: validation schema for eval-suite PR contents",
    "depends-on: jsonschema",
    "token-budget-impact: 0 at runtime"
  ],
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "id",
    "input",
    "expected",
    "rubric_ref",
    "source",
    "admitted_at"
  ],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^er-[a-z0-9-]+$"
    },
    "input": {
      "type": "string"
    },
    "expected": {
      "type": "string"
    },
    "rubric_ref": {
      "type": "string"
    },
    "source": {
      "type": "object",
      "required": [
        "type",
        "candidate_id"
      ],
      "properties": {
        "type": {
          "type": "string",
          "enum": [
            "thumbs-down",
            "report",
            "manual"
          ]
        },
        "candidate_id": {
          "type": "string"
        }
      }
    },
    "admitted_at": {
      "type": "string",
      "format": "date"
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```

### `templates/stop-bleed-alert.json`

```json
{
  "_header": [
    "purpose: PagerDuty-compatible alert payload for stop-the-bleed cluster",
    "consumes: cluster from step 3 with size >=3",
    "produces: HTTP POST body for PD events API v2",
    "depends-on: pagerduty events-api v2",
    "token-budget-impact: 0 at runtime"
  ],
  "routing_key": "<integration-key>",
  "event_action": "trigger",
  "dedup_key": "td-eval-cluster-<cluster_id>",
  "payload": {
    "summary": "Stop-the-bleed: 3+ thumbs-down on similar response pattern",
    "severity": "warning",
    "source": "thumbs-down-to-eval-pipeline",
    "custom_details": {
      "cluster_id": "<cluster_id>",
      "size": 3,
      "similarity_centroid": 0.91,
      "first_seen": "<timestamp>",
      "intent": "<intent_name>",
      "runbook": "https://runbooks.example.com/td-stop-bleed"
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "_header": [
    "purpose: minimum-viable EvalCandidate fixture",
    "consumes: nothing",
    "produces: JSON instance for --self-test",
    "depends-on: eval-candidate.schema.json",
    "token-budget-impact: 0 at runtime"
  ],
  "interaction_id": "i-001",
  "prompt": "What is the refund window?",
  "response": "refund window is 60 days",
  "signal": "down",
  "comment": "actually it's 30 days",
  "timestamp": "2026-05-22T14:32:00Z",
  "user_hash": "u-deadbeef",
  "pii_clean": true,
  "judge_votes": [
    "ADMIT",
    "ADMIT",
    "REJECT"
  ],
  "cluster_size": 3,
  "admitted_this_week": 12
}
```
