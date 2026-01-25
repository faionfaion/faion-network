# Marketing Workflows

Standard workflows and processes for the Marketing Manager skill.

---

## 1. GTM Manifest Creation

**Purpose:** Create comprehensive go-to-market strategy document.

**Steps:**
1. Read product research documentation
2. Ask user for sales model and timeline
3. Generate 12 GTM sections using [M-MKT-001](references/gtm-strategy.md)
4. Combine into `gtm-manifest-full.md`

**Output:** Complete GTM manifest with strategy, positioning, channels, metrics.

**Agent:** Direct execution (no agent needed)

**References:**
- [references/gtm-strategy.md](references/gtm-strategy.md)
- [growth-gtm-strategy.md](growth-gtm-strategy.md)

---

## 2. Landing Page Creation

**Purpose:** Design, write copy, and implement high-converting landing pages.

**Steps:**
1. **Discovery** - Understand product, audience, goals
2. **Copy** - Write using AIDA/PAS frameworks
3. **Design** - Create wireframes and mockups
4. **Implementation** - Build with HTML/CSS/JS or framework
5. **Analysis** - Track metrics and optimize

**Agent:** `faion-landing-agent` (analyze/copy/design modes)

**References:**
- [references/landing-page.md](references/landing-page.md)
- [growth-landing-page-design.md](growth-landing-page-design.md)
- [growth-copywriting-fundamentals.md](growth-copywriting-fundamentals.md)

---

## 3. Content Marketing

**Purpose:** Build organic traffic through strategic content creation.

**Steps:**
1. **Keyword Research** - Identify target keywords using SEO tools
2. **Content Plan** - Map keywords to content types (blog, video, infographic)
3. **Creation** - Write/produce content following SEO best practices
4. **Optimization** - On-page SEO, internal linking, meta tags
5. **Distribution** - Publish and promote across channels

**Agent:** `faion-content-agent`

**References:**
- [references/content-marketing.md](references/content-marketing.md)
- [growth-content-marketing.md](growth-content-marketing.md)
- [ai-content-strategy.md](ai-content-strategy.md)

---

## 4. Email Marketing Campaign

**Purpose:** Nurture leads and drive conversions through email.

**Steps:**
1. **Segmentation** - Group subscribers by behavior/stage
2. **Sequence Design** - Map email journey (welcome, nurture, conversion)
3. **Copywriting** - Write subject lines and body copy
4. **Setup** - Configure in email platform (SendGrid, Mailchimp, etc.)
5. **Analysis** - Track open rates, CTR, conversions

**Agent:** `faion-email-agent`

**References:**
- [references/email-marketing.md](references/email-marketing.md)
- [growth-email-marketing.md](growth-email-marketing.md)
- [growth-onboarding-emails.md](growth-onboarding-emails.md)

---

## 5. Paid Advertising Campaign

**Purpose:** Acquire users quickly through paid channels.

**Steps:**
1. **Platform Selection** - Choose Google Ads, Meta Ads, or LinkedIn based on audience
2. **Campaign Setup** - Define objectives, budget, targeting
3. **Creative Development** - Design ads (copy + visuals)
4. **Launch & Monitor** - Start campaign, track key metrics
5. **Optimization** - A/B test ads, adjust targeting, improve ROI

**Agent:** `faion-ads-agent`

**References:**
- [references/paid-advertising.md](references/paid-advertising.md)
- [references/google-ads.md](references/google-ads.md)
- [references/meta-ads.md](references/meta-ads.md)

---

## 6. Social Media Strategy

**Purpose:** Build brand awareness and community engagement.

**Steps:**
1. **Platform Selection** - Choose platforms based on audience (Twitter, LinkedIn, TikTok, etc.)
2. **Content Calendar** - Plan posts for 30-90 days
3. **Content Creation** - Write posts, create visuals, schedule
4. **Engagement** - Respond to comments, engage with followers
5. **Analysis** - Track reach, engagement, follower growth

**Agent:** `faion-social-agent`

