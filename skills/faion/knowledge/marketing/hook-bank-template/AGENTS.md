# Hook Bank Template

## Summary

**One-sentence:** Maintain a 6-field hook bank (text, pattern, platform, post_url, impressions_24h, qualified_replies) bucketed flopped/average/spiked against a 90-day rolling median, remixed before every new post.

**One-paragraph:** A versioned swipe-file of hook patterns paired with concrete instances tagged by format, platform, and observed result. Each row carries six fields and is bucketed FLOPPED (≤0.5× median) / AVERAGE (0.5-2×) / SPIKED (≥2×) against the author's own rolling-90-day baseline — never gut feel. The bank lives in git, is reviewed weekly, capped at ≤15 patterns, and re-read before any new post. Output is the working bank file plus a monthly review summary surfacing rising vs falling patterns.

**Ефективно для:**

- Solo founders posting on X / LinkedIn / IndieHackers ≥3× per week.
- Reducing daily writing time from 20 minutes to 3 minutes via remix-not-blank-page.
- Surfacing which hook patterns actually move impressions on each platform.
- Build-in-public operators who want to compound learning across months.

## Applies If (ALL must hold)

- You post on X / IndieHackers / LinkedIn / Threads at least 3× per week.
- You have shipped ≥30 posts and can label each as FLOPPED / AVERAGE / SPIKED against your own median.
- Daily writing time is the bottleneck, not idea generation.
- You want to optimise hook quality, not topic generation.

## Skip If (ANY kills it)

- You post fewer than 3× per week — sample too small to learn from.
- You write only long-form (blogs, newsletters) where hooks are buried.
- You delegate writing to a ghostwriter — give them the bank instead.
- You have not yet posted anything — use a generic swipe file for cold start first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 90-day post history with impression counts + replies | CSV / sheet export | platform analytics |
| Rolling 90-day median impressions per platform | scalar per platform | computed locally |
| Pattern allowlist (≤15) | YAML list | author |
| Storage location (git repo or sheet) under version control | git path | author |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[icp-fit-scorecard-solo]] | Qualified replies feed back into who you should be writing for. |
| [[ih-build-update-template]] | Build-update posts are the most common hook test bed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: 6 fields, bucket thresholds, versioned file, pre-write remix, retire-flops, cap ≤15 patterns, monthly review | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for bank file + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (gut-feel bucketing, pattern explosion, dead-bank, blank-page-restart) with symptom/root-cause/fix | 700 |
| `content/04-procedure.xml` | essential | 6-step procedure: snapshot 90d → compute median → bucket rows → cap patterns → pre-write remix → monthly review | 800 |
| `content/05-examples.xml` | essential | Worked example: 4-week bank build for indie hacker on X | 600 |
| `content/06-decision-tree.xml` | essential | Tree routing observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `bucket_rows_against_median` | haiku | Arithmetic comparison, no judgement. |
| `pattern_tagging` | sonnet | Bounded enum classification with edge cases. |
| `monthly_review_summary` | sonnet | Aggregate + narrate the rising / falling patterns. |
| `pattern_retirement_decision` | sonnet | Decide retire vs keep using flop streak + recency. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hook-bank.csv` | 6-field skeleton CSV ready to fill |
| `templates/pattern-allowlist.yaml` | Default ≤15 pattern enum |
| `templates/_smoke-test.csv` | Minimum viable filled bank for validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hook-bank-template.py` | Validate bank rows + bucket math against 02-output-contract schema | Pre-commit / weekly review |

## Related

- [[icp-fit-scorecard-solo]]
- [[ih-build-update-template]]
- [[in-issue-ad-format-library]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps post volume, baseline availability, and pattern count to a rule from `01-core-rules.xml`, telling the agent whether to apply the bank protocol or skip until enough data exists. Walk it on every fresh invocation; do not cache outcomes across distinct engagements.
