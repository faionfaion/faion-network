"""Extract requirements from a PDF document using Claude.

Input: PDF file path.
Output: list of dicts with id, type, description, source, ambiguous.
"""
import json
import pdfplumber
import anthropic


def extract_requirements_from_pdf(pdf_path: str) -> list[dict]:
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": f"""
Extract all requirements from this document. Return a JSON array where each item has:
- id (REQ-001, REQ-002, ...)
- type (Functional|Non-Functional|Constraint|Assumption)
- description (the requirement text)
- source (verbatim source sentence)
- ambiguous (true/false)

Document:
{text[:50000]}
"""}],
    )
    return json.loads(resp.content[0].text)
