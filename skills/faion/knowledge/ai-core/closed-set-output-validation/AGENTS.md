# Closed-Set Output Validation

## Summary

**One-sentence:** Produces a Closed-Set Validation Contract: when the legal values of an output field are an enumerable set you supplied in the request, groundedness is set membership — exact, zero tokens, no model, no threshold — and the whole entailment stack is the wrong tool.

**One-paragraph:** Groundedness research is written for systems that generate prose, so it teaches claim decomposition and entailment scoring: split the answer into atomic claims, ask an NLI model whether each is supported, divide. That is an approximation, and the approximations are expensive and only ~64-77% balanced-accurate. But a large share of real LLM outputs are not prose at all — they are selections: an identifier, a slug, a category, a file path, a customer record, a ranked list of things you handed the model a moment ago. For those the exact answer is free. Compute `grounding_rate = |E ∩ C| / |E|` over emitted values `E` and the candidate set `C` you supplied, and you have a groundedness metric with no false positives, no threshold to tune, no judge cost and no dependency. This methodology gives the test for whether your space is genuinely closed, the contract for enforcing membership, the rule that a dropped value must be counted rather than logged, and the boundary line: mixed outputs have a closed field and an open field, and the metric only ever covers the closed one.

**Ефективно для:**

- Retrieval and search that returns identifiers from a candidate list rather than prose.
- Routing, classification and tool selection — the label space is the enum you wrote.
- Any pipeline about to add a groundedness scorer, a judge model or a RAG-eval dependency for a field whose legal values are already written down.
- Teams whose hallucination handling is a `logger.Warn` and who therefore have no idea what their rate is.

## Applies If (ALL must hold)

- At least one output field's legal values can be enumerated at request time.
- That enumeration comes from an artefact YOU supplied or control — not from the model's memory of the world.
- Something downstream acts on the value, so a wrong one has a consequence.

## Skip If (ANY kills it)

- The output is genuinely open prose and every field is free text — you need entailment, not membership.
- The candidate set is only knowable after the model answers (open-world lookup, arbitrary URL, novel identifier) — the space is not closed and pretending it is will drop valid answers.
- The set is closed but unbounded in practice (millions of members streamed at request time) and the membership check would cost more than the error it prevents.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Seven testable rules. R1 is the closedness test; R2-R4 are the enforcement and the metric; R5-R7 are the boundaries — mixed outputs, the anti-pattern, and the licences on the fallback scorers. |
| `content/02-output-contract.xml` | The Closed-Set Validation Contract: every field, the metric definition, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six failure modes with symptom, cause and the rule that prevents each. |
| `content/06-decision-tree.xml` | Routing from observable output shape to membership check / entailment / neither. |
| `scripts/validate-closed-set-output-validation.py` | Validates a contract; rejects log-only handling, unbaselined thresholds, non-commercial scorers and claim decomposition of short justification strings. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/closed-set-validation-contract.yaml` | Fill-in contract for a fully closed output; ships valid. |
| `templates/closed-set-validation-contract-mixed.yaml` | The common real case — a closed identifier field beside an open prose field, with the metric scoped honestly. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `hallucination-attribution-checklist` — attribution for open outputs; this methodology is the closed-set branch of the same question.
- `hallucination-detection-online` — the runtime scorers, their accuracies and their licences, for the open fields this contract deliberately does not cover.
- `llm-hallucination-test-patterns` — packages the membership check as a CI test class; this methodology defines the metric it asserts on.
- `schema-semantic-constraint-gap` — membership is the strongest instance of post-validating what the grammar cannot express; a `pattern` on an ID field is weaker than checking the ID is one you supplied.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/closed-set-validation-contract.yaml`

```yaml
#
# Closed-Set Validation Contract — fully closed output.
# One contract per closed field. See content/02-output-contract.xml.
# If the field's legal values cannot be enumerated from an artefact YOU supplied,
# do not edit this file — the field is open and belongs to the entailment branch.
#
# Validate:  validate-closed-set-output-validation.py closed-set-validation-contract.yaml

system: "route an incoming support message to one of the configured queues"

closed_field: "queue_id"

# --- The gate (r1). Name the artefact and when it is materialised. ---
candidate_set_source: >
  the queue registry loaded from config at request time and serialised into the
  prompt as an id + name list
closedness_evidence: >
  Every legal queue_id is a key of the registry we serialise into this request; the
  registry is our own config, not the model's knowledge; a queue_id outside it routes
  the message nowhere and is wrong by definition.

# --- Select, do not author (r2). ---
selection_prompt_shape: set_in_request

# --- Enforcement (r4). A policy plus a counter; never a log line. ---
membership_check: "router.validate() lookup against the same registry map that built the prompt"
on_violation: reject
counter: hallucinated_queue_rate

# --- The metric (r3). Empty emission is its own rate, never a perfect score. ---
metrics:
  - grounding_rate
  - empty_result_rate
  - hallucinated_queue_rate

# Optional alert threshold. Requires a measured baseline — otherwise it is a guess
# and the validator says so.
threshold: 0.01
baseline_measured: true

# --- Scope (r5). No open fields here: the response is the id and nothing else. ---
open_fields: []

scorer: none
```

### `templates/closed-set-validation-contract-mixed.yaml`

```yaml
#
# Closed-Set Validation Contract — mixed output (the common real case).
# A closed identifier field beside an open prose field. The grounding rate covers
# the identifier and NOTHING ELSE; open_fields exists so that stays written down (r5).
#
# Validate:  validate-closed-set-output-validation.py closed-set-validation-contract-mixed.yaml

system: "rank a supplied candidate list of methodologies and justify each hit in one line"

closed_field: "hits[].id"

candidate_set_source: >
  the candidate map assembled by the local index for this query and serialised into
  the request body as an id + title + tier list
closedness_evidence: >
  Every legal id is a key of the candidate map built this request; the map is supplied
  verbatim in the prompt rather than recalled; an id outside it points at no document
  in the corpus, so it is wrong by definition rather than merely unusual.

selection_prompt_shape: narrowed_set_in_request

membership_check: "agent.go candByID lookup over the decoded hits, before the Result is built"
on_violation: drop
counter: hallucinated_id_rate

metrics:
  - grounding_rate
  - empty_result_rate
  - hallucinated_id_rate

# No threshold: we have no baseline yet. Do not invent one — an unmeasured
# threshold is a guess wearing a number.

# --- Scope (r5). The `why` string is NOT covered by grounding_rate. It is a UX
#     affordance under a hard cap, so it is sampled, not decomposed (r6). ---
open_fields:
  - name: "hits[].why"
    max_chars: 240
    review: sampling
    claim_decompose: false

# --- No scorer in the product. If one is ever added for the open field it is
#     HHEM-2.1-Open (Apache 2.0) as triage only; Bespoke-MiniCheck is CC BY-NC 4.0
#     and is barred from a commercial product outright (r7). ---
scorer: none
```
