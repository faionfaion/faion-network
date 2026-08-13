# Distribution Channel Research

## Summary

**One-sentence:** Bullseye-style channel evaluation: shortlist 3 of 19 channels, run small-budget tests (<=$500 each), score on CAC + reach + time-to-signal, lock the top 1-2 channels with stop-loss tripwires.

**One-paragraph:** Methodology to evaluate distribution channels (Traction's 19 + AI-era variants) without spreading budget thin. Shortlist 3 channels with the highest fit signal, run bounded small-budget tests (<=$500 each), score each on CAC + reach + time-to-signal + retention-of-channel-customers, and lock the top 1-2 with explicit stop-loss tripwires. Output: channel-report.md with the picked channels + tripwires + test results.

**Ефективно для:**

- Pre-launch або post-PMF: треба обрати 1-2 канали з 19 кандидатів без розпорошення бюджету.
- Бюджет на тестування <= $5k загалом; на канал <= $500.
- Сегмент ICP стабільний (не міняється кожного тижня).
- Маркетинговий найм або agency selection - треба обґрунтувати канал чисельно.
- Channel fatigue: один канал давав CAC, тепер CAC виріс 3x - треба перетестувати.

## Applies If (ALL must hold)

- Pre-launch or post-PMF: must select 1-2 channels from 19 candidates without budget spread.
- Test budget <= $5k total, <=$500 per channel.
- Stable ICP segment (does not change weekly).
- Marketing hire or agency selection requires a numeric channel justification.
- Channel fatigue: one channel that delivered CAC X now delivers 3x; retest needed.

## Skip If (ANY kills it)

- Pre-MVP with no product to attribute conversion to.
- Single channel mandated by the platform (e.g., Shopify App Store).
- Regulated industry where most channels are off-limits.
- Pure organic / word-of-mouth strategy that does not pay for acquisition.
- Investor-driven 'spend the round in 90 days' mandate - run a different playbook.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Persona doc | markdown | persona-building output |
| ARPU + payback target | CSV | business-model-research output |
| Test budget cap | decimal USD | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[persona-building]] | supplies the ICP that filters channel fit signals |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `channel-shortlist` | sonnet | Score 19 channels against persona + product shape. |
| `test-design` | sonnet | Design <=$500 test per channel with explicit stop-loss. |
| `results-score` | haiku | Mechanical CAC + reach + time-to-signal calculation. |
| `verdict` | sonnet | Pick top 1-2 with tripwires. |

## Templates

| File | Purpose |
|------|---------|
| `templates/channels.yaml` | Channel catalog with fit signals and tooling notes |
| `templates/channel-fit-scorer.py` | Score each channel on fit + cost + speed + measurability |
| `templates/channel-report.md` | Channel-evaluation report skeleton: shortlist + tests + tripwires |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-distribution-channel-research.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[business-model-research]]
- [[persona-building]]
- [[market-research-tam-sam-som]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/channels.yaml`

```yaml
# channels.yaml — input for channel-fit-scorer.py
# Scores 1-5 per criterion. Edit for your product context.
# audience: target users present on this channel (1=low, 5=high)
# competitors: competitors actively using this channel (1=none, 5=all)
# cost: cost to run a meaningful test (1=very expensive, 5=very cheap)
# time: speed to see meaningful results (1=very slow, 5=immediate)
# scale: long-term scalability potential (1=capped, 5=unlimited)
# capability: team's current ability to execute (1=none, 5=expert)

channels:
  - name: SEO
    scores:
      audience: 5
      competitors: 5
      cost: 4
      time: 2
      scale: 5
      capability: 4

  - name: LinkedIn Ads
    scores:
      audience: 4
      competitors: 4
      cost: 2
      time: 5
      scale: 4
      capability: 3

  - name: Referral Program
    scores:
      audience: 3
      competitors: 2
      cost: 5
      time: 3
      scale: 3
      capability: 5
```

### `templates/channel-fit-scorer.py`

```python
# channel_fit_scorer.py — score channels vs fixed weights, emit ranked markdown table
# Input: channels.yaml with channel scores per criterion
# Output: ranked markdown table to stdout
# Usage: python channel_fit_scorer.py channels.yaml
import sys, yaml

WEIGHTS = {
    "audience":    0.25,
    "competitors": 0.15,
    "cost":        0.20,
    "time":        0.15,
    "scale":       0.15,
    "capability":  0.10,
}


def weighted_score(ch: dict) -> float:
    return round(sum(ch["scores"][k] * w for k, w in WEIGHTS.items()), 2)


def main(path: str) -> None:
    data = yaml.safe_load(open(path))
    rows = [(c["name"], c["scores"], weighted_score(c)) for c in data["channels"]]
    rows.sort(key=lambda r: -r[2])

    cols = list(WEIGHTS.keys())
    header = "| Channel | " + " | ".join(cols) + " | Total |"
    sep = "|" + "---|" * (len(cols) + 2)
    print(header)
    print(sep)
    for name, sc, total in rows:
        cells = " | ".join(str(sc.get(k, "-")) for k in cols)
        print(f"| {name} | {cells} | {total} |")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "channels.yaml")
```
