# Competitive Intelligence

## Summary

**One-sentence:** Continuous CI pipeline that splits mechanical collection (Haiku) from strategic synthesis (Opus); produces dated weekly digests, monthly threat assessments, and battlecards with a hard 14-day TTL.

**One-paragraph:** Point-in-time competitor snapshots go stale within weeks. This methodology builds a continuous CI pipeline where six subagents split mechanical collection (Haiku) from strategic synthesis (Opus), publish weekly digests, monthly threat assessments, and battlecards with a hard 14-day TTL. Every claim must cite a fetched URL, every URL passes a fact-checker HEAD request before distribution.

**Ефективно для:**

- Live B2B/SaaS ринок, де конкуренти шиплять щотижня та змінюють pricing.
- Sales team потребує свіжих battlecards (deal cycle > 30 днів робить stale-дані видимими).
- Roadmap-рішення заблоковані на feature parity або диференціації.
- Funding / M&A / executive-hire сигнали мають з'являтись у вікні 24h.
- Вже маєте 3+ названих direct competitors з стабільними URL для моніторингу.

## Applies If (ALL must hold)

- Live B2B/SaaS market where competitors ship weekly and pricing changes often.
- Sales team needs current battlecards; deal cycle > 30 days exposes stale data fast.
- Product roadmap decisions are blocked on feature parity or differentiation gaps.
- Funding, M&A, or executive-hire signals must surface within 24 hours.
- You already have 3+ named direct competitors with stable URLs to track.

## Skip If (ANY kills it)

- Pre-PMF or category-creation phase — competitors are not the bottleneck.
- Fewer than 5 known competitors — a manual quarterly snapshot beats infrastructure overhead.
- Highly regulated or closed markets (defense, sealed bids) where public signals are noise.
- Personal projects with no GTM motion — output has no consumer.
- When the team will not act on alerts — CI without an action loop is theater.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Watchlist | YAML (competitor, URLs, signal types) | GTM team + sales |
| Positioning doc | markdown | marketing |
| Win/loss interview notes | markdown / transcripts | sales ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[competitor-analysis]] | supplies the seed competitor list and positioning baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 7-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ci-collector` | haiku | Mechanical polling of YAML watchlist. |
| `ci-classifier` | haiku | Tag events by signal type; near-deterministic. |
| `ci-synthesizer` | sonnet | Weekly digest writing with cited sources. |
| `ci-threat-analyst` | opus | Strategic threat scoring + scenario planning. |
| `ci-battlecard-writer` | sonnet | Per-competitor battlecard regeneration. |
| `ci-fact-checker` | sonnet | Adversarial pass: every claim cites a HEAD-validated URL. |

## Templates

| File | Purpose |
|------|---------|
| `templates/watchlist.yaml` | Input config: competitor + URLs + signal types |
| `templates/ci-collector.py` | Minimal collector: fetches watchlist URLs and emits NDJSON delta events |
| `templates/battlecard.md.j2` | Per-competitor battlecard skeleton with 14-day TTL stamp |
| `templates/battlecard.md` | Per-competitor battlecard skeleton with 14-day TTL stamp Generated from `templates/battlecard.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/weekly-digest.md.j2` | Weekly digest skeleton with event-id provenance |
| `templates/weekly-digest.md` | Weekly digest skeleton with event-id provenance Generated from `templates/weekly-digest.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-competitive-intelligence.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[competitor-analysis]]
- [[trend-analysis]]
- [[continuous-discovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/watchlist.yaml`

```yaml
# watchlist.yaml — input config for ci-collector.py
# One entry per competitor; list all URLs to monitor and their signal type.
competitors:
  - name: CompetitorA
    type: pricing
    urls:
      - https://competitora.com/pricing
      - https://competitora.com/changelog
  - name: CompetitorB
    type: site
    urls:
      - https://competitorb.com
      - https://competitorb.com/features
```

### `templates/ci-collector.py`

```python
# ci_collector.py — schedule via cron hourly
# Input: watchlist.yaml (competitors with urls and signal types)
# Output: events.ndjson (one JSON event per delta detected)
import json, hashlib, pathlib, datetime, httpx, yaml

WATCH = yaml.safe_load(open("watchlist.yaml"))
STATE = pathlib.Path(".ci_state"); STATE.mkdir(exist_ok=True)
EVENTS = pathlib.Path("events.ndjson")


def fetch(url: str) -> str:
    """Fetch URL via Jina reader for LLM-ready text extraction."""
    r = httpx.get(f"https://r.jina.ai/{url}", timeout=30)
    r.raise_for_status()
    return r.text


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def emit(event: dict) -> None:
    event["ts"] = datetime.datetime.utcnow().isoformat() + "Z"
    with EVENTS.open("a") as f:
        f.write(json.dumps(event) + "\n")


for competitor in WATCH["competitors"]:
    for url in competitor["urls"]:
        try:
            body = fetch(url)
        except Exception as e:
            emit({"competitor": competitor["name"], "url": url, "error": str(e)})
            continue
        fp_path = STATE / hashlib.md5(url.encode()).hexdigest()
        prev = fp_path.read_text() if fp_path.exists() else ""
        cur = fingerprint(body)
        if cur != prev:
            emit({
                "competitor": competitor["name"],
                "url": url,
                "signal_type": competitor.get("type", "site"),
                "excerpt": body[:2000],
            })
            fp_path.write_text(cur)
```
