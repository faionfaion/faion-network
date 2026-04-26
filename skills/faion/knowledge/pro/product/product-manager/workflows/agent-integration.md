# Agent Integration — Product Manager Workflows

This methodology defines two PM pipelines: **Project Bootstrap** (idea → constitution → TASK_000) and **MLP Planning** (MVP → Most Lovable Product). It is the PM-side companion to `pro/research/researcher/workflows`. Where the researcher variant focuses on discovery state-machines, this file focuses on the **operating cadence** of the PM role: daily backlog hygiene, sprint ceremonies, release management, and sync with execution tools (Jira, Linear, Shortcut, GitHub Projects).

## When to use

- New project bootstrap where `.aidocs/` is empty and `constitution.md` plus `roadmap.md` need to be authored before any code task is dispatched.
- MVP-to-MLP transition after first usable build is shipped — agents must reread competitor scope and inject WOW features without losing original AC numbering (`FR-NN.N`, `AC-NN.N`).
- Sprint kickoff and review ceremonies where backlog needs grooming, sized, and synced to a tracker (Jira/Linear/GitHub Projects).
- Release coordination where a single PM agent owns the cut: changelog generation, release-notes draft, GTM handoff to `faion-marketing-manager`.
- Daily PM ritual: backlog re-prioritisation (RICE/MoSCoW), stakeholder digest, blocker surfacing.

## When NOT to use

- During SDD task execution itself — code tasks belong to `faion-feature-executor` / `faion-sdd-execution`. The PM workflow stops at `TASK_000` creation; do not let it rewrite engineering tasks.
- One-off feature requests inside an active sprint — log to backlog via tracker API, do not run the full bootstrap pipeline.
- Spec changes after spec freeze — route through change management (see `pro/pm/pm-traditional/raci-matrix`), not a workflow re-run.
- Solo Phase 1 of a project before there is anything to prioritise — use `solo/product/product-planning/mvp-scoping` instead, this pro workflow is heavier.

## Where it fails / limitations

- **Tracker drift.** Workflow writes to `.aidocs/features/backlog/` but Jira/Linear are the source of truth for many teams. Without a sync subagent, the two diverge within one sprint.
- **No stakeholder loop.** Bootstrap Phase 4 is a single user confirmation; real PM workflows require sign-off from eng lead, design, and exec sponsor. Agent skips this and produces unsigned constitutions.
- **MLP "WOW" generation hallucinates.** `faion-mlp-agent` mode=`propose` invents features without competitor evidence unless explicitly grounded in `mvp-scope-analysis.md`.
- **Numbering collisions.** `{NN}-{feature}` and `TASK_{NNN}` numbering breaks when two parallel agents create features simultaneously — no lock file in current spec.
- **No definition-of-ready / definition-of-done gates.** Tasks land in `todo/` whether or not the spec passes INVEST. Add a validator subagent.
- **Release management absent.** README does not cover release branching, RC tagging, or rollback windows. Use `pro/product/product-manager/release-planning` alongside.
- **Capacity blindness.** RICE Effort assumes a homogeneous team; agent has no model of available developer-days, so prioritisation drift is common.

## Agentic workflow

Drive the PM cadence as a **daily orchestrator** (cron + on-demand) plus three event-driven flows: **bootstrap**, **sprint**, **release**. The orchestrator wakes, reads `.aidocs/features/`, syncs deltas to the tracker, and emits a digest. Sprint and release flows are explicit `Task` invocations from the user. Never run bootstrap from cron — it is interactive (Phase 4 confirmation is mandatory). For MLP, sequence the five `faion-mlp-agent` modes strictly (`analyze → find-gaps → propose → update → plan`); each mode persists its artefact so a failed run resumes.

### Recommended subagents

- `faion-mvp-scope-analyzer-agent` — Pulls competitor MVP scope; required input for Phase 3 of bootstrap and Phase 1 of MLP.
- `faion-mlp-agent` — Five-mode orchestrator (`analyze`, `find-gaps`, `propose`, `update`, `plan`). Each mode = one Task invocation.
- `faion-research-agent` (mode=ideas/market/competitors) — Feeds bootstrap Phases 1-3 with `.aidocs/product_docs/*.md` artefacts.
- `faion-sdd-executor-agent` (in `agents/`) — Downstream of TASK_000 creation; receives the first executable task.
- `faion-marketing-manager` — Downstream of release flow; consumes `executive-summary.md` plus release-notes draft for GTM.
- `faion-business-analyst` — Required between Phase 5 (backlog) and Phase 6 (constitution) for FR/AC formalisation.
- General-purpose `Task` subagent — Use for backlog grooming + tracker sync when no specialised PM-ops agent is registered.

