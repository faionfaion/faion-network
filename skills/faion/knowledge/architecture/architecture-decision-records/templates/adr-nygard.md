<!--
purpose: Nygard ADR template.
consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
produces: a architecture-decision-records artefact validating against scripts/validate-architecture-decision-records.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~400-1500 tokens once filled
variables:
  - name: adr_number
    type: string
    required: true
    description: The sequence number, zero-padded to three digits (007). It is the filename and what reviewers cite for years. Take the next free number in docs/adr; never reuse one, even from a rejected draft.
  - name: slug
    type: string
    required: true
    description: Two or three kebab-case words naming the thing being decided, not the winner - "session-storage", not "use-redis". A superseding ADR reuses the slug, so it must outlive the answer.
  - name: decision_title
    type: string
    required: true
    description: The decision as a noun phrase someone can scan in a list of forty - "Session storage for the checkout service". No verbs, no "we should", no product name.
  - name: owner
    type: string
    required: true
    description: The one person accountable for this record. A team alias here means nobody answers when the decision is questioned in eighteen months and everyone who was in the room has moved on.
  - name: email
    type: string
    required: true
    description: The owner's email. It has to be reachable after they change teams - this is the address a future engineer writes to before reversing the decision.
  - name: date
    type: string
    required: true
    description: The day the decision was agreed, ISO - not the day it was written up. The gap between those two dates is itself information about how the team decides.
  - name: status
    type: enum
    required: true
    default: "Proposed"
    options: [Proposed, Accepted, Deprecated, Superseded]
    description: Where this record stands. adr-lint.sh closes the enum at exactly these four, and Superseded additionally requires a "Superseded by ADR-NNNN" line in the body.
  - name: alternative_option
    type: string
    required: true
    description: The strongest option you did not pick, named. Rule r3 wants at least two genuine alternatives - if the only one you can name is a strawman, the decision has not been made yet.
  - name: rejection_reason
    type: text
    required: true
    description: Why that option lost, in one sentence a proponent of it would accept as fair. "Not a good fit" is what people write when the real reason was that nobody knew it.
  - name: context
    type: text
    required: true
    description: What forced the decision - the constraint, the deadline, the load figure, the incident. Give me facts and numbers in value-neutral language; if it argues for the option you already picked, it belongs under Decision.
  - name: decision
    type: text
    required: true
    description: What was decided, one paragraph, active voice, present tense. Name the thing chosen and the scope it binds. Reasons go in Context, costs go in Consequences.
  - name: consequences
    type: text
    required: true
    description: What this buys AND what it costs - what gets harder, who carries the new work, what is now expensive to reverse. A consequences list with no negatives is a sales pitch, and I will not write the negatives for you.
-->
---
artefact_id: adr-{{slug}}-{{adr_number}}
owner: {{owner}} <{{email}}>
version: 1.0.0
last_reviewed: 2026-05-23
adr_id: {{adr_number}}
title: {{decision_title}}
status: {{status}}
date: {{date}}
---

## Context

{{context}}

## Decision

{{decision}}

## Consequences

{{consequences}}

## Alternatives Rejected

| Option | Reason rejected |
|--------|-----------------|
| {{alternative_option}} | {{rejection_reason}} |
