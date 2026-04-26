# Agent Integration — Search Everywhere Optimization (GEO/AEO)

## When to use
- Publishing content that should be cited by AI engines (ChatGPT, Perplexity, Gemini) in addition to ranking in Google
- Auditing existing content library for GEO/AEO readiness (structured data, entity clarity, content freshness)
- Creating new content targeted at AI Overview inclusion, featured snippets, and voice search
- Building brand entity presence across the web (consistent mentions, structured citations, schema markup)
- Monitoring AI share of voice and citation frequency for a brand or product

## When NOT to use
- Content is purely transactional/local (restaurant menu, service area page) — traditional local SEO still dominates these query types
- Audience is exclusively finding products via Amazon or TikTok search — GEO/AEO optimization for Google/Perplexity has no lift here
- Existing domain authority is near-zero — GEO requires some level of established web presence and backlink authority before AI engines will cite the content
- No content publishing cadence exists — GEO is a content strategy layer, not a substitute for having content

## Where it fails / limitations
- AI citation tracking tools (Otterly.AI, Profound, Semrush AI Visibility) are paid SaaS with no free API tier — monitoring requires budget
- AI engine citation behavior is non-deterministic and changes with model updates — optimization today may not hold in 3-6 months
- Brand mention consistency across the web (PR, guest posts, citations) requires human relationship-building that agents cannot automate
- Schema markup validation requires testing tools (Google Rich Results Test, Schema.org validator) that are not natively accessible to agents
- "Content freshness" as a GEO signal means content must be actively updated (within 30 days) — maintenance burden is ongoing

## Agentic workflow
Claude agents are well-suited for: auditing existing content pages against GEO/AEO criteria, rewriting content sections to use question-answer format, generating FAQ schema markup, and producing structured content outlines optimized for AI extraction. Sonnet handles content rewrites and schema generation; Opus handles multi-platform visibility strategy and content gap analysis. Agents cannot verify if content is actually being cited by AI engines — that requires external monitoring tools. All schema markup produced by agents must be validated through Google Rich Results Test before deployment.

### Recommended subagents
- `faion-sdd-executor-agent` — for managing GEO/AEO as a structured content optimization initiative
- General Claude Sonnet subagent — for content rewriting into Q&A format, FAQ schema generation, structured content outlines
- General Claude Opus subagent — for multi-platform visibility strategy, entity relationship mapping

### Prompt pattern
```
Audit this content page for GEO/AEO readiness. Evaluate:
1. Does each heading have a direct answer within 2 sentences?
2. Are there FAQ sections with question-format headings?
3. Is entity language consistent (brand name, product names)?
4. Are there tables, bullet points, or numbered lists for key data?
5. Is there original data, framework, or insight an AI would cite?
Output: score per criterion (Pass/Fail), specific fix per Fail.

Content: [paste content]
```

```
Generate FAQ schema markup (JSON-LD) for the following Q&A pairs.
Format: valid schema.org/FAQPage JSON-LD, ready to paste into <head>.
Q&A pairs:
- Q: [question 1] A: [answer 1]
- Q: [question 2] A: [answer 2]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `curl` | Fetch Google Rich Results API, Semrush API | Standard |
| `schema-dts` | TypeScript types for schema.org markup generation | `npm install schema-dts` |
| `structured-data-testing-tool` (deprecated) | Legacy schema validation | Replaced by Rich Results Test |
| `lighthouse` | Technical SEO audit including structured data | `npm install -g lighthouse` |
| `semrush-cli` (unofficial) | Keyword and visibility data via Semrush API | Semrush API docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Semrush AI Visibility Toolkit | SaaS | Yes — API | AI share of voice tracking; GEO-specific metrics |
| Otterly.AI | SaaS | Partial | Brand citation monitoring in ChatGPT/Perplexity; no bulk API |
| Profound | SaaS | Partial | AI answer monitoring; enterprise pricing |
| Similarweb Gen AI Intelligence | SaaS | Partial | Traffic analysis with AI engine breakdowns |
| Google Search Console | SaaS | Yes — API | AI Overviews impression data (limited); standard organic metrics |
| Schema.org validator | OSS | No | Manual validation; use Google Rich Results Test instead |
| Perplexity API | SaaS | Yes — API | Test how Perplexity responds to brand queries; no bulk mode |
| BrightEdge | SaaS | Partial | Enterprise SEO with AI visibility features |

## Templates & scripts
Inline — Python script to generate FAQ schema markup:
```python
import json

def generate_faq_schema(qa_pairs: list[dict]) -> str:
    """Generate JSON-LD FAQ schema from Q&A pairs."""
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": pair["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": pair["a"]
                }
            }
            for pair in qa_pairs
        ]
    }
    return json.dumps(schema, indent=2)

qa_pairs = [
    {"q": "What is GEO?", "a": "GEO (Generative Engine Optimization) is the practice of optimizing content to be cited by AI-powered search engines like ChatGPT and Perplexity."},
    {"q": "How does AEO differ from SEO?", "a": "AEO focuses on providing direct answers for AI-generated responses, while traditional SEO targets ranked links in search results pages."},
]

print(generate_faq_schema(qa_pairs))
```

## Best practices
- Structure every content page so each H2/H3 heading is a question and the first paragraph directly answers it — this is the highest-impact single change for AEO
- Update content at least monthly; AI engines weight recency heavily (within-30-days content gets 3.2x more citations per Semrush research)
- Build entity consistency: use the exact same brand name, product names, and founder names across all pages, social profiles, and external mentions
- Add HowTo schema to tutorial content and Speakable schema to key answer paragraphs — these are explicitly used by voice search and AI engines
- Publish original research, frameworks, or proprietary data — AI engines prefer citable primary sources over generic summaries of existing content
- Monitor AI citation with Otterly.AI or Profound monthly; set up Google Alerts for brand name mentions as a proxy
- Earn high-authority backlinks from publications in your industry — AI engines use external citations as authority signals, mirroring traditional PageRank logic

## AI-agent gotchas
- Schema markup generated by agents must be validated before deployment — agents produce syntactically plausible but semantically incorrect schema (wrong @type, missing required fields)
- Agents cannot query Perplexity or ChatGPT to check if the brand is being cited — this requires manual testing or third-party monitoring tools
- GEO recommendations from agents that include "publish more content" without specificity are not actionable; require the agent to output specific content gaps as article titles and target queries
- Content freshness signals require actual content updates, not just updated dates in metadata — agents should produce a specific "update brief" per article, not just flag it for review
- Entity relationship recommendations (linking brand to specific named individuals, concepts, or products) must be cross-checked against what AI engines actually associate with the brand; agents may suggest associations that are not currently established

## References
- https://www.semrush.com/blog/generative-engine-optimization/
- https://searchengineland.com/guide/what-is-answer-engine-optimization-aeo
- https://www.otterly.ai/
- https://www.similarweb.com/corp/marketing/generative-ai-intelligence/
- https://developers.google.com/search/docs/appearance/structured-data/faqpage
