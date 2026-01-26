# Vision LLM Prompts

Optimized prompts for vision tasks with OpenAI, Claude, and Gemini.

## OCR Prompts

### Basic Text Extraction

```
Extract all text visible in this image.
Maintain the original formatting, layout, and line breaks where possible.
If text is unclear or partially visible, indicate with [unclear] or [partial].
```

### Structured Text Extraction

```
Extract all text from this image and return as JSON with this structure:
{
  "title": "main heading or title if present",
  "body": "main body text",
  "lists": ["any bulleted or numbered items"],
  "tables": [{"headers": [], "rows": [[]]}],
  "footnotes": "any footer or footnote text"
}

Use null for sections that don't exist in the image.
```

### Handwritten Text

```
This image contains handwritten text. Please:
1. Transcribe all handwritten content you can read
2. Maintain paragraph structure
3. Use [illegible] for words you cannot decipher
4. Note any crossed-out or corrected text in [brackets]

Return the transcription with best effort accuracy.
```

## Document Analysis Prompts

### Invoice Extraction

```
Analyze this invoice and extract all data into this exact JSON structure:
{
  "vendor": {
    "name": "",
    "address": "",
    "phone": "",
    "email": ""
  },
  "invoice_details": {
    "number": "",
    "date": "YYYY-MM-DD",
    "due_date": "YYYY-MM-DD",
    "po_number": ""
  },
  "customer": {
    "name": "",
    "address": ""
  },
  "line_items": [
    {
      "description": "",
      "quantity": 0,
      "unit_price": 0.00,
      "total": 0.00
    }
  ],
  "totals": {
    "subtotal": 0.00,
    "tax_rate": 0.00,
    "tax_amount": 0.00,
    "shipping": 0.00,
    "total": 0.00
  },
  "payment": {
    "terms": "",
    "method": "",
    "bank_details": ""
  }
}

Use null for any field not visible in the document.
Format all monetary values as numbers without currency symbols.
```

### Receipt Extraction

```
Extract receipt information into this JSON format:
{
  "merchant": {
    "name": "",
    "address": "",
    "phone": ""
  },
  "transaction": {
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "receipt_number": "",
    "cashier": ""
  },
  "items": [
    {
      "name": "",
      "sku": "",
      "quantity": 1,
      "unit_price": 0.00,
      "total": 0.00,
      "discount": 0.00
    }
  ],
  "totals": {
    "subtotal": 0.00,
    "tax": 0.00,
    "total": 0.00,
    "savings": 0.00
  },
  "payment": {
    "method": "",
    "card_type": "",
    "last_four": "",
    "amount_tendered": 0.00,
    "change": 0.00
  }
}

Parse all prices as decimal numbers.
```

### Contract Key Terms

```
Analyze this contract/agreement and extract key terms:
{
  "document_type": "contract type (NDA, Employment, Service Agreement, etc.)",
  "parties": [
    {"name": "", "role": "Party A/Party B/Vendor/Client/etc."}
  ],
  "effective_date": "YYYY-MM-DD",
  "termination_date": "YYYY-MM-DD or conditions",
  "key_terms": {
    "payment_terms": "",
    "deliverables": [],
    "confidentiality_period": "",
    "non_compete_period": "",
    "termination_conditions": [],
    "liability_cap": "",
    "jurisdiction": ""
  },
  "important_clauses": [
    {"clause_name": "", "summary": ""}
  ],
  "signatures": [
    {"party": "", "signed": true/false, "date": ""}
  ]
}

Focus on legally significant terms and obligations.
```

## Image Analysis Prompts

### Product Description

```
Analyze this product image and provide:
{
  "product_type": "category of product",
  "brand": "if visible",
  "color": "primary colors",
  "material": "if identifiable",
  "condition": "new/used/damaged",
  "visible_features": ["list of notable features"],
  "text_on_product": "any visible text/labels",
  "suitable_for": ["suggested use cases"],
  "description": "2-3 sentence marketing description"
}
```

### Technical Diagram

```
Analyze this technical diagram/schematic:
{
  "diagram_type": "flowchart/circuit/architecture/UML/etc.",
  "title": "if present",
  "components": [
    {"name": "", "type": "", "description": ""}
  ],
  "connections": [
    {"from": "", "to": "", "label": "", "type": ""}
  ],
  "flow_direction": "left-to-right/top-to-bottom/etc.",
  "annotations": ["any notes or labels"],
  "summary": "brief explanation of what this diagram shows"
}
```

### Chart/Graph Analysis

```
Analyze this chart/graph and extract the data:
{
  "chart_type": "bar/line/pie/scatter/etc.",
  "title": "",
  "x_axis": {"label": "", "type": "categorical/numerical/date"},
  "y_axis": {"label": "", "unit": ""},
  "legend": ["series names if multiple"],
  "data_points": [
    {"x": "", "y": 0, "series": ""}
  ],
  "trends": "describe any notable trends",
  "key_insights": ["main takeaways from this visualization"],
  "source": "if attributed"
}

Extract actual numerical values where visible.
```

## Classification Prompts

