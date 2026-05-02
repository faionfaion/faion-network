---
name: technical-seo-audit
description: Run a 12-point technical SEO audit of your site using only free tools and fix critical issues before they suppress rankings.
tier: solo
group: seo-essentials
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have completed a 12-point technical SEO audit of your site — crawl errors found, sitemap validated, Core Web Vitals scored, robots.txt verified, and a prioritised fix list — using only free tools (Google Search Console, PageSpeed Insights, Screaming Frog free tier, and direct URL checks). No agency, no paid subscription.

## Prerequisites

- Your site is live and indexed (at least one URL appears in Google Search).
- Google Search Console property verified for your domain (e.g. `yourdomain.com`).
- Screaming Frog SEO Spider installed: https://www.screamingfrog.co.uk/seo-spider/ (free tier: up to 500 URLs).
- Python 3.x available (for the optional `sitemap-check` step).
- Access to `robots.txt` and `sitemap.xml` on your server or CMS.

## Steps

### 1. Connect Google Search Console and collect baseline data

1. Open https://search.google.com/search-console/ and select your property.
2. Navigate to **Coverage** (or **Indexing → Pages** in the new UI). Note the count of:
   - Valid pages
   - Excluded pages (check "Crawled - currently not indexed" and "Discovered - currently not indexed")
   - Errors (e.g. 404, redirect errors, server errors)
3. Export the error list: click the error type → **Export** → CSV. Save as `gsc-errors.csv`.
4. Navigate to **Core Web Vitals** and note whether mobile/desktop pass or fail.

### 2. Verify robots.txt allows crawling

Open your `robots.txt` directly in a browser:

```
https://yourdomain.com/robots.txt
```

Check that:
- No `Disallow: /` rule blocks Googlebot (or all bots).
- The `Sitemap:` directive points to your sitemap URL.

Test a specific URL using Google Search Console: **Settings → robots.txt Tester**.

Common fix: if a staging rule like `Disallow: /` was accidentally left in production, remove it and redeploy.

### 3. Validate your sitemap.xml

Fetch the sitemap directly:

```bash
curl -s https://yourdomain.com/sitemap.xml | python3 -c "
import sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.stdin)
root = tree.getroot()
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = root.findall('.//sm:loc', ns)
print(f'URLs found: {len(urls)}')
for u in urls[:5]:
    print(' ', u.text)
"
```

Then submit/refresh in Google Search Console: **Sitemaps → Enter sitemap URL → Submit**.

Verify the sitemap has no pending errors (GSC shows "Success" and a non-zero URL count).

### 4. Crawl the site with Screaming Frog (free tier ≤500 URLs)

1. Open Screaming Frog → **File → Configuration → Spider** — enable "Crawl all subdomains", disable JavaScript rendering (for a fast first pass).
2. Enter `https://yourdomain.com` in the URL bar and press Start.
3. After crawl, check these tabs:
   - **Response Codes → 4xx** — collect broken internal links.
   - **Response Codes → 3xx** — check redirect chains longer than 1 hop.
   - **Page Titles → Missing / Duplicate** — pages with blank or repeated `<title>` tags.
   - **Meta Description → Missing / Duplicate**.
   - **H1 → Missing / Multiple**.
   - **Images → Missing Alt Text**.
4. Export each problem tab: **Export** → CSV.

### 5. Check for duplicate content and canonical tags

In Screaming Frog → **Directives → Canonicals**:
- Look for pages with `rel=canonical` pointing to a different URL (signal of intentional deduplication).
- Look for pages with NO canonical (potential duplicate risk).

Also verify that HTTP redirects to HTTPS:

```bash
curl -I http://yourdomain.com/ | grep -i location
```

Expected output: `Location: https://yourdomain.com/` (301 or 308).

### 6. Audit Core Web Vitals with PageSpeed Insights

Run for your homepage and your most-visited content page:

```bash
# Replace <URL> with the full page URL
open "https://pagespeed.web.dev/report?url=https%3A%2F%2Fyourdomain.com%2F"
```

Note the three field metrics: LCP (target <2.5 s), INP (target <200 ms), CLS (target <0.1).

For any failing metric, expand the **Opportunities** and **Diagnostics** sections and copy the top two recommendations into your fix list.

### 7. Check mobile-friendliness

Open Google's Mobile-Friendly Test:

```
https://search.google.com/test/mobile-friendly?url=https://yourdomain.com
```

If it fails, the test names the specific issues (viewport meta tag missing, tap targets too small, text too small to read). Fix each one.

### 8. Verify HTTPS and mixed-content

```bash
curl -sv https://yourdomain.com/ 2>&1 | grep -E "SSL|TLS|certificate|ALPN"
```

In a browser: open DevTools → **Console** — look for "Mixed Content" warnings (HTTP sub-resources on an HTTPS page). Fix by changing asset URLs to relative or HTTPS.

### 9. Check structured data (if applicable)

If your site has articles, products, or FAQs, test one URL:

```
https://search.google.com/test/rich-results?url=https://yourdomain.com/your-page
```

Errors here prevent rich snippets. Fix by correcting the JSON-LD block or missing required fields.

