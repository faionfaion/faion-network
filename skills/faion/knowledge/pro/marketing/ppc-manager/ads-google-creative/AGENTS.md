# Google Ads Creative (RSA)

## Summary

Writing and structuring Responsive Search Ads (RSA) for Google Search: craft 15 unique headlines covering keyword match, benefits, social proof, CTAs, and differentiators; write 4 descriptions using full 90-character limits; set keyword-rich display paths; pin critical headlines to fixed positions; and target "Excellent" ad strength. The core rule is: every headline must serve a distinct purpose — repeating similar angles wastes testing slots and prevents Google from finding the highest-performing combination.

## Why

Google's RSA format dynamically combines headlines and descriptions to maximize Quality Score for each query. More unique, varied assets give the algorithm more combinations to test. Ad strength correlates with Quality Score, which directly determines ad rank and cost-per-click — an "Excellent" RSA can achieve 10-30% lower CPC than an "Average" one for identical bids. Assets that fail to differentiate produce statistically indistinguishable combinations and stall optimization.

## When To Use

- Writing new RSAs for any Google Search ad group
- Auditing existing RSAs with "Poor" or "Average" ad strength
- Adapting copy to a specific search intent (transactional, commercial, informational)
- Testing benefit-led vs feature-led vs social-proof-led headlines
- Creating ad variations (2-3 RSAs per ad group) to segment by messaging theme

## When NOT To Use

- Google Display, Shopping, or Performance Max creative — RSA format is Search-only
- Campaign and ad group structure — use `ads-google-campaign-setup`
- Bidding strategy and Quality Score optimization beyond copy — use `google-ads-optimization`
- Keyword research and match type selection — use `ads-google-keywords`

## Content

| File | What's inside |
|------|---------------|
| `content/01-rsa-structure.xml` | RSA format specs, character limits, headline/description count, ad strength factors |
| `content/02-headline-angles.xml` | 10 headline angle categories with examples, pinning rules, keyword inclusion guidelines |
| `content/03-descriptions.xml` | 4-description framework, full-character-count rule, formula and examples |
| `content/04-intent-variants.xml` | Copy templates by intent: transactional, commercial, informational |
| `content/05-antipatterns.xml` | Before/after examples, common mistakes: no keywords, repetitive headlines, short copy |

## Templates

| File | Purpose |
|------|---------|
| `templates/rsa-template.md` | Full RSA template: 15 headlines + 4 descriptions + display path + pinning notes |
