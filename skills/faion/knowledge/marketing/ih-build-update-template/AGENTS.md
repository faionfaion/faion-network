# Indie Hackers Build-Update Template

## Summary

**One-sentence:** Per-post Indie Hackers build-update template optimised for the IH algorithm — TL;DR + 3 numbers + 1 ask, body 600-1200 chars, weekly cadence on Tuesday morning ET.

**One-paragraph:** `growth-indiehackers-strategy` covers the broad IH platform play; this template is the per-post fill-in. The IH algorithm rewards posts that lead with a TL;DR, surface 3 concrete numbers (MRR, signup count, conversion, churn, retention) and end with one specific ask answerable in &lt;1 min. Body sweet spot is 600-1200 chars (above 1500 buries the ask; below 400 reads as low-effort). Posts on Tuesday 8-10am ET reliably out-perform other slots. Output is a markdown post draft + scheduled cadence.

**Ефективно для:**

- Solo founders building in public on IndieHackers ≥1×/week.
- Converting build-progress into qualified replies (founder-mode operators read IH for signal).
- Stacking with a hook-bank methodology — the IH post is one row in the bank.
- Recruiting affiliates / co-marketers from the IH audience.

## Applies If (ALL must hold)

- Operator has an Indie Hackers account and is shipping a product or service.
- Operator has at least 3 numeric signals this week (MRR delta, signup count, conv rate, etc.).
- A specific ask exists (e.g. "Which of these three landing-page variants reads cleaner?").
- Operator can post within the Tuesday 8-10am ET window OR has scheduling enabled.

## Skip If (ANY kills it)

- Nothing shipped or measured this week — IH has zero tolerance for "thoughts" posts.
- The product is enterprise B2B with no public surface — IH audience cannot reciprocate.
- Operator already pushed an IH post within the last 72h — over-posting hurts reach.
- No genuine ask available — fake asks burn trust.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 3 numeric signals from the last 7 days | scalars | analytics / billing |
| TL;DR draft ≤180 chars | string | founder |
| Specific ask | string | founder |
| Product link or screenshot | URL / image | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[hook-bank-template]] | IH post hooks feed the bank; bank patterns feed the hook draft. |
| [[icp-fit-scorecard-solo]] | Replies from IH are an input signal for the scorecard. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: TL;DR ≤180, 3 numbers required, 1 ask, 600-1200 char body, Tue 8-10am ET, weekly cadence | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for IH post bundle + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix): no numbers, vague ask, wall of text, off-slot post | 700 |
| `content/04-procedure.xml` | essential | 6-step procedure: collect numbers → draft TL;DR → write body → set ask → schedule slot → log reply outcomes | 800 |
| `content/05-examples.xml` | essential | Worked example: full post with 3 numbers + ask + observed reply pattern | 600 |
| `content/06-decision-tree.xml` | essential | Tree routing observable signals → rule id | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `numbers_extraction` | haiku | Mechanical CSV read. |
| `tldr_drafting` | sonnet | 180-char hook with tone control. |
| `body_writing` | sonnet | 600-1200 char narrative tying numbers to the ask. |
| `reply_outcome_tagging` | sonnet | Classify qualified vs noise replies after 24h. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ih-post.md.j2` | IH post skeleton with required sections |
| `templates/ih-post.md` | IH post skeleton with required sections Generated from `templates/ih-post.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/reply-triage.csv` | Reply outcome log for the bank |
| `templates/_smoke-test.json` | Minimum viable IH post bundle for validator self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ih-build-update-template.py` | Validate IH post bundle (TL;DR length, body char range, 3 numbers, ask present) against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[hook-bank-template]]
- [[icp-fit-scorecard-solo]]
- [[gumroad-ops-playbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps numeric-signal availability, ask quality, body length, and slot timing to a rule from `01-core-rules.xml`, telling the agent whether to publish, block on a missing element, or skip the week. Walk it on every fresh post; do not cache outcomes across posts.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/reply-triage.csv`

```csv
post_url,replies_total,qualified_replies,new_follows,bucket_relative_to_median
https://www.indiehackers.com/post/REPLACE,0,0,0,average
```

### `templates/_smoke-test.json`

```json
{
  "title": "Week 14 \u2014 first $1k MRR, here is what flipped it",
  "tldr": "TL;DR: hit $1k MRR week 14 after switching to one-niche LinkedIn DMs. Two questions for IH on what to test next.",
  "body": "Background: 14 weeks solo on a small SaaS for Shopify owners. Spent weeks 1-10 on generic outreach: 200 DMs/week, 0.5 percent reply, zero sales. Week 11 I picked one niche and rewrote the opener around their actual pain. MRR moved because trial-to-paid finally caught up; DMs sent dropped because I spend more time per DM now. The lesson I keep relearning: smaller niche, higher reply rate. The open question is whether to double down on Shopify or pick a second niche in parallel for the next six weeks. The numbers below cover the last seven days only, so they are not a victory lap; they are a checkpoint. If you have stepped through a similar inflection, I want to know what you tried next \u2014 and what you wish you had done instead.",
  "numbers": [
    {
      "label": "MRR",
      "value": "$1040",
      "window_days": 7
    },
    {
      "label": "Trial-to-paid",
      "value": "21%",
      "window_days": 7
    },
    {
      "label": "DMs sent",
      "value": "47",
      "window_days": 7
    }
  ],
  "ask": "If you hit $1k MRR via cold outreach, what was the opener message that worked \u2014 verbatim if possible?",
  "scheduled_at": "2026-05-26T13:00:00Z",
  "weekday_et": "tue",
  "hour_et": 9
}
```
