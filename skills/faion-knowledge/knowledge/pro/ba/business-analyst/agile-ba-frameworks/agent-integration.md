# Agent Integration — Agile BA in Scrum & Scaled Agile

This methodology maps Business Analyst competencies onto Scrum ceremonies and Scaled Agile (SAFe-style) levels. For an LLM agent the deliverable is not "the BA" — it is per-ceremony artifacts (refined stories, AC, dependency notes, retro inputs) produced on a cadence that matches the team's sprint clock. Drive it as a recurring pipeline keyed off backlog state and sprint events, not as a one-shot Q&A.

## When to use

- A team running 1-2 week sprints with a backlog tool (Jira, Linear, GitHub Projects, Azure DevOps) where stories are routinely under-refined and block sprint planning.
- Solo / two-person operators acting as Product Owner + BA where backlog refinement is skipped because nobody owns it.
- SAFe ART (Agile Release Train) preparing for PI Planning: features need decomposition into team stories with dependencies mapped across ARTs.
- Migration from waterfall BA artifacts (BRD/SRS) into incremental story-based delivery — the agent reformats existing requirements into user-story + AC pairs sprint-by-sprint.
- Backlog hygiene audits before a release: sweep open items for missing AC, ambiguous wording, orphan stories with no parent epic.

## When NOT to use

- Pre-product-discovery work. Use `continuous-discovery`, `user-story-mapping`, or the `researcher` skill for opportunity framing — agile BA is downstream of those.
- Hard-deadline regulated builds (medical, aviation, banking core) where signed BRDs and traceability matrices are contractual. Agile-BA techniques inform but don't replace those — switch to `requirements-documentation` + `requirements-traceability`.
- Pure Kanban with no sprint cadence — the sprint-keyed templates here misfire. Use a flow-based BA loop (WIP-triggered refinement) instead.
- One-off feasibility studies — single-shot deliverable, no iteration, no ceremony. Use `strategy-analysis` + `solution-assessment`.
- Teams without a backlog tool API. The agent has nothing to read or write into; manual-only environments waste agent capability.

## Where it fails / limitations

- **No explicit BA role in Scrum or SAFe** — agent has to choose a "host" role (PO, SM, system architect) for each artifact; mis-attribution causes ownership conflicts on the team.
- **Story-splitting heuristics are subjective.** SPIDR / INVEST patterns guide but don't determine the split — LLMs over-split or under-split without team feedback loops.
- **Acceptance criteria drift.** Generated AC reflect the agent's interpretation of the story title, not stakeholder intent. Without a real PO review the team builds the wrong thing fast.
- **Cross-team dependency discovery is structural, not textual.** An LLM reading one team's backlog cannot see another ART's hidden constraints; needs portfolio-level data feed.
- **Velocity / capacity data is gameable.** Estimating BA workload by "pre-refined story count" rewards superficial refinement.
- **Retrospective inputs from an agent feel inhuman.** Teams ignore AI-generated retro themes; better to extract data (cycle time, AC pass rate) and let humans interpret.
- **SAFe terminology drift.** SAFe 6.0 renamed several constructs (Solution Train → Large Solution; Program → Essential). Templates referencing older terms confuse certified teams.

## Agentic workflow

Run as a **sprint-clock-driven pipeline** orchestrated by a BA subagent that subscribes to backlog events. Trigger points: (1) `T-3 days` before sprint planning → refinement pass; (2) sprint planning end → AC freeze + dependency report; (3) mid-sprint → ad-hoc clarification responder; (4) sprint review → AC verification against demo; (5) retrospective → process-metric extraction. State persists per-sprint in `.aidocs/sprints/<sprint-id>/` with subfiles for refined-stories, dependencies, ac-verification, retro-data. Each phase reads previous-sprint state to detect carry-over patterns (chronic under-refinement, recurring blockers). Hand artifacts to the team's PO for sign-off — never auto-update backlog tickets without human approval gate on AC and story splits.

### Recommended subagents

- `faion-sdd-executor-agent` — Wraps refined stories with full SDD context (constitution, design) when stories cross spec boundaries; consumes user-story-mapping output.
- `faion-research-agent` (mode=pains, mode=validate) — Pulls user pain evidence to attach to AC under "Why" sections.
- `faion-software-architect` skill — Loaded when a story implies architectural change; flags the story for ARB review before refinement closes.
- `faion-brainstorm` — Used in PI Planning prep to diverge feature decomposition options before converging on a team-by-team breakdown.
- General `Task` subagent — One per refinement batch; pass `templates.md` + the methodology's `llm-prompts.md` as system context.
- `password-scrubber-agent` — Run on any backlog export before persisting to repo; tickets routinely contain credentials in comments.

### Prompt pattern

Refinement pass (T-3 before planning):

```
Read .aidocs/sprints/<prev-sprint>/retro-data.md and the next 15 unrefined backlog items from <jira-export>.
For each item produce: story (As a / I want / so that), 3-7 AC in Given/When/Then, INVEST self-check (pass/fail per letter with one-line reason), dependency list.
Flag for human PO review: stories that fail INVEST-N (Negotiable) or INVEST-S (Small > 5 SP).
Output to .aidocs/sprints/<sprint-id>/refined-stories.md. Do not push to Jira.
```

AC verification (sprint review):

```
Read .aidocs/sprints/<sprint-id>/refined-stories.md and the demo notes at <path>.
For each story emit AC-pass-rate (X/Y), list of failed AC with quoted demo evidence, recommended carry-over or re-open decision.
Output to .aidocs/sprints/<sprint-id>/ac-verification.md.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `acli` (Atlassian CLI) | Read/write Jira issues, JQL queries, bulk AC updates | https://developer.atlassian.com/cloud/acli |
| `jira-cli` (`go-jira`) | Lightweight Jira CLI alternative for headless agents | https://github.com/ankitpokhrel/jira-cli |
| `gh project` | GitHub Projects v2 backlog automation, story export | https://cli.github.com/manual/gh_project |
| `linear` (TypeScript SDK + CLI wrappers) | Read/write Linear issues, cycles | https://developers.linear.app |
| `az boards` | Azure DevOps work item CRUD for SAFe teams on ADO | https://learn.microsoft.com/azure/devops/cli |
| `cucumber` / `behave` | Validate Given/When/Then AC compile to executable specs | https://cucumber.io |
| `gherkin-lint` | Lint AC syntax before AC freeze | `npm i -g gherkin-lint` |
| `jq` + `mermaid-cli` | Convert dependency JSON to PI Planning board diagrams | `apt install jq` / `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert refined-stories.md → DOCX for stakeholders who refuse Markdown | `apt install pandoc` |
| `git` + `pre-commit` | Version sprint state files; reject commits missing AC | https://pre-commit.com |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira Cloud | SaaS | Yes — REST v3, OAuth + API token | De-facto SAFe tool; supports Advanced Roadmaps for PI Planning |
| Jira Align | SaaS (enterprise) | Limited — REST exists but rate-limited | Portfolio-level SAFe; expensive, agent-friendliness depends on plan |
| Linear | SaaS | Yes — GraphQL API, webhook events | Cleanest API of the lot, fits sprint-clock triggers |
| Azure DevOps Boards | SaaS / on-prem | Yes — REST + Service Hooks | Common in MS-stack SAFe shops |
| GitHub Projects v2 | SaaS | Yes — GraphQL only | Lightweight, missing SAFe-specific fields (PI, ART) — model in custom fields |
| Shortcut | SaaS | Yes — REST | Iteration-based, fits Scrum but not SAFe out of the box |
| Targetprocess | SaaS | Yes — REST | SAFe-native UI, niche |
| Easy Agile (Jira app) | SaaS plugin | Indirect — via Jira API | User Story Maps, PI Planning boards, SAFe ceremonies |
| Miro / Mural | SaaS | Limited — REST for boards, no semantic story map API | Use for human-in-the-loop story mapping; export to Markdown |
| Confluence | SaaS | Yes — REST | Persist refinement artifacts as living docs alongside stories |
| Slack / MS Teams | SaaS | Yes — webhooks + bots | Mid-sprint clarification responder runs as a bot |
| OpenProject | OSS | Yes — REST | Self-hosted alternative for cost-sensitive teams |
| Taiga | OSS | Yes — REST | Scrum + Kanban, light SAFe support |
| Cucumber Studio (HipTest) | SaaS | Yes — REST | Living AC repository, integrates with CI |

## Templates & scripts

The methodology's `templates.md` is empty in this tree — start from `examples.md` for the sprint activity skeleton and the inline tools below.

INVEST + AC validator (≤50 lines bash, runs in CI on refined-stories.md):

```bash
#!/usr/bin/env bash
# usage: validate-stories.sh refined-stories.md
# fails (exit 1) if any story missing AC, INVEST flags, or Given/When/Then
set -euo pipefail
FILE="${1:?path to refined-stories.md}"
fail=0
awk '
  /^## Story / { story=$0; ac=0; gwt=0; invest=0; next }
  /^### Acceptance Criteria/ { ac=1; next }
  /^- *Given .* When .* Then / && ac { gwt++ }
  /^### INVEST/ { invest=1; next }
  /^- *(I|N|V|E|S|T)[: ]/ && invest { i++ }
  /^## Story / || /^# / {
    if (story != "" && (gwt < 3 || i < 6)) {
      print "FAIL: " story " gwt=" gwt " invest=" i
      bad++
    }
    story=""; ac=0; gwt=0; invest=0; i=0
  }
  END {
    if (story != "" && (gwt < 3 || i < 6)) {
      print "FAIL: " story " gwt=" gwt " invest=" i; bad++
    }
    exit (bad > 0 ? 1 : 0)
  }
' "$FILE" || fail=1
exit $fail
```

Sprint state file (`.aidocs/sprints/<sprint-id>/_state.json`):

```json
{
  "sprint_id": "S42",
  "team": "ART-payments-team-3",
  "framework": "safe-6.0",
  "phase": "refinement|planning|execution|review|retro",
  "stories_refined": 0,
  "ac_pass_rate": null,
  "carry_over": [],
  "blockers": [],
  "human_review_pending": []
}
```

## Best practices

- **Treat the agent as a refiner, never an approver.** Generated AC always pass through the human PO; track sign-off in `_state.json.human_review_pending`.
- **Anchor every AC to evidence.** Link from AC to user-research note (`pains.md`), interview quote, or analytics query — kills the "made-up AC" failure mode.
- **One epic = one .md file with story stubs.** Encourages story-splitting via Markdown headings, makes diff-review trivial in PRs.
- **Run INVEST as a hard gate, not a suggestion.** A story failing N or S returns to backlog automatically — no negotiation in the agent loop.
- **Map BA "host role" per organization once, then reuse.** Document in the team's `constitution.md`: "BA work lives with PO at team level, with System Architect at program level." Removes ceremony-by-ceremony role disputes.
- **Cap refinement output at 1.5x team velocity.** Refining the whole backlog wastes effort; refine one sprint ahead, not five.
- **Use the retrospective phase for metric extraction only.** Cycle time, AC churn rate, carry-over %, blocked-by-clarification time. Feed numbers to the team — let humans synthesize themes.
- **For SAFe, drive PI Planning prep two weeks early.** Generate feature → story decomposition + cross-team dependency draft, then host humans to refine. Day-of generation is too late.
- **Version sprint state in git, not the backlog tool.** Backlog tools mutate; git is the truth source for retrospective analysis 6 months later.

## AI-agent gotchas

- **Story title infatuation.** Agents elaborate AC from the title alone, missing the description and comments where the real intent lives. Always feed full ticket body + last 5 comments.
- **AC plagiarism across stories.** Same Given/When/Then copy-pasted across 4 stories with cosmetic edits. Add a similarity check (Jaccard on AC tokens) — flag any pair > 0.7 for human review.
- **INVEST passes that hide non-testability.** Agents claim "T: yes" for AC that have no measurable outcome. Force AC tokens to include a quantitative threshold or an observable system state.
- **Dependency hallucination.** "This story depends on payments service" with no evidence. Require dependency rows to cite a ticket key, repo path, or service name from a known registry.
- **Sprint-clock drift.** Long-running orchestrators lose sync with the actual sprint dates. Always pull sprint metadata fresh from the tool API at phase start, never cache > 24h.
- **PI Planning load.** SAFe PI Planning generates 200-500 stories at once; LLM context blows out. Chunk by team, run in parallel subagents, merge dependency lists at the end.
- **Auto-pushing to Jira/Linear.** Direct write-back via API mutates auditable team state. Always require an explicit human approval (PR-style or chat-confirm) — never `--yes` flags.
- **SAFe term confusion.** Agents trained pre-2023 may use SAFe 4 terms (Solution Train, Program Backlog) that SAFe 6 renamed. Pin the SAFe version in agent system prompt; reject mismatched output.
- **Retro themes feel synthetic.** "We need better communication" with no data. If retro phase runs, output numbers and trends only; never narrative.
- **Mid-sprint clarification race.** Two agents (clarifier bot + human PO) answering the same question give contradictory guidance. Single-writer rule: bot replies with a draft, PO confirms before posting.
- **Cross-ART invisible dependencies.** Team backlog has no view of another ART's queue. Without a portfolio data feed, dependency reports systematically miss 30-40% of cross-team blockers — flag the gap, don't hide it.

## References

- Methodology files: `./README.md`, `./examples.md`, `./llm-prompts.md`
- Sibling: `../user-story-mapping/README.md`, `../acceptance-criteria/README.md`, `../requirements-prioritization/README.md`
- Scaled Agile Framework 6.0: https://framework.scaledagile.com
- Scrum Guide 2020: https://scrumguides.org/scrum-guide.html
- IIBA Agile Extension to the BABOK: https://www.iiba.org/standards-and-resources/agile-extension/
- INVEST criteria: https://agileforall.com/new-to-agile-invest-in-good-user-stories
- SPIDR story splitting: https://www.mountaingoatsoftware.com/blog/the-spidr-approach-to-splitting-user-stories
- Atlassian Jira REST API v3: https://developer.atlassian.com/cloud/jira/platform/rest/v3
- Linear API: https://developers.linear.app/docs
- Azure DevOps REST: https://learn.microsoft.com/rest/api/azure/devops
- GitHub Projects API: https://docs.github.com/en/issues/planning-and-tracking-with-projects
- Cucumber Gherkin reference: https://cucumber.io/docs/gherkin/reference
