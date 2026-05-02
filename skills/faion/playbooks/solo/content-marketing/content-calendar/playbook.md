---
name: content-calendar
description: Build and run a 12-week rotating content calendar that lets a solo SaaS founder publish consistently without daily decisions.
tier: solo
group: content-marketing
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a `content-calendar.md` file that maps 12 repeating weekly themes to a four-post rotation (problem → story → tutorial → recap), a Sunday 2-hour batching session that produces the full week's content in one go, and a single long-form post repurposed into five social cuts — all scoped to a real SaaS niche so you never stare at a blank page on a Monday.

## Prerequisites

- A defined ICP (ideal customer profile): e.g., "indie SaaS founders using Django who sell B2B subscriptions under $99/mo".
- At least one published long-form post or blog article to use as repurposing raw material on Week 1.
- A writing tool with plain-text export (Notion, Obsidian, iA Writer, or similar).
- A scheduling tool: Buffer free tier, Typefully, or direct platform drafts.
- Two hours blocked on Sunday for the weekly batching session — protect this slot like a meeting.

## Steps

1. Create the file `content-calendar.md` in your writing tool (or repo root). Add the 12-theme table below — copy it as-is and fill column "Niche angle" for your product before you start Week 1.

   ```
   | Week | Theme               | Niche angle (fill in)                     |
   |------|---------------------|-------------------------------------------|
   |  1   | Onboarding friction | Where new users drop off in your trial    |
   |  2   | Pricing psychology  | Why you chose your price point            |
   |  3   | Feature spotlight   | The one feature power users swear by      |
   |  4   | Competitive framing | How you differ from the obvious alt       |
   |  5   | Founder story       | The real reason you built this            |
   |  6   | Integration depth   | The integration your users request most   |
   |  7   | Churn signal        | The warning sign before a cancellation    |
   |  8   | Activation metric   | What "aha moment" looks like in your data |
   |  9   | Community proof     | Best testimonial or user story you have   |
   | 10   | Roadmap teaser      | Something shipping in the next 30 days    |
   | 11   | Productivity hack   | How you ship fast as a solo founder       |
   | 12   | Year-in-review      | One win, one mistake, one lesson          |
   ```

2. Map each week's theme to the four-post rotation. For Week N, the posts are:

   - **Monday — Problem post:** state the problem your theme exposes, one real data point or user quote.
   - **Wednesday — Story post:** a short personal narrative (150–300 words) showing you lived this problem.
   - **Friday — Tutorial post:** the concrete fix or workflow, with a step-by-step or screenshot.
   - **Sunday (published end of next session) — Recap post:** one-line summary of what the week's thread taught and a CTA to your product's relevant feature.

   Add a "Post type" column to the table in `content-calendar.md` to track which four slots belong to each week.

