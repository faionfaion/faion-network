<!-- purpose: next-PR checklist skeleton the junior pastes into the PR description — same fields as content/02-output-contract.xml -->
<!-- consumes: the completed review's comments with permalinks, the previous checklist and its ticks, the team style guide / ADRs / CONTRIBUTING.md, lint and CI config (AGENTS.md Prerequisites) -->
<!-- produces: a checklist validating against scripts/validate-junior-next-pr-checklist-template.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~400 tokens when filled -->

## Next-PR checklist for <owner_handle> (from <trigger_url>, confirmed by <reviewer_name> on: )

3 to 7 items, severity first, at most one blocking. Each line: `[ ]` tick (the junior ticks; the mentor only verifies) — severity — id — yes/no check — (standard cited, or preference:@mentor) — [origin](permalink into the reviewed PR).

- [ ] **blocking** c1 — (check phrased so a reviewer answers yes or no on this PR) — (ADR / style-guide section / CONTRIBUTING anchor) — [origin](https://...#discussion_r...)
- [ ] should c2 — (check) — (standard or preference:@handle) — [origin](permalink)
- [ ] should c3 — (check) — (standard; if a linter can enforce it: rule name + automation ticket, dropped one PR after it lands) — [origin](permalink)

Status per item: new | carried x1 | carried x2 (a third carry becomes a pairing session; an item ticked on two consecutive PRs is retired).

Retired: (checks ticked on two consecutive PRs). Deferred: (candidates with permalinks, promoted when an item retires). Pairing sessions: (item, date).

Posting rule: paste this block into the next PR description and tick every item before requesting review; an unticked or missing checklist is sent back before code is read.

Validation of the JSON form: `python scripts/validate-junior-next-pr-checklist-template.py --file <checklist.json>`.
