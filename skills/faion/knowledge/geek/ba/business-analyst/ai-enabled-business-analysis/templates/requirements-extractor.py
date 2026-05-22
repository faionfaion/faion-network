"""
purpose: extract requirements from a source document using an LLM.
consumes: typed inputs per content/02-output-contract.xml.
produces: artefact field rows ready for the ai-enabled-business-analysis record.
depends-on: content/01-core-rules.xml, content/02-output-contract.xml.
token-budget-impact: ~250 tokens.
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
