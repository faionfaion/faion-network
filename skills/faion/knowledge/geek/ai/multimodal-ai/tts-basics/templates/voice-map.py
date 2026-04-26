"""
Semantic voice routing by content type.
Use semantic labels (news/assistant/narrator) not provider-specific voice names.
Provider names are non-portable: "nova" (OpenAI) != "en-US-Neural2-D" (Google).
"""

OPENAI_VOICE_MAP: dict[str, str] = {
    "news": "onyx",       # authoritative male
    "assistant": "nova",  # friendly female
    "narrator": "fable",  # storytelling tone
    "neutral": "alloy",   # balanced default
    "whisper": "shimmer", # soft, gentle
    "formal": "echo",     # neutral male
}

GOOGLE_VOICE_MAP: dict[str, str] = {
    "news": "en-US-Neural2-D",
    "assistant": "en-US-Neural2-F",
    "narrator": "en-US-Neural2-J",
    "neutral": "en-US-Neural2-A",
}


def select_voice(
    content_type: str,
    provider: str = "openai",
) -> str:
    """
    Return provider-specific voice name for a semantic content type.
    Falls back to neutral/alloy if content_type is unknown.
    """
    if provider == "openai":
        return OPENAI_VOICE_MAP.get(content_type, "alloy")
    elif provider == "google":
        return GOOGLE_VOICE_MAP.get(content_type, "en-US-Neural2-A")
    raise ValueError(f"Unknown provider: {provider}")
