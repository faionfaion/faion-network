# Risk-Scored Fan-Out Audit

## Summary

**One-sentence:** Audits a corpus far larger than any one context using many agents, without the audit inventing findings: a deterministic scout emits a risk-scored, wave-ordered work manifest; a cheap triage pass fans out over slices; an adversarial refute pass kills plausible-but-wrong findings before a human sees them; an aggregator enforces an evidence floor as arithmetic; and nothing is ever applied automatically.

**One-paragraph:** The naive multi-agent audit is a fan-out plus a merge, and it lies to you in three specific ways. It flags plausible items with confident reasoning, because triage is tuned for recall. It reports findings with no evidence, because "always cite evidence" is a prompt instruction rather than a control. And it silently loses rows, because agents drift a schema when they write files even when the value they returned through the tool boundary validated — one run wrote `judgment` where the contract said `verdict`, and those rows disappeared from every tally with no error anywhere. This methodology is the shape that survives all three: risk score → waves → triage → refute-only-the-suspects → evidence floor applied in the aggregator → defensive field read with a counted fallback → human-gated apply. The cost discipline is structural rather than exhortative — no agent, and never the orchestrating loop, reads the whole corpus; each verifier gets one slice plus at most the single source document that slice cites.

**Ефективно для:** content-correctness audits over large item banks, link and citation verification, spec-to-implementation conformance sweeps, licence and policy scans over a monorepo — any job where the corpus does not fit and the findings will change something.

## Applies If (ALL must hold)

- The corpus is too large for one context to read.
- Ground truth exists that individual items can be checked against.
- Items are independently checkable — one item's verdict does not depend on another's.
- A human will approve changes; the audit itself edits nothing.

## Skip If (ANY kills it)

- The corpus fits in one context — one reviewer beats a manifest, a merge and a drift normaliser.
- No source of truth exists — every verdict would be `UNVERIFIABLE`, determinable for free.
- Findings would be applied automatically — fix the governance first; an audit with an apply path is a rewrite engine.
- The corpus needs holistic judgement (tone, narrative arc) rather than per-item verdicts — slicing destroys exactly the signal.

## Prerequisites

| Input artefact | Format | Source |
|---|---|---|
| Enumerable corpus with stable item ids | files or records | the repo |
| Source-of-truth documents | files, addressable per item | the corpus owner |
| Risk signals per item (provenance, citation, classification, status) | fields on the item | the corpus itself |
| Rate-limit / budget check | GO / HOLD | run before each wave's fan-out |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[citation-contract-back-to-source]]` | Defines what counts as evidence; this methodology only enforces that it is present. |
| `[[gate-fail-closed-rule]]` | The evidence floor and the no-auto-apply rule are both fail-closed gates. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 rules: scout before agents, risk-first waves, evidence-or-downgrade, triage then adversarial refute, disagreement is ambiguous, never auto-apply, normalise field drift on read, calibrate before the bulk, machine-compute every count, unverifiable is a result | ~1400 |
| `content/02-output-contract.xml` | essential | JSON Schema for a per-wave verdict set + seven forbidden patterns, with a failing example built from real run output | ~1000 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns (schema-validated return vs unvalidated file, one-pass audit, "check" instead of "refute", evidence floor as prompt text, auto-apply, fan-out before the mapping is checked, uniform waves) + cheap symptoms | ~950 |
| `content/06-decision-tree.xml` | essential | Root: "too big for one context AND checkable against a source?" then one branch per missing pipeline part | ~750 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Write the scout / manifest generator | sonnet | Deterministic local code over known fields. |
| Triage pass over a slice | sonnet | High volume, recall-oriented, cheap per item. |
| Adversarial refute pass | opus | Small flagged set; this is where a wrong call costs the most. |
| Aggregate and report | haiku | Arithmetic and formatting; all judgement already happened. |
| Hand calibration | human | The one step that must not be delegated — it measures the pipeline. |

## Templates

