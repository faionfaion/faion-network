# Idea Generation

## Summary

Seven systematic frameworks for discovering solopreneur business ideas: skills inventory, pain-point
mining, job substitution, productized service, unbundling, market stacking, and own problems. Each
framework produces candidate ideas; all candidates are scored on a weighted 5-criterion matrix
(market size, personal fit, competition, monetization, speed-to-MVP) before handoff to
`niche-evaluation`.

## Why

Waiting for inspiration produces mode-collapsed output: "AI-powered X", "task tracker for Y". The
seven frameworks force different ideation angles and surface ideas grounded in actual skills and
observed pains. Scoring before choosing prevents gut-feel selection that ignores market or fit
signals. The two-pass diverge/converge pattern — generate 30+ candidates, then score top 5 —
avoids premature convergence and fabricated scoring.

## When To Use

- Solopreneur stuck on "what to build" with skills inventory but no candidate list.
- Need 20-50 raw candidates fast across 7 frameworks for downstream `niche-evaluation` scoring.
- Refresh of stale roadmap: feed weekly capture template into agent on cron.

## When NOT To Use

- Already have a validated idea with paying customers — skip to `pricing-research` or `mvp-scoping`.
- Generating ideas without skills/constraints input — agents produce generic, ungrounded lists.
- Scientific or research-domain novelty needed — LLMs converge on consensus; use literature-driven discovery.

## Content

| File | What's inside |
|------|---------------|
| `content/01-frameworks.xml` | All 7 frameworks with definitions, idea formulas, and worked examples. |
| `content/02-scoring.xml` | 5-criterion weighted scoring matrix, guide, worked examples (developer + marketer). |
| `content/03-gotchas.xml` | Mode-collapse patterns, fabrication risks, human-in-loop checkpoints. |

## Templates

| File | Purpose |
|------|---------|
| `templates/discovery-session.md` | Idea Discovery Session template: frameworks used, per-idea capture, top-3 selection. |
| `templates/weekly-capture.md` | Weekly Idea Capture template for pipeline cron runs. |
| `templates/prompt-diverge.txt` | Diverge agent prompt: 7-framework expansion against skills+constraints brief, JSON output. |
| `templates/prompt-score.txt` | Converge agent prompt: 5-criterion scoring with no-fabrication rule. |
