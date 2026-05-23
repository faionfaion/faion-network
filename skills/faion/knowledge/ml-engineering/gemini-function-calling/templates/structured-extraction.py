"""
purpose: Gemini schema-constrained extraction via response_mime_type=application/json.
consumes: raw text + pydantic / JSON schema
produces: parsed dataclass / dict matching schema
depends-on: content/01-core-rules.xml r6
token-budget-impact: per-call; reliable JSON shape

Usage:
    data = extract_article(article_text)
    # data.title, data.topics, data.sentiment
"""
from pydantic import BaseModel
from typing import List
import google.generativeai as genai

genai.configure(api_key="GOOGLE_API_KEY")


class Article(BaseModel):
    title: str
    topics: List[str]
    sentiment: str  # positive | negative | neutral


def extract_article(text: str) -> Article:
    """Extract structured data from article text using JSON schema output.

    Args:
        text: Raw article text to extract from.

    Returns:
        Validated Article instance.
    """
    model = genai.GenerativeModel(
        "gemini-1.5-pro",
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": Article.model_json_schema(),
        },
    )
    resp = model.generate_content("Extract from: " + text)
    # Always validate — Gemini may return valid JSON that violates the schema
    return Article.model_validate_json(resp.text)
