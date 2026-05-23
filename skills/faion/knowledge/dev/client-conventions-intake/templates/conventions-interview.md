<!--
purpose: 8-dimension intake interview script.
consumes: nothing — used live with the client contact.
produces: raw answers per dimension that the report consumes.
depends-on: client contact available for a 30 min call.
token-budget-impact: ~200 tokens when copied.
-->

# Client conventions intake — 30 min interview

For each dimension: ask the question; record answer verbatim; ask "where is this written?" — capture the source.

## 1. Branching
- What is the branching model? (trunk-based / gitflow / other)
- Maximum branch age?
- Branch-naming convention?

## 2. Commit style
- Convention? (conventional-commits / freeform / other)
- Squash / merge / rebase?
- Commit-message template?

## 3. Code review
- Required reviewers (count + roles)?
- SLA — turnaround target?
- Self-review allowed?

## 4. Naming
- File naming (kebab / snake / camel)?
- Language-specific (Python snake, TS camel, etc.)?
- Branch naming?

## 5. CI gates
- What runs on every PR?
- What blocks merge?
- Wall-clock budget?

## 6. Security
- Secrets in code policy?
- Vault / secret manager?
- Dependency-audit cadence?

## 7. Documentation
- Required docs per change (CHANGELOG, AGENTS.md, etc.)?
- Where do design docs live?
- ADR / decision log?

## 8. Communication
- Channels (Slack / email / tickets)?
- Async vs sync default?
- Working hours / timezone?

After the call: cross-check stated against last 30 days of merged PRs. Send mismatch list to contact. Get signed reply.
