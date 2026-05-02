---
name: on-page-seo
description: Optimise every on-page SEO signal for a single content page — title tag, meta description, headings, semantic HTML, OpenGraph image, and JSON-LD structured data — so it can rank.
tier: solo
group: seo-essentials
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a fully optimised content page: a title tag ≤60 chars with the primary keyword first, a meta description ≤160 chars that earns clicks, a single H1, a descriptive H2/H3 heading hierarchy, semantic HTML5 landmarks, an OpenGraph image at 1200×630 px, and a valid schema.org JSON-LD block — all verified by a free validator.

## Prerequisites

- A live page you own (on any CMS, static site generator, or custom HTML).
- The primary keyword you want this page to rank for (one phrase, e.g. `invoicing software for freelancers`).
- Access to edit `<head>` and `<body>` HTML of the page (or its CMS template).
- A free Google Rich Results Test account is not required — the tool works without login: https://search.google.com/test/rich-results
- Optional but helpful: Google Search Console property verified for your domain.

## Steps

### 1. Research the exact primary keyword and note its search intent

Before writing a single tag, confirm the keyword in Google Search Console or a free tool such as Ahrefs Webmaster Tools (https://ahrefs.com/webmaster-tools):

1. Sign in to https://search.google.com/search-console/ and open **Performance → Search results**.
2. Filter by your page URL under **Pages** to see which query already sends the most impressions.
3. If the page is new, open https://ahrefs.com/webmaster-tools → **Site Explorer → Organic keywords** or use the free keyword idea tool at https://ahrefs.com/keyword-generator.
4. Write down one primary keyword (e.g. `freelance invoicing software`) and note the intent: informational, navigational, or transactional. The intent controls how you phrase every tag below.

### 2. Write the title tag (≤60 chars, primary keyword first)

Open the page template or CMS field for `<title>`.

Rules:
- Primary keyword must appear in the first 60 characters (Google truncates beyond that).
- Brand name goes at the end after a separator: `Primary keyword — Brand`.
- No keyword stuffing: one keyword phrase, one modifier at most.

Before (bad):
```html
<title>Welcome to InvoiceApp — The Best Invoicing Tool for Freelancers | InvoiceApp by Acme Inc.</title>
```

After (good):
```html
<title>Freelance Invoicing Software — InvoiceApp</title>
```

Character count check (run in your browser DevTools console):
```js
document.title.length
```

Target: ≤60. Anything over 60 is likely to be rewritten by Google.

### 3. Write the meta description (≤160 chars, action-leading)

Open the `<meta name="description">` tag (or its CMS equivalent).

Rules:
- Include the primary keyword naturally in the first 150 characters.
- Write one concrete benefit + one call-to-action verb.
- No duplicate of the title.

Before (bad):
```html
<meta name="description" content="InvoiceApp is a software that helps with invoices.">
```

After (good):
```html
<meta name="description" content="Send professional invoices in 60 seconds. InvoiceApp is free for freelancers — no credit card needed. Start today.">
```

Character count check:
```js
document.querySelector('meta[name="description"]').content.length
```

Target: ≤160.

### 4. Set exactly one H1 that matches the title topic

Scan the page HTML:
```bash
curl -s https://yoursite.com/your-page | grep -oi '<h1[^>]*>.*</h1>'
```

Rules:
- Exactly one `<h1>` per page. Multiple H1s are a ranking signal waste.
- H1 should contain the primary keyword but can be phrased differently from the title tag — it is what the reader sees on the page.
- Keep it under 70 characters.

Example:
```html
<h1>The Best Freelance Invoicing Software in 2026</h1>
```

### 5. Build a descriptive H2/H3 hierarchy

Map out the content sections and assign heading levels. Rules:
- H2 = top-level section. Each H2 should target a secondary keyword or sub-topic of the primary.
- H3 = sub-section inside an H2. Use for steps, features, or FAQs.
- Never skip levels (no H4 without an H3 parent).
- Each heading should be self-descriptive — a reader scanning only headings should understand the page structure.

Before (vague):
```html
<h2>Features</h2>
<h2>Pricing</h2>
<h2>More Info</h2>
```

After (descriptive):
```html
<h2>Core Features of Freelance Invoicing Software</h2>
<h2>Pricing Plans for Independent Contractors</h2>
<h2>How to Send Your First Invoice in 60 Seconds</h2>
```

Audit existing headings with:
```bash
curl -s https://yoursite.com/your-page | grep -oi '<h[1-6][^>]*>.*</h[1-6]>'
```

### 6. Use semantic HTML5 landmarks

Wrap your page structure in semantic elements — Google uses them to understand page architecture:

```html
<header>   <!-- site header, nav, logo -->
<main>     <!-- the primary page content -->
  <article>  <!-- the post/product/landing body -->
  </article>
</main>
<aside>    <!-- sidebar, related links -->
<footer>   <!-- site footer -->
```

Check what your page currently uses:
```bash
curl -s https://yoursite.com/your-page | grep -oi '<\(main\|article\|section\|aside\|header\|footer\)[^>]*>'
```

If you see only `<div>` wrappers, replace the outer containers with the correct semantic tags. No visual change is needed — semantic elements are styled identically to `<div>` by default.

### 7. Add the OpenGraph image (1200×630 px)

Open Graph tags control how your page looks when shared on LinkedIn, Slack, or iMessage. Google also uses the OG image as a content quality signal.

Required OG tags in `<head>`:
```html
<meta property="og:title" content="Freelance Invoicing Software — InvoiceApp">
<meta property="og:description" content="Send professional invoices in 60 seconds. Free for freelancers.">
<meta property="og:image" content="https://yoursite.com/images/og-invoice-app.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://yoursite.com/freelance-invoicing-software">
<meta property="og:type" content="website">
```

Image requirements:
- Dimensions: exactly 1200×630 px (2:1 aspect ratio).
- Format: JPG preferred for file size; PNG acceptable.
- File size: under 300 KB. Compress at https://squoosh.app.
- Content: include the product name or key benefit as legible text overlaid on the image.

Test with Facebook's Sharing Debugger:
```
https://developers.facebook.com/tools/debug/?q=https://yoursite.com/your-page
```

### 8. Add schema.org JSON-LD (Article or Product)

Structured data enables rich snippets in Google Search. Choose the type that matches your page:

**For a blog post or guide (Article):**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "The Best Freelance Invoicing Software in 2026",
  "description": "Send professional invoices in 60 seconds. InvoiceApp is free for freelancers.",
  "image": "https://yoursite.com/images/og-invoice-app.jpg",
  "author": {
    "@type": "Person",
    "name": "Your Name",
    "url": "https://yoursite.com/about"
  },
  "publisher": {
    "@type": "Organization",
    "name": "InvoiceApp",
    "logo": {
      "@type": "ImageObject",
      "url": "https://yoursite.com/logo.png"
    }
  },
  "datePublished": "2026-05-01",
  "dateModified": "2026-05-02",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://yoursite.com/freelance-invoicing-software"
  }
}
</script>
```

**For a product or SaaS landing page (Product):**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "InvoiceApp",
  "description": "Freelance invoicing software. Send professional invoices in 60 seconds.",
  "image": "https://yoursite.com/images/og-invoice-app.jpg",
  "brand": {
    "@type": "Brand",
    "name": "InvoiceApp"
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "0",
    "priceValidUntil": "2027-01-01",
    "availability": "https://schema.org/InStock",
    "url": "https://yoursite.com/pricing"
  }
}
</script>
```

