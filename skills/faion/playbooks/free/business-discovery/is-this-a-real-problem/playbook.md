---
name: is-this-a-real-problem
description: Gather three types of evidence — search signals, revealed-preference signals, and unprompted interview mentions — to decide whether a problem is real before building anything.
tier: free
group: business-discovery
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have scored your problem hypothesis against three evidence types — search volume signals, revealed-preference signals, and behavioral signals from user interviews — and arrived at a binary pass/fail verdict (pass = two or more evidence types confirmed). If you pass, you have enough external validation to justify spending time on a solution.

## Prerequisites

- A problem hypothesis written as one sentence: "People who [persona] struggle to [action] because [reason]." Example: "Solo consultants struggle to manage their calendar because they have no system for protecting deep-work blocks."
- A Google account (for Google Trends — free).
- Access to Reddit (free, no account needed for reading).
- Access to the interviewee pool you started building in [mom-test-customer-interview](../mom-test-customer-interview/playbook.md), or at least five direct contacts who match your target persona.
- A plain text file or spreadsheet to record findings.

## Steps

### Evidence type 1 — Search volume signals

1. Open https://trends.google.com/trends/explore and type the core pain phrase from your hypothesis. For the calendar example: type `calendar overload consultant`. Set region to "Worldwide" and time range to "Past 5 years".

2. Declare a pass for this signal if the interest-over-time graph shows a consistent non-zero baseline (any value above 10 in at least 6 of the last 12 months). A graph that flatlines at 0 or only spikes once is a fail.

3. Open https://www.reddit.com, type the same phrase into the Reddit search field at the top of the page, and press Enter. Count the threads that appear in the results. Write down the count.

4. Open https://stackoverflow.com/tags and search the closest technical tag if your problem has a software component (e.g., `calendar` or `scheduling`). Note the number of questions tagged. For non-technical problems, skip Stack Overflow and rely solely on Reddit and Google Trends.

5. Declare this evidence type confirmed if at least one of the following is true:
   - Google Trends baseline > 10 for six or more of the past twelve months.
   - Reddit shows 20 or more threads discussing the pain, with at least three threads having 10 or more comments.
   - Stack Overflow tag has 500 or more questions.

   For the calendar example, a search for `calendar overload consultant` on Reddit typically returns dozens of threads in communities like r/freelance and r/productivity with hundreds of comments — confirmed.

### Evidence type 2 — Revealed-preference signals

6. Search Google for existing paid solutions to your problem. Use queries like `[pain keyword] app pricing`, `[pain keyword] software cost`, `best tools for [persona] [pain keyword]`. Write down every paid product you find, its price, and any visible review count.

7. Open https://www.g2.com and search the pain keyword. Count how many products appear in the category. Note the top product's review count.

8. Open https://www.producthunt.com and search the pain keyword. Count the number of launched products. Products with more than 100 upvotes indicate a paying audience exists.

9. Search for workarounds that people are paying for indirectly. Look for Notion templates on https://www.notioneverything.com or https://gumroad.com with the pain keyword in the title. A paid template that has sold 50 or more copies is a revealed-preference signal — people paying for a workaround rather than a complete solution.

10. Declare this evidence type confirmed if at least one of the following is true:
    - Two or more paid products exist with 50 or more reviews on G2, Capterra, or the App Store.
    - A paid workaround (template, spreadsheet, script) has 50 or more buyers.
    - Product Hunt shows three or more launches on the topic with a combined 300 or more upvotes.

    For the calendar example: searching "consultant scheduling" on G2 returns products like Calendly ($8–$16/mo) and Acuity ($16–$61/mo) with thousands of reviews. Revealed-preference confirmed.

### Evidence type 3 — Behavioral signals from interviews

11. Schedule five interviews with people who match your persona. Use the interview format from [mom-test-customer-interview](../mom-test-customer-interview/playbook.md). Do not mention your idea or the problem — let them talk about their work.

