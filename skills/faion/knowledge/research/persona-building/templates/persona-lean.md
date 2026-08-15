<!--
purpose: Lean persona card (1-page) for ad/landing copy
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~200-1500 tokens when loaded as context
variables:
  - name: persona_name
    type: string
    required: true
    description: The label the team will say out loud in standups and ad-set names. A first name plus the thing they own beats a demographic - "Ops-Lead Olena", not "Female 35-44".
  - name: persona_role
    type: text
    required: true
    description: Who they are in one sentence - job title, size of company, and what they are on the hook for. Tell me what their manager judges them on; do not let me guess it.
  - name: primary_goal
    type: text
    required: true
    description: What they are trying to achieve, stated as their outcome and not your feature. What does "done" look like on their side, in their words?
  - name: frustration
    type: text
    required: true
    description: The single biggest thing blocking that goal, with the transcript citation (e.g. T03:L142). If no interview says it, it is your guess and it does not belong on this card.
  - name: verbatim_quote
    type: text
    required: true
    description: How they described the problem themselves. Paste the actual sentence from a transcript. If all you have is a paraphrase, say so - I will not invent one.
  - name: buying_trigger
    type: text
    required: true
    description: The event or threshold that makes them act - the renewal date, the headcount number, the outage. What has to happen before they open the wallet?
  - name: interview_count
    type: integer
    required: true
    description: How many real interviews this card is built from. Under five it is a hypothesis, not a persona - give the true number and let the reader discount it.
-->
# {{persona_name}}

**Who:** {{persona_role}}

**Goal:** {{primary_goal}}

**Frustration:** {{frustration}}

**Quote:** "{{verbatim_quote}}"

**Buys when:** {{buying_trigger}}

**Based on:** {{interview_count}} interviews
**Last validated:** [YYYY-MM-DD]
