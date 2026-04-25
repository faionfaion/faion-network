# Agent Integration — Cross-Tool Migration (PM Tools)

## When to use
- Migrating a portfolio between Jira, Linear, Asana, ClickUp, Monday, GitHub Projects, GitLab Issues, Azure DevOps, Notion, Trello, Pivotal Tracker, Shortcut, Wrike, ServiceNow, etc.
- Consolidating after an acquisition (two trackers → one) or a tooling decree (procurement / cost / standards).
- Splitting a single tracker into multiple tools (e.g., engineering → Linear, marketing → Asana, support → Zendesk).
- Cloud relocation (Jira Server/Data Center → Cloud) within the same vendor (still a migration; same risk profile).
- Pairing with `pm-tool-selection/` (decide first), `change-control/` (cutover gate), `communications-management/` (the change comms plan), `lessons-learned/` (post-cutover).

## When NOT to use
- Tool unhappiness without root-cause diagnosis — most "we hate Jira" complaints reduce to bad workflows or admin neglect; fix that first, migrating moves the problem.
- Active feature freeze period (release lock, audit window, year-end close) — wait until traffic dips.
- Solo / very small teams (<10 users, <500 issues) — copy by hand, do not build a pipeline.
- When the source tool has critical custom plugins (e.g., Tempo time-tracking, Insight asset mgmt) without target equivalents — fix the gap before migration, not during.

## Where it fails / limitations
- Field-mapping fidelity is a long tail. Status, priority, and labels migrate cleanly; custom fields, parent links, sprint history, time logs, and audit history almost never do.
- Attachments, inline images, and rich-text (panels, expanders, code macros) lose formatting; LLM-driven cleanup helps but is imperfect.
- User identity remapping fails silently — orphaned assignees, deactivated accounts, mismatched emails. The migration says "success" while losing accountability.
- Issue links (blocks, relates, duplicates, subtask) require a two-pass migration (create issues, then link by ID map). Single-pass migrations lose all links.
- Permissions and project roles do not translate; target ACLs must be designed from scratch.
- Automations / webhooks / integrations (Slack notifs, CI hooks, deploy triggers) break at cutover; many are discovered only when they stop firing.
- Reporting history (velocity charts, dashboards, gadgets) is rarely portable — past performance graphs may need to be recreated as static screenshots.

## Agentic workflow
Treat migration as ETL: a config file (`migration.yaml`) declares source, target, field/status/priority maps, dry-run flag, and id-mapping output path. A subagent runs Extract → Transform → Validate → Load in waves; every step is idempotent and writes a JSONL audit log to git. Human gates between extract validation, pilot wave, and full waves. Never let the agent run a destructive cutover (read-only on source, decommission) — that is a human decision after a 2-week soak.

### Recommended subagents
- `faion-sdd-executor-agent` — owns migration as a feature with TASK_field_map_design, TASK_extract_dry_run, TASK_pilot_wave, TASK_full_wave, TASK_link_pass, TASK_cutover, TASK_decommission. Each task = commit + execution report.
- A custom `migration-config-agent` (model: opus per README "strategic decision"): designs field/status/priority maps from sample issues; flags low-confidence mappings for human review.
- A custom `extract-validator-agent` (model: sonnet): runs extract dry-runs, diffs source ↔ target counts, flags lossy fields.
- A custom `transform-runner-agent` (model: haiku): executes the deterministic transform engine; raises on schema violations, never invents values.
- A custom `link-pass-agent` (model: haiku): builds blocks/relates/parent-child links using the id-map after the create pass.
- A custom `cutover-runbook-agent` (model: sonnet): generates the T-24/T-4/T+1/T+24/T+1w runbook from the README cutover checklist, customized to the actual tools.
- `password-scrubber-agent` — runs over migration logs and exports; tickets often contain credentials, internal URLs, customer PII.

### Prompt pattern
Two stages: mapping design → execution.

```
You are the migration-config agent. Inputs:
1. Sample of 100 source issues (random + 20 outliers).
2. Target tool's field schema (custom fields, allowed enums).
3. README field/status/priority sections.

Emit STRICT YAML matching MigrationConfig:
field_mapping: { source_field: target_field, ... }
status_mapping: { source_status: target_state, ... }
priority_mapping: { ... }
unmapped_fields: [ ... ]            # explicit, must be reviewed
low_confidence: [ ... ]             # heuristic; human gate
notes: { source_field: "rationale" }

Rules: never collapse two source values to one target unless explicit "lossy: true".
Reject any mapping that drops history fields without rationale.
```

