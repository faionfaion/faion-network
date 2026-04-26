# Agent Integration — Lessons Learned

## When to use
- Capturing knowledge during and at the end of a project (milestone close, post-incident, full close-out).
- Building a searchable, structured organizational memory across many projects.
- Onboarding new PMs / engineers with curated patterns + anti-patterns.
- Feeding a continuous-improvement loop: lesson → updated checklist → applied next sprint / project.
- Post-incident reviews (PIR / blameless postmortems) when the incident touched scope / cost / schedule.

## When NOT to use
- One-person, one-week project — overhead exceeds value; a 5-line note in the README is enough.
- Already-mature org with strong RCA culture and a working knowledge base — just contribute, don't re-invent the methodology.
- Live incident — capture facts now, lessons later. Do not derail incident response with a retro.

## When it fails / limitations
- "Captured but never used": the canonical failure mode. Lessons sit in a Confluence graveyard.
- Blame culture turns sessions into theater; people stop sharing real failures.
- Sessions held only at project end mean small-but-frequent lessons are forgotten.
- Vague write-ups ("communication was poor") are not actionable; agents and humans both produce these without structured prompts.
- Unsearchable storage (tagged inconsistently, scattered across tools) makes lessons unfindable when relevant.
- Recommendation half-life: tooling lessons stale within 12-24 months as stack changes.

## Agentic workflow
The agent's job is to enforce structure, surface relevance, and close the application loop. Three phases: (1) capture — agent prompts at milestones, after problems, after wins, with a structured form (Situation → Impact → Root Cause → Lesson → Recommendation); writes to a single canonical store. (2) curation — periodic dedup, categorization, severity tagging, expiration of stale lessons. (3) application — at project kickoff, agent retrieves relevant lessons by tag / similarity and inserts them into the planning checklist. Treat the lessons store like a code repo: versioned, reviewed, indexed.

### Recommended subagents
- A `lesson-capturer` subagent (define inline) — interactive prompt, enforces structured fields, never accepts vague entries.
- A `lesson-curator` subagent — weekly cron: dedup, categorize, mark stale (> 24 months for tooling, > 5 years for process).
- A `lesson-retriever` subagent (RAG-style) — at project kickoff, pulls top-k relevant lessons via embedding search + tag filter.
- `password-scrubber` — sweep lessons before publication; people paste credentials into "what went wrong" boxes.

### Prompt pattern
```
You are capturing a lesson. Required fields:
- title (≤ 80 chars, action-oriented)
- project, date, category (planning|execution|technical|team|vendor|stakeholder|security)
- impact_level (high|medium|low) with quantified effect (days delayed, $ overrun, incidents)
- situation (what happened, ≤ 5 sentences, facts only)
- root_cause (5-whys output; reject "human error" without depth)
- lesson (≤ 2 sentences, generalizable)
- recommendation (specific, with owner_role and where_applied: planning|kickoff|review|standup)
- evidence (links to artifacts, metrics)
Reject submission if any field empty or "TBD".
Reject "communication was bad" — push for specific mechanism + fix.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` | Lessons-as-code: Markdown files, PR review per lesson | https://git-scm.com/ |
| `jq` | Query lessons store JSON | https://stedolan.github.io/jq/ |
| `ripgrep` (`rg`) | Full-text search across lesson corpus | https://github.com/BurntSushi/ripgrep |
| `chromadb` / `qdrant` / `weaviate` CLIs | Embedding-based retrieval for relevance search | https://www.trychroma.com/ |
| `notion-cli` / `confluence-cli` | Programmatic write to existing wiki | https://developers.notion.com/ |
| `dataview` (Obsidian) | Local PKM-style lesson queries | https://blacksmithgu.github.io/obsidian-dataview/ |
| `pandoc` | Export lesson summaries to PDF / DOCX for execs | https://pandoc.org/ |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Notion | SaaS | Yes — REST | Lessons DB with rich tags |
| Confluence | SaaS / on-prem | Yes — REST | Enterprise standard |
| Obsidian + sync | OSS / SaaS | Partial | Local-first; agent via filesystem |
| GitHub / GitLab repo | SaaS / on-prem | Yes — REST + git | Lessons-as-code; PR review enforces quality |
| Glean / Mem | SaaS | Yes — REST | Cross-tool retrieval; auto-relevance |
| Coda | SaaS | Yes — REST | Structured + tabular |
| Linear Insights | SaaS | Partial | Project-level retrospectives + linkback |
| Parabol / EasyRetro | SaaS | Yes — REST | Retro tools that export to lessons store |
| Backstage TechDocs | OSS | Yes | Internal-developer-portal lessons section |
| Atlassian Compass | SaaS | Yes — REST | Component-level lessons + scorecards |

