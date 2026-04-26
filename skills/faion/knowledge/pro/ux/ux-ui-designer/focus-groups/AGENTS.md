# Focus Groups

## Summary

A moderated qualitative method with 6–10 participants per group, 60–90 minutes, run in a minimum of 3 groups per segment before themes are treated as stable. Structure: warm-up (10 min), three core topics with probe ladders (40–60 min), concept reveal late (last 25%), wrap-up. Use written-first exercises before open discussion to capture unanchored individual opinions. Recruit one extra participant per group to absorb ~20% no-show rate.

## Why

Focus groups surface group vocabulary, attitude ranges, and concept reactions faster than sequential 1:1 interviews. The key mechanism is social elicitation: participants build on and contrast each other's views, revealing disagreements that solo interviewees suppress. The minimum-3-groups rule exists because themes from 1–2 groups systematically over-represent the first articulate speaker.

## When To Use

- Early-stage concept exploration before quantitative or 1:1 interview research.
- Generating reaction data on copy, naming, value propositions, or visual concepts.
- Mapping user vocabulary — how customers describe a problem in their own words.
- Recruiting stakeholder buy-in by letting PMs observe live discussion.

## When NOT To Use

- Usability testing — group dynamics drown individual task behavior.
- Sensitive or personal topics (health, finance, harassment) — social pressure distorts answers.
- Final decision-making — small N plus groupthink does not equal representative data.
- Anything shipped without a 1:1 follow-up — group consensus is unreliable signal alone.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Session structure, group composition rules, moderation techniques, recruitment rules. |
| `content/02-antipatterns-and-analysis.xml` | Groupthink antipattern, dominant-voice antipattern, analysis framework, agentic coding schema. |

## Templates

| File | Purpose |
|------|---------|
| `templates/discussion-guide.md` | Full 90-min discussion guide: welcome, ground rules, warm-up, topics, concept reaction, wrap-up. |
| `templates/note-taking.md` | Per-session note-taking template with participant table, group dynamics, and quote capture. |
| `templates/transcript-themer.py` | TF-IDF + k-means theme extraction from transcript JSON with speaker attribution. |