Extract validator prompt: `Compare source export to extract output. Emit JSON: { "source_count", "extract_count", "missing_ids", "extra_ids", "field_drift": [...] }. Fail if missing_ids non-empty.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git-lfs` | Version every export, mapping, and id-map; lfs for large attachment dumps | preinstalled |
| `jira-cli` (`ankitpokhrel/jira-cli`) | JQL-driven extract from Jira | https://github.com/ankitpokhrel/jira-cli |
| Linear API + `linear-cli` (`evangodon/linear-cli`) | GraphQL load/extract for Linear | https://developers.linear.app |
| `gh` / `glab` | GitHub Projects v2 / GitLab Issues drivers | https://cli.github.com / https://gitlab.com/gitlab-org/cli |
| `asana` (Python SDK) | Asana extract/load | https://github.com/asana/python-asana |
| `clickup-py` / ClickUp REST | ClickUp drivers | https://clickup.com/api |
| `monday-graphql` | Monday.com GraphQL client | https://developer.monday.com |
| Atlassian Jira Cloud Migration Assistant (JCMA) | Jira → Jira Cloud official tool | https://support.atlassian.com/migration/ |
| `node-jira-importer` / `pivotal-to-linear` | Off-the-shelf importers — read source first | github community |
| `csvkit` / `duckdb` | Aggregate, dedupe, profile exported CSVs | `pip install csvkit duckdb` |
| `httpie` / `curl` | Quick API probing during mapping design | https://httpie.io |
| `pandoc` | Convert rich-text fields between markdown / wiki / ADF / HTML | https://pandoc.org |
| `dvc` / `lakeFS` | Version control for attachment dumps and id-maps | https://dvc.org / https://lakefs.io |
| `pre-commit` | Block commits to `migration.yaml` without rationale; lint id-map | https://pre-commit.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira (Cloud + DC) | SaaS / on-prem | REST v3 + JQL + JCMA | Most common source. JCMA for same-vendor moves; REST for cross-tool. |
| Linear | SaaS | GraphQL | Strong import wizard; CSV + native importers for Jira, Asana, GitHub, Trello, ClickUp. |
| Asana | SaaS | REST | Rich custom fields → maps to Jira/Linear/ClickUp with care. |
| ClickUp | SaaS | REST | Native importers; nested hierarchy (space/folder/list) doesn't always survive. |
| Monday.com | SaaS | GraphQL | Board-centric; mapping to issue-tracker model is lossy. |
| GitHub Projects v2 | SaaS | GraphQL | Lightweight target; field set is shallow but stable. |
| GitLab Issues + Boards | SaaS / OSS | REST + GraphQL | Native Jira importer; OSS variant for self-hosted. |
| Azure DevOps Boards | SaaS / on-prem | REST | Process templates (Agile/Scrum/CMMI) shape mapping. |
| Notion | SaaS | REST | Database-as-tracker; mapping to relational issue model is brittle. |
| Trello | SaaS | REST | List/card model; mostly a source these days. |
| Wrike | SaaS | REST | Custom-field-heavy; mapping is laborious. |
| ServiceNow ITSM/SPM | SaaS | REST + ScriptedREST | Heavy enterprise; migrations involve change-mgmt + CMDB linkage. |
| Pivotal Tracker (sunset) | SaaS | REST | One-way migrations only; vendor-provided exporter. |
| Shortcut (formerly Clubhouse) | SaaS | REST | Native importers; clean target. |
| Smartsheet | SaaS | REST | Sheet-as-tracker; spreadsheet-style schema. |
| Fivetran / Airbyte | SaaS / OSS | Connector | Pre-built source connectors for analytics; not transactional load but useful for extract phase. |
| Tempo / Clockify / Toggl | SaaS | REST | Time-tracking add-ons that often migrate separately. |

## Templates & scripts
The README provides phases, a Python `MigrationEngine` class skeleton, rollback YAML, and cutover/communications templates. Inline below: a small shell helper that runs the dry-run → diff → flag low-confidence loop.

