# AI Overview Presence Tracker

## Summary

**One-sentence:** Generates a per-query AIO presence report: aio_present, citations, our_domain_cited, selected_snippet, panel_position over an 8-week window.

**One-paragraph:** Generates a per-query AIO presence report: aio_present, citations, our_domain_cited, selected_snippet, panel_position over an 8-week window. Use it when growth marketer має >= 20 indexed pages таргетуючих aio queries. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Growth marketer має >= 20 indexed pages таргетуючих AIO queries.
- Weekly Search Console + analytics review — існуюча cadence.
- Stable AIO scrape adapter (SE Ranking або equivalent) налаштовано.
- 8-week trend view per query доступний для retrofit prioritization.

## Applies If (ALL must hold)

- A scrape adapter (SE Ranking or equivalent) returns AI Overview panels with their citation URLs for the chosen country, language and device.
- At least 20 queries can be mapped one-to-one to indexed pages on the tracked domain.
- The team can scrape every query once a week on the same weekday for 8 weeks without changing country, language, device or logged-out state.
- Search Console impressions per query are available for the window, to rank the retrofit list.
- A weekly Search Console and analytics review already exists where the report is read.

## Skip If (ANY kills it)

- AI Overviews are not available in the target country and language, or the adapter returns no panels: there is nothing to track.
- Fewer than 20 queries map to pages on the domain: extend the set first; a smaller set moves the rate by more than five points per query.
- The question is how many clicks AI Overviews cost: Search Console does not separate AIO traffic, and this tracker reports presence and citation only.
- The query list or scrape configuration must change every week: the trend is not comparable; freeze them or do not report a trend.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Query set | at least 20 rows: query, target URL on the tracked domain | Search Console queries mapped to pages |
| Scrape adapter output | per query per week: panel present, cited URLs, snippet text, panel position | SE Ranking AIO tracker or equivalent, logged-out session |
| Scrape configuration | country, language, device, logged-out flag, AIO availability confirmed | adapter settings + Google Search Central availability list |
| Search Console impressions | impressions per query for the window | Search Console performance export |
| Tracked domain and subdomains | registrable domain plus any subdomains that count as ours | tracker config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: fixed 20-query set, typed per-query rows, fixed locale and device, weekly no-interpolation, exact host match for citation, presence and citation-rate denominators, no click attribution, 5-of-8 retrofit rule | 1800 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the report: versioned 20-query set with target URLs, fixed scrape config, per-query weekly rows (present / citations / cited / snippet / position, missing weeks as nulls), the three metrics with denominators per week and window, co-occurrence findings, retrofit list gated on 5-of-8 and 4 uncited weeks; valid and invalid reports; 8 forbidden patterns | ~8800 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 7 steps: freeze the versioned query set, pin the scrape configuration, scrape weekly and record failures as missing, set citation by host match, compute the three metrics, write co-occurrence findings, build the retrofit list and validate | ~1500 |
| `content/05-examples.xml` | recommended | Complete 8-week report for a CRM vendor (rows for 4 of 20 queries, one missing week, presence 0.806, citation 0.32, two-entry retrofit list) with a note per value, plus the report as usually run and what the validator prints | ~6550 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-ai-overview-presence-tracker.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-overview-presence-tracker.report.md.j2` | Markdown report skeleton: query set and window, scrape configuration, queries, weekly rows, metrics with denominators, findings, retrofit list |
| `templates/ai-overview-presence-tracker.report.md` | Markdown report skeleton: query set and window, scrape configuration, queries, weekly rows, metrics with denominators, findings, retrofit list. Generated from `templates/ai-overview-presence-tracker.report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ai-overview-presence-tracker.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-overview-presence-tracker.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
