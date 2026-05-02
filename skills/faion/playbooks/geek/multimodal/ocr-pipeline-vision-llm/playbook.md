---
name: ocr-pipeline-vision-llm
description: Scan a PDF invoice page by page, extract text and table structure with the Anthropic vision API, normalize with regex, and validate into a Pydantic schema.
tier: geek
group: multimodal
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working Python pipeline that opens a PDF invoice, converts each page to a JPEG, sends each image to `claude-sonnet-4-6` via the Anthropic Messages API using `image` content blocks, receives structured JSON with vendor info and line items, normalizes currency strings and dates with regex, and validates the result against a Pydantic v2 `Invoice` schema. The final output is a list of `Invoice` objects ready for downstream processing.

## Prerequisites

- Python 3.11+ with a virtual environment active.
- `pip install anthropic pydantic pymupdf pillow`
- `ANTHROPIC_API_KEY` set in your environment (`export ANTHROPIC_API_KEY=sk-ant-...`).
- A PDF invoice to test with (any real invoice with a vendor block and a line-item table).
- Familiarity with Pydantic v2 model validators and the Anthropic Python SDK `messages.create()` call.

## Steps

1. Install dependencies and verify the SDK version:

```bash
pip install "anthropic>=0.30" "pydantic>=2.7" pymupdf pillow
python -c "import anthropic; print(anthropic.__version__)"
```

Expected output: `0.30.x` or higher.

2. Convert each PDF page to a JPEG in memory using PyMuPDF:

```python
# pdf_to_images.py
from __future__ import annotations
import base64
import io
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image


def pdf_pages_as_base64(pdf_path: str | Path, dpi: int = 150) -> list[str]:
    """Return a base64-encoded JPEG string for every page in the PDF.

    150 DPI gives ~1240px wide for A4 — enough for Claude vision without
    burning excessive input tokens (detail='auto' downsizes to 1092px anyway).
    """
    doc = fitz.open(str(pdf_path))
    pages: list[str] = []
    for page in doc:
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        # Convert pixmap bytes → PIL Image → JPEG bytes → base64
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        pages.append(base64.standard_b64encode(buf.getvalue()).decode())
    doc.close()
    return pages
```

3. Define the Pydantic v2 schema for an invoice:

```python
# schema.py
from __future__ import annotations
import re
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, field_validator


class LineItem(BaseModel):
    description: str
    quantity: Decimal
    unit_price: Decimal
    total: Decimal


class Invoice(BaseModel):
    vendor_name: str
    vendor_address: Optional[str] = None
    invoice_number: str
    invoice_date: str          # normalized to YYYY-MM-DD in validator
    due_date: Optional[str] = None
    subtotal: Decimal
    tax: Optional[Decimal] = None
    total: Decimal
    currency: str = "USD"
    line_items: list[LineItem]

    @field_validator("invoice_date", "due_date", mode="before")
    @classmethod
    def normalise_date(cls, v: str | None) -> str | None:
        """Convert common date formats to YYYY-MM-DD."""
        if v is None:
            return None
        # Handle MM/DD/YYYY, DD-MM-YYYY, Month DD YYYY, etc.
        v = str(v).strip()
        patterns = [
            (r"(\d{1,2})/(\d{1,2})/(\d{4})", r"\3-\1-\2"),
            (r"(\d{1,2})-(\d{1,2})-(\d{4})", r"\3-\1-\2"),
        ]
        for pat, repl in patterns:
            if re.fullmatch(pat, v):
                return re.sub(pat, repl, v)
        # Pass through ISO format or anything already normalized
        return v

    @field_validator("currency", mode="before")
    @classmethod
    def normalise_currency(cls, v: str) -> str:
        """Strip symbols, uppercase, default to USD."""
        mapping = {"$": "USD", "€": "EUR", "£": "GBP", "¥": "JPY"}
        v = str(v).strip()
        return mapping.get(v, v.upper()[:3] if v else "USD")
```

4. Build the extraction function that calls the Anthropic vision API:

```python
# extractor.py
from __future__ import annotations
import json
import re

import anthropic

_client = anthropic.Anthropic()

_SYSTEM = """\
You are an invoice extraction assistant. Given an image of an invoice page,
return a JSON object with these exact keys:
  vendor_name, vendor_address, invoice_number, invoice_date, due_date,
  subtotal, tax, total, currency, line_items.

line_items is an array of objects: {description, quantity, unit_price, total}.
All monetary values as plain decimal strings (no currency symbols).
Dates as found on the invoice — the caller will normalise them.
If a field is absent, use null.
Return ONLY valid JSON, no markdown fences, no explanation.
"""


def extract_invoice_from_image(page_b64: str) -> dict:
    """Send one page image to Claude and return the parsed JSON dict."""
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": page_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Extract all invoice fields from this image.",
                    },
                ],
            }
        ],
    )
    raw = response.content[0].text.strip()
    # Strip accidental markdown fences if model adds them despite instructions
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    return json.loads(raw)
```

5. Post-process raw decimal strings for common OCR artifacts before Pydantic validation:

