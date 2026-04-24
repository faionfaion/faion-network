# Reclass Tick Instructions

Fire at the start of each 5-min cron tick. Execute steps in order.

**Working dir:** `/home/nero/workspace/projects/faion-net/faion-network`

## Step 1 — queue check

Read `skills/faion-knowledge/.reclass/candidates.ambiguous.tsv`. If missing or 0 lines:

1. If there are staged/unstaged changes under `skills/faion-knowledge/knowledge/`, commit them: `refactor: reclass final batch`.
2. `git push origin main`.
3. Invoke `CronList` → find the cron whose prompt references `TICK.md` → `CronDelete` it.
4. Tell user: "tier reclass complete — N methodologies reviewed across M rounds."
5. Stop this tick.

## Step 2 — load rubric

Read `skills/faion-knowledge/.reclass/RULES.md` sections **Tier definitions** and **Decision procedure**.

## Step 3 — take next 40 paths

```
head -n 40 skills/faion-knowledge/.reclass/candidates.ambiguous.tsv
```

Each line is `current_tier\tunknown\tambiguous\tpath`.

## Step 4 — classify each

For each of the 40 paths:
1. Read the methodology's `README.md` — first 50 lines only.
2. Decide tier per RULES §"Tier definitions":
   - **geek** — subject is AI / LLM / ML / agents / RAG / multimodal / Claude-specific / prompt engineering / vector DBs / embeddings
   - **pro** — enterprise stacks, scale patterns, distributed systems, Kubernetes/Terraform, formal PM (SAFe, PMBoK), BA modeling (BPMN/UML), WCAG, paid marketing, formal research, HR
   - **solo** — solopreneur craft: API design, architecture basics, MVP/roadmap, single-server ops, content/technical-SEO, SDD, customer dev
   - **free** — genuine entry-level single-dev material with no enterprise/AI/scale context
3. If tier matches the current tier in the path → no move.
4. Else queue a move: `knowledge/<new_tier>/<group>/<domain>/<methodology>/`.

**Conservative bias:** when in doubt between two tiers, keep the current tier. Only move on strong signal.

**Never downgrade to `free`** unless README explicitly frames the content as "basics of X" where X is a broadly free-tier subject (common language features, git, unit testing).

## Step 5 — apply moves

For each queued move, from repo root:
```bash
mkdir -p "$(dirname destination)"
git mv source destination
```

Append to `skills/faion-knowledge/.reclass/decisions.log` (one line per decision):
```
MOVED\t<source>\t-> <destination>
KEPT\t<path>\t(reason)
```

## Step 6 — trim queue

Remove the processed 40 lines:
```bash
sed -i '1,40d' skills/faion-knowledge/.reclass/candidates.ambiguous.tsv
```

## Step 7 — commit if enough moves

If ≥5 moves applied in this tick:
1. Find last "round N" number in `git log --oneline --grep='reclass.*round'`, pick N+1.
2. `git add -A && git commit -m "refactor: reclass <N_moved> methodologies (round <N+1>)"`.
3. Do NOT push every tick — push every 3rd tick or at the end.

## Step 8 — report

One line to user: `Tick: <N_moved> moved, <remaining> ambiguous remaining.`
