# Match Between System and Real World

## Summary

Nielsen Heuristic #2: the interface must use words, icons, and organizational patterns that match users' mental models — not internal system or developer terminology. Replace jargon ("terminate session") with user vocabulary ("log out"). Follow domain conventions (shopping cart, inbox, trash) even when the underlying metaphor is dated. Information must appear in the order users expect, not the order the system processes it.

## Why

When interfaces use system-centric language, users must translate between what they see and what they know — this translation cost increases errors, learning curve, and abandonment. Users already have mental models from real-world experience and other products; matching those models makes the product feel intuitive without any learning. Mismatches (technical abbreviations, wrong date formats, system-centric navigation labels) are invisible to developers but immediately felt by users.

## When To Use

- Auditing UI copy for jargon, abbreviations, or technical terms before a release
- Reviewing API-generated UI strings (error messages, status labels, field names) for plain language
- Localization: verifying translated content matches mental models in the target locale
- When user research reveals confusion about specific labels or navigation terms
- Code review: checking that developer-written placeholder text and labels are user-friendly

## When NOT To Use

- Technical admin dashboards used exclusively by engineers — technical language is correct there
- B2B products where users are domain experts who expect precise technical vocabulary
- When user research or A/B tests have already validated the existing language
- Early prototype stages where content is placeholder — audit when real content is set

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Jargon substitution rules, domain convention table (e-commerce, documents, email, social), icon metaphor guidelines, localization requirements |
| `content/02-examples.xml` | Good examples (Airbnb, Gmail), bad examples (system-centric messages), language audit worked case |

## Templates

| File | Purpose |
|------|---------|
| `templates/language-audit.md` | Audit table: current term, user-friendly assessment, suggested alternative; sections for terminology, error messages, labels |
| `templates/extract-strings.py` | Python script: flatten i18n JSON to key:value list for batch language audit |
