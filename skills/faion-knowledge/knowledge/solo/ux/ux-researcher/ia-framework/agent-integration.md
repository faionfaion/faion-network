# Agent Integration — Information Architecture Framework

## When to use
- At the start of a product or site build, before any navigation or page structure is committed to code
- When users consistently report they "can't find things" and analytics confirm high search usage and low direct navigation
- During a content migration or redesign where the existing structure needs to be evaluated and reorganized
- When adding a new content type or feature to an existing product — to validate it fits the current IA before creating a one-off page
- When onboarding stakeholders who need to understand the product's structural logic before contributing content

## When NOT to use
- For single-purpose tools with fewer than 10 distinct screens — a simple user flow diagram suffices
- When the product's navigation is already well-validated by tree testing and usability data — redo IA only when evidence warrants it
- As the first step in a research process; IA should follow user research (card sorting, interviews), not precede it
- When the team has no authority over navigation or content organization (e.g., working inside a locked CMS template)

## Where it fails / limitations
- IA designed without user input reflects the organization's mental model, not users' — org-chart navigation is the most common failure
- Tree testing validates findability of a specific label structure but not the navigation experience (visual design, microcopy, discoverability)
- Deep hierarchies (5+ levels) test well in tree testing but fail in practice because users lose context of where they are
- IA framework covers structure and labeling; it does not address search quality, which becomes the primary navigation for large content sets
- Scalability assumptions built into the taxonomy break when content volume grows faster than planned

## Agentic workflow
An agent can generate a first-pass IA structure from a content inventory or product description, evaluate an existing sitemap against IA principles (findability, understandability, scalability, flexibility), and produce tree testing questions from a proposed IA. A human validates against user research findings, conducts or reviews card sorting/tree testing, and makes final structural decisions.

For ongoing governance, an agent can flag when new content added to a CMS does not fit existing categories, suggest taxonomy placement, and produce a quarterly IA health report from page analytics.

### Recommended subagents
- `faion-sdd-executor-agent` — generate IA strategy document, evaluate existing sitemap against IA principles, produce tree testing task list
- General Claude subagent — suggest category groupings from a content list, evaluate label clarity, flag jargon terms in navigation labels

### Prompt pattern
```
You are an information architect. Evaluate this sitemap against the four IA principles:
1. Findability — can users locate what they need?
2. Understandability — are labels in plain user language?
3. Scalability — will the structure hold as content grows?
4. Flexibility — can content appear in multiple contexts?

Sitemap:
[paste sitemap]

For each principle, identify: what works, what is at risk, and a specific recommendation.
```

```
Given this list of content items: [list]
And this user research showing how users group them: [card sort summary or list of user mental model terms]

Propose an IA structure:
- Organization scheme: [task / topic / audience — choose one and justify]
- Top-level categories (max 7): [suggest with plain-language labels]
- Problematic items that don't fit neatly: [flag these explicitly]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tree` | Visualize directory-tree IA in markdown docs | Built-in on Linux; `brew install tree` on macOS |
| `csvkit` + `sqlite3` | Query and filter large page inventories for IA analysis | `pip install csvkit` / csvkit.readthedocs.io |
| `markdown-toc` | Auto-generate navigable TOC for large IA documents | `npm i -g markdown-toc` / github.com/jonschlinkert/markdown-toc |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optimal Workshop (Treejack) | SaaS | Partial (API) | Tree testing; results export via API for agent analysis |
| Optimal Workshop (OptimalSort) | SaaS | Partial (API) | Card sorting; dendrograms and similarity matrix export |
| Whimsical | SaaS | No | Fast sitemap creation; no programmatic API |
| Miro | SaaS | Partial (REST API) | Collaborative IA mapping; API for board creation and card management |
| Airtable | SaaS | Yes (REST API) | Taxonomy and content inventory management; full CRUD via API |
| Contentful | SaaS | Yes (REST API + GraphQL) | CMS with structured content types; IA reflected in content model |

## Templates & scripts
See `ia-templates/` directory for: IA strategy document, sitemap template with legend and page inventory, taxonomy document template, and common IA pattern references (mega menu, hub-and-spoke, flat structure).

Inline: IA principle audit scoring function:
```python
def score_ia_label(label: str, jargon_terms: list[str], max_words: int = 4) -> dict:
    """
    Score a navigation label for basic IA quality.
    Returns a dict with pass/fail per criterion.
    """
    words = label.split()
    has_jargon = any(j.lower() in label.lower() for j in jargon_terms)
    return {
        "label": label,
        "length_ok": len(words) <= max_words,
        "no_jargon": not has_jargon,
        "not_generic": label.lower() not in {"resources", "solutions", "misc", "other", "general"},
        "sentence_case": label[0].isupper() and label[1:].islower() if len(label) > 1 else True,
    }
```

## Best practices
- Conduct card sorting before finalizing category labels; generate the IA structure from user groupings, then validate with tree testing before committing to code
- Navigation labels should be in the user's vocabulary, not the organization's; test labels with a simple first-click test if card sorting is not feasible
- Limit navigation depth to 3 levels maximum for task-based UIs; content-heavy sites can justify 4 but rarely 5
- Separate the IA structure from the visual navigation design — the structure (what exists and how it relates) is separate from the UI pattern (how it's presented)
- Assign a taxonomy owner with authority to approve new categories; without governance, taxonomies become internally inconsistent within 6-12 months
- Review the IA annually against analytics: pages with no traffic despite good placement indicate label or discoverability problems; pages with high exit rates despite being the right destination indicate content problems

## AI-agent gotchas
- Agents default to topic-based organization schemes; if the product needs task-based or audience-based IA, specify this explicitly — the default will not match
- Agent-generated category labels often include marketing language ("Solutions", "Resources") that users do not recognize as navigation targets; instruct the agent to flag these
- LLMs cannot evaluate label clarity without knowing the target user's vocabulary; provide a glossary of user terms vs. internal terms in the prompt
- Agent structural suggestions are based on training data patterns (common SaaS, e-commerce, content site structures); niche domains may require significantly different IA patterns
- Do not use agent-generated IA as input to tree testing without human review; poorly structured agent IA will produce misleading tree test results

## References
- Rosenfeld, L., Morville, P., Arango, J. "Information Architecture for the Web and Beyond." O'Reilly, 2015.
- Covert, A. "How to Make Sense of Any Mess." Self-published, 2014. https://www.howtomakesenseofanymess.com/
- Martin, L.M. "Everyday Information Architecture." A Book Apart, 2019.
- NNg IA 101: https://www.nngroup.com/articles/information-architecture-101/
- IA Institute: https://www.iainstitute.org/
- UX Booth complete guide: https://www.uxbooth.com/articles/complete-beginners-guide-to-information-architecture/
