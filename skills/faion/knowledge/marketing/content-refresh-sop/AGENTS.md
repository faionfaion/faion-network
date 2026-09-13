# Content Refresh SOP

## Summary

**One-sentence:** Playbook step: scores each evergreen URL on refresh / consolidate / kill / leave matrix and runs a 9-step refresh checklist.

**One-paragraph:** Playbook step: scores each evergreen URL on refresh / consolidate / kill / leave matrix and runs a 9-step refresh checklist. Use it when url_age_months >= 12 для evergreen content. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- url_age_months >= 12 для evergreen content.
- Impressions trend, top-position decay, intent shift signals доступні.
- GSC + GA4 + rank-tracker integrated в один dataset.
- Готовність до 90-day post-refresh re-evaluation.

## Applies If (ALL must hold)

- The inventory tags evergreen content and records publish dates, so URLs at least 12 months old can be selected.
- Search Console, GA4 and a rank tracker can each be read per URL for a trailing window and an equal prior window; spans over 16 months come from a persisted Search Console export.
- The team can write numeric thresholds for impressions trend, position decay and intent shift before scoring.
- Writers can execute all nine refresh steps, engineering can ship 301 / 308 redirects and 410 responses, and someone will re-score at day 90.

## Skip If (ANY kills it)

- The content is news, release notes, dated announcements or campaign pages: it decays by design and is not refreshed.
- The URL is under 12 months old: its curve cannot be separated from launch effects and seasonality.
- Only one data source is available (GSC alone or GA4 alone): a verdict from a single source is invalid; complete the dataset first.
- The request is a slug or domain migration: that is a separate migration decision, not a refresh.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Evergreen inventory | url, content type, publish date, url_age_months | CMS export |
| Search Console performance export | per page: clicks, impressions, average position for the trailing and prior windows | bulk data export or scheduled API pull (UI keeps 16 months) |
| GA4 landing-page report | per landing page: sessions, key events, both windows | GA4 explorations or API |
| Rank tracker export | per URL: target query and position, both windows | rank tracker (Ahrefs, Semrush, SE Ranking or equivalent) |
| Thresholds | three numbers: impressions trend percent, position decay, query-mix change percent | SEO lead, before scoring |
| Top-ranking pages for each target query | SERP capture on the scoring date | manual or SERP API |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: evergreen 12-month eligibility, GSC+GA4+rank dataset, thresholded signals, exhaustive verdicts, consolidate 301, kill 410, URL and honest date, nine-step checklist, 90-day baseline | 2600 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the playbook step: thresholds, equal windows with source, per-URL rows with GSC / GA4 / rank dataset for both windows, computed signals, one verdict and its block (nine-step refresh with unchanged URL, baseline and day-90 re-score; consolidate with redirect map; kill with 410 and no redirect; leave with reason), decision branches; valid and invalid steps; 8 forbidden patterns | ~5900 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 8 steps: thresholds and windows, eligible URLs, three-source dataset, signals and one verdict, consolidate with redirects, kill with 410, refresh through the nine steps, validate and schedule the day-90 re-score | ~1650 |
| `content/05-examples.xml` | recommended | Complete playbook step for two evergreen guides (one refresh through all nine steps at -32 percent impressions with a day-90 re-score, one leave inside thresholds) with a note per value, plus the usual playbook step and what the validator prints | ~2850 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-content-refresh-sop.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/content-refresh-sop.playbook-step.md.j2` | Markdown playbook-step skeleton: thresholds, window, decision branches, URL rows with the three-source dataset, refresh / consolidate / kill / leave blocks |
| `templates/content-refresh-sop.playbook-step.md` | Markdown playbook-step skeleton: thresholds, window, decision branches, URL rows with the three-source dataset, refresh / consolidate / kill / leave blocks. Generated from `templates/content-refresh-sop.playbook-step.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/content-refresh-sop.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-content-refresh-sop.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