**References:**
- [references/social-media.md](references/social-media.md)
- [growth-tiktok-marketing.md](growth-tiktok-marketing.md)
- [growth-youtube-strategy.md](growth-youtube-strategy.md)

---

## 7. Growth Experiments

**Purpose:** Systematically test growth hypotheses to find scalable channels.

**Steps:**
1. **Hypothesis** - Define what you believe will drive growth
2. **Experiment Design** - Plan test (metrics, duration, success criteria)
3. **Run** - Execute experiment with minimal viable effort
4. **Analyze** - Measure results against success criteria
5. **Learn** - Document insights, decide to scale or kill
6. **Iterate** - Repeat with new hypotheses

**Agent:** `faion-growth-agent`

**References:**
- [references/growth-operations.md](references/growth-operations.md)
- [ab-testing-framework.md](ab-testing-framework.md)
- [growth-loops.md](growth-loops.md)

---

## 8. Product Launch

**Purpose:** Coordinate multi-channel launch for maximum visibility.

**Steps:**
1. **Pre-Launch** (2-4 weeks before)
   - Build email list
   - Create landing page
   - Prepare launch content (blog post, video, etc.)
   - Line up partnerships/influencers

2. **Launch Day**
   - Post to Product Hunt, Hacker News, Indie Hackers
   - Send email announcement
   - Social media blitz
   - Engage with comments/feedback

3. **Post-Launch** (1-2 weeks after)
   - Publish case studies/testimonials
   - Content marketing push
   - Paid ads (if successful organic launch)
   - Iterate based on feedback

**Agent:** Direct execution (coordinating multiple agents)

**References:**
- [growth-product-hunt-launch.md](growth-product-hunt-launch.md)
- [growth-hacker-news-launch.md](growth-hacker-news-launch.md)
- [growth-indiehackers-strategy.md](growth-indiehackers-strategy.md)

---

## 9. Analytics Setup

**Purpose:** Configure tracking to measure marketing effectiveness.

**Steps:**
1. **Tool Selection** - Choose analytics platform (GA4, Plausible, Mixpanel, etc.)
2. **Event Tracking** - Define key events (signup, activation, conversion)
3. **Implementation** - Install tracking code, configure events
4. **Dashboard Setup** - Create dashboards for key metrics
5. **Regular Review** - Weekly/monthly analysis and reporting

**Agent:** Direct execution (technical implementation)

**References:**
- [references/analytics.md](references/analytics.md)
- [ops-metrics-dashboards.md](ops-metrics-dashboards.md)

---

## 10. SEO Optimization

**Purpose:** Improve organic search rankings and traffic.

**Steps:**
1. **Technical SEO Audit** - Check site speed, mobile-friendliness, indexing
2. **Keyword Research** - Identify high-value keywords
3. **On-Page Optimization** - Optimize titles, meta descriptions, headings, content
4. **Content Creation** - Write new content targeting keywords
5. **Link Building** - Acquire backlinks through outreach, content marketing
6. **Monitor & Iterate** - Track rankings, adjust strategy

**Agent:** `faion-content-agent`

**References:**
- [references/seo.md](references/seo.md)
- [references/seo-2026.md](references/seo-2026.md)
- [search-everywhere-optimization.md](search-everywhere-optimization.md)

---

## Workflow Selection Decision Tree

```
What is your goal?
├─ Launch product → Workflow #8 (Product Launch)
├─ Get traffic → Workflow #10 (SEO) or #3 (Content Marketing)
├─ Convert visitors → Workflow #2 (Landing Page)
├─ Nurture leads → Workflow #4 (Email Marketing)
├─ Scale quickly → Workflow #5 (Paid Advertising)
├─ Build community → Workflow #6 (Social Media)
├─ Find growth channels → Workflow #7 (Growth Experiments)
├─ Measure results → Workflow #9 (Analytics Setup)
└─ Full GTM strategy → Workflow #1 (GTM Manifest)
```

---

*Marketing Workflows v1.0*
