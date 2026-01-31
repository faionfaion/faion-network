# SEO & AEO Mastery Checklist

## Phase 1: Technical Foundation

### Core SEO Setup
- [ ] robots.txt configured and tested
- [ ] XML sitemap created and submitted
- [ ] HTTPS enabled on entire domain
- [ ] Domain redirects (HTTP → HTTPS, www/non-www)
- [ ] Google Search Console verified
- [ ] Bing Webmaster Tools verified
- [ ] Analytics configured (GA4)

### Performance Optimization
- [ ] LCP < 2.5s (test in PageSpeed Insights)
- [ ] INP < 200ms (test with Web Vitals extension)
- [ ] CLS < 0.1 (monitor in Lighthouse)
- [ ] Mobile-friendly verified
- [ ] Images optimized (WebP/AVIF)
- [ ] JavaScript deferred/minimized
- [ ] CSS deferred/minimized
- [ ] CDN configured for static assets

## Phase 2: On-Page Optimization

### Content Structure
- [ ] Single H1 per page with primary keyword
- [ ] Logical H2-H6 hierarchy
- [ ] Proper semantic HTML structure
- [ ] Meta tags optimized (title, description)
- [ ] Canonical tags implemented
- [ ] Internal links strategy mapped
- [ ] External links to authoritative sources

### Accessibility & User Experience
- [ ] WCAG 2.2 Level A compliance
- [ ] Color contrast 4.5:1 minimum
- [ ] All images have alt text
- [ ] Form labels associated with inputs
- [ ] Keyboard navigation functional
- [ ] ARIA labels added where needed
- [ ] Tested with screen reader

## Phase 3: AI Search Optimization (AEO)

### llms.txt Implementation
- [ ] Create /llms.txt file at root
- [ ] Define core pages to be crawled
- [ ] Exclude premium/paywalled content
- [ ] Specify citation format preferences
- [ ] Mark important pages for crawlers
- [ ] Update as site changes

### Schema Markup for AI
- [ ] Organization schema implemented
- [ ] Article schema on blog posts
- [ ] Author/expert credentials marked
- [ ] Publication dates structured
- [ ] Entity mentions optimized
- [ ] BreadcrumbList for navigation
- [ ] Product schema (if applicable)

### Entity Optimization for LLMs
- [ ] Key entities clearly defined in first paragraph
- [ ] Entity mentions consistent across pages
- [ ] Related entities cross-linked
- [ ] Entity descriptions comprehensive
- [ ] Author expertise/credentials visible
- [ ] Source citations clear

## Phase 4: Multilingual SEO

### hreflang Implementation
- [ ] URL structure chosen (/en/, /uk/ recommended)
- [ ] Hreflang tags on all pages
- [ ] Self-referencing hreflang on each version
- [ ] Bidirectional hreflang linking
- [ ] x-default specified
- [ ] ISO 639-1 codes used (en, uk, de)
- [ ] Sitemap includes hreflang

### Metadata Localization
- [ ] Title tags translated
- [ ] Meta descriptions translated
- [ ] Content in correct language
- [ ] Language switcher prominent
- [ ] Metadata matches page language
- [ ] Tested in Search Console

## Phase 5: Social Sharing Optimization

### Open Graph Tags
- [ ] og:title on all pages
- [ ] og:description on all pages
- [ ] og:image on all pages (1200x630px)
- [ ] og:url specified
- [ ] og:type set correctly
- [ ] og:locale for multilingual

### Twitter Cards
- [ ] twitter:card specified
- [ ] twitter:title on key pages
- [ ] twitter:description on key pages
- [ ] twitter:image on key pages
- [ ] twitter:creator if author
- [ ] Twitter card validated

### LinkedIn Meta Tags
- [ ] Company name specified
- [ ] Business category defined
- [ ] Logo/image for sharing
- [ ] Description optimized
- [ ] Keywords relevant

## Phase 6: Advanced Schema Markup

### Essential Schema
- [ ] Organization (global)
- [ ] Article/NewsArticle (blog posts)
- [ ] BreadcrumbList (navigation)
- [ ] LocalBusiness (if applicable)
- [ ] Product (e-commerce)
- [ ] Person (author pages)
- [ ] FAQPage (FAQ content)

### Schema Validation
- [ ] Valid JSON-LD syntax
- [ ] No schema validation errors
- [ ] Rich Results Test passing
- [ ] Multiple schema types working together
- [ ] Tested in Google Search Console

## Phase 7: Crawlability & Indexing

### Crawl Optimization
- [ ] robots.txt allows important pages
- [ ] No important pages blocked
- [ ] Crawl budget optimized (no infinite crawls)
- [ ] Parameter handling configured
- [ ] URL canonicalization proper
- [ ] Redirect chains avoided

### Indexing Management
- [ ] Important pages indexed (site:domain.com)
- [ ] No duplicate content issues
- [ ] noindex used only where appropriate
- [ ] Nofollow links minimal and justified
- [ ] Mobile-first indexing enabled
- [ ] Indexed pages monitored monthly

## Phase 8: Core Web Vitals Maintenance

### LCP (Largest Contentful Paint)
- [ ] Preload critical images
- [ ] WebP/AVIF image formats used
- [ ] Responsive images (srcset)
- [ ] Image lazy loading configured
- [ ] Server response time < 800ms
- [ ] Critical CSS inlined
- [ ] Non-critical resources deferred

### INP (Interaction to Next Paint)
- [ ] Event listeners optimized
- [ ] No JavaScript long tasks (>50ms)
- [ ] Non-critical JS deferred
- [ ] Main thread not blocked
- [ ] Web Worker used for heavy computation
- [ ] requestIdleCallback for non-critical work

### CLS (Cumulative Layout Shift)
- [ ] Width/height on all images
- [ ] Space reserved for ads/embeds
- [ ] No content insertion above existing
- [ ] font-display: swap on custom fonts
- [ ] Fonts preloaded
- [ ] No animation-induced shifts

## Phase 9: Monitoring & Reporting

### Monthly Audit
- [ ] Core Web Vitals status
- [ ] Search Console coverage
- [ ] Indexing status
- [ ] Ranking position changes
- [ ] Backlink growth
- [ ] Traffic trends

### Quarterly Review
- [ ] SEO audit with tool (Ahrefs, Semrush)
- [ ] Competitor analysis
- [ ] Technical debt assessment
- [ ] Content gaps analysis
- [ ] Strategy adjustment
- [ ] Roadmap update

## Phase 10: Documentation & Maintenance

### SEO Documentation
- [ ] SEO guidelines documented
- [ ] Schema markup templates
- [ ] Testing procedures documented
- [ ] Tools and access list
- [ ] Keyword target list
- [ ] Monthly reporting template

### Ongoing Maintenance
- [ ] Monitor Search Console daily
- [ ] Review Core Web Vitals weekly
- [ ] Respond to indexing issues
- [ ] Update outdated content
- [ ] Remove redundant pages
- [ ] Fix broken links monthly