### 10. Audit hreflang (multi-language sites only)

Skip this step if your site is single-language.

In Screaming Frog → **Hreflang**:
- **Missing return tag** — page A links to page B in hreflang, but B does not link back to A.
- **Incorrect language code** — e.g. `uk` (Ukrainian) vs `en-gb`.
- **Non-canonical hreflang** — hreflang pointing to a URL that itself canonicals elsewhere.

Manual check for a specific page:

```bash
curl -s https://yourdomain.com/your-page | grep -i hreflang
```

### 11. Review crawl budget (large sites only)

Skip for sites under 200 pages.

In Google Search Console → **Settings → Crawl Stats**:
- Check **Total crawl requests** trend (should be stable or growing).
- Check **Response codes** breakdown — any spike in 4xx consumes budget without benefit.

Remove low-value pages (tag archives, parameter URLs) from the sitemap and add `<meta name="robots" content="noindex">` or block in `robots.txt`.

### 12. Compile the fix list and prioritise

Create a local `seo-audit-YYYY-MM-DD.md` file with three sections:

```markdown
## Critical (ranking impact)
- [ ] Fix 404 broken links found in Screaming Frog (list URLs from 4xx export)
- [ ] Remove robots.txt Disallow blocking key pages (if found in Step 2)
- [ ] Fix LCP > 4s pages (see PageSpeed report)

## Important (trust and coverage)
- [ ] Add missing canonical tags to duplicated content pages
- [ ] Submit corrected sitemap (after removing noindex pages from it)
- [ ] Fix mixed-content HTTPS warnings

## Nice to have
- [ ] Add missing meta descriptions (Screaming Frog export)
- [ ] Add alt text to images (Screaming Frog export)
- [ ] Fix hreflang return tags (if multilang)
```

## Verify

Run the Screaming Frog re-crawl after applying fixes. The 4xx Response Codes tab should return 0 rows. Confirm in Google Search Console → Coverage that the error count has decreased within 3–7 days of GSC re-crawling:

```bash
# Quick CLI check: confirm no internal 404s from your homepage
curl -s https://yourdomain.com/ | grep -oP 'href="[^"]*"' | grep -v "^http" | head -20
```

Then validate the top five internal links return 200:

```bash
for path in /about /blog /pricing /contact /features; do
  code=$(curl -o /dev/null -sw "%{http_code}" https://yourdomain.com${path})
  echo "$code https://yourdomain.com${path}"
done
```

All lines should print `200`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Screaming Frog crawls only 1 URL then stops | JavaScript-only navigation with no static links | Enable JS rendering in Screaming Frog → Configuration → Spider → Rendering: AJAX (slower but discovers JS routes) |
| GSC Coverage shows thousands of "Discovered - currently not indexed" | Crawl budget exhausted or pages low-quality | Remove thin/duplicate pages from sitemap; add `noindex` to tag/archive pages; wait 2 weeks for GSC to re-crawl |
| PageSpeed LCP > 4s but images look small | LCP element is a hero background-image set in CSS, not an `<img>` tag | Add `<link rel="preload" as="image">` for the hero image in `<head>` and switch to `<img>` with `fetchpriority="high"` |
| `curl robots.txt` shows correct rules but GSC Tester blocks a URL | Whitespace or encoding issue in `robots.txt` (Windows line endings `\r\n`) | Re-save `robots.txt` with Unix line endings: `sed -i 's/\r//' robots.txt` then redeploy |
| hreflang validation shows "missing return tag" | CMS generates hreflang only on pages it knows about; new pages miss the reciprocal tag | Run the Screaming Frog hreflang audit after every content publish cycle; or use a plugin that auto-generates return tags |
| Structured data test returns "Missing required field: name" | JSON-LD block generated by CMS omits a field Google now requires | Add the missing field directly in your CMS template or theme; re-test after deploy |

## Next

- Run this audit quarterly and compare the fix list to the previous one to track improvement velocity.
- `content-audit-and-pruning` — after fixing technical issues, prune thin content that drags down crawl quality.
- Upgrade to the [knowledge/solo/marketing/seo-manager/growth-seo-fundamentals](../../../knowledge/solo/marketing/seo-manager/growth-seo-fundamentals) methodology once technical health is stable, to layer on link-building and topical authority work.

## References

- [knowledge/solo/marketing/seo-manager/seo-basics](../../../knowledge/solo/marketing/seo-manager/seo-basics) — provides the foundational model for crawlability, indexability, and ranking signals that underlies the 12 checkpoints in Steps 1–11 of this audit.
- [knowledge/solo/marketing/seo-manager/seo-techniques](../../../knowledge/solo/marketing/seo-manager/seo-techniques) — covers Core Web Vitals optimisation patterns and canonical strategy applied in Steps 5–6 of this audit.
- [knowledge/solo/marketing/seo-manager/growth-seo-fundamentals](../../../knowledge/solo/marketing/seo-manager/growth-seo-fundamentals) — frames the crawl-budget and topical authority logic behind Step 11 (crawl budget review) and the prioritisation hierarchy in Step 12.
