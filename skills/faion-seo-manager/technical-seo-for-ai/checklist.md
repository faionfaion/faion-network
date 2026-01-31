# Technical SEO for AI Checklist

## Phase 1: AI Crawler Fundamentals

### AI Crawler Management
- [ ] Identify AI crawlers: GPTBot, Claude-Web, PerplexityBot, etc.
- [ ] Configure separate rules for AI crawlers in robots.txt
- [ ] Allow/disallow public content appropriately
- [ ] Block premium/paywalled content from AI crawlers
- [ ] Create llms.txt for AI guidance
- [ ] Monitor AI crawler access patterns
- [ ] Analyze AI crawler behavior

### URL Structure for AI
- [ ] Use clean, descriptive URLs (not hash-based)
- [ ] Avoid session IDs in URLs
- [ ] Use hyphens in URLs (not underscores)
- [ ] Keep URLs under 100 characters
- [ ] Avoid dynamic parameters where possible
- [ ] Use consistent URL patterns
- [ ] Test URL structure with AI crawlers

## Phase 2: Content Structure for AI

### Semantic HTML for AI Extraction
- [ ] Single H1 per page describing main topic
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Clear topic introduction in first paragraph
- [ ] Concise answers near relevant headings
- [ ] Logical content sections
- [ ] Related topics clearly marked

### Entity Clarity
- [ ] Define main entity in opening (who/what is this about?)
- [ ] Use consistent entity naming throughout
- [ ] Link to entity pages when relevant
- [ ] Define entity relationships explicitly
- [ ] Include entity attributes clearly
- [ ] Mark entity properties with schema

### Factual Content Structure
- [ ] Statistics with sources cited
- [ ] Dates on all time-sensitive information
- [ ] Author credentials explicitly stated
- [ ] Source attribution for claims
- [ ] Data presented clearly (tables/lists)
- [ ] No contradictory information
- [ ] Verifiable facts only

## Phase 3: Schema Implementation for AI

### AI-Optimized Schema
- [ ] Article schema with author and date
- [ ] Author schema with credentials
- [ ] Organization schema
- [ ] BreadcrumbList for topic hierarchy
- [ ] FAQSchema for Q&A content
- [ ] Schema with proper nesting
- [ ] No conflicting schema types

### Author & Authority Markup
- [ ] Author name explicitly stated
- [ ] Author credentials and expertise
- [ ] Author bio or credentials page
- [ ] Author email/contact (optional)
- [ ] Publication date (datePublished)
- [ ] Last modified date (dateModified)
- [ ] Creator/publisher information

### Entity Schema
- [ ] Main entity clearly identified
- [ ] Entity type appropriate (Article, NewsArticle, etc.)
- [ ] Entity relationships defined
- [ ] Related entities linked
- [ ] Entity properties complete
- [ ] Property values accurate

## Phase 4: llms.txt Implementation

### File Creation & Structure
- [ ] Create /llms.txt at domain root
- [ ] List domain name and description
- [ ] Include core pages (about, contact, etc.)
- [ ] List main products/services
- [ ] Provide documentation links
- [ ] Include exclusions (admin, premium)
- [ ] Specify citation format preferences

### Content Guidelines in llms.txt
- [ ] Crawl permissions explicit
- [ ] Important pages marked
- [ ] Content quality guidelines
- [ ] Citation format specified
- [ ] Accuracy requirements
- [ ] Freshness expectations
- [ ] Attribution requirements

### Maintenance
- [ ] Update llms.txt when content changes
- [ ] Add new important sections
- [ ] Remove outdated pages
- [ ] Review quarterly
- [ ] Monitor AI crawler compliance
- [ ] Adjust rules as needed

## Phase 5: Content Freshness for AI

### Update Strategy
- [ ] Identify time-sensitive content
- [ ] Set update frequency targets
- [ ] Create content refresh schedule
- [ ] Flag outdated information
- [ ] Update statistics/data regularly
- [ ] Change "last modified" dates
- [ ] Archive outdated versions

### Fact Verification
- [ ] Verify all claims are accurate
- [ ] Check statistics still current
- [ ] Update research/studies
- [ ] Verify expert credentials
- [ ] Check link viability
- [ ] Validate data accuracy
- [ ] No misleading information

### Update Monitoring
- [ ] Track content age (Google Search Console)
- [ ] Monitor freshness signals
- [ ] Analyze update frequency impact
- [ ] Update 30+ days old content
- [ ] Test impact on AI citations
- [ ] Measure ranking improvements

## Phase 6: Performance for AI

### Loading Speed Optimization
- [ ] LCP < 2.5s (Largest Contentful Paint)
- [ ] INP < 200ms (Interaction to Next Paint)
- [ ] CLS < 0.1 (Cumulative Layout Shift)
- [ ] TTFB < 800ms (Time to First Byte)
- [ ] Images optimized (WebP/AVIF)
- [ ] JavaScript deferred
- [ ] CSS optimized

### Mobile Performance
- [ ] Mobile-first design approach
- [ ] Responsive images
- [ ] Fast mobile loading
- [ ] Touch-friendly interface
- [ ] Mobile readability
- [ ] Mobile crawlability

### Accessibility for AI
- [ ] Proper HTML structure
- [ ] Semantic markup
- [ ] Images with alt text
- [ ] Links descriptive
- [ ] Keyboard navigation
- [ ] No JavaScript-only content
- [ ] Screen reader friendly

## Phase 7: Authority & Trust Signals

### Author Credentials
- [ ] Author expertise documented
- [ ] Credentials visible on page
- [ ] Author bio/profile link
- [ ] Author track record
- [ ] Third-party author verification
- [ ] Staff/team credentials
- [ ] Expert qualifications

### Trust Signals
- [ ] HTTPS enabled
- [ ] Privacy policy present
- [ ] Contact information visible
- [ ] Company background
- [ ] User reviews/testimonials
- [ ] Third-party certifications
- [ ] Security badges

### Citation Network
- [ ] Link to authoritative sources
- [ ] Cite recent studies/research
- [ ] Link to primary sources
- [ ] Mention reputable organizations
- [ ] Include relevant entity mentions
- [ ] Build topical authority

## Phase 8: Monitoring & Optimization

### AI Citation Tracking
- [ ] Monitor AI Overview citations
- [ ] Track Perplexity mentions
- [ ] Monitor Claude usage
- [ ] Track ChatGPT references
- [ ] Analyze citation patterns
- [ ] Identify high-performing content
- [ ] Optimize underperforming pages

### Performance Metrics
- [ ] Track AI-generated traffic (if available)
- [ ] Monitor ranking positions
- [ ] Track keyword rankings
- [ ] Monitor backlink growth
- [ ] Track brand mentions
- [ ] Measure AI citations
- [ ] Analyze AI-sourced traffic

### Continuous Improvement
- [ ] Audit AI-unfriendly content
- [ ] Update underperforming pages
- [ ] Improve schema markup
- [ ] Enhance content clarity
- [ ] Update outdated information
- [ ] Expand authoritative content
- [ ] Test new AI optimization tactics