```python
# normalise.py
from __future__ import annotations
import re


def clean_decimal(value: str | None) -> str | None:
    """Remove thousands separators and currency symbols; keep sign and decimals."""
    if value is None:
        return None
    value = str(value).strip()
    # Remove currency symbols and thousand separators like 1,234.56 or 1.234,56
    value = re.sub(r"[€$£¥]", "", value)
    # European style: 1.234,56 → 1234.56
    if re.search(r"\d\.\d{3},\d{2}$", value):
        value = value.replace(".", "").replace(",", ".")
    else:
        # US style: 1,234.56 → 1234.56
        value = value.replace(",", "")
    return value.strip() or "0"


def clean_invoice_dict(raw: dict) -> dict:
    """Apply decimal and structural normalization to a raw extraction dict."""
    decimal_fields = ("subtotal", "tax", "total")
    for field in decimal_fields:
        if field in raw and raw[field] is not None:
            raw[field] = clean_decimal(str(raw[field]))

    if "line_items" in raw and raw["line_items"]:
        cleaned_items = []
        for item in raw["line_items"]:
            cleaned_items.append(
                {
                    "description": item.get("description", ""),
                    "quantity": clean_decimal(str(item.get("quantity", "1"))) or "1",
                    "unit_price": clean_decimal(str(item.get("unit_price", "0"))) or "0",
                    "total": clean_decimal(str(item.get("total", "0"))) or "0",
                }
            )
        raw["line_items"] = cleaned_items

    return raw
```

6. Wire up the full pipeline in `run_ocr.py`:

```python
# run_ocr.py
from __future__ import annotations
import json
import sys
from pathlib import Path

from extractor import extract_invoice_from_image
from normalise import clean_invoice_dict
from pdf_to_images import pdf_pages_as_base64
from schema import Invoice

from pydantic import ValidationError


def process_invoice(pdf_path: str | Path) -> list[Invoice]:
    """Extract and validate all invoice pages from a PDF."""
    pages = pdf_pages_as_base64(pdf_path)
    invoices: list[Invoice] = []

    for page_num, page_b64 in enumerate(pages, start=1):
        raw = extract_invoice_from_image(page_b64)
        cleaned = clean_invoice_dict(raw)
        try:
            invoice = Invoice.model_validate(cleaned)
            invoices.append(invoice)
        except ValidationError as exc:
            print(f"Page {page_num}: validation failed — {exc.error_count()} errors")
            for err in exc.errors():
                print(f"  {err['loc']}: {err['msg']}")

    return invoices


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "invoice.pdf"
    results = process_invoice(pdf)
    for inv in results:
        print(json.dumps(inv.model_dump(mode="json"), indent=2))
```

7. Run the pipeline against your invoice:

```bash
python run_ocr.py acme-invoice-2026-04.pdf
```

Expected: JSON output with `vendor_name`, `invoice_number`, `invoice_date` in `YYYY-MM-DD`, `line_items` array, `total`.

## Verify

Run the pipeline and check that the output is valid JSON with the required keys:

```bash
python run_ocr.py acme-invoice-2026-04.pdf | python -c "
import json, sys
data = json.load(sys.stdin)
required = {'vendor_name', 'invoice_number', 'invoice_date', 'total', 'line_items'}
missing = required - data.keys()
assert not missing, f'missing keys: {missing}'
assert isinstance(data['line_items'], list), 'line_items must be a list'
assert len(data['line_items']) > 0, 'no line items extracted'
print('PASS — all required keys present, line_items non-empty')
"
```

Expected final line: `PASS — all required keys present, line_items non-empty`

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `json.JSONDecodeError` on Claude response | Model wrapped JSON in a markdown fence despite `system` instruction | The `re.sub` stripping in `extractor.py` covers this; if it still fails, add `"Return raw JSON only."` as the last line of `_SYSTEM`. |
| `ValidationError` on `quantity` field with value `"N/A"` | Line item row is a section header or total row, not a real item | Pre-filter items in `clean_invoice_dict`: skip rows where `description` matches `re.search(r"(?i)total|subtotal|tax|discount", item["description"])`. |
| `fitz.FileNotFoundError` | PDF path is wrong or file is not a valid PDF | Verify with `file invoice.pdf` (should show `PDF document`). |
| Extracted totals are off by 100x | European decimal format (1.234,56) not detected | Check `clean_decimal`; add a heuristic: if `total > subtotal * 10`, re-parse with the European branch. |
| Empty `line_items` list on a two-page invoice | Second page contains only the item table; first page has headers | Run `pdf_pages_as_base64` with `dpi=200` to improve table legibility. |
| `anthropic.RateLimitError` on a 20-page PDF | Default rate limit exceeded for concurrent calls | Process pages sequentially (the loop in `run_ocr.py` already does this); add `time.sleep(0.5)` between pages if bursts remain. |
| Pydantic rejects `invoice_date` of format `"April 15, 2026"` | `normalise_date` only handles MM/DD/YYYY and DD-MM-YYYY | Add `from dateutil import parser; return parser.parse(v).strftime("%Y-%m-%d")` as the fallback in the validator (requires `pip install python-dateutil`). |

## Next

- Add a two-pass confidence check: re-extract any page where `total != sum(item.total for item in line_items)` with a more explicit prompt before raising a validation error.
- Replace per-page synchronous calls with `asyncio.gather` + `anthropic.AsyncAnthropic()` to parallelize extraction across pages for large batches.
- Extend `Invoice` with a `source_pdf` and `page_number` field, then persist results to PostgreSQL via SQLAlchemy for searchable invoice archives.

## References

- [knowledge/geek/ai/multimodal-ai/vision-applications](../../../knowledge/geek/ai/multimodal-ai/vision-applications) — defines OCR and document-extraction as a primary vision LLM use case; this playbook implements the invoice digitization pattern described there with structured JSON output and cost-control via 150 DPI pre-scaling
- [knowledge/geek/ai/multimodal-ai/vision-basics](../../../knowledge/geek/ai/multimodal-ai/vision-basics) — specifies the base64 image encoding path and the `image` content block structure used verbatim in Step 4's `extract_invoice_from_image` function
