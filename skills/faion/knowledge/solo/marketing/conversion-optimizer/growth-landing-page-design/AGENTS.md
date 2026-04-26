# Landing Page Design

## Summary

AIDA-structured landing page copy methodology: Attention (hero captures interest in 5 seconds),
Interest (benefits not features), Desire (social proof), Action (single CTA per section).
Headline formula: [Outcome] + [Timeframe] + [Without Pain Point]. One primary CTA per page.
Social proof placed directly below the hero CTA increases CVR by 10-15%.

## Why

Most landing pages fail by trying to do too much — multiple CTAs confuse visitors, feature
focus loses customers who care about outcomes, and slow load times (over 3 seconds) cause
abandonment before the page renders. The "So what?" test converts features to benefits:
"AI-powered" → "Get answers in seconds, not hours." FAQ sections should address conversion
objections ("Can I cancel anytime?"), not product questions. Numbers outperform vague claims
everywhere: "40% improvement" beats "significant improvement" for click-through.

## When To Use

- Writing multiple headline variations for A/B testing (5-10 per session)
- Drafting full landing page copy: hero, problem agitation, benefits, how-it-works, FAQ, final CTA
- Auditing existing copy against the conversion checklist (above-fold, copy, trust, technical)
- Generating testimonial rewrites: transforming generic quotes into specific-result format
- Applying the "So what?" test to a feature list to produce benefit copy

## When NOT To Use

- Visual design and layout decisions — agent produces copy; Figma/Webflow work is separate
- A/B test execution — agent writes variants but cannot run tests (use Optimizely or VWO)
- Page speed optimization — a technical task outside copy scope; run Lighthouse separately
- Generating fake testimonials — fabricated quotes are FTC violations
- Final CVR prediction — agent-estimated ranges are benchmarks, not guarantees

## Content

| File | What's inside |
|------|---------------|
| `content/01-aida-structure.xml` | Section-by-section rules: hero, problem, benefits, how-it-works, social proof, FAQ, final CTA |
| `content/02-copy-rules.xml` | Headline formula, "So what?" test, testimonial format, common mistakes |

## Templates

| File | Purpose |
|------|---------|
| `templates/saas-page-structure.md` | Full SaaS landing page section order with placeholder content |
| `templates/audit-checklist.md` | Above-fold, copy, trust, technical conversion checklist |
| `templates/prompt-full-copy.txt` | Agent prompt: complete AIDA landing page copy from ICP brief |
| `templates/audit-score.py` | Score landing page sections against checklist criteria |
