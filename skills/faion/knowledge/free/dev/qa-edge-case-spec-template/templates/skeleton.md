<!--
purpose: Canonical fixed-shape skeleton for a QA edge-case spec.
consumes: An incident URL + reproduction steps + evidence links + a named owner.
produces: A filled spec file at tests/specs/qa-edge-case-<slug>.md, ready to commit.
depends-on: templates/header.yaml for the frontmatter contract.
token-budget-impact: ~600 tokens to fill end-to-end; review costs ~200 tokens.
-->
---
version: 0.1.0           # bump on every refresh
owner: qa-eng:<person>   # person, not team
last_reviewed: YYYY-MM-DD
incident_url: https://...
---

# Given

<state of the system + actor preconditions; one paragraph max>

# When

<the action that triggers the edge case; HTTP call, CLI command, UI flow>

# Then

- <observable consequence 1 — assert this in the test>
- <observable consequence 2 — side effect, log, metric>
- <observable consequence 3 — absence of side effects (no order, no webhook)>

# Evidence

- <Sentry / Jira / ticket URL>
- <PR URL>
- <regression test path: tests/regression/...>

# Decisions

- next_actions:
  - <owner: action — eg. "alice: pin pytest regression at tests/regression/...">
- next_review: YYYY-MM-DD   # default = today + 6 months

# Not applicable

<list canonical sections that genuinely don't apply for this case + the reason; never silently skip>
