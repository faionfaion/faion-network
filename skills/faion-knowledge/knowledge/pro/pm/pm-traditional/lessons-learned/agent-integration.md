# Agent Integration — Lessons Learned (PM Traditional)

## When to use
- Capturing decision rationale + outcomes continuously through a project, not only at close-out.
- Running structured retrospectives (per milestone, per sprint, project-end) where the team produces searchable lessons.
- Building an organisation-level knowledge base where future PMs query "what went wrong on similar projects?" before starting work.
- Updating onboarding docs / checklists / templates with concrete, evidence-backed improvements after each project.
- Feeding the `faion-improver` and `faion-sdd-execution` mistake/pattern memories with structured PM lessons.
- Generating a project close-out report whose top 5 lessons are the executive summary, not the body.

## When NOT to use
- Trivial routine work where lessons are predictable; capturing them adds noise.
- Active blame / political environments — lessons-learned sessions become weapons; fix the culture first or run anonymous-only retros.
- Live-incident postmortems (use blameless postmortem templates, not project lessons).
- Confidential / regulated programs where lesson-sharing requires legal review per item — defaults break.

## Where it fails / limitations
- Most lessons-learned databases are write-only: people log entries no one ever reads. Without a query path at project-start, the methodology fails.
- Lessons captured at project end suffer recency bias and survivorship bias; only people still on the project participate.
- "Communication was bad" is the median lesson — vague, unactionable, repeated forever. Without specificity rules, the database becomes wallpaper.
- LLM summarisation flattens nuance: two distinct lessons collapse into a generic platitude.
- Cross-project search depends on consistent tagging; ad-hoc category fields drift over years and become ungroupable.
- Anonymisation tension: removing names hides the source context that gives a lesson credibility; keeping names suppresses honesty.
- Recommendations rarely close the loop into checklists/process; without a feedback mechanism, the lesson is decorative.

## Agentic workflow
The agent runs three loops. (1) Capture loop: a daily Slack/Discord bot prompts "any lesson today?" and parses unstructured replies into the standard schema. (2) Retro loop: a facilitator agent runs structured sessions (5-min phases), captures sticky-note input, clusters via embeddings, surfaces root causes. (3) Apply loop: at every new project's kickoff, a `kickoff-briefer` agent queries the lessons DB for matching context (similar tech, similar team size, similar vendor) and pre-loads the relevant top-5. Humans verify, edit, and commit lessons; humans also own the action items.

### Recommended subagents
- `lesson-capturer` — converts free-text retro notes into the canonical schema (situation/impact/root-cause/lesson/recommendation).
- `retro-facilitator` — runs the 6-phase agenda; enforces equal speaking time; clusters themes via embedding similarity.
- `kickoff-briefer` — given a new project profile, retrieves top-N matching lessons from history.
- `recommendation-tracker` — tracks whether lessons' recommendations got integrated into checklists/templates; flags decay.
- `faion-improver` — already runs an audit/improve loop; lessons feed the mistakes.md memory.
- `faion-sdd-execution` — patterns and mistakes from lessons feed reflexion memory in the next sprint.

