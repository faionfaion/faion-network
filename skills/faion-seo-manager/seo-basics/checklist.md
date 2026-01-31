# SEO Basics Setup Checklist

## Phase 1: Technical Foundation

### robots.txt Setup
- [ ] Create/review robots.txt file
- [ ] Block admin and internal API paths
- [ ] Allow important pages and assets
- [ ] Block session ID and tracking parameters
- [ ] Add sitemap directive
- [ ] Test in Google Search Console
- [ ] Deploy and verify

### XML Sitemap Implementation
- [ ] Create XML sitemap or use plugin
- [ ] Include all important pages
- [ ] Set correct lastmod dates
- [ ] Set appropriate priority levels
- [ ] Include hreflang for multilingual (if applicable)
- [ ] Test sitemap syntax
- [ ] Submit to Google Search Console
- [ ] Submit to Bing Webmaster Tools

### HTTPS & Security
- [ ] Ensure SSL certificate installed
- [ ] Test for mixed content (HTTP resources on HTTPS page)
- [ ] Configure security headers
- [ ] Set up redirects from HTTP → HTTPS
- [ ] Test in browser (padlock icon)
- [ ] Update robots.txt and sitemap to HTTPS

## Phase 2: Semantic HTML & Accessibility

### Semantic Markup
- [ ] Use proper HTML structure (header, main, footer, article)
- [ ] Implement single H1 per page
- [ ] Create logical heading hierarchy (H1 → H2 → H3)
- [ ] Use semantic elements (article, section, aside)
- [ ] Add ARIA labels where needed
- [ ] Remove divitis (excessive divs)
- [ ] Test with HTML validator

### Image Optimization
- [ ] Add descriptive alt text to all images
- [ ] Mark decorative images as alt=""
- [ ] Compress images (WebP/AVIF formats)
- [ ] Add width and height attributes
- [ ] Implement lazy loading for below-fold images
- [ ] Use descriptive filenames (not "image-1.png")
- [ ] Create image sitemap (optional)

### Accessibility Compliance
- [ ] Ensure minimum 4.5:1 color contrast ratio
- [ ] Make all interactive elements keyboard accessible
- [ ] Test with screen reader (NVDA, JAWS)
- [ ] Verify form labels are associated with inputs
- [ ] Test with accessibility tool (WAVE, Axe)
- [ ] Fix WCAG 2.2 level A violations

## Phase 3: Multilingual SEO (if applicable)

### URL Structure
- [ ] Choose URL strategy: subdirectories (/en/, /uk/) recommended
- [ ] Implement hreflang tags
- [ ] Self-reference each language version
- [ ] Use ISO 639-1 language codes
- [ ] Ensure bidirectional hreflang linking
- [ ] Include x-default for regional targeting

### Metadata Localization
- [ ] Translate title tags (not keyword stuffing)
- [ ] Translate meta descriptions
- [ ] Ensure metadata matches page language
- [ ] Create language switcher on site
- [ ] Test hreflang with Google Search Console

## Phase 4: Core Web Vitals Optimization

### LCP (Largest Contentful Paint) < 2.5s
- [ ] Identify LCP element
- [ ] Preload critical images
- [ ] Convert to WebP/AVIF formats
- [ ] Optimize image size (responsive images)
- [ ] Defer non-critical CSS
- [ ] Optimize server response time (TTFB < 800ms)
- [ ] Use CDN for static assets
- [ ] Test in PageSpeed Insights

### INP (Interaction to Next Paint) < 200ms
- [ ] Profile with Chrome DevTools
- [ ] Break up long JavaScript tasks (< 50ms)
- [ ] Defer non-critical JavaScript
- [ ] Move heavy work to Web Workers
- [ ] Use requestIdleCallback for low-priority tasks
- [ ] Minimize event listener overhead
- [ ] Test with Web Vitals extension

### CLS (Cumulative Layout Shift) < 0.1
- [ ] Add width/height to all images
- [ ] Reserve space for ads and embeds
- [ ] Avoid inserting content above existing content
- [ ] Use font-display: swap for custom fonts
- [ ] Preload fonts to avoid layout shift
- [ ] Fix animations that cause layout shifts
- [ ] Test in Lighthouse

## Phase 5: Mobile Optimization

### Mobile Responsiveness
- [ ] Test on various device sizes (mobile-first approach)
- [ ] Verify readable text without zoom
- [ ] Ensure proper tap target spacing (48x48px minimum)
- [ ] Remove Flash or plugins
- [ ] Test with mobile-friendly test tool
- [ ] Check viewport meta tag set correctly

### Mobile Performance
- [ ] Optimize for slower 4G speeds
- [ ] Reduce JavaScript for mobile
- [ ] Implement adaptive loading
- [ ] Test with mobile PageSpeed Insights
- [ ] Monitor mobile Core Web Vitals

## Phase 6: Meta Tags & Markup

### Essential Meta Tags
- [ ] Charset declaration (UTF-8)
- [ ] Viewport meta tag (mobile responsive)
- [ ] Title tag (50-60 chars, primary keyword)
- [ ] Meta description (120-160 chars, compelling)
- [ ] Canonical tag (self-referencing)
- [ ] Robots meta tag (if restricting indexing)
- [ ] Open Graph tags (social sharing)
- [ ] Twitter Card tags

### Schema.org Markup
- [ ] Add Organization schema
- [ ] Add Article/NewsArticle schema (for blog)
- [ ] Add BreadcrumbList schema (navigation)
- [ ] Add local business schema (if applicable)
- [ ] Add Product schema (e-commerce pages)
- [ ] Test with Rich Results Test tool
- [ ] Validate with schema.org validator

## Phase 7: Analytics & Monitoring

### Google Search Console
- [ ] Verify domain ownership
- [ ] Submit sitemap
- [ ] Set preferred domain
- [ ] Monitor indexing status
- [ ] Review Core Web Vitals
- [ ] Check for manual actions
- [ ] Monitor coverage errors
- [ ] Track search performance

### Google Analytics 4
- [ ] Create GA4 property
- [ ] Install GA4 tracking code
- [ ] Set up conversion tracking
- [ ] Configure custom events
- [ ] Link to Google Search Console
- [ ] Create custom reports for organic traffic
- [ ] Set up audience segments

### Ongoing Monitoring
- [ ] Monitor crawl stats in Search Console
- [ ] Track Core Web Vitals
- [ ] Monitor indexing (site:domain.com)
- [ ] Check for crawl errors
- [ ] Review AMP issues (if applicable)
- [ ] Monitor mobile usability issues

## Phase 8: Launch Checklist

### Pre-Launch Testing
- [ ] All pages load without errors
- [ ] Links are working (internal and external)
- [ ] Forms are functioning
- [ ] HTTPS working properly
- [ ] Robots.txt and sitemap deployed
- [ ] Redirects working (if redesign)
- [ ] Analytics tracking firing

### Post-Launch
- [ ] Submit sitemap to Search Console
- [ ] Submit sitemap to Bing Webmaster
- [ ] Monitor Google Analytics
- [ ] Monitor Search Console
- [ ] Check Core Web Vitals
- [ ] Monitor for crawl errors
- [ ] Verify indexing after 1-2 weeks
