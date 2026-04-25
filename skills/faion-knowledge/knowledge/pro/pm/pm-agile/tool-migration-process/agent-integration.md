# Agent Integration — Cross-Tool Migration (Process)

## When to use
- You've completed mapping and audit (`tool-migration-basics`) and need a phase-by-phase execution playbook.
- Org-wide migration touching ≥3 teams, ≥1k issues, or any compliance scope.
- Multi-wave migrations where teams cut over in batches over weeks.
- Cutover windows requiring rollback rehearsal and freeze coordination.
- Post-merger consolidation requiring two source tools → one target.

## When NOT to use
- Single-team or <100 issue migration — use the basics + a one-day cutover.
- Vendor-managed migration where their tooling does extract/transform/load — defer to it.
- Live, no-freeze migrations of an active product launch — defer to a quieter window.
- Migrations whose primary risk is political (team adoption), not technical — invest in change management instead of process detail.

## Where it fails / limitations
- Phase durations from the README are guidance, not law; novel custom-field setups blow up the Preparation phase.
- "Pilot project" selection bias — picking the simplest team makes the pilot succeed and gives false confidence.
- Cutover windows assume linear API access; rate limits routinely double the planned downtime.
- Stabilization always overruns; budget 2× the planned support window.
- Rollback only works if no critical data was created in the target during cutover — a single shipped feature with target-only context can pin you.
- Mid-migration "small scope additions" silently double the work; freeze the mapping spec at the end of Preparation.

## Agentic workflow
A planning agent owns Phase 1–2 artifacts: scope doc, mapping spreadsheet, risk register, comms calendar. A migration-engine agent (built around the Python ETL skeleton in README) handles Phase 3–4 in dry-run-first mode, with checkpointing per wave. A cutover agent runs the T-24 / T-4 / T-0 / T+1 / T+24 / T+1w checklist, posting status to Slack at each milestone. A retrospective agent ingests post-migration metrics + tickets and drafts the lessons-learned doc.

### Recommended subagents
- `migration-planner` — produces the project plan Markdown from scope inputs, risk register, comms calendar.
- `migration-engine` — runs Extract → Transform → Load with dry-run flag, checkpoint files, ID mapping JSON.
- `cutover-runner` — executes the checklist top-to-bottom, halts on validation failure, posts status updates.
- `link-fixer` — runs after main migration; updates issue links in commit messages, wikis, Slack archives via search/replace bots.
- `migration-retro` — collects user-feedback survey + support tickets, produces lessons-learned doc.

### Prompt pattern
```
You are migration-engine running in dry-run mode. Inputs: source export (JSONL),
field mapping (YAML), target schema (JSON). For each source record output a JSON object
matching target schema with a `_source_id` field. Set `_validation_errors` array per
record where mapping failed. Do not call any APIs. Do not invent fields.
```

```
You are cutover-runner. Input: checklist YAML with steps, owners, validation commands.
Execute one step at a time. Wait for the command's exit code. If non-zero, halt and emit
{step, command, exit_code, stdout, stderr} as JSON. Never skip steps. Never run two in parallel.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` / Linear GraphQL / `gh` / `az devops` | Source/target API drivers | per-tool docs |
| `parallel` (GNU) | Batch ETL with controlled concurrency + retries | `apt install parallel` |
| `flock` | Single-writer cutover lock for shared state | coreutils builtin |
| `restic` / `rclone` | Backup source attachments before cutover | https://restic.net |
| `dataset` (Python) | SQLite staging for ID mapping + checkpoints | `pip install dataset` |
| `httpx` (Python) | Async HTTP client with retry/backoff for migration engine | `pip install httpx[http2]` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Unito | SaaS sync | Yes — REST API | Two-way mirror during parallel run; useful for soft cutover. |
| Exalate | SaaS | Yes — Groovy | Programmable sync rules; good for partial scope migration. |
| Atlassian Jira Cloud Migration Assistant | SaaS | No — UI | Server→Cloud only; not for cross-vendor. |
| Solidify Migrator | SaaS | No — UI | Azure DevOps ↔ Jira; CMMI safe. |
| Linear Importer | SaaS | Partial — JSON upload | Good for one-shot, not for incremental waves. |
| Slack / Teams (notifications) | SaaS | Yes — Webhooks | Post each phase milestone for stakeholder transparency. |
| 1Password / Vault | SaaS / OSS | Yes — CLI | Store source + target API tokens; rotate post-cutover. |

## Templates & scripts
See `templates.md` for the project plan, cutover checklist, and rollback playbook. Inline checkpointed loader (`scripts/load_resume.py`):

```python
#!/usr/bin/env python3
"""Load JSONL of target-shaped issues; resumes from .checkpoint on rerun."""
import json, os, sys, time, requests

CHECKPOINT = ".load_checkpoint"
done = set(open(CHECKPOINT).read().split()) if os.path.exists(CHECKPOINT) else set()
URL = os.environ["TARGET_API_URL"]; TOK = os.environ["TARGET_TOKEN"]

with open(CHECKPOINT, "a") as ck:
    for line in sys.stdin:
        rec = json.loads(line); sid = rec["_source_id"]
        if sid in done: continue
        for attempt in range(5):
            r = requests.post(URL, json=rec, headers={"Authorization": TOK})
            if r.status_code < 300: break
            if r.status_code == 429:
                time.sleep(2 ** attempt); continue
            sys.exit(f"FAIL {sid}: {r.status_code} {r.text[:200]}")
        ck.write(sid + "\n"); ck.flush()
        print(f"OK {sid} -> {r.json()['id']}")
```

## Best practices
- Run a full dry-run on production data into a sandbox target one week before cutover; measure exact runtime, then add 50% buffer.
- Migrate in waves by team or by project, not by record-type (so each team gets a complete-feeling tool, not a half-mirror).
- Keep the source read-only for ≥30 days post-cutover; cheap insurance.
- Cutover on Friday afternoon if the org tolerates a quiet weekend; never mid-week.
- Pre-write the rollback comms — "we are reverting to <source> while we resolve <issue>" — so you can ship it in seconds.
- Always validate three numbers (issues, comments, attachments-by-byte) and 50 random sampled items by hand before declaring success.
- Decommission source on a calendar reminder, not on a vibe; teams will stay on it for years if you don't force the move.

## AI-agent gotchas
- Long-running migrations exceed agent token budgets; design the engine as a CLI tool the agent invokes, not as inline LLM calls.
- LLMs love to "fix" mappings on the fly — explicitly forbid runtime mapping mutation; mapping is frozen at start.
- A successful Phase 4 with 99.5% success looks fine, but the missing 0.5% is always the most-linked tickets. Force-list them.
- Cutover checklist: agents mark steps complete based on stdout text matches, which lie. Use exit codes, not greps.
- Comment / mention preservation needs user-ID resolution; agents that skip this strip @mentions silently.
- Webhook-based comms can spam channels under retry storms; rate-limit notifications, prefer one summary per phase.
- Token costs balloon if agents read raw issue bodies; pre-summarize to ≤200 tokens per record before reasoning.

## References
- See sibling `tool-migration-basics` for assessment, mapping, change-management.
- https://www.prosci.com/methodology/adkar — change-management framework
- https://martinfowler.com/articles/branching-patterns.html — analogous "release train" thinking
- "Release It!" (Michael Nygard) — failure-mode patterns applicable to cutovers
- https://sre.google/sre-book/release-engineering/ — SRE-style staged rollouts