### Prompt pattern
```
Capture mode:
Input: free text (Slack message, retro note)
Output JSON:
{ "title": "<short>",
  "category": "planning|execution|technical|team|vendor|stakeholder|other",
  "impact_level": "high|medium|low",
  "situation": "<facts>",
  "impact": "<effect on project>",
  "root_cause": "<why>",
  "lesson": "<insight>",
  "recommendation": "<actionable change>",
  "evidence_links": ["<URL>"] }
Reject if recommendation is not actionable (no verb, no owner, no metric).

Retrieval mode (kickoff):
Input: {project_type, tech_stack, team_size, vendor_count, regulated}
Output: top 5 lessons by semantic + tag similarity, with confidence.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `obsidian-cli` | Manage lessons in an Obsidian vault with bidirectional links | https://github.com/Yakitrak/obsidian-cli |
| `git` | Version-control lessons; review via PRs | https://git-scm.com/ |
| `chromadb` / `qdrant` / `weaviate` | Embedding store for semantic retrieval | https://www.trychroma.com/ |
| `pandoc` | Convert lessons MD → close-out PDF / DOCX | https://pandoc.org/ |
| `mermaid-cli` | Render fishbone / 5-whys diagrams in lessons | https://github.com/mermaid-js/mermaid-cli |
| `jq` | Query JSONL lesson archives | https://stedolan.github.io/jq/ |
| `gh issue` | Track recommendation actions as GitHub issues | https://cli.github.com/ |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Confluence + AI | SaaS | Yes — REST | Standard PMO knowledge home; weak tagging |
| Notion | SaaS | Yes — REST | Database + relations; good for tagging |
| Obsidian | OSS | Yes — file-based | Markdown vault; agent-friendly |
| GitBook | SaaS | Yes — REST | Public-facing playbooks |
| Glean / Mem | SaaS | Yes — REST | Org-wide enterprise search over lessons |
| Coda | SaaS | Yes — REST | Database-driven retros |
| Miro / Mural | SaaS | Yes — REST | Live retro boards; export to MD |
| FunRetro / Parabol / EasyRetro | SaaS | Yes — REST | Dedicated retro tools |
| Linear / Jira | SaaS | Yes — REST | Track recommendation actions |

## Templates & scripts
See `templates.md` for the lessons log + retro agenda. Lesson-capture validator (~25 lines):

```python
REQUIRED = ["situation","impact","root_cause","lesson","recommendation"]
def validate(lesson):
    missing = [k for k in REQUIRED if not lesson.get(k)]
    if missing:
        return False, f"missing: {missing}"
    rec = lesson["recommendation"].lower()
    has_verb = any(v in rec for v in
        ["add","remove","change","require","reject","schedule","train",
         "document","review","escalate","measure","tag","automate"])
    if not has_verb:
        return False, "recommendation lacks action verb"
    if len(lesson["recommendation"].split()) < 6:
        return False, "recommendation too vague"
    if lesson.get("impact_level") not in ("high","medium","low"):
        return False, "impact_level required"
    return True, "ok"
```

## Best practices
- Capture lessons within 24 hours of the trigger event; weekly retros lose specifics.
- Make the recommendation testable: "Add 25% buffer when introducing new framework" beats "improve estimation".
- Tag lessons by context (tech, team size, vendor type, regulation), not just by category. Retrieval needs context match, not topic match.
- Review the top 3 matching lessons at every kickoff out loud; an unread database is dead weight.
- Sunset lessons older than 24 months (or re-validate); industry context drifts and stale lessons mislead.
- Track which lessons led to checklist/template updates — these are the high-value ones. Archive the rest.
- Run lessons-learned blame-free: facilitator opens with "we discuss processes, not people", and enforces it.

## AI-agent gotchas
- LLMs flatten distinct lessons into homogeneous platitudes during summarisation. Preserve verbatim quotes plus a derived summary.
- Categorisation drift: ten retros run by ten agents create twenty category names. Pin a closed enum (planning/execution/technical/team/vendor/stakeholder/other) and reject others.
- Sentiment bias: positive-framed prompts harvest "what went well" > "what went wrong" by 3:1; balance the prompt explicitly.
- Hallucinated impact metrics: agents fabricate "delayed 3 weeks" when the source said "some delay". Demand evidence_links or refuse.
- Privacy: lesson capture often contains PII / vendor names / financials; run a PII redactor before storing in shared DB.
- Embedding drift: model upgrades silently change retrieval; re-index with version pinned.
- "Action item theatre": agents emit recommendations with no owner/due-date and the database fills with orphans. Require owner + by-date or reject the lesson.
- Survivorship bias in retro: only project survivors speak; quitters' lessons are missing. Run mid-project pulse surveys for early signal.

## References
- PMI PMBOK Guide 6th Ed., Chapter 4 — Project Integration Management (Lessons Learned Register).
- "Project Retrospectives" — Norman Kerth (originator of the Prime Directive, blame-free retros).
- "Agile Retrospectives" — Esther Derby & Diana Larsen.
- Atlassian's Blameless Postmortem playbook (https://www.atlassian.com/incident-management/postmortem/blameless).
- Edmondson, *The Fearless Organization* — psychological safety preconditions for honest lessons.
- ISO 30401:2018 — Knowledge Management Systems.
