# Agent Integration — VUI Testing Best Practices

## When to use
- Pre-launch validation of an Alexa skill, Google Action, custom IVR, or LLM voice agent.
- Regression testing after NLU model updates or prompt changes.
- Measuring intent accuracy, task completion, and error rate against a baseline.
- Stress-testing under realistic noise and accent diversity before scaling.

## When NOT to use
- TTS-only output systems (read-aloud, screen readers) — that's a11y testing, not VUI.
- Pure copy review without runtime testing — covered by content design heuristics.
- Latency/load tuning of the speech stack — use load testing tooling instead.

## Where it fails / limitations
- Synthetic test utterances correlate poorly with real-world speech distributions; "100% intent accuracy on test set" still hides field failures.
- Short studies miss long-context retention bugs that only emerge after 5+ turns.
- Single-language test panels mask code-switching and accent-tail performance.
- Closed-source platforms (Siri, Bixby) don't expose raw ASR confidence — limits diagnosis.
- LLM voice agents drift across runs; deterministic regression tests need fixed seeds + transcripts, not audio.

## Agentic workflow
Use Claude to scaffold a 4-layer test plan (unit → integration → user → stress) per intent, then generate adversarial utterance batches with `nlpaug` and run them through the platform CLI. A second agent ingests the resulting transcripts and computes per-intent accuracy, error-rate, and time-to-complete tables. Human-in-loop reviews escalation paths and recordings flagged as "user frustration" by sentiment scoring.

### Recommended subagents
- `faion-usability-agent` — synthesize moderated session findings into theme tables.
- `faion-ux-researcher-agent` — design the participant screen for diverse accents/abilities.
- A project-local `vui-eval-runner` — drive `ask-cli simulate` / `gactions test` in batch, collect JSON.

### Prompt pattern
```
Given <skill manifest>, generate a test matrix:
- 50 utterances per intent (10 clean, 20 noisy, 10 accented, 10 adversarial).
- Expected intent + slots per utterance.
Output as JSONL for batch CLI runner.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask-cli simulate` | Send utterance, get JSON of intent+slots+response | `ask simulate -t "<text>" -l en-US` |
| `gactions test` | Run Google Actions against test scenarios | github.com/actions-on-google/gactions |
| `rasa test` | NLU + core stories with confusion matrix | `rasa test --stories tests/` |
| `nlpaug` | Synonym/back-translation/noise augmentation | `pip install nlpaug` |
| `whisper` (OpenAI) | Reference ASR transcription for ground truth | `pip install openai-whisper` |
| `pyaudio` + `soundfile` | Inject synthetic background noise into eval audio | `pip install pyaudio soundfile` |
| `pytest-voice` | Voice flow assertion library | github.com/dialogflow/pytest-voice |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Voiceflow Test API | SaaS | Yes | Replay flows, get transcript JSON |
| Bespoken Tools | SaaS | Yes | E2E test framework for Alexa/Google with CI integration |
| UserTesting Live (audio-only) | SaaS | Partial | Moderated voice testing, manual transcript export |
| Dialogflow CX Test Cases | SaaS | Yes (REST) | Native test suite with assertions per page |
| Rasa Open Source | OSS | Yes | Story-based regression tests, confusion matrix output |
| Speechmatics | SaaS | Yes | Reference ASR for ground-truth transcription of audio panels |
| Common Voice (Mozilla) | OSS dataset | Yes | Diverse accent corpus for offline accuracy testing |

## Templates & scripts
See `templates.md` for the test matrix format. Inline batch-runner stub (≤50 lines):

```python
import json, subprocess
def simulate(text, locale="en-US"):
    out = subprocess.check_output(
        ["ask", "simulate", "-t", text, "-l", locale, "-s", "amzn1.ask.skill.X"]
    )
    return json.loads(out)

def run(matrix_path):
    rows = []
    for line in open(matrix_path):
        case = json.loads(line)
        r = simulate(case["utterance"])
        intent = r["result"]["skillExecutionInfo"]["invocationResponse"]["body"][
            "response"
        ].get("intent", {}).get("name")
        rows.append({**case, "got": intent, "ok": intent == case["expected_intent"]})
    return rows

if __name__ == "__main__":
    import sys, statistics
    rows = run(sys.argv[1])
    by_intent = {}
    for r in rows: by_intent.setdefault(r["expected_intent"], []).append(r["ok"])
    for k, v in by_intent.items():
        print(f"{k}: {sum(v)}/{len(v)} ({statistics.mean(v):.1%})")
```

## Best practices
- Always test with at least one telephony-codec channel (8 kHz μ-law) — drastically different from device mic.
- Lock seeds for LLM voice agents during regression; otherwise comparisons are noise.
- Bucket accuracy by accent/age/gender — overall % hides subgroup failures (typical 15-30 pt gap).
- Pair every quantitative metric with a 5-user moderated session — numbers don't surface frustration.
- Test "long tail" 20% of utterances explicitly; common phrases pass without revealing weak points.
- Track "completion at attempt N" not just "completion" — N=2 is acceptable, N=4 is failure.

## AI-agent gotchas
- Synthetic adversarial utterances from LLMs over-represent the model's own training distribution; mix with real user logs.
- Auto-graded scoring underweights tone/empathy — use a separate sentiment pass before declaring "pass".
- Endpointing differences between simulator and device mean simulator success ≠ device success; require at least one device-loop test.
- Human-in-loop checkpoint: after batch run, hand 20 random failures to a designer for root-cause categorization (NLU vs. dialog vs. ASR vs. content).
- Voice IP/PII redaction must happen BEFORE transcripts go to the agent; bake redaction into the runner, not as a post-step.

## References
- Nielsen Norman Group — *Voice Interaction UX Testing* — nngroup.com/articles/testing-voice-usability
- Google Conversation Design — Testing chapter — designguidelines.withgoogle.com/conversation
- Voiceflow — *Voice Prototype Testing* — voiceflow.com/blog/voice-prototype-testing
- Bespoken — bespoken.io
- Cohen, Giangola, Balogh — *Voice User Interface Design*
