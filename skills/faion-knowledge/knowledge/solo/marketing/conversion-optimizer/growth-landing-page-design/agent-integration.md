# Agent Integration — Landing Page Design

## When to use
- Writing multiple headline variations for A/B testing (5-10 per session using the README formula)
- Drafting full landing page copy: hero, problem agitation, solution/benefits, how-it-works, FAQ, final CTA
- Auditing existing landing page copy against the conversion checklist (above-the-fold, copy, trust, technical)
- Generating testimonial rewrites: transforming generic customer quotes into specific-result format
- Writing FAQ sections from a list of known customer objections
- Producing benefit reframes: given a feature list, applying the "So what?" test to produce benefit copy

## When NOT to use
- Visual design and layout decisions — the agent produces copy and structure; Figma/Webflow work is separate
- A/B test execution — the agent can write variants but cannot run tests; that requires Optimizely, VWO, or Google Optimize
- Page speed optimization — a technical task outside copy scope
- Generating fake testimonials or social proof — fabricated quotes are FTC violations and destroy trust when discovered
- Final conversion rate prediction — agent-estimated CVR ranges are benchmarks, not guarantees

## Where it fails / limitations
- Hero headline quality is highly dependent on deep ICP research; agent headlines without specific customer pain language are generic
- The "So what?" feature-to-benefit translation often requires product-specific knowledge the agent lacks without detailed briefing
- Social proof copy requires real customer quotes and real company logos; the agent can format and polish them but cannot create them
- FAQ generation without a real list of customer objections produces questions the target audience does not actually ask
- Mobile rendering and above-the-fold layout depend on the builder (Webflow, Framer, Carrd) and screen size — agent cannot audit visual layout

## Agentic workflow
Use a sequential pipeline: (1) brief the agent with ICP, product description, top 3 pain points, and existing customer testimonials; (2) generate the full page copy in one Sonnet call following the README section structure; (3) run a separate audit pass against the conversion checklist; (4) generate 5 headline A/B variants for the hero. Human designer implements in the chosen builder, then an analytics subagent monitors CVR and bounce rate after launch. Human approval required before any page goes live.

### Recommended subagents
- `faion-sdd-executor-agent` — execute landing page build SDD tasks (copywriting → design → analytics setup → A/B test)
- `password-scrubber-agent` — strip any real customer PII from testimonials before agent processing

### Prompt pattern
```
You are a conversion copywriter. Given:
- Product: <product_name> — <one_sentence_description>
- ICP: <icp>
- Top 3 pain points: <pains>
- Key benefits (not features): <benefits>
- Social proof: <testimonials_and_numbers>
- CTA goal: <goal> (free trial / demo / purchase / email signup)

Write a complete landing page using AIDA structure:
1. Hero: 3 headline variants (formula: [Outcome] + [Timeframe] + [Without pain])
2. Problem section: pain → consequences → transition (3 sentences each)
3. Solution: "Introducing [Product]" + 3 benefits with icons
4. How it works: 3 steps (action + outcome per step)
5. Testimonials: reformat the provided quotes to [specific result] + [timeframe] + [before/after] format
6. FAQ: 5 questions addressing objections to <CTA goal>
7. Final CTA: benefit reminder + risk reversal + CTA button text
```

