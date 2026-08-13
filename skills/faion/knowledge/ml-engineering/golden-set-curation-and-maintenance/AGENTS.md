# Golden Set Curation and Maintenance

## Summary

**One-sentence:** Curates 50-200 hand-labelled I/O pairs (stratified buckets + anti-output + incident-derived growth + quarterly drift audit + versioned promotion) as the anchor dataset for AI-feature regression eval.

**One-paragraph:** Curates 50-200 hand-labelled I/O pairs (stratified buckets + anti-output + incident-derived growth + quarterly drift audit + versioned promotion) as the anchor dataset for AI-feature regression eval. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- AI-feature shipped до production з measurable correctness criteria.
- Регулярні regressions: model swap, prompt change, schema migration — потрібен anchor.
- Incident-driven growth: кожен production-bug → golden-set candidate.
- Quarterly drift audit: 10-20% items застаріває за квартал — потрібен retire-loop.
- Eval-pipeline gate: CI blocks merge коли golden-set score regresses >X%.

## Applies If (ALL must hold)

- AI feature is shipped or near-shipping into a non-AI product.
- Feature has measurable correctness criteria (not just vibes).
- Team owns the model boundary (input + output schema).
- Production logging captures inputs + outputs with PII-safe redaction.
- Team is willing to spend ~1 engineer-week to seed the initial set.

## Skip If (ANY kills it)

- Pre-prototype unstable schema — golden items rot daily.
- Pure exploratory research with no production-deploy plan.
- Creative-content output without consensus correctness (poetry, brand copy).
- Existing RAG-eval framework already covers golden-set discipline.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature input/output schema | JSON Schema / Protobuf | Eng team |
| Production log sample | JSONL / parquet (PII-safe) | Logging pipeline |
| Incident channel | PagerDuty / Slack / ticketing export | Ops team |
| `golden/` directory in repo | Git directory | Eng team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ai/ml-engineer/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | essential | Worked example end-to-end (input → output) | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-golden-set-curation-and-maintenance` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Markdown spec skeleton — sections + acceptance criteria slots |
| `templates/spec-instance.json` | Instance of a filled spec (machine-readable mirror) |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-golden-set-curation-and-maintenance.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ai/ml-engineer/AGENTS.md`
- [[shadow-traffic-rollout-pattern]]
- [[llm-hallucination-test-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/spec-instance.json`

```json
{
  "dataset_version": "1.0.0",
  "items": [
    {
      "id": "gld-0000",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 0"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0001",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 1"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0002",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 2"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0003",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 3"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0004",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 4"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0005",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 5"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0006",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 6"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0007",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 7"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0008",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 8"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0009",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 9"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0010",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 10"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0011",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 11"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0012",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 12"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0013",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 13"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0014",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 14"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0015",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 15"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0016",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 16"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0017",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 17"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0018",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 18"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0019",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 19"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0020",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 20"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0021",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 21"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0022",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 22"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0023",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 23"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0024",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 24"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0025",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 25"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0026",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 26"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0027",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 27"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0028",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 28"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0029",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 29"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0030",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 30"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0031",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 31"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0032",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 32"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0033",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 33"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0034",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 34"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0035",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 35"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0036",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 36"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0037",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 37"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0038",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 38"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0039",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 39"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0040",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 40"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0041",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 41"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0042",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 42"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0043",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 43"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0044",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 44"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0045",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 45"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0046",
      "bucket": "adversarial",
      "input": {
        "text": "sample input 46"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0047",
      "bucket": "known_failure_class",
      "input": {
        "text": "sample input 47"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0048",
      "bucket": "happy_path",
      "input": {
        "text": "sample input 48"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    },
    {
      "id": "gld-0049",
      "bucket": "edge_case",
      "input": {
        "text": "sample input 49"
      },
      "expected_output": {
        "label": "correct"
      },
      "anti_output": [
        {
          "label": "plausible-wrong"
        }
      ],
      "metadata": {
        "difficulty": "medium",
        "added_from": "seed",
        "reviewer": "jane@team.io"
      }
    }
  ],
  "coverage_report": {
    "per_bucket_count": {
      "happy_path": 13,
      "edge_case": 13,
      "adversarial": 12,
      "known_failure_class": 12
    },
    "min_per_bucket": 12
  },
  "owner": "jane@team.io",
  "promotion_review": {
    "reviewer": "alex@team.io",
    "reviewed_at": "2026-05-23"
  }
}
```
