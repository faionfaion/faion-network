# Schema Markup Templates Reference

## Implementation

All schemas use JSON-LD format, placed in `<head>` or before `</body>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "...",
  ...
}
</script>
```

---

## Organization Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Faion Network",
  "alternateName": "Faion",
  "url": "https://faion.net",
  "logo": {
    "@type": "ImageObject",
    "url": "https://faion.net/logo.png",
    "width": 512,
    "height": 512
  },
  "description": "AI-powered framework for solopreneurs",
  "foundingDate": "2024",
  "founder": {
    "@type": "Person",
    "name": "Ruslan Faion"
  },
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "UA"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "email": "support@faion.net",
    "availableLanguage": ["English", "Ukrainian"]
  },
  "sameAs": [
    "https://twitter.com/faion",
    "https://linkedin.com/company/faion",
    "https://github.com/faion"
  ]
}
```

---

## Article Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "SDD Methodology: Complete Guide for 2026",
  "description": "Learn how to implement Specification-Driven Development...",
  "image": {
    "@type": "ImageObject",
    "url": "https://faion.net/images/sdd-guide.jpg",
    "width": 1200,
    "height": 630
  },
  "author": {
    "@type": "Person",
    "name": "Ruslan Faion",
    "url": "https://faion.net/about/"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Faion Network",
    "logo": {
      "@type": "ImageObject",
      "url": "https://faion.net/logo.png"
    }
  },
  "datePublished": "2026-01-15",
  "dateModified": "2026-01-18",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://faion.net/guides/sdd/"
  },
  "inLanguage": "en",
  "keywords": ["SDD", "specification-driven development", "solopreneur"],
  "articleSection": "Guides",
  "wordCount": 5000
}
```

---

## BlogPosting Schema

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "How I Built a SaaS in 30 Days Using SDD",
  "description": "A step-by-step breakdown of building a SaaS product...",
  "image": "https://faion.net/images/blog/saas-30-days.jpg",
  "author": {
    "@type": "Person",
    "name": "Ruslan Faion"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Faion Network"
  },
  "datePublished": "2026-01-10",
  "dateModified": "2026-01-15"
}
```

---

## Product Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Faion Network Pro",
  "description": "Full access to 282 methodologies and 43 AI agents",
  "image": "https://faion.net/images/pro-plan.jpg",
  "brand": {
    "@type": "Brand",
    "name": "Faion Network"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://faion.net/pricing/",
    "priceCurrency": "USD",
    "price": "35.00",
    "priceValidUntil": "2026-12-31",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "Faion Network"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "127"
  }
}
```

---

## SoftwareApplication Schema

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Faion Network Framework",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Cross-platform",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "ratingCount": "89"
  }
}
```

---

## FAQPage Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is Faion Network?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Faion Network is an AI-powered framework for solopreneurs that includes 282 methodologies and 43 AI agents to help build products faster."
      }
    },
    {
      "@type": "Question",
      "name": "Is there a free plan?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, Faion Network offers a free tier for personal, non-commercial use. It includes 5 methodologies and 2 AI agents."
      }
    },
    {
      "@type": "Question",
      "name": "What payment methods are accepted?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We accept all major credit cards through Stripe. Annual plans receive a discount."
      }
    }
  ]
}
```

---

## HowTo Schema

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Set Up Faion Network",
  "description": "Complete guide to getting started with Faion Network",
  "image": "https://faion.net/images/setup-guide.jpg",
  "totalTime": "PT15M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "0"
  },
  "tool": [
    {
      "@type": "HowToTool",
      "name": "Claude Code CLI"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "name": "Install Claude Code",
      "text": "Install Claude Code CLI using npm: npm install -g @anthropic/claude-code",
      "url": "https://faion.net/docs/setup/#step-1",
      "image": "https://faion.net/images/step1.jpg"
    },
    {
      "@type": "HowToStep",
      "name": "Clone Faion Skills",
      "text": "Clone the Faion Network skills repository to your .claude directory",
      "url": "https://faion.net/docs/setup/#step-2"
    },
    {
      "@type": "HowToStep",
      "name": "Configure Your Project",
      "text": "Run /faion-net to initialize your project with SDD structure",
      "url": "https://faion.net/docs/setup/#step-3"
    }
  ]
}
```

---

## BreadcrumbList Schema

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://faion.net/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Guides",
      "item": "https://faion.net/guides/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "SDD Methodology"
    }
  ]
}
```

---

## Person Schema (Author)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Ruslan Faion",
  "url": "https://faion.net/about/",
  "image": "https://faion.net/images/ruslan.jpg",
  "jobTitle": "Founder & CEO",
  "worksFor": {
    "@type": "Organization",
    "name": "Faion Network"
  },
  "sameAs": [
    "https://twitter.com/ruslanfaion",
    "https://linkedin.com/in/ruslanfaion",
    "https://github.com/ruslanfaion"
  ],
  "knowsAbout": ["AI Development", "Solopreneurship", "SDD Methodology"]
}
```

---

## WebPage Schema

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Faion Network - AI Framework for Solopreneurs",
  "description": "Build products 10x faster with 282 methodologies and 43 AI agents",
  "url": "https://faion.net/",
  "inLanguage": "en",
  "isPartOf": {
    "@type": "WebSite",
    "name": "Faion Network",
    "url": "https://faion.net/"
  },
  "about": {
    "@type": "Thing",
    "name": "AI Development Framework"
  },
  "mainEntity": {
    "@type": "Organization",
    "name": "Faion Network"
  }
}
```

---

## WebSite Schema (with Search)

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Faion Network",
  "url": "https://faion.net/",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://faion.net/search/?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

---

## Validation Checklist

Before deploying schema:

- [ ] Valid JSON syntax (use JSON validator)
- [ ] Test with [Google Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Test with [Schema Validator](https://validator.schema.org/)
- [ ] Required properties present
- [ ] URLs are absolute and accessible
- [ ] Images exist and are proper dimensions
- [ ] Dates in ISO 8601 format
- [ ] No schema on noindex pages
