# Agent Integration — User Research at Scale

## When to use

- N >= 500 sessions/week or >= 50 unmoderated tests where manual coding is the bottleneck.
- Continuous discovery teams that need a steady weekly pulse (Teresa Torres cadence).
- Mature funnels with telemetry where qualitative needs to be cross-cut against quantitative cohorts.
- Product orgs with multiple teams running parallel studies (research-as-platform).
- Localization at scale — same study run across 5+ languages/regions, AI handles transcription + translation.
- High-volume B2C testing of micro-changes where moderated interviews are infeasible.
- Survey + behavior + interview triangulation when a single researcher cannot read everything.

## When NOT to use

- Small N (<10 deep interviews) — AI noise overwhelms signal; human coding is faster and richer.
- Strategic generative discovery — pattern-recognition is the value, not throughput.
- Sensitive/regulated topics (health, finance, minors) where consent + chain-of-custody require humans.
- Early-stage startups with <100 users — you do not have scale problems yet.
- Hypothesis-poor work — AI scaling amplifies bad questions linearly.
- Studies where rapport, body language, or longitudinal trust is the data.

## Where it fails / limitations

- Sentiment models miss sarcasm, code-switching, and culture-specific affect (especially non-English).
- AI auto-coding produces theme drift across batches if no fixed taxonomy is locked.
- Synthetic users / AI panels still bias toward training distribution; do not substitute for real users for novel UX.
- Bias detection (e.g., Maze) flags syntax not intent — leading questions slip through if phrased neutrally.
- Recordings without screen-region annotation lead AI to hallucinate user actions.
- LLM summarization compresses outliers — the most valuable quotes are the ones that get smoothed away.
- Cross-demographic clustering tends to reproduce platform demographics, not target market.
- No causal inference — patterns at scale still need experimental validation.

## Agentic workflow

Pipeline: `intake -> sampling -> instrumentation -> collection -> transcription -> coding -> synthesis -> review -> publish`.

### Recommended subagents

| Subagent | Model | Role | Inputs | Outputs |
|----------|-------|------|--------|---------|
| `research-intake` | sonnet | Convert PM brief to study spec, screener, hypotheses | one-pager | `study-spec.md`, screener JSON |
| `panel-sampler` | haiku | Build quotas, randomize, dedupe panel respondents | spec + panel API | participant CSV |
| `protocol-runner` | haiku | Execute unmoderated test scripts in Maze/Userlytics | study-spec | session IDs |
| `transcript-cleaner` | haiku | Strip filler, redact PII, normalize timestamps | raw VTT/JSON | clean transcripts |
| `theme-coder` | sonnet | Apply fixed codebook, tag quotes with codes + valence | transcripts + codebook | coded JSONL |
| `pattern-analyst` | opus | Cross-segment pattern mining, find non-obvious clusters | coded JSONL + segments | findings draft |
| `quote-curator` | sonnet | Select representative + outlier quotes per finding | coded JSONL | quote bank |
| `report-writer` | opus | Executive synthesis, recommendations, confidence tiers | findings + quotes | final report MD |
| `bias-auditor` | sonnet | Re-read questions/findings for leading phrasing, sample bias | spec + report | audit notes |
| `dashboard-publisher` | haiku | Push themes/sentiment to Looker/Notion/Dovetail | report | URLs |

Run `theme-coder` and `bias-auditor` in parallel; gate `report-writer` on a researcher human-in-loop checkpoint.

### Prompt pattern

```xml
<task>code-transcript</task>
<codebook src=".aidocs/research/codebook.yaml"/>
<rules>
  <rule>One quote may receive multiple codes; record span offsets.</rule>
  <rule>Reject codes not in codebook. Emit `proposed_codes` list instead.</rule>
  <rule>Tag valence in {-2,-1,0,1,2} with one-line evidence.</rule>
  <rule>If transcript is <80% English confidence, halt and request translation.</rule>
</rules>
<output schema="coded_quote_v1">JSONL</output>
<gotcha>Do not summarize. Preserve verbatim spans.</gotcha>
```

Use a frozen codebook + a separate `proposed_codes` channel — this prevents theme drift and surfaces emergent codes for human review.

## CLI tools

| Tool | Use |
|------|-----|
| `whisperx` | Forced-aligned transcription with diarization, faster than vanilla Whisper |
| `pyannote-audio` | Speaker diarization when WhisperX is insufficient |
| `ffmpeg` | Slice session recordings into per-task clips for AI scoring |
| `yt-dlp` | Pull session videos from CDN URLs given by panel platforms |
| `jq` / `duckdb` | Query coded JSONL transcripts and platform exports |
| `pandas` + `sentence-transformers` | Embed and cluster open-ended survey responses |
| `openai whisper` | Fallback transcription when WhisperX dependencies fail |
| `bertopic` | Topic modeling on large response corpora |
| `dvc` / `lakefs` | Version control for transcripts + codebooks (audit trail) |
| `presidio` | PII redaction before sending to external LLMs |
| `vale` / `textstat` | Screener readability checks (Flesch >= 60) |

## Services & apps

