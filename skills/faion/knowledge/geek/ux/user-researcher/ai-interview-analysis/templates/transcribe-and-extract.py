"""
Full interview analysis pipeline: audio → local transcription → Claude theme extraction.
Input: list of audio file paths, research topic string.
Output: cross-interview theme report (text).
"""
import anthropic
import faster_whisper


def transcribe(audio_path: str) -> str:
    """Transcribe audio file locally — no data leaves the machine."""
    model = faster_whisper.WhisperModel("medium", device="cpu")
    segments, _ = model.transcribe(audio_path, beam_size=5)
    return "\n".join(f"[{s.start:.1f}s] {s.text}" for s in segments)


def extract_themes(transcripts: list[str], topic: str) -> str:
    """Extract cross-interview themes using Claude. Only reports themes with 2+ quotes."""
    client = anthropic.Anthropic()
    combined = "\n\n---NEXT TRANSCRIPT---\n\n".join(
        f"Transcript {i + 1}:\n{t}" for i, t in enumerate(transcripts)
    )
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        system=(
            "You are a UX research analyst. Extract themes from interview transcripts. "
            "Only report themes with 2+ supporting verbatim quotes from different transcripts. "
            "Preserve exact participant quotes — never paraphrase. "
            "Mark themes from only 1 transcript as 'weak signal'."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Topic: {topic}\n\nTranscripts:\n{combined}\n\n"
                "Output: top themes with verbatim quotes, weak signals, contradictions, "
                "and gaps (discussion guide questions with no usable responses)."
            ),
        }],
    )
    return response.content[0].text


# Usage
if __name__ == "__main__":
    audio_files = ["session_1.mp3", "session_2.mp3"]
    transcripts = [transcribe(f) for f in audio_files]
    report = extract_themes(transcripts, "onboarding experience for new SaaS users")
    print(report)