### Prompt pattern

Bootstrap Phase 5 (backlog from validated ideas):

```
You are the PM orchestrator. Inputs:
  .aidocs/product_docs/idea-validation.md
  .aidocs/product_docs/competitive-analysis.md
For each MVP feature (max 5), create:
  .aidocs/features/backlog/{NN}-{slug}/spec.md
with sections: User Story, FR-NN.N (max 5), AC-NN.N (Given/When/Then),
RICE score, MoSCoW tag. Refuse to invent features not present in inputs.
Return: list of created paths, RICE table, blocking questions.
```

Sprint kickoff (after a release):

```
mode=sprint-kickoff sprint_id={N}
Steps:
  1. Read .aidocs/features/backlog/, sort by RICE desc
  2. Pull next K features whose sum(effort) <= team_capacity_pd
  3. Move backlog/ → todo/, generate TASK_NNN_*.md per feature
  4. Sync to Jira/Linear via MCP; attach spec.md as description
Output: sprint plan as table, list of skipped features with reason.
```

MLP propose (grounded):

```
mode=propose project_path=.
Constraints: every WOW feature must cite a row in mvp-scope-analysis.md.
If no competitor evidence exists for a feature, label it "speculative"
and place under "Deferred — needs validation". Max 7 WOW items.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh project` | Read/write GitHub Projects v2 fields, issues, PRs | `gh extension install github/gh-projects` · https://cli.github.com/manual/gh_project |
| `jira-cli` (ankitpokhrel) | Headless Jira ops: issue create, transition, JQL search | `go install github.com/ankitpokhrel/jira-cli/cmd/jira@latest` |
| `linear-cli` (community) | Linear teams/issues from terminal | `npm i -g @evangodon/linear-cli` |
| `shortcut-cli` | Shortcut (Clubhouse) story CRUD | `npm i -g shortcut-cli` |
| `notion-cli` (litencatt) | Notion DB read/write for roadmap pages | `brew install litencatt/tap/notion-cli` |
| `productboard-cli` (community) | Productboard feature ingest | https://www.npmjs.com/package/productboard-api |
| `git-changelog-command-line` | Auto-changelog by conventional commits | `npm i -g conventional-changelog-cli` |
| `release-please` (Google) | Release PRs from conventional commits | `npm i -g release-please` |
| `semver-cli` | Validate / bump semver in release flow | `npm i -g semver` |
| `dust` (renamed `dst`) | RICE/MoSCoW spreadsheet via CSV | local Python script |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira Cloud | SaaS | Yes — REST + JQL + MCP server | Use Atlassian Remote MCP or `jira-cli`; rate limit 100 req/min/user. |
| Linear | SaaS | Yes — GraphQL + official MCP | Best-in-class API; webhooks for sprint events. |
| Shortcut | SaaS | Yes — REST | Story `external_id` field for two-way sync. |
| GitHub Projects v2 | SaaS | Yes — GraphQL | Use `gh` CLI; fields are typed (single-select, iteration). |
| Productboard | SaaS | Partial — REST, no MCP | Good for feedback ingest; portal not scriptable. |
| Aha! | SaaS | Partial — REST | Heavy enterprise; PMs use for portfolio, not sprint. |
| Notion | SaaS | Yes — REST + MCP | Roadmap source-of-truth for solo/small teams. |
| ClickUp | SaaS | Yes — REST | Watch rate limits; many fields are custom. |
| OpenProject | OSS (self-hosted) | Yes — REST | Run on faion-net server; Docker compose. |
| Plane (makeplane) | OSS (self-hosted) | Yes — REST | Modern Linear-alternative; active dev. |
| Taiga | OSS | Yes — REST | Scrum + Kanban; smaller community. |
| Focalboard | OSS | Limited — API closed since Mattermost merge | Local-only kanban. |
| LaunchDarkly | SaaS | Yes — REST | Feature flag gates for release management. |
| Statsig | SaaS | Yes — REST | Experimentation + flags; PM owns config. |

## Templates & scripts

Inline RICE → backlog reorder script. Reads `spec.md` frontmatter, scores, rewrites `.aidocs/features/backlog/INDEX.md`:

