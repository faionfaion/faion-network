# Agent Integration — Match Between System and Real World

## When to use
- Content audit: reviewing all UI labels, error messages, and instructions for technical language
- Localization prep: ensuring terminology matches user vocabulary before translation
- Error message redesign: replacing system-generated error codes with plain language
- Onboarding copy review: new users encounter the most jargon because they lack domain context
- B2B product launches into a new industry vertical: the same feature may need entirely different terminology for finance vs. healthcare vs. logistics users

## When NOT to use
- Developer tools and CLIs intentionally targeted at technical users — technical language is correct for the audience
- Internal admin panels where all users are trained staff familiar with system terminology
- When users have explicitly indicated they prefer technical precision over simplicity (e.g., API documentation)

## Where it fails / limitations
- "User language" varies by segment — what is familiar to one cohort is jargon to another; a single audit cannot cover all segments
- Finding user language requires actual research (interviews, search logs, support tickets) — guessing produces plausible-sounding but wrong vocabulary choices
- A/B testing terminology changes is expensive; teams often ship the agent's suggestion without validation
- Localization is deeper than word substitution — logical information order, date formats, and cultural metaphors require locale-specific review that agents cannot fully handle
- Consistency enforcement across a large codebase is tedious; a one-time audit without tooling degrades back to jargon over time

## Agentic workflow
Claude subagents can audit a provided list of UI strings, error messages, and labels against a set of plain-language rules, generating a Language Audit Checklist with suggested replacements. Agents can also generate locale-appropriate copy variants when given a target locale and base English text. For systematic enforcement, agents can generate ESLint or custom linter rules that flag hard-coded technical strings. Human review is required for domain-specific terminology where the "plain language" alternative changes meaning.

### Recommended subagents
- `faion-usability-agent` — language audit; generates plain-language replacements for technical UI strings
- `faion-sdd-executor-agent` — implements terminology changes in code; updates i18n string files

### Prompt pattern
```
Audit the following UI strings for violations of "Match Between System and Real World" (Nielsen #2).
For each string:
1. Identify technical terms, jargon, or system-centric language
2. Suggest a plain-language alternative in the user's vocabulary
3. Flag if the meaning changes with the replacement (requires human review)

User type: {user_description}
UI strings:
{strings_list}
```

```
Rewrite the following error messages so they:
1. Explain what happened in plain language (no error codes or HTTP status)
2. Tell the user what to do next
3. Match the tone: {tone: friendly/professional/minimal}

Current error messages:
{error_messages}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `write-good` | Lints prose for passive voice, weasel words, jargon | `npm i -g write-good` |
| `alex` | Flags insensitive or unequal language in text | `npm i -g alex`; alexjs.com |
| `textlint` | Extensible text linting; custom rules for domain jargon | `npm i -g textlint`; textlint.github.io |
| `vale` | Prose style linter for technical writing; custom vocab lists | `brew install vale`; vale.sh |
| `i18next-parser` | Extract i18n keys from code for audit | `npm i -g i18next-parser` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hemingway Editor | SaaS | No | Grade-level readability check; web-only |
| Readable.io | SaaS | Partial | Readability API; Flesch-Kincaid scoring |
| Vale + GitHub Actions | OSS | Yes | CI prose linting; enforce custom style guide in PRs |
| Lokalise | SaaS | Yes | i18n management with API; stores locale string variants |
| Phrase (Memsource) | SaaS | Yes | Translation management; API for string extraction |
| Crowdin | SaaS | Yes | OSS-friendly localization platform with API |

## Templates & scripts
See `templates.md` for Language Audit Checklist.

Inline script — scan i18n JSON for technical terms using a blocklist:
```python
import json, re

JARGON_BLOCKLIST = [
    r"\bauth(enticate|entication)?\b",
    r"\brepository\b",
    r"\bsync(hronize)?\b",
    r"\bvalidat(e|ion)\b",
    r"\bterminate\b",
    r"\bexecut(e|ion)\b",
    r"\bquery\b",
    r"error\s+\d{3}",  # HTTP status codes in messages
]

def audit_i18n_file(path: str) -> list[dict]:
    with open(path) as f:
        strings = json.load(f)

    violations = []
    for key, value in strings.items():
        if not isinstance(value, str):
            continue
        for pattern in JARGON_BLOCKLIST:
            if re.search(pattern, value, re.IGNORECASE):
                violations.append({
                    "key": key,
                    "value": value,
                    "pattern": pattern,
                    "action": "Replace with plain-language alternative",
                })
    return violations

for v in audit_i18n_file("en.json"):
    print(v)
```

## Best practices
- Source plain-language alternatives from support tickets and user interview transcripts, not from the team's internal vocabulary
- Apply terminology decisions to a shared glossary first, then update the codebase — consistent terminology across the product is more important than any single perfect label
- Error messages are the highest-ROI target: they occur at moments of user frustration and must be maximally clear
- Test terminology with a comprehension task, not a preference question — ask "what would you do after reading this?" not "which version do you prefer?"
- Maintain a two-column forbidden-terms list: left column system term, right column user term; feed this list to the linter and the agent's prompt
- For multi-locale products, have a native speaker validate terminology in each locale independently — direct translation of English user-friendly terms can produce awkward or misleading text

## AI-agent gotchas
- Agents rewriting technical terms often change meaning subtly — "repository" replaced with "folder" loses the version-control concept; require the agent to flag ambiguous replacements
- Plain-language alternatives generated for generic instructions may not match the product's specific feature names; provide a product glossary as context
- Error message rewrites by agents default to overly apologetic tone ("We're so sorry something went wrong!") — specify the desired tone explicitly
- Agents do not know what terms your specific user segment actually uses; without interview or support ticket data as input, they will use generic consumer-app vocabulary
- Human checkpoint required before terminology changes are deployed — wrong plain-language replacements erode trust faster than technical jargon

## References
- Nielsen Norman Group: Match Between System and Real World — https://www.nngroup.com/articles/match-system-real-world/
- PlainLanguage.gov: Federal Plain Language Guidelines — https://www.plainlanguage.gov/guidelines/
- Karen McGrane: *Content Strategy for Mobile* (A Book Apart)
- Vale prose linter: https://vale.sh
- textlint: https://textlint.github.io
- Microsoft Writing Style Guide: https://learn.microsoft.com/en-us/style-guide/