```bash
#!/usr/bin/env bash
# migrate_dry_run.sh — extract, transform, diff vs. source counts.
set -euo pipefail
CFG="${1:-migration.yaml}"
OUT="dryrun-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"

python -m migration extract --config "$CFG" --out "$OUT/extract.jsonl"
python -m migration transform --config "$CFG" \
  --in "$OUT/extract.jsonl" --out "$OUT/transform.jsonl"

src_n=$(wc -l < "$OUT/extract.jsonl")
tgt_n=$(wc -l < "$OUT/transform.jsonl")
echo "extract=$src_n transform=$tgt_n"
[ "$src_n" = "$tgt_n" ] || { echo "COUNT DRIFT" >&2; exit 1; }

# Field drift: any source field absent from mapping
python -m migration audit-fields --config "$CFG" --in "$OUT/extract.jsonl" \
  > "$OUT/field-drift.json"
jq '.unmapped_count' "$OUT/field-drift.json" | xargs -I{} bash -c '
  [ "$1" = "0" ] || { echo "UNMAPPED FIELDS"; exit 1; }' _ {}
echo "Dry-run OK → $OUT"
```

Use as the gate before each pilot/full wave. Output goes into the migration audit trail.

## Best practices
- Migrate in waves. Pilot one project (≤200 issues) before any production wave; pause for retros.
- Source goes read-only at T-4h cutover, not T-0 — last-minute writes are lost otherwise. Communicate the read-only window 1+ weeks ahead.
- Keep source live in read-only for 30 days minimum after cutover; do not decommission until no team has needed it for 2 weeks.
- Two-pass loading: pass 1 = create issues, pass 2 = re-create links/parents/blocks using the id-map. Single-pass loses references.
- Username/email reconciliation is a separate workstream — extract identity from both tools, dedupe, build a name-map, get HR sign-off before load.
- Anchor on outcomes that matter (open work-in-progress, active sprints, current-quarter epics). Archive cold issues to CSV/JSON in cold storage rather than migrate.
- Disable target-side automations during load (Slack notifs, escalations). Re-enable after final id-map is stable.
- Validate by sampling: random sample of 50 issues + 10 outliers (oldest, largest attachment, deepest subtask tree, most comments). Diff field-by-field with humans, not LLMs only.
- Treat the id-map as a permanent artifact. Store with the project and reference it in code/docs that contain old issue IDs.
- Define rollback triggers in advance with hard thresholds (data loss detected → immediate; productivity drop >50% → 48h). Avoid rolling back on vibes.
- Train support team before cutover; the first week's tickets predict the next quarter's adoption.
- Update integrations (Slack, deploy hooks, browser extensions) on T-0; expect to find 2–3 hidden ones.

## AI-agent gotchas
- Agents fabricate plausible field maps for unknown custom fields ("legacy_id" → "external_id") that are wrong. Force `low_confidence` reviews on any unmapped or pattern-matched field.
- Status enum collapse: agents will silently merge `In QA` and `In Review` into `Review` if both partially match. Force explicit one-to-one mapping or `lossy: true` flag.
- Bulk loads at full vendor API rate get throttled; agents misinterpret 429s as transient and burn budget. Implement backoff in the engine, not in prompts.
- Description rewriting / "cleanup": never let an LLM rewrite ticket descriptions during migration. Humans depend on exact wording for diagnosis. Translate formatting (e.g., Jira ADF → markdown) deterministically.
- Markdown of inline images requires re-uploading attachments first and rewriting URLs. Order matters: attachments → comments → descriptions.
- Attachment dumps may include credentials, customer PII, GDPR-relevant data. Run `password-scrubber-agent` and a sampling DLP scan before pushing to target.
- Identity hallucination: agents will assign issues to user IDs that look right but belong to a different person — disambiguate by email, not display name.
- Two-tool reporting drift during transition: agents will produce conflicting status from source vs. target. Pick a system-of-record per metric and freeze.
- Auto-cutover is forbidden. The agent prepares the runbook; a human declares go-live.
- Long-context drift: do not feed the entire export into a single prompt. Page by 50–200 issues; the engine, not the LLM, holds full state.
- Decommission is destructive. Require a human-typed token (e.g., the project key) before any "delete source project" call.
- Human-in-the-loop checkpoints (mandatory): mapping sign-off, pilot acceptance, cutover go/no-go, decommission.

## References
- Atlassian Migration Cloud Assistant (JCMA) — https://support.atlassian.com/migration/
- Linear Import Docs — https://linear.app/docs/import
- Asana CSV Importer — https://help.asana.com/hc/en-us/articles/14186773124891
- ClickUp Imports — https://help.clickup.com/hc/en-us/categories/20329671523479-Import-Export
- ADKAR change-management framework — https://www.prosci.com/methodology/adkar
- Kotter "Leading Change" — change rollout guidance for cutover comms.
- Sibling methodologies in this repo: `pm-tool-selection/`, `change-control/`, `communications-management/`, `lessons-learned/`.
- ETL pattern primers: Kimball "The Data Warehouse Toolkit" — applies to PM-tool ETL by analogy.
