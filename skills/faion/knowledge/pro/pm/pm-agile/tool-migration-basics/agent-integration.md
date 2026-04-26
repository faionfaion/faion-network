# Agent Integration — Cross-Tool Migration (Basics)

## When to use
- Switching PM tools (Jira → Linear, Trello → ClickUp, Asana → Notion).
- Consolidating two or more tools after acquisition or department merge.
- Outgrowing a starter tool (Trello/Notion) onto an enterprise tool (Jira/Azure DevOps).
- Compliance push forces the org onto a tool with audit trails (SOC2, ISO 27001).
- The current vendor's pricing model becomes hostile (per-seat hike, mandatory tier upgrade).

## When NOT to use
- One person and <100 issues — re-create them by hand in an afternoon.
- Vendor offers a guided/managed migration that already does data ETL — use it; this brief is overhead.
- Tool change is being driven by hype, not pain — wait three months and re-evaluate.
- Active product launch / freeze period — defer until after.
- Source data is too dirty to be worth migrating; archive and start fresh.

## Where it fails / limitations
- Field semantics rarely map 1:1; "Priority: High" in Jira ≠ "Priority: High" in Linear if scales differ.
- Attachment size limits and rate limits silently drop files mid-migration.
- Comment threads lose ordering or @mentions when user IDs don't resolve in the target.
- Custom Jira plugins (Tempo, Structure, ScriptRunner) have no target equivalent — features get lost.
- "Reporter" / "Created date" fields are usually system-managed in the target → audit trail gap.
- ID changes (PROJ-1234 → ABC-5) break every external link, commit message, and bookmark.

## Agentic workflow
A planning subagent reads the source export plus the migration scope and emits the field-mapping spreadsheet, the status-mapping table, and a list of unmapped fields requiring human decision. A second agent runs a dry-run extraction (read-only API calls), counts entities, and reports a delta against the live source. Humans approve mappings; only then a third agent triggers the actual ETL. Keep humans in the loop for: mapping approval, cutover go/no-go, and rollback decisions.

### Recommended subagents
- `migration-auditor` — runs pre-migration audit, returns YAML with counts, custom fields, integrations.
- `field-mapper` — proposes source→target field mappings + status/priority lookup tables; flags ambiguities.
- `dry-run-extractor` — calls source API read-only, validates auth, counts records, exports to JSONL.
- `mapping-validator` — checks mapping coverage: 100% of source fields either mapped or explicitly dropped.

### Prompt pattern
```
You are field-mapper. Inputs: source schema (JSON), target schema (JSON), org policy (markdown).
Output a Markdown table with columns: source_field, target_field, transformation, ambiguity_flag.
Where mapping is lossy or ambiguous, set ambiguity_flag=YES and propose two alternatives.
Do not invent target fields not in the schema input.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` (ankitpokhrel) | Jira export, JQL, batch mutations | https://github.com/ankitpokhrel/jira-cli |
| Linear CLI / GraphQL | Linear ingestion via official GraphQL API | https://developers.linear.app |
| `gh` CLI | GitHub Projects v2 (GraphQL) for source or target | https://cli.github.com |
| `notion-cli` (community) | Notion exports/imports for migration drafts | https://github.com/jakeswenson/notion |
| `csvkit` | Slice/dice large issue CSV exports during mapping | `pip install csvkit` |
| `jq` | Transform JSONL exports between API shapes | https://stedolan.github.io/jq/ |
| `dataset` (Python) | Quick SQLite staging of intermediate rows | `pip install dataset` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Atlassian JCMA | SaaS (managed) | No — UI-driven | Use for Jira Server→Cloud only; no agent hooks. |
| Linear Importer | SaaS | Partial — JSON upload | Decent Jira/Asana coverage; no API to drive it. |
| Plandek / Unito | SaaS sync | Yes — REST API | Two-way sync during parallel-run phase, not full migration. |
| Project Migrator (Solidify) | SaaS | No — UI | Azure DevOps ↔ Jira, supports CMMI; non-trivial cost. |
| Exalate | SaaS | Yes — Groovy scripts | Sync rules between Jira/Zendesk/ServiceNow during cutover. |
| Backbone (community) | OSS | Yes — Node | Open-source Jira→GitHub Issues; hackable. |
| ClickUp Importer | SaaS | No — UI | Zapier or built-in only. |

## Templates & scripts
See `templates.md` for the full audit checklist YAML. Inline Python skeleton for a dry-run count check (`scripts/count_check.py`):

```python
#!/usr/bin/env python3
"""Compare source vs target counts after migration. Fail if drift > threshold."""
import sys, requests, os
JIRA = os.environ["JIRA_URL"]; LINEAR = "https://api.linear.app/graphql"
JT = os.environ["JIRA_TOKEN"]; LT = os.environ["LINEAR_TOKEN"]

src = requests.get(f"{JIRA}/rest/api/3/search?jql=project=PROJ&maxResults=0",
                   headers={"Authorization": f"Bearer {JT}"}).json()["total"]
q = '{ issues(filter:{team:{key:{eq:"ABC"}}}) { totalCount } }'
tgt = requests.post(LINEAR, json={"query": q},
                    headers={"Authorization": LT}).json()["data"]["issues"]["totalCount"]

drift = abs(src - tgt) / max(src, 1)
print(f"source={src} target={tgt} drift={drift:.2%}")
sys.exit(0 if drift < 0.01 else 1)
```

## Best practices
- Run the migration three times: dev test, full dry-run with rollback, real cutover. Each catches a different class of bug.
- Freeze the source 4 hours before cutover; new tickets created during the window go to a known "intake" queue and get re-keyed by hand.
- Preserve source IDs in a "legacy_id" custom field on the target — every external system that hardcoded PROJ-123 still resolves.
- Keep the source read-only for 30+ days. Inevitably someone needs to look up "what was decided in PROJ-456".
- Validate three numbers before declaring success: total issues, total comments, total attachments by byte count.
- Document every "won't migrate" decision; it pre-empts the post-cutover blame meeting.

## AI-agent gotchas
- Agents underestimate rate limits and crash mid-batch — always implement exponential backoff and resumable state (issue ID checkpoint file).
- LLMs invent custom-field names confidently; constrain field-mapping output to the actual target schema, fail fast if hallucinated.
- Comment migration breaks @mentions because user IDs differ; map users in advance, drop unresolved mentions, log them.
- A "successful" migration with wrong status mapping silently buries 30% of work in the wrong column. Always sample-validate 50 random items by hand.
- Token cost scales with issue count × description size; export to JSONL and let agents read summaries, not raw bodies.

## References
- https://support.atlassian.com/jira-cloud/docs/migrate-from-jira-server-to-jira-cloud/
- https://linear.app/docs/import
- https://www.prosci.com/methodology/adkar — change-management framework
- "Data Migration: Extending and Vitalizing Enterprise Data" (Morris)
- See sibling `tool-migration-process` for phase-by-phase execution playbook.
