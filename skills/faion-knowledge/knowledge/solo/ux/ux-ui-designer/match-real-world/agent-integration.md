# Agent Integration — Match Between System and Real World (Nielsen Heuristic #2)

## When to use
- Auditing UI copy for jargon, abbreviations, or technical terms before a user-facing release
- Reviewing API-generated UI strings (error messages, status labels, form field names) for plain language compliance
- Localization: verifying that translated content still matches users' mental models in the target locale
- When user research reveals confusion about specific labels or navigation terms
- Code review: checking that developer-written placeholder text and labels are user-friendly

## When NOT to use
- Technical admin dashboards used exclusively by engineers — technical language is appropriate there
- B2B products where the users are domain experts who expect and prefer precise technical vocabulary
- When you already have validated language from user research or A/B tests — do not rework what works
- Early prototype stages where content is placeholder — wait until real content is set

## Where it fails / limitations
- Agents lack cultural and regional knowledge — "plain English" rewrites may not match the mental models of non-English-native user bases
- Some technical terms have no plain-language equivalent (e.g., "two-factor authentication") — forced simplification can be less clear
- Industry conventions shift over time; agents trained on older data may suggest outdated metaphors
- Language audit alone cannot surface whether users understand icons — requires usability testing with real users
- Agents cannot detect inconsistency across multi-product environments without being given all string sources simultaneously

## Agentic workflow
An agent can perform a full language audit by extracting all UI strings from a codebase or design file, classifying each as jargon/technical/abbreviation/unclear, and proposing plain-language alternatives using the substitution table pattern. The agent needs the product's target user persona as context — "plain language for a 65-year-old first-time smartphone user" differs from "plain language for a freelance accountant." Human review is required for any string that relates to legal, financial, medical, or security contexts.

### Recommended subagents
- `faion-usability-agent` — applies full heuristic review, including #2, across all UI screens
- general code-search agent — extracts all user-visible strings from i18n files, template files, and error messages

### Prompt pattern
```
You are auditing UI strings for real-world language match (Nielsen Heuristic #2).
Target user: [persona description, e.g., "small business owner, non-technical, age 30-55"].
For each string below, classify it as: OK | JARGON | TECHNICAL | ABBREVIATION | UNCLEAR
Then provide a plain-language alternative for non-OK items.
Strings to audit:
[list of strings]
```

```
Rewrite the following navigation labels so they use the words users would naturally say
when describing the task they want to do. Avoid verbs from the system perspective.
Example: "Repository" → "Your files". Do not use more than 3 words per label.
Labels: [list]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vale` | Prose linter; enforce plain language rules, flag jargon, check reading level | `brew install vale` / docs.errata.ai/vale |
| `write-good` | Node CLI; flags passive voice, weasel words, lexical illusions in copy | `npm i -g write-good` / github.com/btford/write-good |
| `hemingway-cli` | Readability scoring; ensures copy stays at target grade level | `npm i -g hemingway-cli` / github.com/nicksuch/hemingway |
| `jq` | Extract i18n JSON key-value pairs for batch audit | `apt install jq` / jq.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Phrase / Lokalise | SaaS | Yes — REST API | Central i18n string repository; agent pulls strings, rewrites, pushes back for review |
| Hemingway Editor | SaaS | No API | Manual readability check; use hemingway-cli for automation |
| Grammarly Business | SaaS | Partial — browser extension | Style guide enforcement; does not expose batch API |
| Contentful | SaaS | Yes — REST API | CMS with content model; agent can fetch and audit all microcopy fields |
| Hotjar | SaaS | Partial | Session recordings reveal where users pause at confusing labels — provides evidence for audit prioritization |
| UserTesting | SaaS | No API for results | Comprehension testing tool; use to validate agent-proposed rewrites with real users |

## Templates & scripts
See `templates.md` for the Language Audit Checklist template.

Inline script — extract all string values from an i18n JSON file for batch audit:
```python
#!/usr/bin/env python3
# Usage: python extract_strings.py en.json > audit_input.txt
import json, sys

def flatten(obj, prefix=""):
    rows = []
    for k, v in obj.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, str):
            rows.append(f"{key}: {v}")
        elif isinstance(v, dict):
            rows.extend(flatten(v, key))
    return rows

with open(sys.argv[1]) as f:
    data = json.load(f)

for line in flatten(data):
    print(line)
```

## Best practices
- Audit user-visible strings separately from developer-visible strings — do not apply plain language rules to log messages or API error codes
- Use real user vocabulary: search support tickets and user interview transcripts for the exact words users use to describe features, then adopt those words in the UI
- Icon + label is always safer than icon alone — even universally recognized icons (save = floppy disk) should have a visible text label in primary navigation
- Date and number format localization is mandatory, not optional — a US-format date shown to a European user is a real-world mismatch with legal implications in some contexts
- Consistency across the product is as important as individual clarity — "sign in" and "log in" on different screens of the same product is a heuristic #2 violation
- When a technical term is unavoidable, introduce it with a plain-language explanation on first use and use it consistently thereafter
- A/B test terminology changes before rolling out product-wide — users build habits around existing labels; sudden changes cause confusion even if the new label is objectively clearer

## AI-agent gotchas
- Agents default to US English conventions even when locale is explicitly set — review all rewrites for locale-specific idioms and formatting
- Agents may over-simplify industry-standard terms that expert users expect (e.g., changing "invoice" to "bill" in an accounting tool)
- Plain-language rewrites often increase string length, which can break fixed-width UI containers — agents must be told character limits
- Consistency checking across a large codebase requires the agent to hold the full string inventory in context — chunk the audit by feature area and reconcile at the end
- Agents cannot detect if an icon metaphor is culturally appropriate — visual element review requires human judgment or structured user research

## References
- https://www.nngroup.com/articles/match-system-real-world/
- https://www.plainlanguage.gov/guidelines/
- https://m3.material.io/foundations/content-design/writing
- https://learn.microsoft.com/en-us/style-guide/brand-voice-above-all-simple-human
- Content Strategy for Mobile — Karen McGrane (A Book Apart)
