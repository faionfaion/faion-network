# Agent Integration — Elicitation Techniques

## When to use

- Kickoff phase of a new initiative when stakeholder needs are vague, contradictory, or undocumented and the team needs a defensible record of who said what.
- Migration / replatforming projects where the only source of truth is tribal knowledge in 3-5 senior employees' heads and existing systems / documents.
- Regulated domains (medical, fintech, gov) where elicitation evidence (transcripts, observation logs, signed-off workshop minutes) is part of the audit trail.
- Pairing with `stakeholder-analysis/` (who to talk to), `ba-planning/` (when, what techniques), and `requirements-lifecycle/` (where the captured needs go next).
- Discovery sprints where the BA must mix techniques (interview + observation + document analysis) inside one week to triangulate a process.
- Distributed / async teams where surveys, recorded interviews, and Loom-style observation are the only feasible channels.

## When NOT to use

- Solo founder / 1-2-person team where direct conversation in Slack is faster than scheduling formal sessions.
- Backlog refinement on a stable product — Definition of Ready and slice conversations cover it; a workshop is overhead.
- When the answer is already in a spec, ADR, or RFC — read first, elicit only the gaps. LLMs love to propose interviews for problems already documented.
- Bug triage, incident postmortems — those have their own templates (5-whys, blameless retro), not BA elicitation.
- When stakeholders are unwilling or unavailable — surveys to a non-responsive group produce noise; escalate sponsorship instead.
- Throwaway prototypes / spikes where learning trumps a documented requirements set.

## Where it fails / limitations

- Stated needs ≠ actual needs. Interviews capture what people say they do; observation captures what they actually do. Skipping observation produces requirements that pass review and fail in production.
- Workshop dynamics get hijacked by the loudest voice. Without dot-voting or anonymous input the loudest stakeholder's view is recorded as "consensus".
- Surveys with <30% response rate are not data, they are anecdotes with statistics applied — the README does not flag this.
- Document analysis surfaces the *as-documented* state, which is usually 6-18 months behind the *as-implemented* state. Pair with observation or it lies.
- Prototyping anchors stakeholders on the prototype's affordances; they stop imagining alternatives. Use only after divergent elicitation, never as the first technique.
- Recordings + transcripts contain PII, salaries, performance complaints, customer names. Without a retention policy the elicitation archive becomes a compliance liability.
- Single-technique programs miss requirements. Triangulation (≥2 techniques per area) is the empirical fix; the README mentions it but does not enforce it.
- LLM-driven "interviews via chatbot" suppress emotional / non-verbal signal — sarcasm, hesitation, eye-rolls — which often carry the real requirement.

## Agentic workflow

Treat elicitation as a pipeline of evidence: each session produces a typed artifact (interview transcript, observation log, survey CSV, document-analysis note, workshop minutes) committed to git under `.aidocs/elicitation/<session-id>/` with YAML frontmatter (`session_id`, `technique`, `stakeholders`, `date`, `consent`, `pii_redacted`). A planner subagent reads `stakeholder-analysis/` and `ba-planning/` to schedule sessions and pick techniques; a transcriber agent ingests recordings (Whisper / Deepgram) and emits redacted transcripts; a synthesis agent extracts candidate requirements as `REQ-NNN` stubs feeding `requirements-lifecycle/`. Triangulation is enforced by a check that every `REQ-NNN` cites ≥2 distinct `session_id`s of different techniques before promotion to draft. Humans run the live sessions; agents prepare guides, transcribe, synthesise, and flag contradictions — never speak to stakeholders unattended.

### Recommended subagents