Place the `<script>` block anywhere inside `<head>` or at the bottom of `<body>`.

## Verify

Run the Rich Results Test against your live page URL:

```
https://search.google.com/test/rich-results?url=https://yoursite.com/your-page
```

Pass criteria:
- No **Errors** listed (warnings are acceptable for initial publish).
- At least one detected item type (Article or Product) shown in the results panel.

Then check title and meta description length from the terminal:
```bash
curl -s https://yoursite.com/your-page \
  | python3 -c "
import sys, re
html = sys.stdin.read()
title = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
desc = re.search(r'<meta[^>]+name=[\"\\x27]description[\"\\x27][^>]+content=[\"\\x27]([^\"\\x27]+)', html)
print('Title length:', len(title.group(1).strip()) if title else 'NOT FOUND')
print('Desc length :', len(desc.group(1).strip()) if desc else 'NOT FOUND')
"
```

Target output: `Title length: ≤60` and `Desc length: ≤160`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Rich Results Test shows "No items detected" | JSON-LD block has a syntax error or is missing a required field | Paste the JSON block into https://jsonlint.com; fix the error; re-test |
| Google rewrites the title tag in SERPs | Title exceeds 60 chars or does not match page content | Shorten to ≤60 chars and align title wording with the H1 |
| OG image not showing when link is shared on Slack/LinkedIn | OG image URL is relative instead of absolute, or the image is behind login | Use an absolute URL (`https://`) and confirm the image loads in a private browser window |
| Multiple H1 tags found after CMS template update | CMS injects a default H1 in a sidebar or hero component alongside your post H1 | Inspect the DOM with DevTools → Elements → search `<h1`; remove or demote the duplicate to H2 |
| `curl` shows `<main>` is missing | Legacy page template uses only `<div id="main">` | Replace the wrapper `<div>` with `<main>`; update any CSS selectors accordingly |
| Schema.org "datePublished" triggers a warning | Date is in wrong format or missing | Use ISO 8601 format: `"2026-05-01"` (full date, no time component required) |

## Next

- Run `technical-seo-audit` to verify crawlability before optimising individual pages — on-page signals only matter if Googlebot can index the page.
- `content-audit-and-pruning` — after optimising key pages, remove or merge thin pages that dilute overall site quality.
- Upgrade to [knowledge/solo/marketing/seo-manager/topical-authority](../../../knowledge/solo/marketing/seo-manager/topical-authority) to build a cluster of related pages that reinforces the primary page's rankings.

## References

- [knowledge/solo/marketing/seo-manager/seo-basics](../../../knowledge/solo/marketing/seo-manager/seo-basics) — provides the crawlability and indexability model that explains why title tags and meta descriptions are read before body content, directly underpinning Steps 2–3.
- [knowledge/solo/marketing/seo-manager/seo-techniques](../../../knowledge/solo/marketing/seo-manager/seo-techniques) — covers semantic HTML structure and heading hierarchy optimisation applied in Steps 5–6, and structured data markup patterns applied in Step 8.
- [knowledge/solo/marketing/seo-manager/seo](../../../knowledge/solo/marketing/seo-manager/seo) — grounds the OG image and JSON-LD requirements (Steps 7–8) in the broader on-page signal model for solo-tier sites.
