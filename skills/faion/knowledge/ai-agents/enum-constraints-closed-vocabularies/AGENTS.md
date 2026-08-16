# Enum Constraints for Closed Vocabularies

## Summary

**One-sentence:** Declares finite answer sets as Literal/enum so constrained decoders mask non-enum tokens to zero probability at sampling time, eliminating hallucinated labels and giving the highest accuracy-per-token ratio of any structured-output trick.

**One-paragraph:** Whenever the answer set is finite, declare it as a typed enum (`Literal[...]` in Pydantic, `enum` in JSON Schema) instead of a free-form string. Constrained decoders mask every non-enum token to probability zero, so a hallucinated label becomes mathematically impossible. The rule is a one-line schema change with the highest accuracy-per-token ratio of any structured-output trick — production classification tasks go from 80-95% raw to ~100% with `Literal[...]` plus strict mode.

**Ефективно для:** будь-яких полів класифікації з фіксованим набором значень: sentiment, severity, routing labels, статусні стани, мовні коди.

## Applies If (ALL must hold)

- A classification field has a finite, known set of valid values.
- The field maps to a downstream switch/case, DB enum column, or routing dispatch.
- Provider supports strict mode or a constrained decoder (OpenAI strict, Pydantic v2, Outlines, XGrammar, vLLM guided).
- Pipelines fail when an unknown label slips through.

## Skip If (ANY kills it)

- Open vocabularies (free-text tags, novel entity types, user names) — enum would clip valid answers.
- Semi-open sets — use Literal + discriminated-union fallback instead.
- JSON-mode-only fallback paths on mini/nano models — enums are advisory there; pair with strict mode to enforce.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Finite value set | List of strings | Domain taxonomy |
| Schema definition | Pydantic BaseModel or JSON Schema | Application code |
| Decoder mode | strict / grammar-backed | Provider config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `decimal-as-string-pattern` | Same sampling-time-mask principle for numeric/format fields. |
| `discriminated-union-output` | Discriminator literals are the canonical enum-with-routing pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Four testable rules: enum-not-string, strict-mode required, semi-open via union, retry-feedback on JSON-mode | ~900 |
| `content/02-output-contract.xml` | essential | Pydantic + JSON Schema forms, semi-open union, validation table | ~900 |
| `content/03-failure-modes.xml` | essential | Listed-in-prompt-but-str-type, no-strict-mode-trust, value-typo drift | ~700 |
| `content/06-decision-tree.xml` | essential | Closed → enum, semi-open → union, open → free-string | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Add enums to existing free-string fields | haiku | Mechanical conversion |
| Audit schemas for prompt-only enum hints | sonnet | Pattern detection across files |
| Design semi-open hybrid for novel taxonomy | opus | Tradeoffs with downstream routing |

## Templates

| File | Purpose |
|------|---------|
| `templates/enum_schema.py` | Pydantic model with Literal enum fields wired for OpenAI strict mode |
| `templates/_smoke-test.json` | Minimum valid ticket object for self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-enum-constraints-closed-vocabularies.py` | Validates a JSON instance against the enum value set | Pre-commit on schema changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[decimal-as-string-pattern]]
- [[discriminated-union-output]]
- [[field-descriptions-as-prompts]]

## Decision tree

See `content/06-decision-tree.xml`. The root question is whether the value set is finite. The tree then routes finite-closed sets to `Literal[...]`, finite-mostly-closed sets to a discriminated union with a "novel" branch, and genuinely open sets to free-string. Each leaf maps to a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/enum_schema.py`

```python
"""Strict-mode Pydantic schema with Literal enum fields.

Use with OpenAI:
    client.responses.parse(model="gpt-5", input=msgs, text_format=Ticket)

Or Anthropic tool-call mode:
    tools=[{"name": "submit_ticket", "input_schema": Ticket.model_json_schema()}]
    tool_choice={"type": "tool", "name": "submit_ticket"}
"""

from typing import Literal

from pydantic import BaseModel, Field

# Closed enums — every valid value listed; decoder masks all others.
Category = Literal["billing", "tech_support", "refund", "spam", "other"]
Priority = Literal["P0", "P1", "P2", "P3"]
Sentiment = Literal["angry", "frustrated", "neutral", "happy"]


class Ticket(BaseModel):
    """Support ticket classification.

    `extra=forbid` translates to JSON Schema `additionalProperties: false`,
    which is mandatory under OpenAI strict mode.
    """

    model_config = {"extra": "forbid"}

    reasoning: str = Field(
        description="Brief evidence for the labels below. Keep under 60 words."
    )
    category: Category = Field(description="Primary intent of the message.")
    priority: Priority = Field(description="Urgency level; P0 = service down.")
    sentiment: Sentiment = Field(description="Emotional tone of the customer.")
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "smallest valid ticket for the enum validator",
  "_consumes": "nothing",
  "_produces": "example Ticket with all-enum fields",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "~50 tokens",
  "category": "billing",
  "priority": "P1",
  "sentiment": "frustrated"
}
```
