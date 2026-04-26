# Continuous Discovery Habits

## Summary

Teresa Torres' framework for making customer discovery a weekly practice rather than a project-kickoff event. The Product Trio (PM + Design Lead + Tech Lead) maintains an Opportunity Solution Tree (OST) as a shared artifact — every opportunity maps to a customer need with verbatim evidence, every solution maps to an opportunity, and every assumption gets tested before the solution enters the roadmap. The PM operates the loop; agents handle mechanical passes (triage, coding, synthesis).

## Why

Sporadic discovery produces roadmaps that reflect the loudest internal voice, not customer evidence. Teams at Spotify, CarMax, and Tesco consistently out-discover competitors by maintaining one customer interview per week as a keystone habit. The OST forces every roadmap item to have a traceable chain: outcome ← opportunity ← verbatim quote with participant ID.

## When To Use

- PM owns one product area and needs a defensible weekly cadence (one interview/week minimum).
- Roadmaps drifting to feature-list mode — leadership cannot articulate what outcome each item serves.
- Product Trio is forming and needs a shared artifact to triangulate on.
- Quarterly planning prep — agents synthesize 60-80 interviews into a refreshed OST.
- "Why are we building this?" challenges from leadership — OST + interview log answer with a traceable chain.

## When NOT To Use

- Pre-PMF zero-to-one with founder-led customer development — no outcome metric or established access.
- Regulated domains where weekly outside-customer interviews require legal review per touchpoint.
- B2B with fewer than 20 logo accounts and a 12-month sales cycle — weekly interviews aren't sustainable.
- Mature growth-stage where experimentation-at-scale has displaced qualitative discovery.
- One-shot launches and migrations (rebrand, platform cutover) — need stakeholder management, not weekly touchpoints.

## Content

| File | What's inside |
|------|---------------|
| `content/01-ost-framework.xml` | OST structure, weekly cadence table, interview best practices, discovery-delivery balance |
| `content/02-agent-pipeline.xml` | Five weekly agent hand-offs, subagent table, prompt pattern, OST schema, failure modes |

## Templates

| File | Purpose |
|------|---------|
| `templates/ost.yaml` | OST schema: outcome, opportunities, solutions, assumption tests |
| `templates/weekly-discovery.md` | Friday readout skeleton (outcome, touchpoints, OST diff, roadmap input) |
| `templates/ost-apply.py` | Apply OST diffs emitted by agents — patch-based, PM reviews before applying |
