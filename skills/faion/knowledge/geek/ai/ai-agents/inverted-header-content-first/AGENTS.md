# Inverted Header — Content First, Metadata Last

## Summary

When one structured-output call must produce both a long-form body and metadata about that body (title, slug, summary, tags, sentiment), declare the body field FIRST in the schema and every metadata field AFTER it. The autoregressive model can only condition the title on tokens that already exist; if `title` is generated before `body`, the body is forced to fit a blind title; if `body` comes first, the title becomes a faithful summary of what was actually written.

## Why

This is the schema-field-order rule applied to the title-vs-body case. The body IS the reasoning trace for the title — every paragraph of body becomes context for the next-token prediction of title, slug, and tags. AWS Bedrock's 2026 SO design guide states it directly: "Field ordering represents a form of Chain of Thought embedded directly into your data structure." Castillo's empirical study showed a 13 pp accuracy gap (46.67% vs 33.33%, p < 0.01) on LiveBench from field reorder alone, and the title/body case is the most common production manifestation.

## When To Use

- Article, blog post, email, social-media post generation in one SO call
- Product description plus tags, slug, SEO title
- Code generation followed by an explanation summary
- Image caption with both long alt-text and short title
- Any single-call output where short metadata fields summarize a long content field

## When NOT To Use

- The title is a hard input constraint provided by the user — pass it in the prompt, omit from schema
- Streaming UI must show a title before the body finishes — split into two calls instead
- Metadata is fully deterministic from the prompt (e.g., `lang="en"` from a known input) — order does not matter
- The "metadata" field is in fact a routing decision the user already gave you — keep that out of generated output

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | The body-before-metadata rule with empirical anchor and a Pydantic example. |
| `content/02-streaming-tradeoff.xml` | Anti-pattern of splitting too eagerly when streaming, and the two-call escape hatch. |

## Templates

| File | Purpose |
|------|---------|
| `templates/blog_post_schema.py` | Pydantic `BlogPost` model with body first, then title/slug/tags. |

## References

- [AWS Bedrock structured-output JSON schema design (2026)](https://explore.n1n.ai/blog/aws-bedrock-json-schema-structured-output-guide-2026-02-16)
- [Dylan Castillo — Structured outputs: don't put the cart before the horse](https://dylancastillo.co/posts/llm-pydantic-order-matters.html)
