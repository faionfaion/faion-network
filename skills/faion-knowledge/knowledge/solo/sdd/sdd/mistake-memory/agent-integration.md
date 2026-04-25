# Agent Integration — Mistake Memory

## When to use
- Before starting any task: load `.aidocs/memory/mistakes.md` and inject relevant warnings into the task prompt
- After a task fails (CI failure, bug found in review, production incident): document the failure in mistakes.md immediately
- When the same failure pattern occurs twice — the second occurrence triggers a mandatory rule addition (not just a doc update)
- When onboarding a new agent to an existing project: load mistakes.md as part of the project context so it inherits accumulated warnings

## When NOT to use
- For tracking bugs in a bug tracker (that is separate from mistake memory — mistakes.md captures LLM/agent execution patterns, not product defects)
- As a replacement for post-mortems on infrastructure incidents — mistake memory is development-workflow focused
- When the project has fewer than 3 completed tasks — there is not enough history to make patterns useful

## Where it fails / limitations
- Mistake memory only works if it is actually loaded before each task; agents that skip the pre-task loading phase get no benefit
- The file grows unbounded — after 50+ entries, querying for relevant mistakes by keyword becomes unreliable; entries need periodic archiving or tagging
- LLM agents reading mistakes.md cannot reliably self-judge relevance; keyword matching is more reliable than semantic matching in prompts
- "Blameless culture" principle breaks down under token pressure: agents write terse entries that omit root cause and prevention, making them useless for future avoidance
- Automated CI capture (Layer 3) requires engineering investment; most projects start with manual-only capture, which misses failures that don't trigger human attention

## Agentic workflow
The `faion-sdd-executor-agent` loads `mistakes.md` at the start of each task (pre-task phase), extracts entries matching the current task's domain keywords, and prepends them as a `## Warnings` section in the task prompt. After task completion, if any unexpected failure occurred, the agent appends a new entry to mistakes.md following the MIS-NNN template before moving the task to done/. A second agent (or the same one in a review pass) validates the entry has root cause, prevention step, and severity.

### Recommended subagents
- `faion-sdd-executor-agent` — primary consumer; reads mistakes.md at task start, writes new entries on failure
- Sonnet-tier subagent — root cause analysis pass on a failure; generates the Five Whys chain for a new MIS-NNN entry
- CI bot / pre-commit hook — catches Layer 3 patterns (hardcoded secrets, missing tests) before they become mistakes

### Prompt pattern
```
Before executing TASK-042, load the relevant warnings from mistakes.md.
Search for entries matching keywords: [database, migration, schema].
For each match, prepend this warning to your working context:
"Warning [MIS-ID]: [title]. Prevention: [prevention step]."
Then proceed with task execution.
```

```
Task TASK-042 failed with: [error description].
Write a new mistakes.md entry:
- ID: MIS-[next sequential number]
- Severity: High/Medium/Low
- Context: what type of task was being executed
- What happened: exact failure description
- Root cause: Five Whys chain (at least 3 levels)
- Prevention: concrete, specific step to avoid this next time
- First occurrence: today's date
Append to .aidocs/memory/mistakes.md.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `grep` / `rg` | Keyword-match mistakes.md before task injection | Built-in / `brew install ripgrep` |
| `jq` | Query `mistakes.jsonl` for structured mistake records | `brew install jq` / [docs](https://jqlang.github.io/jq/) |
| `pre-commit` | Run automated pattern checks (Layer 3) on every commit | `pip install pre-commit` / [docs](https://pre-commit.com/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry | SaaS | Yes — webhook/API | Production errors can auto-trigger mistake capture via webhook |
| PagerDuty | SaaS | Yes — API | Incident alerts can route to mistake capture pipeline |
| GitHub Actions | SaaS CI | Yes | CI failure → auto-open PR adding MIS-NNN to mistakes.md |
| Linear / Jira | SaaS | Partial | Link MIS-NNN entries to bug tickets for cross-referencing |

## Templates & scripts
See `templates.md` for the MIS-NNN entry format and the mistakes.jsonl schema.

Pre-task warning injection (bash, keyword-based):
```bash
#!/usr/bin/env bash
# Usage: ./inject-warnings.sh "database migration schema"
# Outputs relevant mistake entries from mistakes.md
KEYWORDS=$1
MISTAKES_FILE=".aidocs/memory/mistakes.md"
if [[ ! -f "$MISTAKES_FILE" ]]; then echo "No mistakes.md found"; exit 0; fi
echo "=== Relevant Warnings ==="
# Extract MIS-NNN blocks that contain any keyword
awk '/^## MIS-/{block=$0; next} block{block=block"\n"$0}
     /^## MIS-/{if (block ~ /'"$KEYWORDS"'/) print block; block=$0}
     END{if (block ~ /'"$KEYWORDS"'/) print block}' "$MISTAKES_FILE"
```

## Best practices
- Write mistake entries within 24 hours of the failure — details fade; "I'll document it later" means it never gets documented
- Minimum viable entry: severity + what happened + one concrete prevention step; root cause can be added later but prevention cannot be omitted
- Tag entries with domain keywords in the title (e.g., `## MIS-007: Database Migration — Missing Row Count Check`) to enable reliable keyword search
- Review mistakes.md monthly: archive entries older than 6 months with no recurrence into a separate `mistakes-archive.md`
- For recurring mistakes (same pattern, third occurrence): escalate to an automated prevention rule in CI — documenting is not enough if the pattern keeps repeating
- Keep mistakes.md in the same repo as the code; project-level mistakes are not portable to other projects

## AI-agent gotchas
- Agents read mistakes.md and inject ALL entries regardless of relevance when given vague instructions; require explicit keyword filtering
- LLMs writing MIS-NNN entries often produce generic prevention steps ("be more careful," "review before committing") — require specificity: the prevention step must be a concrete action with a clear trigger
- An agent that fails midway through a task and is re-run does not automatically know the previous attempt failed; load session.md in addition to mistakes.md so it inherits the failure context
- Mistake entries written by agents often attribute the root cause to "insufficient context" — this is almost always true but also almost always useless; require the agent to identify the specific missing piece of context
- Agents do not self-report failures by default; executor agents must have explicit post-task instructions to check their own output against AC and write mistake entries when AC are not met

## References
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) — NeurIPS 2023
- [Blameless Post-Mortems — Google SRE](https://sre.google/sre-book/postmortem-culture/)
- [LLM Hallucinations in Code Generation](https://arxiv.org/pdf/2409.20550)
- [LLM Code Generation Mistakes Analysis](https://arxiv.org/html/2411.01414v1)
- [Addy Osmani: AI Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/)
- [Learning from Incidents](https://www.learningfromincidents.io/)
