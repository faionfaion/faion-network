# Agent Integration — Problem Validation 2026

## When to use
- Pre-MVP: validate that the problem is real, painful, and worth paying for before writing code.
- Pivoting: re-validate problem assumptions when retention is low or engagement is sparse.
- Adjacent expansion: testing whether an existing customer segment has a related underserved problem.
- After a hypothesis breaks (low conversion, no upsell), to confirm the problem still holds.

## When NOT to use
- After PMF is established and you have a paying user base — switch to feature-discovery + continuous-discovery.
- For incremental optimization on a known funnel — A/B testing answers faster.
- When you cannot reach the target segment within a week — you'll over-rely on weak proxies.
- For commodity / undifferentiated problems where solution quality matters more than problem existence.

## Where it fails / limitations
- Stated preferences ("I would pay") are unreliable signals; only behavioral commitments count.
- Friends and warm contacts give compliments; weight non-network respondents 5x.
- Survey-only validation systematically over-reports demand. Pair with behavioral signals (LOI, pre-order, time spent in prototype).
- "Vision-Framing-Weakness-Pedestal-Ask" framing helps but is easy to mis-execute; agents tend to skip the weakness step.
- 5-10 interviews give themes, not statistical evidence; 30+ for any quantitative claim.

## Agentic workflow
Run validation as three serial loops: (1) recruit + interview using Mom Test scripts, (2) extract commitment signals + red flags from transcripts, (3) synthesize an evidence ledger that ranks by signal strength. Use a structured-output JSON schema with fields {segment, problem_statement, evidence_tier, citation, signal_type}. Human-in-loop is mandatory before declaring problem validated — the agent's job is evidence aggregation, not the conclusion.

### Recommended subagents
- A `validation-interviewer` (sonnet) subagent that drafts segment-specific Mom Test scripts and follow-up probes.
- A `signal-extractor` (sonnet) subagent that scans transcripts and tags compliments, hypotheticals, generics (red flags) vs. time/reputation/money commitments.
- `faion-sdd-executor-agent` to manage the validation feature lifecycle and close it when evidence threshold is met.

### Prompt pattern
```
Role: signal-extractor.
Input: interview_transcript.txt, segment_context.md.
Output JSON: {commitments:[{type:"time|reputation|money", quote, ts}],
              red_flags:[{type:"compliment|hypothetical|generic", quote, ts}]}.
Rule: never infer; quote verbatim. If transcript has no commitment, return [] — don't fabricate.
```

```
Role: validation-synthesizer.
Input: 10 signal_extraction.json files.
Task: produce evidence ledger sorted by tier 1 (paid) > 2 (signed up) > 3 (engaged) > 4 (interest) > 5 (stated).
Constraint: refuse to label problem "validated" unless ≥3 distinct tier-1/2 evidences from non-network respondents.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper.cpp` / `openai-whisper` | Transcribe interview recordings locally | https://github.com/openai/whisper |
| `gh api` | Mine GitHub issue comments for problem statements | https://cli.github.com |
| `pup` / `htmlq` | Scrape Reddit / Indie Hackers complaint threads | https://github.com/EricChiang/pup |
| `searx` (self-hosted) | Privacy-preserving search across forums | https://docs.searxng.org |
| `nb` / `dasel` | Manage interview notes corpus | https://github.com/xwmx/nb |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Calendly | SaaS | Yes (API) | Schedule interviews; agent writes invites with consent line. |
| Riverside / Descript | SaaS | Yes (API for Descript) | Recording + transcription with timestamps. |
| Otter.ai | SaaS | Partial (limited API) | Cheap transcription; quality lower than Whisper. |
| Dovetail | SaaS | Yes (API) | Tag transcripts, cluster themes; built for research repos. |
| Notably / Marvin | SaaS | Yes (API) | AI-assisted theme extraction over interview corpus. |
| Reddit / IndieHackers / Hacker News | OSS web | Yes (read-only) | Free signal source; respect community rules. |
| Typeform | SaaS | Yes (API) | Pre-screen recruits; not for behavioral validation. |
| Stripe (test mode) | SaaS | Yes (API) | Pre-order / LOI capture as tier-1 signal. |
| LandingPagehost / Carrd | SaaS | Yes (API) | Smoke-test landing for fake-door problem validation. |

## Templates & scripts
See `templates.md` for Mom Test script and Vision-Framing-Weakness-Pedestal-Ask opener.

Inline red-flag scanner (Python, ≤30 lines):
```python
import re, sys, json
RED = {
  "compliment": r"\b(great idea|love it|brilliant|awesome)\b",
  "hypothetical": r"\b(I would|I'd probably|might|could see myself)\b",
  "generic": r"\b(everyone|nobody|always|never)\b",
}
text = open(sys.argv[1]).read().lower()
hits = {}
for tag, pat in RED.items():
    hits[tag] = re.findall(pat, text)
print(json.dumps(hits, indent=2))
```

## Best practices
- Keep an evidence ledger with tier-1 to tier-5 signals; the only "validated" label requires tier-1/2 from non-network respondents.
- Recruit cold (Reddit/LinkedIn DMs) for at least half of interviews; otherwise survivorship bias dominates.
- Open every interview with "I have nothing to sell"; agents tend to drop this and the conversation pivots to product pitch.
- End every interview with a behavioral ask (intro, follow-up, prototype access). The yes/no is the data.
- Re-validate every quarter — markets shift, regulation shifts, AI shifts adjacent products.

## AI-agent gotchas
- Agents anthropomorphize compliments as validation. Encode the rule "compliments are red flags" into the prompt.
- Whisper transcripts mis-attribute speakers; require diarization before signal extraction or you'll mix interviewer prompts into respondent quotes.
- LLMs will summarize an interview with confident generalizations from a single quote — require frequency counts before any "users want X" claim.
- Don't let the agent draft the validation report and decision in one pass; split: (1) ledger, (2) human-reviewed conclusion.
- Mom Test rewriting is a known LLM weakness — the agent will subtly turn behavioral questions into hypothetical ones. Validate the script with a checklist before sending.

## References
- Rob Fitzpatrick, "The Mom Test" (2013, still the canonical source).
- Steve Blank, "The Four Steps to the Epiphany" (customer development).
- YC Startup School 2024-2025 lectures on talking to users.
- Aaron Dignan, "Brave New Work" — commitment as the only signal.
- Dan Olsen, "The Lean Product Playbook" (problem-solution fit hierarchy).
