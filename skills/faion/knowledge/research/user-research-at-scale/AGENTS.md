# User Research at Scale

## Summary

**One-sentence:** 9-stage AI-augmented research-ops pipeline (intake -> sampling -> instrumentation -> collection -> transcription -> coding -> synthesis -> review -> publish) with frozen codebook + N>=500/wk capacity + HITL gates.

**One-paragraph:** Operates at N>=500 interview sessions/week or >=50 unmoderated tests, running a 9-stage AI-augmented pipeline: intake, sampling, instrumentation, collection, transcription, coding (frozen codebook + proposed_codes overflow channel), synthesis, review, publish. Human-in-the-loop checkpoints gate publication; codebook drift is bounded by the proposed_codes channel; PII handling forced through ZDR endpoints.

**Ефективно для:**

- N >= 500 сесій/тиждень або >= 50 unmoderated tests - manual coding не масштабується.
- Continuous discovery: weekly pulse a-la Teresa Torres з high volume.
- Multi-team product orgs з паралельними studies (research-as-platform).
- Localization: одне дослідження у 5+ мовах.
- Survey + behavior + interview triangulation - один researcher не прочитає все.

## Applies If (ALL must hold)

- N>=500 sessions/week or >=50 unmoderated tests where manual coding is the bottleneck.
- Continuous discovery teams needing a weekly pulse.
- Product orgs with multiple teams running parallel studies (research-as-platform).
- Localisation at scale (same study across 5+ languages).
- Survey + behavior + interview triangulation where one researcher cannot read everything.

## Skip If (ANY kills it)

- Small N (<10 deep interviews) - AI noise overwhelms signal.
- Strategic generative discovery where pattern recognition beats throughput.
- Sensitive / regulated topics (health, finance, minors) requiring manual consent chains.
- Early-stage startups with <100 users - no scale problem yet.
- Studies where rapport, body language, or longitudinal trust is the data.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Frozen codebook | YAML | research lead |
| Sampling plan | spreadsheet | research-ops |
| ZDR-eligible LLM endpoint | config | infrastructure / vendor |
| Transcription provider | Otter / Fireflies / Looppanel API | research-ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[continuous-discovery]] | supplies the weekly cadence that this pipeline feeds |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 8-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `intake-classify` | haiku | Classify incoming requests by study type + segment + tier. |
| `sampling-plan` | sonnet | Stratified sampling design + recruit batch sizes. |
| `transcription` | haiku | Mechanical transcript via vendor API. |
| `coding-frozen-book` | sonnet | Apply frozen codebook; route novel themes to proposed_codes. |
| `synthesis` | opus | Cross-study pattern recognition + weekly synthesis. |
| `hitl-gate` | human | Human review checkpoint before publish. |

## Templates

| File | Purpose |
|------|---------|
| `templates/codebook.yaml` | Frozen codebook with proposed_codes overflow channel |
| `templates/code-batch.sh` | Bash launcher: coding-frozen-book agent over a batch of transcripts |
| `templates/research-ops-report.md.j2` | Weekly research-ops report skeleton |
| `templates/research-ops-report.md` | Weekly research-ops report skeleton Generated from `templates/research-ops-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-research-at-scale.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[continuous-discovery]]
- [[persona-building]]
- [[survey-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/codebook.yaml`

```yaml
# codebook.yaml — frozen taxonomy for AI-assisted research coding
# Version: 1.0.0 — bump version with documented change entry when modifying
# Do NOT add codes mid-study. Use proposed_codes overflow channel instead.

version: 1.0.0

codes:
  - id: ONB-FRICTION
    label: Onboarding friction
    valence_default: -1
    examples:
      - "I had to enter my email three times"
      - "I didn't know where to start"

  - id: PRICE-SHOCK
    label: Pricing surprise (unexpected cost)
    valence_default: -2
    examples:
      - "I didn't realize I'd be charged for that"
      - "The price jumped when I added a second user"

  - id: AHA
    label: Aha moment (value realization)
    valence_default: 2
    examples:
      - "Oh, it does that automatically — that's exactly what I needed"
      - "When I saw the dashboard for the first time I got it"

  - id: MISSING-FEATURE
    label: Feature gap (desired capability absent)
    valence_default: -1
    examples:
      - "I wish I could export this as CSV"
      - "There's no way to share this with my team"

  - id: TRUST
    label: Trust signal (security, reliability, brand)
    valence_default: 1
    examples:
      - "I felt confident it would keep my data safe"
      - "The company has been around for 10 years"

segments:
  - persona     # mapped to persona definition in study-spec.md
  - plan        # free | starter | pro | enterprise
  - region      # ISO 3166-1 alpha-2
  - device      # web | mobile | desktop
```

### `templates/code-batch.sh`

```bash
#!/usr/bin/env bash
# code-batch.sh — run theme-coder agent over a transcript directory
# Input: transcripts/*.json (one file per session)
# Output: .aidocs/research/coded/*.jsonl + coded.parquet
# Skips already-coded transcripts (idempotent via output file check).
set -euo pipefail

CODEBOOK=.aidocs/research/codebook.yaml
PROMPTS=prompts/theme-coder.xml
OUT=.aidocs/research/coded
mkdir -p "$OUT"

for f in transcripts/*.json; do
  base=$(basename "$f" .json)
  if [ -f "$OUT/$base.jsonl" ]; then
    echo "skip: $base (already coded)"
    continue
  fi
  echo "coding: $base"
  claude -p "$(cat "$PROMPTS")" \
    --input-file "$f" \
    --context-file "$CODEBOOK" \
    --output-file "$OUT/$base.jsonl" \
    --model claude-sonnet-4-5
done

# Aggregate coded JSONL into parquet for analysis
duckdb -c "COPY (SELECT * FROM read_json_auto('$OUT/*.jsonl')) TO 'coded.parquet'"
echo "Parquet written: coded.parquet"
```
