# Agent Integration — Help and Documentation

## When to use
- Auditing an existing product for help gaps during a UX review sprint
- Generating first-draft contextual tooltips, inline hints, or FAQ entries for a new feature
- Analyzing support ticket logs to identify recurring help needs
- Producing a help article from a list of step-by-step procedures
- Creating onboarding tour scripts tied to specific UI actions

## When NOT to use
- When the interface itself needs a redesign to eliminate confusion (fix the root, not the docs)
- Replacing qualitative usability testing — help content audits do not substitute for observing real users
- Generating legally binding product documentation without human legal review
- When the feature set is still unstable and help content will become outdated before it ships

## Where it fails / limitations
- LLMs generate plausible-sounding but incorrect step sequences without product access
- Screenshots and video captions require human production tooling — an agent cannot produce them
- SEO optimization of help articles requires search volume data that an agent cannot query without tool access
- Help content decay is invisible to agents: they will not detect that a previously generated article became stale

## Agentic workflow
A Claude subagent is most useful for drafting help content at scale: given a feature description or support-ticket dump, it can produce structured articles following the help content template in `templates.md`. A second agent can then audit coverage by cross-referencing a list of product features against existing articles. Human review is mandatory before publishing to catch factual errors.

### Recommended subagents
- `faion-sdd-executor-agent` — execute help content audit tasks from an SDD task list
- Any general Claude subagent with file-write permission — draft help articles and save to a docs directory

### Prompt pattern
```
Given the following feature description, write a help article following this structure:
Title: How to [Task]
Sections: Overview, Steps (numbered), Result, Troubleshooting, Related Topics.
Feature: <paste description>
```

```
You are a help content auditor. Given a list of features and a list of existing help articles,
identify features with no help coverage and output a gap table: | Feature | Coverage | Priority |
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Docusaurus | Static help center with search | `npx create-docusaurus@latest` / docusaurus.io |
| MkDocs | Markdown-based documentation site | `pip install mkdocs` / mkdocs.org |
| Mintlify | Modern docs with AI search | mintlify.com (SaaS + CLI) |
| Vale | Prose linter for consistency/style | `brew install vale` / vale.sh |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Intercom Articles | SaaS | Yes (REST API) | Create/update articles via API; search analytics available |
| Zendesk Guide | SaaS | Yes (REST API) | Article CRUD; search query logs exportable |
| HelpScout Docs | SaaS | Yes (REST API) | Articles API; beacon embed for contextual help |
| Notion | SaaS | Yes (API) | Can host help base; search and create pages via API |
| Docusaurus | OSS | Yes (file-based) | Drop Markdown files → CI builds static site |

## Templates & scripts
See `templates.md` for the Help Content Template and Help Audit Template.

Inline script — help gap finder (given a feature list and an article list):
```python
# help_gap_finder.py — find features missing help coverage
features = ["password reset", "team invite", "export CSV", "billing settings"]
articles = ["how-to-export-csv", "billing-faq", "password-reset-guide"]

def slugify(s):
    return s.lower().replace(" ", "-")

gaps = [f for f in features if not any(slugify(f) in a for a in articles)]
for gap in gaps:
    print(f"MISSING help: {gap}")
```

## Best practices
- Write help articles around user tasks (verbs), not product features (nouns)
- Test search discoverability: type the phrase a frustrated user would type, not the feature name
- Link related articles bidirectionally — users who read "password reset" also need "two-factor auth"
- Add a "Last reviewed" date to every article; schedule quarterly reviews in project backlog
- Measure article quality via deflection rate (tickets created after reading an article = failure)
- Keep FAQs short — five questions max per page; create separate articles for depth

## AI-agent gotchas
- Agents do not have access to the live product UI; every step they generate must be verified against actual flows before publishing
- LLMs tend to over-enumerate steps — instruct the agent to keep articles under 500 words and audit length in a follow-up pass
- If the agent references screenshots or UI labels, those must be validated; UI text changes break accuracy
- Human checkpoint required: legal/compliance review for any article touching billing, security, or account deletion
- Agents cannot test search functionality; include a manual search QA step in the workflow

## References
- https://www.nngroup.com/articles/help-and-documentation/
- https://www.writethedocs.org/guide/
- https://developers.google.com/tech-writing
- Steve Krug, "Don't Make Me Think" (Sensible.com)
- https://learn.microsoft.com/en-us/style-guide/welcome/