## Templates & scripts
See `templates.md` for the lesson record, session agenda, project close-out summary. Inline: extract relevant lessons by tag + similarity for a new project (Python + Chroma).

```python
#!/usr/bin/env python3
import sys, json, chromadb
client = chromadb.PersistentClient(path="./lessons-db")
col = client.get_or_create_collection("lessons")
def retrieve(query, tags=None, k=5):
    where = {"$and": [{"category": t} for t in tags]} if tags else None
    res = col.query(query_texts=[query], n_results=k, where=where)
    out = []
    for i, doc in enumerate(res["documents"][0]):
        out.append({"id": res["ids"][0][i],
                    "title": res["metadatas"][0][i].get("title"),
                    "category": res["metadatas"][0][i].get("category"),
                    "recommendation": res["metadatas"][0][i].get("recommendation"),
                    "snippet": doc[:240]})
    return out
if __name__ == "__main__":
    q = sys.argv[1]
    tags = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    print(json.dumps(retrieve(q, tags), indent=2))
```

## Best practices
- Capture continuously, not just at close-out. Trigger after milestones, incidents, retros, vendor handoffs.
- Enforce a structured schema (Situation, Impact, Root Cause, Lesson, Recommendation). Free-text degrades to noise.
- Quantify impact ($, days, defects, incidents). "Saved time" is not a lesson; "saved 12 dev-days" is.
- Tie every lesson to an *applied* outcome: updated checklist, new test, PR template, training module. Untouched lessons are theater.
- Track lesson-application rate as an SLO: of last quarter's lessons, what % triggered a process change?
- Make the store *findable*: tag taxonomy + embedding search + project-kickoff retrieval ritual.
- Run blameless: focus on systems, not people. Use 5-whys; reject "human error" as terminal cause.
- Expire stale lessons; tooling-specific lessons go stale fast. A `last_validated_on` field with annual review keeps the corpus alive.
- Distribute by audience: PMO gets executive summary, engineering gets technical lessons, sponsors get one-pager.

## AI-agent gotchas
- LLMs generate plausible but vague lessons ("improve communication", "be more proactive"). Force structured fields with rejection on vague input.
- 5-whys done by an LLM tends to be a one-pass narrative, not real root-cause depth. Force iteration: "go one level deeper, what caused that?"
- Agents conflate symptom and cause. Add explicit fields: `symptom`, `cause`, `lesson`. Reject if symptom == cause.
- Retrieval is only as good as the tags. Without a controlled tag taxonomy, agent search returns shallow matches. Curate the taxonomy.
- LLM hallucinates "we did X" details when summarizing — always require evidence links; reject lessons with no artifacts.
- "Recommendation" output drifts to the bland — "consider doing Y". Force: action verb + owner_role + where_applied.
- PII / secrets in lesson text: postmortems often paste log lines with tokens. Run a scrubber pass before commit.
- Cross-team transfer: a lesson from team A applied blindly to team B can be wrong (different stack, different constraints). Tag with applicability scope.
- Lesson corpus drift over years: agents trained on old lessons recommend deprecated tools. Add `last_validated_on`; filter retrieval by recency for tooling category.
- Privacy: blameless culture is policy + tooling. Anonymize names by default; allow opt-in attribution for credit on positive lessons.

## References
- PMBOK Guide 7th Ed. — Development Approach Performance Domain — https://www.pmi.org/pmbok-guide-standards
- "The Field Guide to Understanding 'Human Error'", Sidney Dekker — https://sidneydekker.com/books/
- Google SRE Book — postmortem culture — https://sre.google/sre-book/postmortem-culture/
- Etsy "blameless postmortems" — https://www.etsy.com/codeascraft/blameless-postmortems/
- "Project Retrospectives", Norman Kerth — https://www.dorsethouse.com/books/pr.html
- DORA / Accelerate research — culture + learning correlation with performance — https://dora.dev/
- ITIL 4 — Continual Improvement practice — https://www.axelos.com/certifications/itil-service-management/
