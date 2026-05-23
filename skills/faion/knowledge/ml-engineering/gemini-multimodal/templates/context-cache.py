"""
purpose: Context caching for Gemini — create, reuse, expire caches for large documents.
consumes: large doc content + Gemini client + TTL
produces: cache id used in subsequent generate calls
depends-on: content/01-core-rules.xml r4
token-budget-impact: cuts per-call input cost ~75% on repeated docs

Context caching for Gemini — create, use, and manage caches for large documents.

Requires >=32K tokens in cached content. Cached tokens cost ~75% less than full-price input.

Usage:
    cache = create_document_cache("large_document.pdf", ttl="3600s")
    answer = query_cache(cache, "What are the payment terms?")
    cache.delete()
"""
import google.generativeai as genai
from google.generativeai import caching


def create_document_cache(
    file_path: str,
    display_name: str = "document-cache",
    system_instruction: str = "You are an expert document analyzer.",
    model: str = "gemini-1.5-pro",
    ttl: str = "3600s",
):
    """Upload file and create a context cache. Raises if token count < 32K."""
    document = genai.upload_file(file_path)
    cache = caching.CachedContent.create(
        model=model,
        display_name=display_name,
        system_instruction=system_instruction,
        contents=[document],
        ttl=ttl,
    )
    print(f"Cache: {cache.name}, tokens: {cache.usage_metadata.total_token_count}")
    return cache


def query_cache(cache, question: str) -> str:
    """Query a cached document. All calls reuse cached tokens (75% cheaper)."""
    model = genai.GenerativeModel.from_cached_content(cache)
    return model.generate_content(question).text


def extend_cache(cache, ttl: str = "7200s"):
    """Extend cache TTL before expiry."""
    cache.update(ttl=ttl)
