# Technical SEO Reference

## robots.txt Deep Dive

### Syntax

```txt
User-agent: *           # Applies to all crawlers
Disallow: /private/     # Block this directory
Allow: /private/public/ # But allow this subdirectory
Crawl-delay: 10         # Wait 10 seconds between requests (not Google)

User-agent: Googlebot
Disallow: /tmp/

Sitemap: https://example.com/sitemap.xml
```

### AI Crawler User-Agents (2025)

| Bot | User-Agent | Company |
|-----|------------|---------|
| GPTBot | `GPTBot` | OpenAI |
| ChatGPT-User | `ChatGPT-User` | OpenAI (browsing) |
| Google-Extended | `Google-Extended` | Google (AI training) |
| Claude-Web | `Claude-Web` | Anthropic |
| PerplexityBot | `PerplexityBot` | Perplexity AI |
| Bytespider | `Bytespider` | ByteDance |
| CCBot | `CCBot` | Common Crawl |

### Managing AI Crawlers

```txt
# Allow AI to read, but block training data
User-agent: GPTBot
Allow: /
Disallow: /premium/

User-agent: Google-Extended
Disallow: /  # Block AI training but allow Search

User-agent: CCBot
Disallow: /  # Block Common Crawl (dataset)
```

### What to Block

| Block | Why |
|-------|-----|
| `/admin/`, `/wp-admin/` | Admin panels |
| `/cart/`, `/checkout/` | Transactional pages |
| `/*?sessionid=` | Session URLs |
| `/*?sort=`, `/*?filter=` | Faceted navigation |
| `/search/` | Internal search results |
| `/tag/`, `/author/` | Thin taxonomy pages (optional) |
| `/*.pdf` | PDFs if duplicate content |

### What NOT to Block

- CSS and JavaScript files
- Images (unless you want them hidden)
- Your main content pages
- API endpoints that power your frontend

---

## XML Sitemaps

### Sitemap Index (for large sites)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-pages.xml</loc>
    <lastmod>2026-01-18</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-posts.xml</loc>
    <lastmod>2026-01-18</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-products.xml</loc>
    <lastmod>2026-01-17</lastmod>
  </sitemap>
</sitemapindex>
```

### Priority Values

| Page Type | Priority |
|-----------|----------|
| Homepage | 1.0 |
| Main categories | 0.8 |
| Key landing pages | 0.8 |
| Blog posts | 0.6 |
| Product pages | 0.6 |
| Tag/archive pages | 0.3 |

### Video Sitemap Extension

```xml
<url>
  <loc>https://example.com/video-page/</loc>
  <video:video>
    <video:thumbnail_loc>https://example.com/thumb.jpg</video:thumbnail_loc>
    <video:title>Video Title</video:title>
    <video:description>Description...</video:description>
    <video:content_loc>https://example.com/video.mp4</video:content_loc>
    <video:duration>600</video:duration>
  </video:video>
</url>
```

### Image Sitemap Extension

```xml
<url>
  <loc>https://example.com/page/</loc>
  <image:image>
    <image:loc>https://example.com/image.jpg</image:loc>
    <image:title>Image Title</image:title>
    <image:caption>Description of image</image:caption>
  </image:image>
</url>
```

---

## Crawl Budget Optimization

### What Affects Crawl Budget

| Factor | Impact |
|--------|--------|
| Site size | More pages = less frequent crawls per page |
| Page importance | Popular pages crawled more |
| Freshness | Frequently updated = more crawls |
| Server speed | Slow = fewer crawls |
| Crawl errors | Many errors = reduced crawling |

### Optimization Strategies

1. **Block low-value pages** in robots.txt
2. **Fix crawl errors** immediately
3. **Improve server response time** (< 200ms)
4. **Use internal linking** to signal important pages
5. **Update sitemap** when content changes
6. **Remove duplicate content** or use canonicals
7. **Reduce redirect chains** (max 1 hop)

---

## Canonical Tags

### Usage

```html
<!-- On the preferred version -->
<link rel="canonical" href="https://example.com/preferred-page/" />

<!-- On duplicate versions (with params, www, etc.) -->
<link rel="canonical" href="https://example.com/preferred-page/" />
```

### When to Use

| Scenario | Canonical Points To |
|----------|---------------------|
| HTTP vs HTTPS | HTTPS version |
| www vs non-www | Preferred version |
| Trailing slash variants | Preferred version |
| URL parameters (tracking, sorting) | Clean URL |
| Paginated content | Page 1 or self |
| Syndicated content | Original source |
| Mobile vs Desktop | Desktop (with proper mobile setup) |

### Common Mistakes

- Canonical pointing to 404 page
- Canonical pointing to redirected URL
- Multiple canonical tags on same page
- Canonical on noindex page
- Relative URLs instead of absolute

---

## Redirects

### Types

| Code | Type | Use Case |
|------|------|----------|
| 301 | Permanent | URL changed forever, pass full SEO value |
| 302 | Temporary | Temporary move, testing |
| 307 | Temporary (strict) | Same as 302, preserves method |
| 308 | Permanent (strict) | Same as 301, preserves method |

### Best Practices

1. **Use 301 for permanent changes** - passes ~90-99% of link equity
2. **Avoid redirect chains** - each hop loses equity
3. **Update internal links** - don't rely on redirects
4. **Monitor in Search Console** - check for redirect errors
5. **Keep redirects for at least 1 year** - ensures full value transfer

### Redirect Implementation

```nginx
# Nginx
server {
    # Single redirect
    rewrite ^/old-page/$ /new-page/ permanent;

    # Pattern redirect
    rewrite ^/blog/(\d+)/(.*)$ /articles/$2 permanent;

    # Force HTTPS
    if ($scheme != "https") {
        return 301 https://$host$request_uri;
    }
}
```

```apache
# Apache .htaccess
Redirect 301 /old-page/ /new-page/
RedirectMatch 301 ^/blog/([0-9]+)/(.*)$ /articles/$2

# Force HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```
