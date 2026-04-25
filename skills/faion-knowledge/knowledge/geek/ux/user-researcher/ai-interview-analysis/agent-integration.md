# Agent Integration — AI-Assisted Interview Analysis

## When to use
- Processing large volumes of interview recordings (5+ sessions) where manual transcription/analysis would take days
- Extracting themes and patterns across a set of transcripts for synthesis reporting
- Generating first-pass summaries of individual interviews before researcher review
- Running sentiment scoring on large transcript corpora to prioritize which interviews to review in depth
- Producing cross-interview pattern reports as input for affinity diagramming sessions

## When NOT to use
- Single interview sessions where a researcher can take notes in real time — AI adds no meaningful speed advantage
- Moderated usability studies where facilitator judgment during the session is more valuable than post-hoc analysis
- Studies involving sensitive personal disclosures (health, legal, financial) without explicit participant consent for AI processing
- High-stakes research where nuanced behavioral interpretation (hesitation, emotional cues) is critical — AI misses these
- Any pipeline where AI analysis output is presented directly to stakeholders without researcher review

## Where it fails / limitations
- Transcription accuracy drops sharply with accents, background noise, technical jargon, and cross-talk — always review low-confidence segments
- Speaker identification fails with more than 3 participants or when speakers have similar vocal qualities
- Theme extraction reflects training data bias — minority opinions in transcripts are systematically underweighted
- Sentiment analysis is poor on sarcasm, understatement, and culturally specific expressions
- AI summaries compress nuance; key insight details (timing, specific wording) are often lost
- None of the current tools handle video + behavioral annotation — text only
- Data residency: most SaaS tools (Looppanel, Dovetail, Insight7) process data on US servers — verify compliance before uploading participant data

## Agentic workflow
Claude agents can perform full transcript analysis pipelines: given raw transcript text, the agent (1) segments by speaker, (2) extracts themes with supporting quotes, (3) scores sentiment per segment, (4) produces a cross-interview pattern report. The human uploads recordings to a transcription service (Looppanel, Otter.ai), exports transcript text, feeds to the agent, and then reviews agent output — accepting, rejecting, or re-coding themes. The agent handles volume; the researcher handles interpretation quality.

### Recommended subagents
- `haiku` — transcript segmentation, quote extraction, Likert-scale sentiment scoring at volume
- `sonnet` — theme synthesis, cross-interview pattern detection, insight gap identification, final report generation

### Prompt pattern
```xml
<system>
You are a UX research analyst. Analyze interview transcripts systematically.
Rules: (1) extract only themes with 2+ supporting quotes from different participants,
(2) flag themes appearing in only 1 transcript as "weak signal",
(3) preserve exact participant quotes — never paraphrase,
(4) note where participants hesitate or contradict themselves.
</system>
<human>
Analyze these transcripts from [N] participants interviewed about [topic].
Discussion guide topics: [list].
Output:
1. Top themes (≥2 participants) with evidence quotes
2. Weak signals (1 participant) worth noting
3. Contradictions or outliers
4. Gaps: discussion guide questions with no usable responses
</human>
```

```
Analyze this single interview transcript [paste].
Output structured summary: (1) participant profile (inferred from responses),
(2) key pain points mentioned with direct quotes, (3) positive reactions with quotes,
(4) unresolved questions (things participant was unclear on), (5) follow-up questions for next session.
Max 400 words.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper` (OpenAI) | Local transcription — no data leaves machine | pip install openai-whisper |
| `faster-whisper` | 4x faster Whisper variant, GPU-optional | pip install faster-whisper |
| `pyannote-audio` | Speaker diarization (who spoke when) | pip install pyannote.audio |
| `anthropic` Python SDK | Transcript theme extraction via Claude | pip install anthropic |
| `assemblyai` Python SDK | Cloud transcription + speaker labels + sentiment | pip install assemblyai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Looppanel | SaaS | Yes (API) | UX research focus; 17 languages; REST API for transcript + tags |
| Dovetail | SaaS | Partial | Research repo; no full transcript API; insights exportable |
| Insight7 | SaaS | Yes (API) | Bulk analysis; REST API for upload + theme extraction |
| UserBit | SaaS | No | 50+ languages; no public API |
| AssemblyAI | SaaS | Yes (API) | Best transcription API; sentiment + entities + chapters |
| Otter.ai | SaaS | Partial | REST API for transcript export; no analysis API |
| Fireflies.ai | SaaS | Yes (API) | Meeting transcription + action items; REST API |
| Descript | SaaS | No | Video + transcript editing; no analysis API |
| Whisper (OpenAI OSS) | OSS | Yes | Local transcription; no speaker diarization built-in |