### Multi-Category Classification

```
Classify this image. Analyze carefully and return:
{
  "primary_category": "single best category",
  "confidence": 0.0-1.0,
  "secondary_categories": [
    {"category": "", "confidence": 0.0}
  ],
  "attributes": {
    "has_people": true/false,
    "has_text": true/false,
    "is_indoor": true/false,
    "is_professional": true/false,
    "dominant_colors": []
  },
  "reasoning": "brief explanation"
}

Categories to consider: [INSERT YOUR CATEGORIES HERE]
```

### Quality Assessment

```
Assess the quality of this image:
{
  "overall_quality": "high/medium/low",
  "technical_quality": {
    "resolution": "high/adequate/low",
    "sharpness": "sharp/slightly_blurry/blurry",
    "exposure": "well_exposed/overexposed/underexposed",
    "noise": "minimal/moderate/significant",
    "color_accuracy": "accurate/shifted/desaturated"
  },
  "composition": {
    "framing": "good/acceptable/poor",
    "lighting": "professional/natural/poor",
    "background": "clean/busy/distracting"
  },
  "usability": {
    "suitable_for_web": true/false,
    "suitable_for_print": true/false,
    "needs_editing": true/false
  },
  "issues": ["list any specific problems"],
  "recommendations": ["suggested improvements"]
}
```

## Content Moderation Prompts

### Comprehensive Safety Check

```
Analyze this image for content safety across all categories:
{
  "safe_for_work": true/false,
  "safe_for_minors": true/false,
  "categories": {
    "violence": {"detected": false, "severity": "none/mild/moderate/severe"},
    "gore": {"detected": false, "severity": "none/mild/moderate/severe"},
    "nudity": {"detected": false, "severity": "none/partial/full"},
    "sexual_content": {"detected": false, "severity": "none/suggestive/explicit"},
    "hate_symbols": {"detected": false, "examples": []},
    "weapons": {"detected": false, "type": ""},
    "drugs": {"detected": false, "type": ""},
    "self_harm": {"detected": false, "severity": ""},
    "disturbing": {"detected": false, "reason": ""}
  },
  "overall_severity": "safe/low/medium/high/critical",
  "action": "approve/flag_for_review/reject",
  "explanation": "brief justification for the rating"
}

Be thorough but avoid false positives for artistic, educational, or news content.
```

### Brand Safety

```
Analyze this image for brand safety concerns:
{
  "brand_safe": true/false,
  "concerns": {
    "controversial_topics": [],
    "competitor_presence": [],
    "negative_sentiment": "",
    "inappropriate_context": "",
    "quality_issues": []
  },
  "visible_brands": ["list any brands/logos visible"],
  "context": "describe the overall context",
  "recommendation": "safe/caution/avoid",
  "explanation": ""
}
```

## Accessibility Prompts

### Alt Text Generation

```
Generate accessible alt text for this image.

Return:
{
  "alt_text": "concise description under 125 characters for alt attribute",
  "long_description": "detailed 2-3 sentence description for aria-describedby",
  "image_type": "photo/illustration/icon/chart/screenshot/etc.",
  "is_decorative": false,
  "contains_text": false,
  "text_content": "any text visible in the image"
}

Guidelines:
- Start with the most important information
- Be specific (e.g., "Golden retriever puppy" not "dog")
- Include relevant context for the page purpose
- Mention text in images verbatim if important
- For charts/graphs, summarize the key data point
```

### Scene Description for Visually Impaired

```
Describe this image in detail for someone who cannot see it:

1. Start with the main subject and action
2. Describe the setting and background
3. Note colors, lighting, and mood
4. Mention any text visible
5. Describe spatial relationships (left, right, foreground, background)
6. Include relevant details that convey meaning

Format as natural flowing prose, not a list.
Write 3-4 sentences for a simple image, up to a paragraph for complex scenes.
```

## Best Practices

### Temperature Settings

| Task | Temperature | Rationale |
|------|-------------|-----------|
| OCR/Extraction | 0.0 | Maximum determinism |
| Classification | 0.0-0.3 | Consistency needed |
| Description | 0.5-0.7 | Some creativity ok |
| Creative tasks | 0.7-1.0 | Variety desired |

### Prompt Structure Tips

1. **Be specific about output format** - Always specify JSON structure for extraction tasks
2. **Define edge cases** - Tell the model what to do with missing/unclear data
3. **Provide examples** - For complex formats, show one example
4. **Set constraints** - Character limits, required fields, value ranges
5. **Request confidence** - Ask for confidence scores to filter uncertain results

### Multi-Image Prompts (Gemini)

```
I'm providing [N] images. For each image:
1. [Task description]

Return a JSON array with one object per image in the same order:
[
  {"image_index": 1, ...result fields...},
  {"image_index": 2, ...result fields...}
]
```

### Comparison Prompts

```
Compare these two images and analyze:
{
  "similarities": [],
  "differences": [],
  "image_1_unique": [],
  "image_2_unique": [],
  "preferred": "image_1/image_2/neither",
  "preference_reason": ""
}
```
