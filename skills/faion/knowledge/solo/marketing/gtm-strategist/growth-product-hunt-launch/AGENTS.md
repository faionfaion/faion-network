# Product Hunt Launch

## Summary

A four-phase Product Hunt launch system (Prepare → Optimize → Launch → Leverage):
build an email list of 500+ interested users over 4-8 weeks, secure a hunter with 1,000+
followers in the same niche, launch at 12:01 AM PT on Tuesday-Thursday, reply to every
comment within one hour. Never ask for upvotes directly — it violates TOS.

## Why

Upvote velocity in the first few hours determines the final ranking. Accounts with no
pre-built audience or weak listing assets consistently fail because Product Hunt is a
social product: early supporters with prior product relationships drive the initial spike
that earns Explore placement. The tagline must be under 60 characters and benefit-focused
("Build beautiful landing pages in minutes" not "AI-Powered Landing Page Generator").
A dedicated `/welcome-producthunters` landing page with a custom offer and separate
tracking separates PH conversion from organic traffic.

## When To Use

- Product is polished and launch-ready; need all listing assets (tagline variants, first
  comment, gallery descriptions, launch email, social posts)
- Evaluating launch readiness against the 4-week checklist before committing to a date
- Drafting canned responses for the 5 most likely comment types in advance
- Post-launch: generating a retrospective for IndieHackers from metrics and comment thread
- Building a hunter outreach message or waitlist page copy

## When NOT To Use

- Product is not yet functional or has major UX issues — public launch damages credibility permanently
- Email list under 200 warm contacts — build audience first; launch date can wait
- Planning to launch on a weekend or during a major tech event — timing is non-negotiable
- Expecting automated upvoting, fake comments, or inauthentic support coordination
- Assuming PH traffic alone sustains growth after day 1 — plan post-launch nurture

## Content

| File | What's inside |
|------|---------------|
| `content/01-launch-phases.xml` | 4-phase framework: preparation timeline, listing optimization rules, launch day schedule, post-launch actions |
| `content/02-assets-and-mistakes.xml` | Tagline formula, gallery structure, common mistakes, metrics benchmarks |

## Templates

| File | Purpose |
|------|---------|
| `templates/first-comment.md` | PH first comment: maker intro, differentiators, special offer, roadmap teaser |
| `templates/launch-email.md` | Launch day email to supporters: link, upvote CTA, no-pressure framing |
| `templates/prompt-asset-generation.txt` | Agent prompt: 5 tagline variants + first comment + launch email |
| `templates/check-launch-timing.py` | Validate proposed launch datetime: must be 12:01 AM PT, Tue-Thu |
