# Schema Semantic Constraint Gap

## Summary

**One-sentence:** Produces a Schema Pair Record — a wire schema carrying only the keywords the provider actually compiles, a validation schema carrying the full contract, and a named code-level check plus counter for every semantic constraint the grammar silently drops.

**One-paragraph:** Constrained decoding guarantees SHAPE and nothing else. The provider compiles your JSON Schema into a grammar that masks the token distribution, so `JSON.parse` stops failing — but the grammar has no way to express a numeric range, a string length or a regular expression, so those keywords are stripped from the wire schema and enforced by nobody. On Anthropic (docs read 2026-08-03) `minimum`, `maximum`, `multipleOf`, `minLength`, `maxLength`, `pattern` and `maxItems` are all unsupported; the official Pydantic and Zod helpers quietly fold them into the field `description` as prose. A single schema file that pretends to be both wire contract and validation contract therefore reports green while shipping out-of-range scores and overlong strings. This methodology splits the file in two, forces one post-validation with a counter per dropped keyword, records the transport divergence (Gemini's OpenAPI subset accepts `pattern` and ranges; Claude does not, so the same request validates differently per transport), and carries the one hard interoperability fork: enabling `citations` on a `document` or `search_result` block together with `output_config.format` returns a 400.

**Ефективно для:**

- Anyone treating a passing schema check as a correctness check — the most common false green in an LLM pipeline.
- Schemas whose only real protections are ranges, lengths and regexes, i.e. most extraction and scoring schemas.
- Multi-transport clients where the same schema is sent to Anthropic, Gemini and an OpenAI-compatible endpoint and is enforced at three different strengths.
- Any design that wants both machine-parseable output and provider-emitted citations, which is a two-call design or a 400.

## Applies If (ALL must hold)

- A JSON Schema is sent to a model as a structured-output or strict-tool contract.
- The schema contains at least one constraint that is not a type, an enum, `required` or `additionalProperties: false`.
- Something downstream consumes the parsed values without re-checking them.

## Skip If (ANY kills it)

- The schema is types and enums only — those ARE compiled, and there is nothing to drop.
- Output is free prose that no code parses; there is no schema to split.
- The consumer already re-validates every field against an independent full-Draft-7 validator and counts the failures — you have the outcome, the record is bookkeeping.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Seven testable rules. R1 states the gap; R2-R4 are the split and the enforcement; R5 is the citations fork; R6-R7 are the two ways the wire schema itself bites back. |
| `content/02-output-contract.xml` | The Schema Pair Record: every field, the per-transport unsupported keyword lists, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six production failure modes with symptom, cause and the rule that prevents each. |
| `content/06-decision-tree.xml` | Routing from observable schema and transport properties to split / post-validate / two-call. |
| `scripts/validate-schema-semantic-constraint-gap.py` | Validates a record; walks the wire schema for keywords the declared transport drops and demands a checker plus counter for each. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema-pair-record.yaml` | Fill-in record for a single-transport structured-output call; ships valid against the contract. |
| `templates/schema-pair-record-two-call.yaml` | The citations fork — call 1 structured, call 2 cited, neither doing both. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- `structured-output-mode-picker` — picks json mode vs strict SO vs tool call vs grammar; this methodology starts after that choice and asks what the chosen mode does not enforce.
- `two-pass-reason-then-extract` — where the reasoning goes when a format contract is in play; the semantic gap is orthogonal and applies to both passes' outputs.
- `closed-set-output-validation` — the strongest instance of a post-validation: when the field's legal values are an enumerable set you supplied, membership replaces the regex entirely.
- `citation-contract-back-to-source` — the citation side of the 400 fork.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/schema-pair-record.yaml`

```yaml
#
# Schema Pair Record — single-transport structured-output call.
# See content/02-output-contract.xml. The drop set is COMPUTED by the validator
# from the diff between validation_schema and wire_schema — do not hand-maintain
# it, and do not book a drop the diff cannot see.
#
# Validate:  validate-schema-semantic-constraint-gap.py schema-pair-record.yaml

system: "rank a supplied candidate list into a scored hit list"

transports: [anthropic]

wire_schema_path: "internal/search/schemas/search.wire.json"
validation_schema_path: "internal/search/schemas/search.validation.json"

# --- The full contract. This is what the output must satisfy. ---
validation_schema:
  type: object
  properties:
    hits:
      type: array
      maxItems: 20
      items:
        type: object
        properties:
          id: { type: string, pattern: "^[a-f0-9]{16}$" }
          score: { type: number, minimum: 0, maximum: 1 }
          why: { type: string, maxLength: 240 }

# --- The wire copy. Compiled keywords only (r1). Everything the grammar cannot
#     express has been stripped deliberately, not hopefully (r6). ---
wire_schema:
  type: object
  additionalProperties: false
  properties:
    hits:
      type: array
      minItems: 0            # 0 and 1 compile; any other value does not
      items:
        type: object
        additionalProperties: false
        required: [id, score, why]
        properties:
          id: { type: string }
          score: { type: number }
          why: { type: string }

# --- One entry per computed drop. enforced_by is a code location; a log line
#     is not enforcement (r3). ---
dropped_keywords:
  - keyword: maxItems
    field: "/hits"
    on_violation: clamp
    enforced_by: "search.Run clamps decoded hits to opts.Top before returning"
    counter: overflow_rate
  - keyword: pattern
    field: "/hits[]/id"
    on_violation: drop
    enforced_by: "agent.go candByID membership check (stronger than the regex)"
    counter: hallucinated_id_rate
  - keyword: minimum
    field: "/hits[]/score"
    on_violation: reject
    enforced_by: "search.validateHit range check"
    counter: range_violation_rate
  - keyword: maximum
    field: "/hits[]/score"
    on_violation: reject
    enforced_by: "search.validateHit range check"
    counter: range_violation_rate
  - keyword: maxLength
    field: "/hits[]/why"
    on_violation: clamp
    enforced_by: "search.validateHit rune-length check (runes, not bytes)"
    counter: why_overflow_rate

# --- Prose restated for the model only. NOT enforcement (r6). ---
hints:
  - keyword: maxLength
    field: "/hits[]/why"
    text: "description says: at most 240 characters, one sentence"

structured_output: true
citations_enabled: false
citations_plan: structured_only

# --- schema_valid_rate plus at least one semantic rate (r7). ---
metrics:
  - schema_valid_rate
  - hallucinated_id_rate
  - range_violation_rate
  - why_overflow_rate
  - overflow_rate

value_accuracy_review: >
  Sampled human review of ranking order and of whether each `why` string is true
  of the document it points at — 20 queries per release. Compliance is not reviewed.
```

### `templates/schema-pair-record-two-call.yaml`

```yaml
#
# Schema Pair Record — the citations fork (r5), multi-transport (r4).
# Enabling `citations` on a document / search_result block together with
# `output_config.format` returns 400. This record describes CALL 1 of a two-call
# design: schema-constrained identifier selection, no citations. Call 2 sends the
# bodies of exactly those identifiers with citations on and no format parameter,
# and needs no schema pair because it emits prose.
#
# Validate:  validate-schema-semantic-constraint-gap.py schema-pair-record-two-call.yaml

system: "select source documents to explain, then cite them in prose (call 1 of 2)"

# Two providers, two grammars. The validator takes the UNION of their drop sets,
# so a constraint Gemini would have enforced is still post-validated in code.
transports: [anthropic, gemini]

wire_schema_path: "internal/explain/schemas/select.wire.json"
validation_schema_path: "internal/explain/schemas/select.validation.json"

validation_schema:
  type: object
  properties:
    doc_ids:
      type: array
      maxItems: 10
      items: { type: string, pattern: "^[a-f0-9]{16}$" }
    confidence: { type: number, minimum: 0, maximum: 1 }

wire_schema:
  type: object
  additionalProperties: false
  required: [doc_ids, confidence]
  properties:
    doc_ids:
      type: array
      minItems: 1
      items: { type: string }
    confidence: { type: number }

dropped_keywords:
  - keyword: maxItems
    field: "/doc_ids"
    on_violation: clamp
    enforced_by: "explain.selectDocs truncates to the configured cap"
    counter: doc_overflow_rate
  - keyword: pattern
    field: "/doc_ids[]"
    on_violation: drop
    enforced_by: "explain.selectDocs membership check against the supplied corpus slice"
    counter: hallucinated_id_rate
  - keyword: minimum
    field: "/confidence"
    on_violation: reject
    enforced_by: "explain.validateSelection range check"
    counter: range_violation_rate
  - keyword: maximum
    field: "/confidence"
    on_violation: reject
    enforced_by: "explain.validateSelection range check"
    counter: range_violation_rate

structured_output: true
citations_enabled: false
citations_plan: two_call
two_call_note: >
  Call 1 (this record): output_config.format set, citations off, returns doc_ids.
  Call 2: the bodies of exactly those doc_ids are attached as search_result blocks
  with citations.enabled true and NO output_config.format; the prose it returns is
  verified by search_result_index rather than by a schema.

metrics:
  - schema_valid_rate
  - hallucinated_id_rate
  - range_violation_rate
  - doc_overflow_rate

value_accuracy_review: >
  Call 1 is reviewed on whether the selected documents are the right ones; call 2 is
  reviewed on whether each citation index resolves to text that supports the sentence.
```
