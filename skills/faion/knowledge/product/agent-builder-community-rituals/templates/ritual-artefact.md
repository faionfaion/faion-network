<!--
purpose: Per-session log scaffold for an agent-builder community ritual.
consumes: ritual-calendar entry + actual session attendance.
produces: A public, versioned session log with artefact link.
depends-on: ../scripts/validate-agent-builder-community-rituals.py.
token-budget-impact: ~200 tokens when filled.
-->

---
ritual_id: "<office-hours|eval-sharing|prompt-swap>"
session_date: "<ISO date>"
host: "host:<person>"
organiser: "organiser:<person>"
attendees: ["@a", "@b", "@c"]
artefact_link: "<URL to eval row / prompt diff / runbook update>"
session_index: 1
---

# <ritual_id> — <session_date>

## Topic / agenda

<one-sentence topic>

## Artefact produced

- Type: <eval-row | prompt-diff | runbook-update>
- Link: <URL>

## Retention update

- New members joined this session: <n>
- 90-day retention pct: <number>%

## Next session

- Date: <ISO date>
- Host: <next-host:person> (rotation cycle)
