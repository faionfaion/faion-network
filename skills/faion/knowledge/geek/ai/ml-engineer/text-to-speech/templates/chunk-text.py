# purpose: text normalization + sentence-boundary chunking for TTS pipelines
# consumes: long text input (article, transcript, doc)
# produces: code (drop-in module yielding TTS-sized chunks)
# depends-on: stdlib only
# token-budget-impact: ~80 tokens if loaded into LLM context
"""Text normalization and sentence-boundary chunking for TTS pipelines."""
import re
from typing import Generator


def normalize_for_tts(text: str) -> str:
    """Clean LLM output and markdown for TTS consumption."""
    # Strip markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)          # **bold**
    text = re.sub(r'\*(.*?)\*', r'\1', text)               # *italic*
    text = re.sub(r'`[^`]+`', '', text)                    # `inline code`
    text = re.sub(r'```[\s\S]*?```', '', text)             # code blocks
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # [text](url)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)  # headings

    # Expand common abbreviations for clearer speech
    abbreviations = {
        "e.g.": "for example",
        "i.e.": "that is",
        "vs.": "versus",
        "etc.": "and so on",
        "Dr.": "Doctor",
        "Mr.": "Mister",
        "Mrs.": "Missus",
        "API": "A P I",
        "URL": "U R L",
        "UI": "U I",
    }
    for abbr, expansion in abbreviations.items():
        text = text.replace(abbr, expansion)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def chunk_for_streaming(
    text: str,
    max_sentences: int = 2,
    min_chars: int = 20,
) -> Generator[str, None, None]:
    """
    Split text at sentence boundaries for streaming TTS.
    Yields chunks of max_sentences sentences, never mid-word.
    """
    # Split on sentence-ending punctuation followed by space
    sentence_re = re.compile(r'(?<=[.!?])\s+')
    sentences = [s.strip() for s in sentence_re.split(text.strip()) if s.strip()]

    buffer: list[str] = []
    for sentence in sentences:
        buffer.append(sentence)
        chunk = ' '.join(buffer)
        if len(buffer) >= max_sentences and len(chunk) >= min_chars:
            yield chunk
            buffer = []

    if buffer:
        remaining = ' '.join(buffer)
        if remaining:
            yield remaining


def prepare_for_tts(text: str, chunk: bool = True) -> list[str]:
    """Full pipeline: normalize then optionally chunk into streaming segments."""
    normalized = normalize_for_tts(text)
    if not chunk:
        return [normalized]
    return list(chunk_for_streaming(normalized))
