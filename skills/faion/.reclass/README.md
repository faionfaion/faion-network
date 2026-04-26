# Tier Reclassification State

Intra-domain tier reclassification for faion methodologies.

## Files

| File | Purpose |
|------|---------|
| `RULES.md` | Tier classification rubric + name heuristics + move target rule |
| `inventory.txt` | All 1279 methodology paths (source of truth snapshot) |
| `heuristic.sh` | Name-based tier guess → writes `candidates.tsv` |
| `filter.sh` | Safe-move filter → writes `candidates.safe.tsv`, `candidates.skip.tsv`, `candidates.ambiguous.tsv` |
| `move.sh` | Applies `candidates.safe.tsv` via `git mv` → writes `decisions.log`, `candidates.applied.tsv` |
| `candidates.tsv` | Name-heuristic output: `current \t guess \t verdict \t path` (verdict: keep/move/ambiguous) |
| `candidates.safe.tsv` | High-confidence moves approved for automated application |
| `candidates.skip.tsv` | Moves rejected by filter (heuristic false positives) |
| `candidates.ambiguous.tsv` | Methodologies with no clear name signal — need content review |
| `candidates.applied.tsv` | Moves successfully applied |
| `decisions.log` | Append-only audit log of move operations |

## Rerun

```bash
bash skills/faion/.reclass/heuristic.sh  # regenerate candidates.tsv
bash skills/faion/.reclass/filter.sh     # regenerate safe/skip/ambiguous
bash skills/faion/.reclass/move.sh       # apply candidates.safe.tsv
```

## Progress

- **Round 1 (name heuristic):** 90 safe upgrades applied (free→pro/solo/geek, solo→pro/geek, pro→geek/solo)
- **Remaining ambiguous:** 1009 methodologies — processed per loop tick via README content read