## Templates & scripts
Full pipeline: audio → transcript → theme extraction via Claude:

```python
import anthropic
import faster_whisper

def transcribe(audio_path: str) -> str:
    """Transcribe audio file locally (no data upload)."""
    model = faster_whisper.WhisperModel("medium", device="cpu")
    segments, _ = model.transcribe(audio_path, beam_size=5)
    return "\n".join(f"[{s.start:.1f}s] {s.text}" for s in segments)

def extract_themes(transcripts: list[str], topic: str) -> str:
    """Extract cross-interview themes using Claude."""
    client = anthropic.Anthropic()
    combined = "\n\n---NEXT TRANSCRIPT---\n\n".join(
        f"Transcript {i+1}:\n{t}" for i, t in enumerate(transcripts)
    )
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        system=(
            "You are a UX research analyst. Extract themes from interview transcripts. "
            "Only report themes with 2+ supporting quotes from different transcripts. "
            "Preserve exact participant quotes."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Topic: {topic}\n\nTranscripts:\n{combined}\n\n"
                "Output: top themes with quotes, weak signals, contradictions."
            )
        }]
    )
    return response.content[0].text

# Usage
transcripts = [transcribe("session_1.mp3"), transcribe("session_2.mp3")]
report = extract_themes(transcripts, "onboarding experience for new SaaS users")
print(report)
```

## Best practices
- Always use local transcription (Whisper/faster-whisper) for sensitive participant data before considering cloud services
- Review 100% of speaker diarization output for 3+ participant sessions — misattribution corrupts theme analysis
- Set a minimum quote threshold: reject any theme the agent cannot support with 2+ direct participant quotes
- Structure your discussion guide with labeled sections (e.g., "## Section 3: Task Completion") — agent theme extraction aligns to guide structure when present
- Produce a "confidence annotation" on the final report: mark each theme as High (3+ participants), Medium (2 participants), Low (1 participant / agent inference)
- Never automate insight delivery to product teams without researcher review — AI analysis output is a draft, not a finding

## AI-agent gotchas
- Agents generate plausible-sounding themes that are not grounded in the transcript text — always require exact quotes as evidence; reject any theme without one
- Long transcripts (90min+ sessions) exceed Claude's context window when combined — chunk by discussion guide section, not by arbitrary token count
- Agent-extracted sentiment does not account for researcher tone or framing effects — sentiment findings need human contextualization
- Agents will hallucinate participant demographics from thin cues ("she mentioned her commute" → assigns "urban professional" persona) — flag any demographic inference not directly stated
- GDPR/CCPA: agent analysis of interview data must be disclosed in participant consent forms; verify before automating

## References
- https://www.looppanel.com/docs (Looppanel API)
- https://www.assemblyai.com/docs (AssemblyAI transcription API)
- https://github.com/openai/whisper (Whisper OSS)
- https://github.com/SYSTRAN/faster-whisper (faster-whisper)
- https://dovetail.com/research/ai-analysis/ (Dovetail AI analysis)
- https://www.nngroup.com/articles/affinity-diagram/ (Affinity diagramming — post-analysis step)
