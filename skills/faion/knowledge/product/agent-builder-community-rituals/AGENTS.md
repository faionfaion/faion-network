# Agent-Builder Community Rituals

## Summary

**One-sentence:** A calendar of weekly / biweekly / monthly rituals (office hours, eval-sharing, prompt-swap) plus per-ritual artefact templates and a 90-day retention metric, so isolated LLM-agent developers turn into a learning community instead of yet another dying meetup.

**One-paragraph:** LLM agent developers cite "no shared corpus / community of fellow agent builders" as a top pain. Optional events drift to zero attendance in 8-12 weeks; pure-discussion meetups do not compound. This methodology pins a calendar of named rituals each with cadence (weekly / biweekly / monthly slot in UTC), format (office hours / eval-sharing / prompt-swap), exit-criteria, rotating host (every 4-6 sessions), a versioned artefact per session (eval row added, prompt diff committed, runbook updated), and a public chronological log updated within 48h. Below 30% 90-day retention triggers ritual-design review.

**Ефективно для:** organiser, який запускає community агент-білдерів і не хоче, щоб група вмерла за 8 тижнів від "як справи, нічого нового".

## Applies If (ALL must hold)

- ≥5 builders willing to commit 2-4h/month.
- Shared infra exists (Discord / Slack + docs store + calendar).
- ≥1 organiser with authority to enforce the cadence.
- Builders share at least one technical interest (eval, prompt, infra, RAG).
- Code-of-conduct is published and enforced.

## Skip If (ANY kills it)

- <5 builders — group too small; do 1:1 mentorship instead.
- No shared infra and no budget for it — rituals collapse.
- Purely social meetup with no artefact intent — use a meetup playbook, not this.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| List of founding members | CSV / YAML | organiser |
| Discord / Slack workspace | URL | organiser-owned infra |
| Docs root | Notion / Outline / GitHub | organiser-owned infra |
| Code of conduct | markdown | community charter |
| Calendar | iCal / Google Cal | organiser-owned infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | Parent skill — provides operating context for this methodology. |
| `geek/ai-core/llm-evaluation` | Peer methodology — feeds eval-sharing ritual. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: cadence-not-vibes, artefact-per-ritual, public log, rotating host, 90-day retention metric | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Group-size gate + retention-trend branch | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_calendar` | haiku | Template fill from cadence + UTC slot list. |
| `design_ritual_format` | sonnet | Per-ritual judgment: exit criteria, artefact type, host rotation. |
| `retention_review` | opus | Cross-session synthesis when retention drops below 30%. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ritual-calendar.yaml` | Cadence + slot + ritual-id matrix. |
| `templates/ritual-artefact.md` | Per-session log skeleton (date, host, attendees, artefact link, retention update). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-builder-community-rituals.py` | Validate calendar + per-session log against rule set (cadence, host rotation, artefact link, 90-day retention). | Weekly after each ritual. |

## Related

- [[ai-product-success-metrics-catalog]] — peer geek-product methodology consuming the retention metric.
- [[segment-aware-design-system]] — sibling methodology for product-experience rituals.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks builder count + organiser availability. If <5 builders → skip and do 1:1. If 90-day retention drops below 30% → block calendar continuation and run a ritual-design review. Otherwise → emit the calendar.
