# Tweet-to-launch sprint: idea to paying user in 3 weeks

## Why this playbook exists
Indie hackers run the entire pipeline alone — research, build, ship, market, support, and decide — under tight calendar constraints and often from a nomad schedule. One-line tweeted hypothesis → Gumroad/Stripe-collected first paying customer in 21 days. This playbook turns that ambition into a sequenced set of stages with explicit decision gates so the founder doesn't confuse motion for progress and doesn't keep paying for products that quietly stopped working.

## What changes after running it
Solo indie hacker takes a single tweeted hypothesis through a 3-week audience-driven build sprint: validate via DMs, ship an ugly first version, open paid checkout, and convert at least one tweet reader into a paying user.

## Stage flow
### Hypothesis
Public one-line hypothesis tweeted; signal collected.

**Tasks**
- Draft three single-tweet hypotheses framed as 'X for Y'
- Pick the one that aligns with current audience interests
- Post and pin; reply to every signal within 12 hours

**Decision gate**
> Advance if ≥20 likes OR ≥3 qualified DMs within 48h.
> Re-frame and retweet variant if signal is below threshold.
> Kill the bet if 0 signal after 2 variants.

### Validate
Confirm 5+ prospects describe the pain and accept a paid concept.

**Tasks**
- Run mom-test style DMs with the 10 most-engaged repliers
- Pitch a price (≥$20) inside the conversation
- Capture verbatim quotes that justify the build

**Decision gate**
> Advance if ≥5 DMs confirm the pain and ≥3 verbally commit to paying.
> Pivot scope or price if signal is mixed.
> Kill if no one mentions paying after explicit price.

### Scope
Cut to a one-screen build that ships in 7 days.

**Tasks**
- Write a one-screen micro-MVP spec — one job, one input, one output
- Write the kill list — every feature explicitly NOT shipping
- Define the 'paid' moment — what triggers Stripe checkout

**Decision gate**
> Advance if scope fits on one page AND build is realistic in ≤7 days.
> Re-cut if estimate exceeds a week.

### Build
Ugly-first-version live, paid checkout wired in.

**Tasks**
- Implement only the validated job; skip auth if not needed
- Wire Stripe Payment Link or Gumroad as the checkout
- Push to a public URL by Day 14

**Decision gate**
> Advance when one stranger completes the flow end-to-end and pays.
> Iterate UI ugliness only when paid flow blocks itself.

### Launch
Convert hypothesis tweet readers into paying customers.

**Tasks**
- Drop a launch tweet thread linking to the live product
- DM the 5 strongest Validate stage signals personally
- Cross-post to IndieHackers and Reddit niche subs

**Decision gate**
> Advance to Review if ≥1 paid invoice in 7 days post-launch.
> Re-pitch on a different surface if 0 conversion despite traffic.

### Review
Decide continue / iterate / kill with a written rationale.

**Tasks**
- Run a weekly review with the Discovery and Launch evidence
- Compute first-week unit economics (revenue, refund risk)
- Write a one-paragraph continue/kill decision

**Decision gate**
> Required output: a written verdict. No 'we'll see'.

## When to skip a stage
Every stage exists because indie hackers historically skip exactly that one — Validate is skipped by builders who fall in love with code, Decide is skipped by founders who can't bear to kill a product, and Cadence is skipped when travel tempts a creator into silence. If you must skip a stage, write a one-paragraph rationale in the playbook artefact log so the next run can audit the trade-off.

## How this playbook compounds
The artefacts from each run — quotes, postmortems, conversion tables, hook banks — feed directly into the next playbook the founder runs. A weekly review fed by these outputs is the difference between a portfolio of half-finished projects and a portfolio of compounding bets. Treat every gap[] entry as a methodology to ship; the playbook stays in draft until the gaps clear.

## Reading order
First-time runs should read the playbook YAML end-to-end before starting Stage 1. Repeat runs can jump to the stage matching current ambiguity and skim only that stage's methodologies. The decision gate is always the source of truth — even if the founder feels confident, the gate decides.

## Failure modes to watch
- Mistaking audience engagement for paying intent; the playbook insists on a paid checkpoint.
- Letting one stage drag because the next is intimidating — the gate is meant to force the move.
- Burning out by trying to combine this playbook with two others in the same week.

## Done means done
The playbook is done when every success criterion is checked AND a written verdict exists in the founder's notes. Anything short of a written verdict is an in-progress playbook — file it back into the queue and keep going.
