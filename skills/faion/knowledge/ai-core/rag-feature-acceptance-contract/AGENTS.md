# RAG Feature Acceptance Contract

## Summary

**One-sentence:** Three-party signed contract — PM (intent + business outcome), SME (correctness rubric), ML engineer (offline + online metric gate) — that defines what "good answer" means per intent class and gates the RAG feature ship.

**One-paragraph:** RAG features routinely ship on vanity metrics (BLEU, ROUGE, "looks fluent") because nobody on the team agreed in writing what a correct answer is per user intent. This methodology forces three roles to co-author a single document — the Acceptance Contract — keyed by intent class. For each class the contract pins PM outcome and tolerable failure mode, SME correctness rubric with pass/borderline/fail worked examples, and ML engineer offline-metric thresholds paired with an online telemetry signal. Ship is blocked until all three signatures are recorded. Once signed, the contract is the source of truth for the eval harness, regression gates, and post-launch monitoring. Primary output: a versioned `acceptance-contract.yaml` per RAG feature, consumed by both the eval harness and the production monitor.

**Ефективно для:**

- RAG-фіч de support-bot / docs / KB де галюцинації коштують грошей — контракт перетворює "ship коли виглядає добре" на "ship коли три підписи стоять".
- Команд із PM + SME + ML engineer тріадою — без SME контракт деградує до vibe-check, методологія форсує SME-підпис.
- Multi-intent додатків (policy-lookup vs troubleshooting vs comparison) — один глобальний поріг приховує клас, що падає; контракт декомпозує по intent.
- Регресій після model upgrade — recontract trigger перетворює silent drift на календарну подію з owner-ом.

## Applies If (ALL must hold)

- feature_type == RAG (retrieval-augmented generation: docs, code, support KB, product catalog)
- target_user_population is identifiable and reachable for either CSAT survey or behavioral telemetry
- ≥2 distinct intent classes have been observed in user queries (logs, beta data, or domain analysis)
- a Subject-Matter Expert with authority over correctness is available for ≥4 hours of rubric work
- eval harness exists or is being built in the same iteration

## Skip If (ANY kills it)

- single-intent search-only feature (lexical search, no LLM synthesis) — recall@k is sufficient; full contract is over-engineering
- internal-only demo with no ship date — contracting takes 1-3 days, do not block exploration
- the dataset is <50 labelled queries — there is no way to set defensible thresholds; sample more first
- no SME has authority over correctness (consumer-grade chit-chat) — use preference labels + Elo instead
- you are still in the spike phase deciding whether RAG is the right architecture — defer until architecture is committed

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `per-intent-query-sample.jsonl` | JSONL with `{query, intent}` | production logs OR beta data OR SME-curated query bank |
| `draft-pipeline.yaml` | YAML | retrieval pipeline + generator prompt (vN-1 acceptable) |
| `eval-framework-choice.md` | Markdown | one of: Ragas, TruLens, Phoenix, DeepEval, in-house |
| `stakeholder-roster.yaml` | YAML | named PM, SME, ML engineer + dated commitment |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/rag-evaluation-frameworks` | Vocabulary for faithfulness / answer-relevance / context-precision |
| `geek/ai/ml-engineer/golden-dataset-construction` | Eval set referenced by the contract |
| `geek/ai/ml-engineer/llm-as-judge-design` | Many rubric checks are LLM-judges; calibration discipline lives there |
| `pro/pm/project-manager/release-gates-and-approvals` | Sign-off workflow pattern this contract slots into |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: per-intent decomposition, three signatures, offline+online pairing, threshold defensibility, recontract trigger | 1000 |
| `content/02-output-contract.xml` | essential | YAML schema for `acceptance-contract.yaml`, required fields, forbidden patterns, allowed transformations | 800 |
| `content/03-failure-modes.xml` | essential | 7 failure modes with detector + repair | 1100 |
| `content/04-procedure.xml` | essential | 6 steps: cluster intents → draft rubric → set thresholds → pair telemetry → collect signatures → register triggers | 800 |
| `content/05-examples.xml` | essential | Worked support-RAG contract with two intents | 700 |
| `content/06-decision-tree.xml` | essential | Routing by intent count + SME availability + drift evidence | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `intent_class_extraction_from_logs` | sonnet | Cluster + label real queries; bounded judgement at scale |
| `rubric_drafting_with_sme_interview` | opus | Cross-domain synthesis of PM outcome + SME expertise; needs depth |
| `acceptance_yaml_lint` | haiku | Schema check; cheap and deterministic |
| `regression_gate_check` | sonnet | Per-PR judgement vs contract thresholds; volume; bounded |
| `recontract_recommendation` | opus | Reason about drift evidence and whether to relax / tighten thresholds |

## Templates

| File | Purpose |
|------|---------|
| `templates/acceptance-contract.schema.yaml` | JSON-Schema (YAML form) for the contract document |
| `templates/intent-rubric-card.md.j2` | Per-intent rubric: outcome, pass/borderline/fail examples, metric thresholds |
| `templates/intent-rubric-card.md` | Per-intent rubric: outcome, pass/borderline/fail examples, metric thresholds Generated from `templates/intent-rubric-card.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/sme-interview-guide.md.j2` | 45-minute structured interview with the SME, role-play of edge cases |
| `templates/sme-interview-guide.md` | 45-minute structured interview with the SME, role-play of edge cases Generated from `templates/sme-interview-guide.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.yaml` | Minimum-viable two-intent contract that validates clean |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-feature-acceptance-contract.py` | Lints `acceptance-contract.yaml` against schema, checks every intent has all three signatures and paired metrics | Pre-commit hook on the contract file |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[rag-evaluation]] — vocabulary the contract speaks
- [[golden-set-curation-and-maintenance]] — the eval set referenced by the contract
- [[retrieval-drift-alerting-recipe]] — runtime monitor that fires the recontract trigger