```
Audit this landing page copy:
<landing_page_text>

Score each element against the conversion checklist:
- Above the fold (headline clarity, single CTA, visual, social proof): /20
- Copy (benefits vs features, specificity, scannability): /20
- Trust (testimonials, logos, guarantees): /20

Flag specific lines to rewrite. Provide rewrites for the 3 lowest-scoring elements.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `playwright` | Automated screenshot + above-fold audit | `pip install playwright` / https://playwright.dev |
| `lighthouse` CLI | Page speed, Core Web Vitals, mobile audit | `npm install -g lighthouse` / https://developer.chrome.com/docs/lighthouse |
| `pagespeed-insights` API | Programmatic CWV scores | https://developers.google.com/speed/docs/insights/v5/get-started |
| `vwo-cli` | VWO A/B test management via CLI | https://developers.vwo.com |
| `hotjar` API | Heatmap and session recording data export | https://developers.hotjar.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Webflow | SaaS | Yes (CMS API) | Best no-code builder; CMS API for content management |
| Framer | SaaS | Partial (no public API) | Strong for animated landing pages; manual publishing |
| Carrd | SaaS | No API | Simple one-page sites; manual publishing |
| Unbounce | SaaS | Yes (REST API) | Landing page + A/B testing; purpose-built for CRO |
| Optimizely | SaaS | Yes (REST API) | Enterprise A/B testing; agent can create and monitor experiments |
| VWO | SaaS | Yes (REST API) | Mid-market A/B testing; heatmaps included |
| Google Optimize | SaaS | Deprecated 2023 | Replaced by GA4 experiments |
| Hotjar | SaaS | Yes (REST API) | Heatmaps, scroll maps, session recordings |
| Microsoft Clarity | SaaS | Yes (REST API) | Free heatmaps and session recordings |
| Smartmockups | SaaS | Yes (API) | Product mockup generation for hero visuals |

## Templates & scripts
See `templates.md` for SaaS Landing Page Structure and Conversion Checklist. The README contains the full page layout template.

```python
# Landing page copy audit: score sections against checklist criteria
def audit_landing_page(sections: dict) -> dict:
    """
    sections keys: 'hero', 'problem', 'solution', 'how_it_works',
                   'social_proof', 'faq', 'final_cta'
    Returns score per section and flagged issues.
    """
    checks = {
        "hero": [
            ("has_single_cta", "One primary CTA"),
            ("headline_under_12_words", "Headline 6-12 words"),
            ("has_social_proof", "Social proof visible"),
            ("has_visual", "Product visual present"),
        ],
        "social_proof": [
            ("has_photos", "Testimonials include photos"),
            ("has_specific_results", "Results are specific with numbers"),
            ("has_company_logos", "Company logos present"),
        ],
        "final_cta": [
            ("has_risk_reversal", "Guarantee or risk reversal"),
            ("has_benefit_reminder", "Benefit restated near CTA"),
        ],
    }
    scores = {}
    for section, criteria in checks.items():
        section_text = sections.get(section, "")
        passed = sum(1 for key, _ in criteria if key in section_text.lower() or len(section_text) > 50)
        scores[section] = {"score": passed, "max": len(criteria), "criteria": [c[1] for c in criteria]}
    return scores
```

## Best practices
- Write 10 headline variations before selecting the final one; the first headline is never the best one
- Put social proof as close to the hero CTA as possible — "Trusted by 10,000+ users" directly below the button increases CVR by 10-15%
- FAQ sections should address conversion objections, not product questions — "Is my data secure?" converts better than "How do I import my data?"
- Use numbers everywhere possible: "40% improvement" beats "significant improvement"; "trusted by 5,000 users" beats "trusted by thousands"
- The final CTA section should include a risk reversal (money-back guarantee, free trial, no credit card) — it reduces friction at the decision moment
- Test headlines before designing — validate copy with a 5-person user test before investing in visual design

## AI-agent gotchas
- **Generic ICP problem:** Agent copy without specific ICP pain language sounds like every other SaaS landing page; invest time in the brief before generating copy
- **Feature creep in copy:** Agent defaults to listing all features if not constrained; instruct it to pick the 3 most differentiating benefits and ignore the rest
- **Testimonial fabrication risk:** If given generic quotes, agent will polish them into specific-sounding testimonials — verify all specifics (numbers, company names) against real source material before publishing
- **A/B test interpretation:** Agent can suggest hypotheses but cannot interpret statistical significance from test results without being given the raw data and sample sizes
- **Page speed is not a copy problem:** Agent audits will not catch image size, JavaScript bloat, or CDN configuration issues — run Lighthouse separately
- **Mobile-first blind spot:** Agent generates desktop-first copy structure; above-the-fold elements on mobile differ significantly — validate with a real mobile preview

## References
- https://unbounce.com/landing-page-articles/what-is-a-landing-page/
- https://copyhackers.com/headline-formulas/
- https://blog.hubspot.com/marketing/landing-page-examples-list
- https://conversionxl.com/blog/social-proof/
- https://www.nngroup.com/articles/page-fold-manifesto/
- Sugarman, J. (2012). *The Adweek Copywriting Handbook*. Wiley.