| File | Purpose |
|------|---------|
| `templates/verdict-schema.json` | The per-item verdict contract, ready to pass to a structured-output call. |
| `templates/triage-prompt.txt` | Pass-one prompt: one slice, one source file, suspect generously, evidence or the finding is discarded. |
| `templates/refute-prompt.txt` | Pass-two prompt: refute stance, default "stands", deliberately withholds the triage reasoning. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-risk-scored-fanout-audit.py` | Validates a per-wave verdict set and normalises agent field drift on read (`verdict \|\| judgment \|\| decision \|\| assessment` → `PARSE_ERROR`), counting fallbacks. Enforces the evidence floor, no-auto-apply, suspect coverage, reconciled counts, unique ids and the calibration floor. `--normalise` rewrites with canonical names; `--self-test` replays twelve fixtures. | After every wave aggregation, before the report is shown to anyone. |

## Related

- [[citation-contract-back-to-source]] — what a piece of evidence has to be
- [[gate-fail-closed-rule]] — why the floor lives in the aggregator, not the prompt
- [[ci-eval-gate-config]] — wiring the same shape into a repeatable gate
- [[inc-read-only-investigation-default]] — the same "investigate without mutating" posture, applied to incidents

## Decision tree

See `content/06-decision-tree.xml`. It gates first on two observables — corpus larger than one context, and ground truth exists — then routes each missing pipeline part (manifest, wave ordering, second pass, tie-break rule, evidence floor location, aggregator field read, calibration, hand-typed counts) to the one rule that supplies it.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/verdict-schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "verdict", "suspect", "evidence"],
    "additionalProperties": false,
    "properties": {
      "id": {"type": "string", "minLength": 1},
      "verdict": {"type": "string",
        "enum": ["CONFIRMED", "INCORRECT", "WEAK", "AMBIGUOUS", "OUT_OF_SCOPE", "UNVERIFIABLE"]},
      "confidence": {"type": "number", "minimum": 0, "maximum": 1},
      "suspect": {"type": "boolean"},
      "issue": {"type": "string", "maxLength": 300},
      "fix": {"type": ["string", "null"], "maxLength": 500},
      "evidence": {"type": "string"},
      "refuted_by": {"type": "integer", "minimum": 0},
      "refuter_notes": {"type": "array", "items": {"type": "string"}},
      "verified": {"type": "boolean"}
    }
  }
}
```

### `templates/triage-prompt.txt`

```text
You are reviewing {n} items from a corpus for content correctness. You see only
these items. Do not ask for more.

For each item, decide whether its stated answer is correct and whether the
alternatives offered are fair.

- If the item has a {source_path}, READ THAT ONE FILE and quote the sentence that
  supports or contradicts it. Do not open any other file.
- If the item has no source, use only widely established domain canon, and name it.
- If you cannot source it either way, return UNVERIFIABLE. Never guess.

Set suspect=true whenever you would want a second opinion. A later adversarial
pass will try to refute every suspect, so a false flag is cheap here and a missed
defect is not.

Every INCORRECT, WEAK or OUT_OF_SCOPE verdict MUST carry verbatim evidence or a
named source in `evidence`. A finding without evidence is discarded downstream.

Return ONLY JSON matching {schema}; if you write a file, use the exact field names.

ITEMS:
{slice}
```

### `templates/refute-prompt.txt`

```text
You are trying to REFUTE a proposed finding, not to confirm it.

Your default position is: the item as written is correct, and the finding against
it is wrong. Move off that position only on positive evidence in the source.
Absence of support is not evidence against.

Read {source_path} and nothing else. Quote the sentence you rely on.

You are deliberately NOT shown the reasoning behind the finding — a refuter given
the argument tends to paraphrase it back.

Answer with exactly one of: "stands" · "overturned" (quote + corrected form) ·
"unclear" (a real answer, not a failure to decide).

Your verdict is one vote of {n_refuters}. A majority decides; a split resolves to
AMBIGUOUS with every note recorded.

Return ONLY JSON matching {schema}, note in `issue`, quote in `evidence`.

ITEM:
{item}
```