| Service | Tier | API/CLI | Notes |
|---------|------|---------|-------|
| UserTesting | enterprise | REST API + webhook | Largest panel, AI Insights add-on |
| Userlytics | mid+ | REST API | 2M+ panel, AI analytics, EU-friendly |
| Maze | self-serve+ | API + Zapier | Strong for unmoderated + bias detection |
| dscout | enterprise | API | Mobile ethnography, longitudinal diaries |
| Lookback | mid | API | Live moderated, recording vault |
| Dovetail | all | REST + GraphQL | Repository + AI tagging, codebook host |
| Condens | mid | API | Analysis-only repository, codebook-friendly |
| Notably | self-serve | API beta | AI synthesis, theme suggestions |
| Marvin | self-serve | API | Lightweight repository, low cost |
| Reduct.video | mid | API | Edit-by-transcript, fast quote extraction |
| Sprig | mid | API + JS SDK | In-product micro-surveys at session scale |
| Hotjar / FullStory | mid | API | Session replay + heatmaps for behavior layer |
| Great Question | mid | API | ResearchOps + panel CRM |
| Rally / User Interviews | mid | API | Recruitment + scheduling automation |
| OpenAI / Anthropic | API | SDK | Coding, synthesis, embeddings (use prompt caching) |

## Templates & scripts

`codebook.yaml` (frozen taxonomy):

```yaml
version: 1.3.0
codes:
  - id: ONB-FRICTION
    label: Onboarding friction
    valence_default: -1
    examples: ["I had to enter my email three times"]
  - id: PRICE-SHOCK
    label: Pricing surprise
    valence_default: -2
  - id: AHA
    label: Aha moment
    valence_default: 2
segments: [persona, plan, region, device]
```

Batch-coding shell:

```bash
#!/usr/bin/env bash
# code_batch.sh — run theme-coder agent over a transcript directory
set -euo pipefail
CODEBOOK=.aidocs/research/codebook.yaml
OUT=.aidocs/research/coded
mkdir -p "$OUT"
for f in transcripts/*.json; do
  base=$(basename "$f" .json)
  test -f "$OUT/$base.jsonl" && continue
  claude -p "$(cat prompts/theme-coder.xml)" \
    --input-file "$f" --context-file "$CODEBOOK" \
    --output-file "$OUT/$base.jsonl" --model sonnet
done
duckdb -c "COPY (SELECT * FROM read_json_auto('$OUT/*.jsonl')) TO 'coded.parquet'"
```

Pattern-analyst invocation (Python):

```python
from anthropic import Anthropic
c = Anthropic()
msg = c.messages.create(
    model="claude-opus-4-5",
    max_tokens=4096,
    system=open("prompts/pattern-analyst.xml").read(),
    messages=[{"role": "user", "content": [
        {"type": "text", "text": open("coded.parquet.summary.json").read(),
         "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": "Find clusters per segment. Confidence tier each."},
    ]}],
)
```

## Best practices

- Lock the codebook before collection; version it (`v1.0.0`) and bump only with documented diffs.
- Sample 10% of AI-coded segments for human re-coding every batch; track inter-rater agreement (Cohen's kappa >= 0.7).
- Stratify panels by behavior (active/lapsed/new), not just demographics — demographic-only sampling hides usage truth.
- Cache full transcripts in the LLM context (prompt caching) — coding hundreds of quotes against the same codebook benefits massively.
- Triangulate: AI sentiment + behavioral analytics + verbatim quote — never report a finding from one source alone.
- Confidence tiers in every finding: high (>=3 evidence types), medium (2), low (1, flag for follow-up).
- Always publish the disconfirming quotes too — outliers are signal, not noise.
- Keep raw recordings 90 days minimum for audit; coded data forever.
- Pre-register hypotheses in study-spec — scaled research without hypotheses is exploratory dredging.
- Run the `bias-auditor` BEFORE collection on questions, AFTER on findings — two checkpoints.
- Maintain a `themes-changelog.md` so stakeholders see how findings evolve across waves.

## AI-agent gotchas

- LLMs hallucinate participant IDs when asked to cite quotes — require verbatim span offsets, not paraphrases.
- Sentiment polarity flips on negation in low-resource languages; force a `language` field per quote and route accordingly.
- Long-context models silently truncate transcript bundles >200k tokens; chunk at session boundaries with overlap.
- Theme-coder will invent codes if codebook is unclear; use strict allow-list + `proposed_codes` overflow channel.
- Pattern-analyst over-indexes on the first segment in the prompt — randomize segment order across runs.
- Cost trap: re-running coding on the same transcript without caching burns 10x tokens. Hash + cache outputs.
- Synthetic-user/persona agents leak training-data clichés — never present them as real research.
- Privacy: redact PII before any external LLM call; check that platform recordings have consented to AI processing.
- Transcripts from low-quality audio produce confident-but-wrong text; gate on Whisper confidence scores >= 0.6.
- Cross-platform exports use different timestamp formats (Maze ms, UserTesting ISO); normalize early.
- Agents will quietly drop non-English sessions if prompt does not explicitly handle them — assert language coverage in tests.
- Dashboards auto-update faster than humans can vet — add a "draft/published" gate on every finding.

## References

- Userlytics docs: https://www.userlytics.com/resources/
- Maze API: https://help.maze.co/hc/en-us/sections/4406635693585-API
- UserTesting API: https://api.usertesting.com/docs
- Dovetail API: https://developers.dovetail.com/
- Sprig docs: https://docs.sprig.com/
- Teresa Torres — Continuous Discovery Habits (book) — cadence framework that scales with AI
- Nielsen Norman Group — "AI in UX Research" (2024) — limits and pitfalls
- ReOps Community (researchops.community) — repository, codebook, and panel ops patterns
- Anthropic prompt caching guide — https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- Whisper / WhisperX — https://github.com/m-bain/whisperX
- BERTopic — https://maartengr.github.io/BERTopic/
- Microsoft Presidio (PII redaction) — https://microsoft.github.io/presidio/
- "AI co-pilot" model in research ops — Userlytics, Maze, Dovetail 2025-2026 product docs
