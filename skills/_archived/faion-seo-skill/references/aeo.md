# Answer Engine Optimization (AEO) Reference

## What is AEO?

Answer Engine Optimization is the practice of structuring content so AI-powered systems (ChatGPT, Perplexity, Google AI Overviews, Claude, Microsoft Copilot) can:
- Extract information accurately
- Cite your brand as a trusted source
- Generate on-brand answers

---

## AEO vs SEO Convergence

| Traditional SEO | AEO | Overlap |
|-----------------|-----|---------|
| Rankings on SERPs | Citations in AI answers | Quality content |
| Click-through rate | Brand mentions | Authority signals |
| Keyword targeting | Entity optimization | Structured data |
| Link building | Source credibility | E-E-A-T |

> In 2025, SEO and AEO are converging. The same fundamentals work for both.

---

## llms.txt Standard

### Purpose

`llms.txt` is an emerging standard (like robots.txt for AI) that:
- Provides AI crawlers with curated site structure
- Specifies canonical sources for information
- Reduces hallucination risk
- Controls what AI systems reference

### Format

```txt
# llms.txt - https://example.com/llms.txt

# Company Name
> One-line description of what the company does

## Core Pages
- About: https://example.com/about/
- Products: https://example.com/products/
- Pricing: https://example.com/pricing/
- Documentation: https://example.com/docs/

## Key Content
- Blog: https://example.com/blog/
- Guides: https://example.com/guides/
- Case Studies: https://example.com/cases/

## Products/Services
- Product 1: https://example.com/product-1/ - Brief description
- Product 2: https://example.com/product-2/ - Brief description

## Team/Authors
- CEO: https://example.com/team/ceo/
- CTO: https://example.com/team/cto/

## Contact
- Email: contact@example.com
- Support: https://example.com/support/

## Legal
- Terms: https://example.com/terms/
- Privacy: https://example.com/privacy/

## Exclusions (don't reference)
- /admin/*
- /internal/*
- /premium/* (requires subscription)
```

### Implementation

1. Create `llms.txt` at domain root: `https://example.com/llms.txt`
2. Keep it updated when site structure changes
3. Reference in robots.txt: `# See also: /llms.txt for AI crawlers`
4. Consider language-specific versions for multilingual sites

---

## Structured Data for AI

### Organization Schema (Brand Identity)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Faion Network",
  "alternateName": "Faion",
  "url": "https://faion.net",
  "logo": "https://faion.net/logo.png",
  "description": "AI-powered framework for solopreneurs with 282 methodologies",
  "foundingDate": "2024",
  "founder": {
    "@type": "Person",
    "name": "Ruslan Faion"
  },
  "sameAs": [
    "https://twitter.com/faion",
    "https://linkedin.com/company/faion",
    "https://github.com/faion"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "email": "support@faion.net"
  }
}
```

### FAQPage Schema (High AEO Value)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is SDD methodology?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SDD (Specification-Driven Development) is a methodology that starts every project with a clear specification. It includes 282 battle-tested frameworks covering research, design, development, and deployment."
      }
    },
    {
      "@type": "Question",
      "name": "How much does Faion Network cost?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Faion Network offers a free tier for personal use, Plus at $19/month, Pro at $35/month, and Ultimate (team) at $175/month."
      }
    }
  ]
}
```

### HowTo Schema (Process Content)

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Start a SDD Project",
  "description": "Step-by-step guide to beginning a project with SDD methodology",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Define the Problem",
      "text": "Start by clearly defining the problem you're solving...",
      "url": "https://faion.net/guides/sdd/#step-1"
    },
    {
      "@type": "HowToStep",
      "name": "Write Specification",
      "text": "Create a detailed spec.md document...",
      "url": "https://faion.net/guides/sdd/#step-2"
    }
  ]
}
```

---

## Content Optimization for AI

### Structure for AI Extraction

```markdown
# Clear, Question-Like Heading

**Direct answer in the first paragraph.** This is what AI systems
will likely extract. Keep it concise and factual.

## Supporting Details

Expand on the answer with context, examples, and data.

## Common Follow-up Questions

Address related questions that users might ask.

## Sources and References

Link to authoritative sources that support your claims.
```

### Best Practices

| Do | Don't |
|------|--------|
| Answer questions directly | Bury answers in long paragraphs |
| Use clear headings (H2, H3) | Use vague headings like "More Info" |
| Include specific facts/numbers | Make vague claims |
| Cite sources | Present opinions as facts |
| Update content regularly | Let content become stale |
| Add publish/update dates | Hide content age |

### Date Signals

AI systems favor recent content. Include:

```html
<meta property="article:published_time" content="2026-01-18T00:00:00Z" />
<meta property="article:modified_time" content="2026-01-18T00:00:00Z" />
```

```json
{
  "@type": "Article",
  "datePublished": "2026-01-18",
  "dateModified": "2026-01-18"
}
```

In content:
> Last updated: January 2026

---

## Entity Optimization

### What is an Entity?

An entity is a thing (person, place, organization, concept) that search engines and AI understand as a distinct object in their knowledge graph.

### Building Entity Authority

1. **Consistent NAP** - Name, Address, Phone across web
2. **Wikipedia/Wikidata** - If notable enough
3. **Knowledge Panel** - Claim in Google
4. **Schema markup** - Organization, Person schemas
5. **sameAs links** - Connect social profiles
6. **About page** - Detailed, linked entity

### Author Entity (E-E-A-T)

```json
{
  "@type": "Article",
  "author": {
    "@type": "Person",
    "name": "Ruslan Faion",
    "url": "https://faion.net/about/ruslan/",
    "sameAs": [
      "https://twitter.com/ruslanfaion",
      "https://linkedin.com/in/ruslanfaion"
    ],
    "jobTitle": "Founder",
    "worksFor": {
      "@type": "Organization",
      "name": "Faion Network"
    }
  }
}
```

---

## AI Visibility Metrics

### How to Track AI Citations

1. **Brand monitoring** - Set up alerts for brand mentions
2. **Search your brand + AI** - "faion network chatgpt"
3. **Test in AI systems** - Ask ChatGPT/Perplexity about your topic
4. **Track referral traffic** - From perplexity.ai, chatgpt.com
5. **Use specialized tools** - LLMrefs, Profound, Otterly.ai

### Key Metrics

| Metric | What It Measures |
|--------|------------------|
| AI citation count | Times your brand is cited by AI |
| Citation accuracy | Correctness of AI-generated info about you |
| Share of voice | Your citations vs competitors |
| Referral traffic | Visits from AI answer links |

---

## AI Crawler Management

### robots.txt for AI Bots

```txt
# Search engine crawlers - Allow
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# AI crawlers - Selective access
User-agent: GPTBot
Allow: /
Disallow: /premium/  # Paywalled content

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

# Block AI training but allow chat
User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /
```

### AI Crawler Access Decisions

| Content Type | Recommendation |
|--------------|----------------|
| Public blog posts | Allow all AI |
| Product pages | Allow all AI |
| Pricing/FAQ | Allow all AI (high citation value) |
| Premium content | Consider blocking (or allow teasers) |
| User data | Block all |
| Internal tools | Block all |