```bash
#!/usr/bin/env bash
# rice-reorder.sh — rank backlog by RICE = (R*I*C)/E, write INDEX.md
set -euo pipefail
ROOT="${1:-.aidocs/features/backlog}"
OUT="$ROOT/INDEX.md"
{
  echo "# Backlog (RICE-sorted)"
  echo
  printf '| Feature | Reach | Impact | Conf | Effort | RICE |\n'
  printf '|---------|------:|------:|----:|------:|----:|\n'
  for spec in "$ROOT"/*/spec.md; do
    feat=$(basename "$(dirname "$spec")")
    R=$(awk -F': ' '/^reach:/{print $2; exit}' "$spec")
    I=$(awk -F': ' '/^impact:/{print $2; exit}' "$spec")
    C=$(awk -F': ' '/^confidence:/{print $2; exit}' "$spec")
    E=$(awk -F': ' '/^effort:/{print $2; exit}' "$spec")
    [ -z "$E" ] || [ "$E" = "0" ] && continue
    RICE=$(python3 -c "print(round($R*$I*$C/$E,1))")
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$feat" "$R" "$I" "$C" "$E" "$RICE"
  done | sort -k6 -nr | awk -F'\t' '{printf "| %s | %s | %s | %s | %s | %s |\n",$1,$2,$3,$4,$5,$6}'
} > "$OUT"
echo "wrote $OUT"
```

For Jira/Linear sync, prefer the MCP server pattern over direct REST — sync templates live in `pro/pm/pm-agile/jira-workflow-management/templates.md`.

## Best practices

- Treat `.aidocs/features/` as the planning source of truth and Jira/Linear as the **execution mirror** — never the reverse, or agents lose history when tickets are deleted.
- Lock numbering. When two PM agents may run concurrently, take a flock on `.aidocs/.numbering.lock` before assigning the next `{NN}` or `TASK_{NNN}`.
- Every spec must have a RICE row before it leaves backlog; reject specs without `reach/impact/confidence/effort` frontmatter at grooming time.
- Run MLP propose only after MVP ships and produces real telemetry — propose-without-data is the failure mode README does not warn about.
- Cap WOW features at 7. Empirically, more than that and the MLP becomes a v2.0 plan, not an MLP.
- Daily orchestrator should produce **one** digest file (`.aidocs/digest/YYYY-MM-DD.md`) and `tg-send` only the diff vs yesterday — saves Telegram noise.
- Hold a `release-cut` ceremony agent that creates the release branch, generates changelog, opens the PR, and pings the GTM agent — don't bolt this onto sprint kickoff.

## AI-agent gotchas

- **Phase 4 confirmation cannot be skipped.** LLMs eager to finish will simulate user approval. Hard-fail the flow if the user-message stream lacks an explicit `approve` token.
- **`AskUserQuestion` blocks in non-interactive runs** (cron, CI). Bootstrap must detect non-interactive mode and exit with `FAIL needs-human` — do not invent answers.
- **Specs are markdown, trackers are typed.** When syncing RICE values to Jira numeric custom fields, coerce explicitly; otherwise Jira drops the value silently.
- **MLP "update" mode rewrites spec files in-place.** Always run `git status` before and after — agents have been observed clobbering FR numbering on retry.
- **Tracker MCP token leakage.** Linear and Jira MCP servers cache OAuth tokens; in a worktree-isolated agent, the token may belong to a different user. Verify `whoami` against the tracker before write ops.
- **Capacity field is unreliable.** Sprint kickoff agent should require explicit `team_capacity_pd` argument from user; never compute from velocity alone (velocity is a trailing indicator and breaks on holiday weeks).
- **Hidden features.** PMs sometimes file features as `epic` in the tracker but as `feature/` in `.aidocs/`. The sync agent must understand both shapes; otherwise epics duplicate.
- **No DoD validator.** Add a `definition-of-done.yaml` per feature and a checker subagent — without it, `done/` collects half-merged work.

## References

- Reforge — "PM Operating Model" (sprint cadence + ceremonies): https://www.reforge.com/blog
- Marty Cagan — Inspired (Phase 4 confirmation philosophy): SVPG, 2017.
- Atlassian — Jira Cloud REST v3 + JQL: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- Linear — API + MCP: https://developers.linear.app/
- GitHub Projects v2 GraphQL: https://docs.github.com/en/graphql/reference/objects#projectv2
- release-please (Google): https://github.com/googleapis/release-please
- Companion methodology: `pro/research/researcher/workflows/agent-integration.md` (research-side state machine)
- Companion methodology: `pro/pm/pm-agile/scrum-ceremonies/README.md` (sprint mechanics this workflow drives)
