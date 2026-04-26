# Focus Groups

## Summary

A focus group is a moderated discussion with 6-10 participants who share characteristics relevant to the research. The group explores attitudes, reactions to concepts, and language around a topic. Minimum 2-3 groups per segment; findings are qualitative and directional, not statistically generalizable.

## Why

Focus groups surface group dynamics, shared vocabulary, and cross-segment contrasts that individual interviews spread across too many sessions to achieve quickly. Running 3-4 homogeneous-but-diverse groups (current users, competitor users, non-users) in parallel reveals segment-specific objections and the language people actually use — inputs that feed copy, positioning, and concept prioritization.

## When To Use

- Early concept exploration: diverse reactions to multiple positioning angles before committing to one direction.
- Language and terminology discovery: harvest vocabulary users actually use for copy and search synonyms.
- Stakeholder buy-in: leadership needs to "watch users" to believe research findings.
- Cross-segment comparison: 3-4 groups reveal segment-unique objections and shared concerns.

## When NOT To Use

- Usability testing — group dynamics suppress individual struggle; use moderated 1:1 sessions.
- Sensitive topics (health, finances, conflict) — participants self-censor in groups.
- Behavior measurement — groups capture stated behavior, not actual behavior.
- Final go/no-go decisions — groupthink and dominant voices distort signal.
- Quantitative claims — N=8 per group is not statistically generalizable.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Focus group vs interview tradeoffs, composition rules, discussion guide structure, moderation techniques. |
| `content/02-analysis.xml` | Cross-group comparison framework, theme extraction, reporting structure, online adaptations. |
| `content/03-antipatterns.xml` | Dominant-participant skew, professional respondents, LLM theme-extraction failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/discussion-guide.md` | Full 90-min discussion guide template with opening script, ground rules, topic sections, concept-reaction block. |
| `templates/session-notes.md` | Note-taking template: participant table, group dynamics, concept reactions, moderator observations. |
| `templates/postprocess.sh` | Shell pipeline: ffmpeg audio extract → WhisperX diarize → Claude theme extraction. |