12. Ask only open-ended questions about their workflow. For the calendar example: "Walk me through a typical Monday for you. What's the first thing you do when you open your laptop?" or "What part of managing your work week do you find most annoying right now?"

13. After each interview, open your notes file and create a row in a table with three columns: interviewee number, whether they mentioned the problem unprompted (yes/no), exact quote if yes.

14. Declare this evidence type confirmed if three or more of your five interviewees mentioned the problem spontaneously — without you asking about it. A mention counts only if they described it as a current frustration, not a theoretical concern.

    For the calendar example: in five interviews with solo consultants, a researcher would expect to hear at least three mention scheduling stress ("I lose half a day a week just moving meetings around") without being prompted.

### Scoring and decision

15. Count how many of the three evidence types are confirmed. Write the score in your notes file.

16. Apply the decision rule:
    - **2 or 3 confirmed** → the problem is real. Move to [idea-validation-landing-page](../idea-validation-landing-page/playbook.md).
    - **1 confirmed** → weak signal. Run five more interviews and re-score before deciding.
    - **0 confirmed** → the problem as stated is not validated. Rewrite your hypothesis and start over.

## Verify

Open your notes file and check that it contains exactly three rows — one per evidence type — each marked either "confirmed" or "not confirmed", with at least one supporting data point per row (e.g., "Google Trends baseline 35 for 10/12 months", "Calendly has 12,000+ G2 reviews", "3/5 interviewees mentioned calendar stress unprompted"). Your score must be 2 or 3 to proceed.

If your notes file has any row without a supporting data point, return to that evidence type and collect the missing data before scoring.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Google Trends shows only zeroes | Search phrase is too specific or uses jargon that searchers don't use | Broaden the phrase: remove the persona modifier and search only the core pain word. If "calendar overload consultant" is zero, try "calendar management" and look for spikes. |
| Reddit threads exist but have very few comments | The community is spread across many niche subreddits | Search in the most general subreddit for your persona (e.g., r/freelance, r/smallbusiness, r/sysadmin) rather than highly specialised ones. Use site:reddit.com in a Google search to surface threads that Reddit's own search buries. |
| G2 shows no products in the category | Problem is too niche or the product category uses a different name | Search Capterra (https://www.capterra.com) and GetApp (https://www.getapp.com) with the same keywords. Also try searching the pain phrase on the App Store. |
| All five interviewees mention the problem but they already use a paid solution | The problem is real but the market is already served | Note this in your file. This is not a blocker — it confirms demand. Your next question is whether existing solutions have a meaningful gap. Proceed to [niche-selection-framework](../niche-selection-framework/playbook.md) to find the underserved segment. |
| Interviewees only mention the problem when you bring it up directly | You are leading the witness | Do not mention the problem in your opening. Extend the interview: ask about the last month of their work life before narrowing to any specific topic. If they still don't raise it after 20 minutes, record it as unprompted-no. |

## Next

- [idea-validation-landing-page](../idea-validation-landing-page/playbook.md) — if you scored 2 or 3, test whether people will act on the problem before you write a line of code.
- [mom-test-customer-interview](../mom-test-customer-interview/playbook.md) — if your behavioral signal is weak (fewer than 3 of 5 mentions), run five more structured interviews with this playbook before re-scoring.
- [niche-selection-framework](../niche-selection-framework/playbook.md) — if all three evidence types confirmed but across very different personas, use this to narrow to the most viable segment first.

## References

- [knowledge/free/dev/testing-developer/tdd-workflow](../../../knowledge/free/dev/testing-developer/tdd-workflow) — the red-green-refactor discipline of writing a failing test before writing any production code maps directly onto the scoring logic in Step 16: you must collect evidence that falsifies your hypothesis (red) before treating the problem as real (green). Applying this mindset prevents the common founder error of starting to build (refactor) while still in the red phase.
