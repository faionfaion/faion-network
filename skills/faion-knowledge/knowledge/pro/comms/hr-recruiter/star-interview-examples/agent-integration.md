# Agent Integration — STAR Interview Examples & Implementation

## When to use
- Calibrating new interviewers on the STAR method using example answers (strong, weak, red-flag) and structured probing scripts.
- Generating role-specific STAR question banks per competency and per seniority level (IC2/IC3/IC4 etc.).
- Real-time interview note-taking and STAR-component classification (Situation/Task/Action/Result), reducing recency bias in scorecards.
- Post-debrief calibration: agents compare interviewer scores on the same response and flag divergence > 1 point for committee discussion.
- Producing reference-check question lists tied to specific STAR claims surfaced during interviews.

## When NOT to use
- Live, fully-automated screening of candidates without human interviewer present — produces over-confident pass/fail decisions and risks legal exposure (EEOC, GDPR, EU AI Act high-risk classification).
- Personality / culture-fit assessment — STAR is for past behavior on competencies, not "vibe".
- Roles where past behavior poorly predicts future (early-career with no equivalent experience) — use work-sample tests instead.
- Highly regulated jurisdictions (NYC AEDT law, Illinois AI Video Interview Act, EU AI Act) require bias audits, candidate disclosure, and consent — agents must not silently process recordings.

## Where it fails / limitations
- LLM scoring of STAR responses is biased toward fluent, polished delivery — disadvantages non-native speakers and neurodiverse candidates whose answers may have weaker structure but stronger substance.
- Agents accept hypothetical answers ("I would...") as STAR responses; the methodology requires actual past behavior. Strict prompt rules needed.
- Generated STAR questions trend toward generic ("tell me about a time you led a team") instead of competency-anchored — without the role's competency model, output is shallow.
- Probing scripts in templates assume English-speaking native flow; cross-cultural interviews need adapted phrasing.
- Verbatim transcripts surface protected-class info (pregnancy, religion, age); agents must redact before storage and never use such info in scoring.
- Models trained on Amazon-style Leadership Principles overweight that bar-raiser pattern even when competency model differs.

## Agentic workflow
A pre-interview agent ingests the role's competency model + seniority level and produces 6–8 STAR questions per competency, plus probing follow-ups. During the interview, an in-meeting note-taker (Read.ai / Otter.ai webhook → agent) classifies utterances by STAR component and flags missing components in real time on a Slack DM to the interviewer. Post-interview, the agent drafts a structured scorecard with quoted evidence per competency; the interviewer edits and submits. A calibration agent runs weekly: it pulls scorecards across the same role and flags inter-rater divergence + bias signals.

### Recommended subagents
- `faion-recruiter-agent` (referenced in README) — primary STAR domain agent.
- `faion-interview-coach` (custom, sonnet) — pre-interview prep with interviewers, role-plays, and follow-up probing.
- `faion-scorecard-reviewer` (custom, sonnet, Read-only) — post-interview audit for evidence completeness and protected-class language.
- `faion-improver` — quarterly retrospective on hire quality vs. interview scores → which competencies actually predict performance.
- Pair with the `pro/comms/hr-recruiter/structured-interview-design` methodology for upstream scorecard design.

### Prompt pattern
```
For role <Senior Backend Engineer> with competencies
[ownership, technical depth, collaboration, ambiguity], generate 2 STAR
questions per competency. Each question must:
- ask about specific past situation, not hypothetical
- be open-ended (no yes/no)
- include 3 probing follow-ups for missing S/T/A/R components
- avoid leading language ("a difficult time when...")
Output as YAML with question, probes, and red flags.
```

```
Classify each candidate utterance below into S, T, A, R, or NOT_STAR.
For each missing component, output the exact probing follow-up to ask.
Mark any utterance referencing protected class (age, family, religion,
disability, nationality) with REDACT and DO NOT use in scoring.
<<<TRANSCRIPT>>>
```

