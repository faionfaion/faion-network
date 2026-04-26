# Agent Integration — Problem Validation

## When to use
- After idea-generation, before MVP build — confirm the problem is real, painful, and worth solving.
- When growth has stalled and you suspect product-problem fit, not product-market fit.
- Before adding a major feature: validate that the underlying job-to-be-done exists, not just the feature request.
- During pivots, to test the new problem hypothesis cheaply before any code is written.

## When NOT to use
- Post-launch with strong revenue and retention — validation is for the unknowns; switch to prioritization frameworks.
- High-velocity B2C consumer where behavior trumps stated preference — go straight to a paid-ads landing-page test.
- Regulated / specialized B2B (healthcare, finance) — interviews have NDA and compliance overhead; use expert calls + analyst frameworks.
- When you've already validated and just want validation theatre to feel safe — that's confirmation bias, not validation.

## Where it fails / limitations
- The Mom Test only works if the interviewer is disciplined; agents that auto-generate scripts often slip leading questions back in.
- "Tell me about the last time..." answers are reconstructed memory — recall bias inflates pain frequency.
- Validation hierarchy levels 1-2 (paid / signed up) are strong signal; levels 4-5 (interest / stated problem) are easily faked. Agents weight all five equally if not constrained.
- The "vision → framing → weakness → pedestal → ask" opener feels manipulative when over-rehearsed; people detect the script and respond performatively.
- Commitment signals are forge-able (a "letter of intent" with no exec sign-off is not commitment).
- LLMs cannot conduct interviews — only prepare scripts and analyze transcripts. Replacing the human interview step is the single biggest failure mode.

## Agentic workflow
Three roles, three agents. Script-prep agent (haiku): turns the hypothesis into a Mom-Test-compliant interview guide using the vision/framing/weakness/pedestal/ask pattern. Founder runs the actual interview (LLMs cannot replace this). Analysis agent (sonnet): ingests transcript, tags red flags (compliments, hypotheticals, generics), extracts commitment signals with severity, scores evidence on the 5-level hierarchy. Decision agent (opus): aggregates ≥5 transcripts, recommends "validated / inconclusive / invalidated" with rationale + next-step plan. Human approves the decision.

### Recommended subagents
- A custom `mom-test-script-writer` (haiku) — converts a hypothesis to interview questions; lints for leading questions.
- A custom `transcript-tagger` (sonnet) — annotates compliments, hypotheticals, generics, commitment signals.
- A custom `evidence-aggregator` (opus) — multi-transcript synthesis on the 5-level hierarchy.
- `faion-pain-point-researcher-agent` — feeds problem hypotheses from prior pain-point work.
- `faion-brainstorm` — for generating multiple hypothesis framings before settling on the question to validate.

### Prompt pattern
```
Read skills/faion/knowledge/solo/research/researcher/problem-validation/README.md.
Hypothesis: <H>. Generate a 30-min interview script using vision/framing/weakness/pedestal/
ask + Mom Test rules. No leading questions. Reject any "would you" / "do you think" forms.
Output JSON: {opening, questions[], probe_branches{}, exit_criteria}.
```

```
Tag this transcript. For each turn, label compliment / hypothetical / generic / specific-past
/ commitment-signal{type,strength}. Output a final hierarchy-level score (1-5) with quotes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper` / `whisper-cpp` | Local transcription of recorded calls | https://github.com/openai/whisper |
| `otter.ai` API | Hosted transcription with diarization | https://otter.ai/api |
| Anthropic SDK | Tag transcripts in batch | https://docs.anthropic.com |
| `notion-cli` / `airtable-cli` | Persist interview log + signal scores | https://developers.notion.com |
| `calendly` / `cal.com` API | Auto-book interview slots | https://developer.calendly.com |
| `signupform` (Tally / Typeform) | Pre-screen prospects | https://tally.so |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| User Interviews / Respondent.io | SaaS | Yes | Recruit screened B2B interviewees; pay-per-completed. |
| Wynter | SaaS | Yes | B2B copy + problem testing with pre-vetted ICPs. |
| Maze / Sprig | SaaS | Yes | Async unmoderated tests; weak for problem validation, strong for solution. |
| Loom / Riverside / Zoom | SaaS | Yes | Recording with cloud transcripts; agent-pollable. |
| Notion / Airtable | SaaS | Yes | Interview log + commitment-tracker. |
| Cal.com / Calendly | SaaS | Yes | Automated scheduling; avoid the "would you talk to me" friction. |
| Otter.ai / Fathom / Fireflies | SaaS | Yes | Auto-record, diarize, transcribe meetings. |

## Templates & scripts
See `templates.md` for question templates. Inline transcript-tagger prompt skeleton (Python, ≤25 lines):

```python
import json, sys, anthropic
client = anthropic.Anthropic()
SYSTEM = """Tag each turn in the transcript as one of: COMPLIMENT, HYPOTHETICAL,
GENERIC, SPECIFIC_PAST, COMMITMENT(time|reputation|money,strength:1-5). Return
JSON list of {speaker, text, label, hierarchy_level:1-5, quote_evidence}."""
transcript = sys.stdin.read()
resp = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=4000,
    system=SYSTEM,
    messages=[{"role": "user", "content": transcript}],
)
print(resp.content[0].text)
```

Pipe a transcript through this and aggregate `hierarchy_level` distribution across ≥5 interviews to make the validate/invalidate call.

## Best practices
- Run ≥5 interviews before any decision; ≥10 for confidence. The variance is too high below 5.
- Recruit cold (not your network). Friends compliment.
- Always record (with consent) — memory of an interview is reconstructed and self-serving.
- Score evidence against the hierarchy explicitly — don't let "they were really excited" become the validation. Excitement is hierarchy level 4-5, the weakest.
- Look for behavior trails (what they did before talking to you) over expressed intent.
- Re-validate continuously. The 2025 update is right: validation is not a one-time gate; markets and users drift.
- Disprove, don't prove. The goal is to find out you're wrong cheaply. Confirmation-seeking interviews waste cycles.
- Pair with `pain-point-research`, `jobs-to-be-done`, and `pricing-research` — all four together produce sharper signal than any one alone.

## AI-agent gotchas
- LLMs cannot run live interviews. Synthetic-user simulators are useful for script rehearsal but produce hallucinated insights if treated as real data.
- Script-writer agents reintroduce "would you" / "do you think this is a good idea?" — lint the output before sending to the founder.
- Tagging agents over-classify hypotheticals as commitment signals when the user is enthusiastic. Require explicit past-tense verb evidence for commitment labels.
- "Strong interest" (level 4) sounds like validation to optimistic founders. The decision agent should weight 4-5 at near-zero unless backed by a behavior trail.
- LLMs auto-summarize transcripts and lose verbatim quotes — keep raw quotes in the log; summaries are insufficient for re-analysis.
- Cross-cultural cues differ — Ukrainian / Eastern-European respondents may give blunter "no"s; LLMs trained on US norms misclassify them as red flags rather than honest signal.
- Human checkpoint: validate/invalidate decision must be human-approved. The agent recommends; the founder decides.
- Avoid agent-only loops: an agent that "interviews" another agent generates plausible but useless data.

## References
- https://momtestbook.com/ (Rob Fitzpatrick, The Mom Test)
- https://www.lennysnewsletter.com/p/customer-discovery-interviews
- https://www.strategyzer.com/library/the-test-card
- https://www.startupschool.org/library
- https://yvonneadegoke.medium.com/customer-discovery-101-the-mom-test (summary)
- https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs
