# Agent Integration — Team Development

## When to use
- Onboarding a new hire or contractor and wanting to map them onto Tuckman stages.
- Sprint retro reveals interpersonal conflict (Storming) and PM needs structured mediation steps.
- Solo founder hiring first 1–3 people and needs a written charter, skills matrix, and integration plan.
- Tracking a team's progression so leadership knows when to push autonomy vs. provide direction.

## When NOT to use
- One-off async working groups that disband in a week — Tuckman overhead exceeds value.
- Pure individual-contributor work with no inter-dependency (lone researcher, single-author content).
- Highly transactional vendor relationships (Tuckman assumes a sustained team).

## Where it fails / limitations
- Tuckman is descriptive, not prescriptive — teams skip stages, regress, or stall in Storming for months.
- Does not handle distributed/async-only teams well; assumes synchronous team dynamics.
- Skills matrix scoring is self-reported and drifts toward inflation without 360 feedback.
- "Forming/Storming/etc" labels can become an excuse for inaction ("we're just storming").

## Agentic workflow
Use Claude subagents to keep the artifacts (charter, skills matrix, retro doc) under version control and refreshed each sprint. The PM agent generates draft deltas; the human PM/EM owns merging. Treat each Tuckman transition as a trigger event that re-runs the matrix and charter check.

### Recommended subagents
- `faion-pm-agent` — drafts charter, retro template, action items from sprint logs.
- `faion-sdd-executor-agent` — turns retro action items into SDD tasks under `.aidocs/`.
- General-purpose Claude subagent — synthesises 1-on-1 notes into a Tuckman-stage diagnosis.

### Prompt pattern
```
You are reading 6 weeks of standup notes + 2 retros for team X.
Classify the team's current Tuckman stage with 3 specific quotes
as evidence. Output 5 PM actions targeted to that stage only.
```

```
Update the skills matrix in <path>. New input: <PR review patterns,
who reviewed what, who got stuck>. Bump scores only with at least
one cited PR or incident. Flag gaps where one person is sole owner.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Pull PR review counts to inform skills matrix | `brew install gh` |
| `git shortlog -sne --since='90 days'` | Contribution distribution per teammate | git built-in |
| `tokei` / `scc` | Code ownership by directory (proxy for expertise) | `cargo install tokei` |
| `git-fame` | Per-author line/commit attribution | `gem install git_fame` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes (REST/GraphQL) | Cycle reviews map to Tuckman cadence |
| Jira | SaaS | Yes (REST) | Sprint retros + team velocity in one place |
| Pulse / Officevibe | SaaS | Limited | Pulse surveys feed psychological-safety metric |
| 15Five | SaaS | Limited | 1-on-1 notes input for stage diagnosis |
| Glean / GitDuck | SaaS | Limited | Pair-programming evidence for skills matrix |

## Templates & scripts
See `templates.md` for Team Charter, Skills Matrix, Retro template. Inline helper to seed a skills matrix from `git shortlog`:

```bash
#!/usr/bin/env bash
# seed-skills-matrix.sh — infer expertise from git history per directory.
set -euo pipefail
since="${1:-180 days ago}"
for dir in $(git ls-tree -d --name-only HEAD); do
  echo "## $dir"
  git log --since="$since" --pretty=format:'%an' -- "$dir" \
    | sort | uniq -c | sort -rn | head -5
  echo
done
```

## Best practices
- Run a Tuckman self-assessment with the team after every team-composition change (hire, departure, reorg) — not on a calendar.
- Keep the charter short (one screen). Living document. Review every 8–10 weeks.
- Skills matrix: pair every "1" cell with a named owner who will move it to "2" within a quarter.
- Retro action items must have an owner + due date + a way to verify in next retro. No anonymous TODOs.
- Document Storming-stage decisions in writing — heated discussions get re-litigated unless captured.

## AI-agent gotchas
- LLMs over-pattern-match Tuckman labels; require evidence quotes in the diagnosis prompt.
- Never let an agent auto-publish a retro: humans must redact attribution and tone.
- Agents shouldn't write 1-on-1 notes verbatim into shared docs — privacy boundary.
- When generating a charter, agents tend to produce generic platitudes; force them to cite the team's actual incidents.
- Skills-matrix scoring by an agent must be evidence-backed (PRs, incidents) or it becomes hallucinated.

## References
- Tuckman, B.W. (1965) "Developmental Sequence in Small Groups."
- PMI PMBOK Guide 7th Edition — Team Performance Domain.
- Lencioni, P. "The Five Dysfunctions of a Team."
- Google re:Work — Psychological Safety in teams (https://rework.withgoogle.com/).
