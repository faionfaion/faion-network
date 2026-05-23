# Stakeholder Sentiment Tracker

## Summary

**One-sentence:** A weekly AI-assisted methodology that ingests each stakeholder's text artefacts (emails, chat threads, meeting transcripts) and produces a `supportive | cautious | hostile` classification with a trend chart, giving the PM a 2-4 week head-start before a sponsor publicly turns red.

**One-paragraph:** A static stakeholder register identifies who matters, but says nothing about how their support is trending. On distressed projects, sponsors do not announce that they are going hostile — they go quiet, then mildly critical, then quietly route their team to a competitor. By the time it lands in a status meeting, the PM has lost 4-6 weeks. This methodology defines: an opt-in scope of source artefacts per stakeholder (with retention and consent rules), a fixed classification rubric (supportive / cautious / hostile, with concrete linguistic markers), a weekly run that produces a per-stakeholder score AND a trend line, and an alarm policy — two consecutive weeks of decline OR one week's classification as hostile triggers a documented PM action plan. The output lives in the rescue runbook and is the canonical early-warning artefact for `distressed-project-diagnostic-script`.

**Ефективно для:** PM на distressed-проєкті, який хоче побачити, що спонсор тихо червоніє, ДО офіційного статус-мітингу.

## Applies If (ALL must hold)

- Project is either on a 90-day rescue track OR has at least one sponsor whose engagement is critical to renewal.
- Written consent or organisational policy permits the PM to ingest the named source artefacts for sentiment tracking.
- The PM has access to per-stakeholder text streams (email aliases, Slack DMs, meeting transcripts) — not just public channels.
- A scheduling primitive (cron, scheduled remote agent) is available to run the weekly pipeline.

## Skip If (ANY kills it)

- No consent to ingest the artefacts — the methodology is non-negotiable on consent.
- Stakeholder pool is fluid (changes weekly) — register is not stable enough to track trends.
- Project length under 8 weeks — trend signal needs at least 4 weekly data points to be useful.
- Pure internal team with no external sponsors and no political risk — overhead exceeds value.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Stakeholder register | YAML / CSV | rescue runbook |
| Per-stakeholder source list | YAML | rescue runbook |
| Consent record | YAML / signed doc | legal / org policy |
| Classification rubric | YAML | this methodology's `templates/` |
| Output storage path | dir / repo | `rescue/sentiment/` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/distressed-project-diagnostic-script` | This is the early-warning input to that script's rescue plan. |
| `geek/ai-core/rag-engineer` | Underlying retrieval + classification mechanics for text artefacts. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: consent-first, three-class rubric, weekly cadence, two-week alarm, 72h action-plan | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns + self-check | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (symptom / root-cause / fix) | ~900 |
| `content/06-decision-tree.xml` | essential | Can-run gate + alarm-or-no branch | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ingest-and-rubric-match` | haiku | Marker matching against a closed vocabulary — cheap, deterministic. |
| `classify-with-markers` | sonnet | Per-stakeholder judgment when markers are mixed; cites markers in output. |
| `alarm-and-action-plan-draft` | opus | Synthesises hypothesised cause + intervention from trend + recent artefacts. |

## Templates

| File | Purpose |
|------|---------|
| `templates/header.yaml` | Frontmatter schema: owner, version, last_reviewed, consent_root, rubric_path. |
| `templates/skeleton.md` | Weekly sentiment-run report skeleton with per-stakeholder block + alarm block. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-sentiment-tracker.py` | Validate a weekly run JSON against the output contract (consent dates, three-class output, trend length, alarm/action-plan pairing). | After every weekly run, before commit. |

## Related

- [[ramp-task-difficulty-ladder]] — peer operating artefact in the same PM space.
- [[team-charter-working-agreement]] — peer methodology shaping how the team handles trust signals.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` gates the run on consent + project length + register stability, then branches on whether the current week shows a 2-week decline or single-week hostile signal. If consent is missing → block; if window too short → skip; if a decline triggers → fire alarm and require an action plan within 72h before the next run.
