<!-- purpose: 4-block agenda with time-boxes and facilitator prompts -->
<!-- consumes: inputs declared in AGENTS.md `## Prerequisites` -->
<!-- produces: artefact conforming to content/02-output-contract.xml (report) -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~350 tokens when loaded -->

# Blameless Retro Agenda (75 min)

## Block 1 — Timeline review (20 min)

- Walk through the auto-draft timeline.
- Question prompt: 'What happened, in order, with timestamps?'
- Language rule: system-as-subject ('the deploy pipeline allowed X'), not person-as-subject.

## Block 2 — Contributing factors (25 min)

- Question prompt: 'What made this cause go undetected?', 'What made impact bigger?', 'What made recovery slower?'
- Capture ≥ 3 factors, each categorised: detection-gap / comms-gap / mitigation-gap / tooling-gap / knowledge-gap / dependency-failure / other.

## Block 3 — Action items (15 min)

- Each AI MUST have a named owner + target date ≤ 90 days.
- Cap at top 3 by impact. Others go to a backlog without owners.

## Block 4 — Meta round (10 min, NON-SKIPPABLE)

- Question prompt: 'What did we ALMOST learn from this incident but didn't dig into?'
- Capture unspoken concerns, hypotheses, cross-incident patterns.

## Block 5 — Publish (5 min)

- Finalise the retro-record JSON; push to the postmortem wiki today.
