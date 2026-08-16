# CI Evaluation Gate Config

## Summary

**One-sentence:** CI configuration for running LLM-output evaluation as a merge gate: thresholds per metric (faithfulness, safety, latency), fixture corpus, baseline pinning, regression-only-blocks policy.

**One-paragraph:** Teams shipping LLM-backed features need an automated evaluation gate in CI — but most setups either over-block (every drift fails) or under-gate (everything passes). This methodology defines the gate config: a pinned fixture corpus, per-metric thresholds (faithfulness, safety, latency p95, cost p95), a baseline pin per branch, and a regression-only block policy. Output is a YAML config consumed by the eval runner, plus a JSON report per CI run with metric scores + verdict.

**Ефективно для:**

- The repo ships an LLM-backed feature (chat, summarisation, classification) whose quality is measurable.
- There is a curated fixture corpus of ≥50 inputs with expected behaviour annotations.
- CI has the capacity to run the eval (LLM calls, judge model) on every PR; cost is budgeted.

## Applies If (ALL must hold)

- The repo ships an LLM-backed feature (chat, summarisation, classification) whose quality is measurable.
- There is a curated fixture corpus of ≥50 inputs with expected behaviour annotations.
- CI has the capacity to run the eval (LLM calls, judge model) on every PR; cost is budgeted.

## Skip If (ANY kills it)

- Feature has no measurable quality dimension (UI-only, no LLM output).
- Fixture corpus does not exist and team cannot create one in this release cycle — defer until corpus exists.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Fixture corpus | jsonl | Repo at `evals/fixtures.jsonl` |
| Metric definitions | yaml | Repo at `evals/metrics.yaml` |
| Baseline scores | json | Last green main run, pinned by commit SHA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ci-eval-gate-config` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/eval-gate.yaml` | CI eval gate config |
| `templates/github-action.yml` | GitHub Actions wiring for the gate |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ci-eval-gate-config.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/eval-gate.yaml`

```yaml
fixture_corpus_sha: 0000000000000000000000000000000000000000
baseline_commit: abc1234
metrics:
  faithfulness:
    threshold: 0.88
    tolerance: 0.02
    gated: true
  safety_pii:
    threshold: 0.99
    tolerance: 0.0
    gated: true
    absolute_floor: true
  latency_p95_ms:
    threshold: 2000
    tolerance: 200
    gated: true
publish:
  artifact: ci/eval/report.json
  comment: ci/eval/summary.md
```

### `templates/github-action.yml`

```yaml
name: llm-eval-gate
on: [pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/run-eval.py --config evals/eval-gate.yaml --out report.json
      - run: python scripts/validate-ci-eval-gate-config.py --file report.json
      - uses: actions/upload-artifact@v4
        with: {name: eval-report, path: report.json}
```