3. Run the Sunday batching session. Block 2 hours. Use this order inside that 2-hour window:

   - 0:00–0:20 — Review last week's engagement (likes, replies, click-throughs). Note one thing that worked and one that didn't in `content-calendar.md` under a `## Notes` section.
   - 0:20–0:50 — Draft all four posts for the upcoming week. Write them in `content-calendar.md` under the week heading. Do not edit — just draft.
   - 0:50–1:20 — Edit and tighten. Cut the weakest sentence from each post.
   - 1:20–1:50 — Schedule all four posts in Buffer (https://buffer.com) or Typefully (https://typefully.com). Set Monday 08:00, Wednesday 08:00, Friday 08:00, Sunday 20:00 in your local timezone.
   - 1:50–2:00 — Pick next week's theme from the table, confirm niche angle still applies, adjust if needed.

4. Repurpose the long-form post into 5 social cuts. Take your longest published article (aim for 800+ words). Extract these five formats — each is one scheduled post that can fill a gap week or supplement Week 1:

   - **Cut 1 — Hook thread:** extract the opening problem statement, rewrite as a 3-tweet thread ending with a link.
   - **Cut 2 — Stat or quote card:** find the single sharpest sentence, post it as plain text with no link (engagement bait to be pinned).
   - **Cut 3 — Step list:** if the article has a list or steps, post the list stripped to plain bullets.
   - **Cut 4 — Counterintuitive take:** find the most surprising claim in the article, post it as one sentence + 1-paragraph expansion.
   - **Cut 5 — CTA post:** "I wrote the full breakdown: [link]" — schedule this last, after the four cuts have run.

   Store these drafts under `## Repurposed: [Article title]` in `content-calendar.md`.

5. Apply the Week 1 example below to validate your setup before running Week 2 independently.

   **Example — SaaS: a B2B invoice automation tool for freelancers**

   - Week 1 theme: "Onboarding friction". Niche angle: "Freelancers who abandon setup after connecting their bank account".
   - Monday post: "72% of freelancers who connect a bank account to invoice tools never send their first invoice. Here's why: [screenshot of empty 'Clients' tab]"
   - Wednesday post: "My first version had a 9-step onboarding. I watched 14 screen recordings. Step 4 killed everyone. Here's what I did."
   - Friday post: "How to get from bank-connected to first invoice in under 3 minutes: [numbered steps + GIF]"
   - Recap (Sunday next batch): "This week: why onboarding step 4 was murdering signups. Fix: removed the 'add client' gate. Result: +40% activation. Full breakdown in bio."

6. After completing 12 weeks, reset the cycle. Update niche angles for any theme that under-performed (fewer than average replies or clicks). Retire one theme, add one new theme based on support tickets or user interviews from the past quarter.

## Verify

Open `content-calendar.md` and confirm:

1. The 12-row theme table is filled with niche angles (no blank "fill in" placeholders).
2. Week 1 has four drafted posts under the correct headings (Problem, Story, Tutorial, Recap).
3. Run:
   ```
   grep -c "^| " content-calendar.md
   ```
   Returns at least `13` (header row + 12 week rows).
4. In your scheduling tool, confirm 4 posts are queued with timestamps in the next 7 days.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Sunday batch runs 3+ hours and posts feel rushed | Niche angle too vague — you're re-researching in-session | Spend 10 minutes on Monday to confirm next week's niche angle and save one example tweet or quote; open Sunday with that anchor |
| Engagement drops to near zero by Week 4 | Four post types rotate predictably, audience tunes out | Swap Wednesday Story → a "hot take" post once per month; use the Notes section to flag which week gets the swap |
| Repurposed cuts feel repetitive after Cut 2 | Cuts are too similar because the long-form post was list-heavy | Prioritise narrative articles (personal story + data + fix) for repurposing; skip pure list posts |
| You skip the Sunday session two weeks in a row | Two-hour block is too large to protect amid client work | Split into two 60-minute blocks: Saturday review + draft, Sunday edit + schedule |
| Recap post CTA gets low clicks | CTA links to homepage, not to the specific feature mentioned in the week | Link the Recap post to the feature's in-app URL or a dedicated landing page |

## Next

- [solo/content-marketing/newsletter-setup](../newsletter-setup) — capture the audience you build on social into an owned email list.
- [solo/seo-essentials/technical-seo-audit](../../seo-essentials/technical-seo-audit) — after 12 weeks of content, audit which posts are indexable and driving organic traffic.

## References

- [knowledge/solo/marketing/content-marketer/growth-content-marketing](../../../knowledge/solo/marketing/content-marketer/growth-content-marketing) — provides the batching and rotation model this playbook operationalises: Sunday session structure, post-type sequencing, and the one-to-many repurposing ratio all derive from this methodology.
- [knowledge/solo/marketing/content-marketer/search-everywhere-optimization](../../../knowledge/solo/marketing/content-marketer/search-everywhere-optimization) — informs the Friday tutorial post format: structuring each tutorial for discoverability across search, LLM citations, and social search (LinkedIn/X) is grounded in this methodology's multi-surface optimisation principles.