## Decision tree

See `content/06-decision-tree.xml`. Routes on (a) intent-count ≥2, (b) SME availability, (c) eval-set size ≥50 — drives whether to author the contract, defer, or downgrade to a preference-label flow.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/acceptance-contract.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [feature, version, intents, signatures, recontract_triggers]
properties:
  feature:
    type: string
    pattern: "^[a-z][a-z0-9-]+$"
  version:
    type: string
    pattern: "^\\d+\\.\\d+\\.\\d+$"
  intents:
    type: object
    minProperties: 2
    additionalProperties:
      type: object
      required: [pm_outcome, acceptable_failure, sme_rubric, offline, online]
      properties:
        pm_outcome: { type: string, minLength: 20 }
        acceptable_failure: { type: string, minLength: 20 }
        sme_rubric:
          type: object
          required: [pass, fail]
          properties:
            pass: { type: string, minLength: 10 }
            borderline: { type: string }
            fail: { type: string, minLength: 10 }
        offline:
          type: object
          minProperties: 2
          additionalProperties:
            type: object
            required: [threshold, baseline]
            properties:
              threshold: { type: string }
              baseline: { type: string, minLength: 5 }
        online:
          type: object
          minProperties: 1
          additionalProperties:
            type: object
            required: [threshold, baseline]
            properties:
              threshold: { type: string }
              baseline: { type: string, minLength: 5 }
  signatures:
    type: object
    required: [pm, sme, ml_engineer]
    properties:
      pm: { type: string, pattern: ".+@.+ \\d{4}-\\d{2}-\\d{2} .+" }
      sme: { type: string, pattern: ".+@.+ \\d{4}-\\d{2}-\\d{2} .+" }
      ml_engineer: { type: string, pattern: ".+@.+ \\d{4}-\\d{2}-\\d{2} .+" }
  recontract_triggers:
    type: array
    minItems: 2
    items: { type: string, minLength: 10 }
```

### `templates/_smoke-test.yaml`

```yaml
feature: example-rag
version: 1.0.0

intents:
  policy-lookup:
    pm_outcome: "Resolve customer policy questions without human escalation"
    acceptable_failure: "Refusal to answer is acceptable; hallucination is not"
    sme_rubric:
      pass: "Cites correct policy section with verbatim quote"
      borderline: "Cites correct section but paraphrases"
      fail: "No citation or wrong citation"
    offline:
      faithfulness:
        threshold: ">= 0.90"
        baseline: "junior agent baseline 0.92"
      context-precision:
        threshold: ">= 0.80"
        baseline: "current production 0.75"
    online:
      thumbs-down-rate:
        threshold: "<= 5%"
        baseline: "today 9%"

  troubleshooting:
    pm_outcome: "Walk user through fix; partial diagnosis acceptable"
    acceptable_failure: "Wrong-but-safe step ok; destructive step not"
    sme_rubric:
      pass: "Steps in correct order, no destructive action first"
      fail: "Recommends destructive action without backup"
    offline:
      answer-relevance:
        threshold: ">= 0.80"
        baseline: "previous prompt 0.71"
      destructive-step-detector:
        threshold: "== 0"
        baseline: "hard zero by PM"
    online:
      follow-up-rephrase-rate:
        threshold: "<= 20%"
        baseline: "today 31%"

signatures:
  pm: "alice@example.com 2026-05-22 v1.0"
  sme: "ravi@example.com 2026-05-22 v1.0"
  ml_engineer: "jonas@example.com 2026-05-22 v1.0"

recontract_triggers:
  - "query_intent_distribution_shift_chi2_p < 0.01"
  - "embedding_model_upgrade"
  - "online_vs_offline_divergence >= 0.20"
```