- `faion-sdd-executor-agent` — drives elicitation as SDD tasks: each session is a `TASK-NN` with checklist, artifact path, and a synthesis report. Closes only when transcript + redaction + extracted REQ stubs are committed.
- `faion-brainstorm` — used inside the synthesis step: diverge on possible interpretations of an ambiguous quote, converge to a single REQ stub or a follow-up question, review for leading-question bias.
- `faion-sdd-execution` (skill) — quality gates per session: consent recorded? PII redacted? technique ≠ previous session for this stakeholder group? triangulation count met?
- Custom `interview-prep-agent` (model: sonnet, per the README's Agent Selection table for "Gather and analyze requirements") — generates an interview guide from the topic + stakeholder profile, ranks open vs. closed questions, predicts likely follow-ups.
- Custom `transcript-redactor-agent` (model: haiku, "Format requirements in templates" row) — masks names, emails, SSNs, salaries via a regex + spaCy NER pass; outputs `transcript.redacted.md` next to the raw recording.
- Custom `elicitation-synthesizer-agent` (model: opus, "Perform gap analysis" row) — cross-references all session artifacts, emits the REQ stubs and a contradiction list with cited line ranges.
- Custom `survey-author-agent` (model: sonnet) — drafts the questionnaire from objectives, balances question types, validates against leading-question heuristics before publishing.

### Prompt pattern

Two-shot pattern: prep then synthesis. Both constrained to artifacts on disk.

```
You are interview-prep-agent. Produce an interview guide for {stakeholder_name}
({role}) on topic {topic}. Use the template in elicitation-techniques/templates.md.
Constraints: 6 main questions max; ≥2 open + ≥2 probing + ≥1 closing; no leading
phrasing ("don't you think...", "wouldn't you agree..."); cite the {prior_artifacts}
the question is meant to fill a gap in. Return strict JSON: {objectives[], questions[
{type, text, gap_filled}], pre_read[]}.
```

```
You are elicitation-synthesizer-agent. Given session artifacts {paths[]}, extract
candidate requirements. Each REQ must cite ≥2 session_ids of different techniques
(interview + observation, survey + workshop, etc.). Flag contradictions as
CONFLICT-NNN with the conflicting quotes. Do not invent stakeholders. Forbidden:
"users want", "stakeholders need" without a session citation. Return JSON
{reqs:[{id, text, citations:[{session_id, line_range}], confidence}], conflicts:[]}.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper` / `whisper.cpp` | Local STT for interview / workshop recordings; offline keeps PII out of cloud STT. | https://github.com/openai/whisper |
| `deepgram` CLI / API | Hosted STT with diarization (who-said-what), better for multi-speaker workshops. | https://developers.deepgram.com |
| `ffmpeg` | Pre-process audio (mono, 16kHz, denoise) before STT; chunk long sessions for parallel transcription. | https://ffmpeg.org |
| `git` + `git-lfs` | Version session artifacts; LFS for raw audio/video, plain git for transcripts and minutes. | https://git-lfs.com |
| `presidio-cli` (Microsoft Presidio) | Detect/redact PII (names, emails, SSNs, IBANs) in transcripts before commit. | https://microsoft.github.io/presidio |
| `spacy` + custom NER | Open-source PII / entity extraction when Presidio is too heavy. | `pip install spacy` |
| `pandoc` | Convert workshop minutes Markdown to PDF/DOCX for stakeholder sign-off. | https://pandoc.org |
| `gh issue` / `gh pr` | Mirror elicitation sessions as issues so non-BA team sees the schedule and outputs. | https://cli.github.com |
| `csvkit` | Aggregate survey CSV exports, run quick `csvstat` / `csvsql` analysis. | `pip install csvkit` |
| `lookatme` / `marp` | Render workshop slides from Markdown so the deck and minutes share a source. | https://marp.app |
| `tlp-cli` (Templated Letter Printer) / `mustache` | Generate per-stakeholder interview invites and consent forms. | `npm i -g mustache` |
| `mermaid-cli` (`mmdc`) | Render observed processes from Mermaid into PNG embedded in observation logs. | `npm i -g @mermaid-js/mermaid-cli` |
| `jq` / `yq` | Read/write artifact frontmatter and survey JSON in shell pipelines. | `apt install jq yq` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Otter.ai | SaaS | REST API | Auto-transcribes meetings; OK quality, weak diarization, retention policy is the gotcha. |
| Fireflies.ai | SaaS | REST + webhooks | Records Zoom/Meet/Teams, posts transcript webhooks agents can ingest. |
| Grain | SaaS | REST API | Strong moments / highlights API — good for synthesis agent input. |
| tl;dv | SaaS | REST API | Cheap, multilingual, useful for distributed teams. |
| Zoom Cloud Recording | SaaS | REST API | First-party recording + transcript download; pair with Whisper for better STT. |
| Riverside.fm | SaaS | REST API | High-quality multitrack recording; ideal for podcast-style interviews. |
| Dovetail | SaaS | REST + webhooks | Research-repo: tag transcripts, cluster insights — strong for synthesis. |
| Reduct.video | SaaS | REST API | Edit interviews like a doc, auto-clip moments. |
| EnjoyHQ / Condens | SaaS | REST API | UX-research repos with tagging APIs agents can drive. |
| Typeform | SaaS | REST + webhooks | Survey channel; webhook each response into a synthesis pipeline. |
| Tally.so | SaaS | REST + webhooks | Cheap Typeform alternative, similar webhook flow. |
| Google Forms | SaaS | Apps Script / Sheets API | Free, ubiquitous; pull responses via Sheets API into pandas. |
| LimeSurvey | OSS | REST API | Self-hosted survey when GDPR / on-prem is required. |
| Miro | SaaS | REST API | Workshop whiteboard; export boards as JSON for agents to parse. |
| FigJam | SaaS | REST API | Same role as Miro; integrates with Figma prototype work. |
| Mural | SaaS | REST API | Enterprise-flavoured workshop board with templates. |
| UserTesting / Maze | SaaS | REST API | Remote observation + prototype testing with built-in analytics. |
| Lookback / dscout | SaaS | REST API | Moderated and diary-study observation. |
| Loom | SaaS | REST API | Async observation: stakeholders record their workflow once, agents transcribe. |
| Notion / Confluence | SaaS | REST API | Storage for minutes and synthesis; gate writes via wrapper to avoid corrupting state fields. |

## Templates & scripts

The README has interview-guide and workshop-agenda templates. Inline below: a Python script that validates an elicitation-session artifact (frontmatter, consent, PII-redaction marker) and emits JSON status — wire into pre-commit so unredacted transcripts cannot land.

```python
#!/usr/bin/env python3
"""elicitation_session_check.py — validate session artifact pre-commit."""
from __future__ import annotations
import sys, json, re, datetime as dt, pathlib, yaml

REQUIRED = {"session_id", "technique", "stakeholders", "date",
            "consent", "pii_redacted"}
TECHNIQUES = {"interview", "workshop", "focus_group", "observation",
              "survey", "document_analysis", "prototyping", "brainstorming"}
PII_PATTERNS = [
    re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),               # email
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),                       # US SSN
    re.compile(r"\b(?:\d[ -]*?){13,19}\b"),                     # card-ish
]

def load(path: pathlib.Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"{path}: missing frontmatter")
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm) or {}, body

def main(p: str) -> int:
    path = pathlib.Path(p)
    fm, body = load(path)
    errors: list[str] = []
    if (m := REQUIRED - set(fm)):
        errors.append(f"missing fields: {sorted(m)}")
    if fm.get("technique") not in TECHNIQUES:
        errors.append(f"technique must be in {sorted(TECHNIQUES)}")
    if fm.get("consent") is not True:
        errors.append("consent != true")
    if fm.get("pii_redacted") is not True:
        errors.append("pii_redacted != true")
    leaks = [pat.pattern for pat in PII_PATTERNS if pat.search(body)]
    if leaks:
        errors.append(f"possible PII still present: {leaks}")
    print(json.dumps({"file": str(path), "errors": errors,
                      "ok": not errors}, indent=2, default=str))
    return 0 if not errors else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "session.md"))
```

## Best practices

- Triangulate every requirement: ≥2 techniques (e.g. interview + observation, or survey + workshop) before promoting from candidate to draft. Single-source REQs are flagged.
- Capture consent in the frontmatter (`consent: true`, `consent_basis: email|signed|verbal+recorded`). No consent → no commit.
- Redact PII at ingest, not later — Presidio / spaCy NER pass before the transcript hits git. Keep raw recordings outside the repo (S3 with lifecycle policy).
- Distinguish *stated*, *observed*, and *inferred* needs in the synthesis output. Tag each REQ with its source tier; observed > stated > inferred for credibility.
- Pre-read for interviews: send the guide 24h ahead. Stakeholders prepare, sessions get 30-50% deeper. Skipping pre-read is the most common quality leak.
- Use anonymous dot-voting in workshops (Miro / FigJam) to neutralise the loudest-voice effect; record per-vote anonymised tallies, not names.
- Cap an interview at 60 minutes and a workshop at 90 with a hard break. Past that point signal-to-noise collapses and notes become unreliable.
- Cross-link every elicitation artifact to a `stakeholder-analysis/` ID and a `ba-planning/` deliverable; otherwise the corpus becomes unsearchable within a sprint.
- Keep an "open questions" log per session that the next session is expected to close. Track close-rate as a process metric.
- Recording retention policy lives next to the artifact (`retention: 365d`); a cron job purges past-due recordings and logs the deletion. GDPR-friendly by default.
- For surveys, design with a target N and confidence interval, not "send to everyone". Pre-register the analysis plan to prevent post-hoc fishing.
- Run a "what did we miss" round at the end of every session — single highest-yield question, almost always uncovers an unspoken constraint.

## AI-agent gotchas

- Hallucinated stakeholders: synthesis agents invent plausible quotes ("the CFO said...") when none exists. Forbid any REQ without a `session_id + line_range` citation; reject outputs that fail the regex check.
- Leading-question generation: prep agents bias toward confirmation ("How much do you love feature X?"). Lint the guide for "don't you", "wouldn't", "isn't it true", and superlatives in question stems before sending.
- Transcription drift: Whisper hallucinates fluent text on silence / cross-talk. Always keep timestamps and require the synthesizer to cite line ranges; spot-check 10% manually.
- PII echo: agents quote redacted spans back in summaries because the redaction was only on the transcript copy, not on the indexed embeddings. Redact at the embedding source, not just at view time.
- Sentiment flattening: LLM summaries strip frustration, sarcasm, hesitation. Preserve emotional markers in the transcript (`[long pause]`, `[laughs]`) and require the synthesizer to surface them as a separate "tone" field.
- Workshop minute generation tends toward consensus narrative. Force the agent to also emit a `dissents` list with named (or pseudonymised) speakers.
- Survey design agents balance question types but ignore Likert-scale calibration (5-point vs. 7-point, label asymmetry). Cap the agent to a known-good template; humans approve the final scale.
- Document-analysis agents over-trust outdated docs. Require every "as-is" claim from a document to be cross-checked against ≥1 observation or interview.
- Prototyping prompts: agents propose hi-fi prototypes too early because the corpus is full of them. Constrain to paper / wireframe at the divergent stage; promote fidelity only after stakeholder validation.
- Token budget: long workshops produce 10-20k-token transcripts. Chunk per agenda item with overlap, not arbitrary windows; otherwise the synthesizer loses speaker context across chunks.
- Multi-language sessions: BA in Ukrainian, stakeholder in English mid-session — STT systems silently drop the minority language. Configure language hints per speaker; verify turn-by-turn.
- Human-in-the-loop checkpoints (mandatory): live sessions are run by humans, not agents; consent capture; PII-redaction sign-off before commit; final REQ list approval; any cross-stakeholder contradiction; any decision to close an open-questions log.

## References

- IIBA BABOK Guide v3, ch. 4 "Elicitation and Collaboration" — https://www.iiba.org/standards-and-resources/babok/
- ISO/IEC/IEEE 29148:2018 §6.4 Elicitation — https://www.iso.org/standard/72089.html
- Erika Hall, "Just Enough Research" (Rosenfeld, 2013) — interview & observation craft.
- Steve Portigal, "Interviewing Users" 2nd ed. (Rosenfeld, 2023) — non-leading questioning, recording ethics.
- Gause & Weinberg, "Exploring Requirements: Quality Before Design" — workshop facilitation patterns.
- Microsoft Presidio (PII detection / anonymisation) — https://microsoft.github.io/presidio
- OpenAI Whisper / whisper.cpp — https://github.com/openai/whisper
- Sibling methodologies in this repo: `stakeholder-analysis/`, `ba-planning/`, `requirements-lifecycle/`, `requirements-validation/`, `process-mining-automation/`, `agile-ba-frameworks/`.