```
Two interviewers scored the same candidate on <competency>. Scores
differ by <delta>. Quote each interviewer's evidence. Identify whether
the gap is: (a) different evidence captured, (b) different rubric
interpretation, (c) potential bias signal. Recommend calibration step.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper.cpp` | On-device transcript (privacy-preserving) | https://github.com/ggerganov/whisper.cpp |
| `pyannote.audio` | Speaker diarization (interviewer vs candidate) | `pip install pyannote.audio` |
| `pandoc` | Convert scorecard MD → PDF for committee | OS package |
| `op` | Pull ATS API tokens | https://developer.1password.com/docs/cli |
| `gh` CLI | Open PR adding question banks to repo | https://cli.github.com |
| `jq` | Parse Greenhouse/Lever scorecard JSON | OS package |
| `csvkit` | Slice scorecard CSV exports for calibration | `pip install csvkit` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Greenhouse / Lever / Ashby ATS | SaaS | Yes | Scorecards, competency mapping, candidate stages via API. |
| Metaview / BrightHire | SaaS | Yes | AI interview intelligence; STAR detection out of the box. Check region for legal compliance. |
| Otter.ai / Read.ai / Fireflies | SaaS | Yes | Transcripts via API + webhooks. |
| Zoom / Google Meet recording | SaaS | Partial | Recording + cloud transcript; consent and storage policy critical. |
| HireVue / Modern Hire | SaaS | Yes | Async video; subject to NYC AEDT, IL AIVIA — bias audit required. |
| HackerRank / CoderPad | SaaS | Yes | Pair STAR with technical signal. |
| Notion / Confluence | SaaS | Yes | Question bank repository. |
| Karat | SaaS interviewing-as-a-service | Partial | Outsourced; agents prep but don't execute. |

## Templates & scripts
See `templates.md` for STAR question banks, scorecard structure, and probing scripts. Inline transcript classifier:

```bash
#!/usr/bin/env bash
# classify-star.sh - tag transcript utterances S/T/A/R via Claude
set -euo pipefail
TRANSCRIPT="${1:?transcript.txt}"
OUT="${TRANSCRIPT%.txt}.classified.md"
claude -p "$(cat <<EOF
Classify each line below as S, T, A, R, or NOT_STAR.
Redact protected-class references with [REDACTED].
Output Markdown table: line | tag | redacted_line.
EOF
)" < "$TRANSCRIPT" > "$OUT"
echo "wrote $OUT"
```

## Best practices
- Always anchor STAR questions to a written competency rubric; without it agents produce generic prompts that don't differentiate.
- Score each competency independently before discussing with peers (avoid groupthink); agents enforce this by hiding peer scores until submission.
- Use the same questions for every candidate at the same level; agent should reject "let me ask a different question" mid-loop.
- 80/20 rule: candidate talks 80%, interviewer 20%. Agent in-loop can flag interviewer-talk-time exceeding threshold.
- Note quoted evidence verbatim, not interpretations ("said X" not "seemed confident"); agents enforce in scorecard validators.
- Calibrate interviewers via shared scoring of recorded responses; agents pull 3 candidates per quarter for calibration sessions.

## AI-agent gotchas
- Fluency bias: agents reward polished delivery, penalize accents/disfluencies. Mitigation: score on content (S/T/A/R completeness, specificity, measurable result) not delivery; have humans review flagged-low scores from agents.
- Cultural bias: "I" vs "we" framing; some cultures default to collective. Probing for individual contribution should be a script, not a downgrade.
- Hallucinated quotes: agent invents quotes when transcript ambiguous; require strict "if not in transcript, output [NO_QUOTE]" rule.
- Protected-class leakage: pregnancy, age, religion details surface; agent must redact before any storage and never feed them into scoring prompts.
- Legal: NYC AEDT requires bias audit + candidate notification when AI is used in hiring decisions; IL AIVIA requires consent for AI video analysis. Build compliance gates.
- Human-in-loop checkpoint: every hire/no-hire recommendation; agents propose, humans decide.
- "Strong STAR but wrong fit": agent produces high score because structure was good, even if outcome described shows bad judgment. Add an "outcome quality" sub-score.
- Agents accept "we did X" repeatedly without probing for individual contribution; require auto-probe trigger on consecutive "we" mentions.
- Cross-interviewer drift: same agent run twice produces slightly different question banks; pin seed/temperature for reproducibility.
- Recording without consent is illegal in many jurisdictions (CA, EU, IL); agent must verify consent flag before processing audio.

## References
- Indeed STAR Method Guide: https://www.indeed.com/career-advice/interviewing/how-to-use-the-star-interview-response-technique
- Amazon Leadership Principles + Bar Raiser interview design: https://www.amazon.jobs/content/en/our-workplace/leadership-principles
- Lou Adler, "Hire With Your Head" — performance-based interviewing
- Geoff Smart & Randy Street, "Who: The A Method for Hiring"
- NYC AEDT law: https://rules.cityofnewyork.us/wp-content/uploads/2023/04/DCWP-NOA-for-Use-of-Automated-Employment-Decisionmaking-Tools-2.pdf
- Illinois AI Video Interview Act: 820 ILCS 42
- EU AI Act high-risk classification (Annex III, hiring): https://artificialintelligenceact.eu
- LinkedIn "Future of Recruiting" (annual)
- SHRM: "Structured Employment Interviews"
