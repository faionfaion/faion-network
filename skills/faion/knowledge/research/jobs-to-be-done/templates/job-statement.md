<!--
purpose: Job statement skeleton — situation, motivation, outcome across functional, emotional and social dimensions
consumes: switch interviews with real customers
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~250-700 tokens when loaded as context
variables:
  - name: job_name
    type: string
    required: true
    description: The product or feature this statement is scoped to. One job per statement - a job that covers your whole product is a mission statement wearing JTBD clothes.
  - name: situation
    type: text
    required: true
    description: The circumstance that makes this job live, emotional context included - "when the invoice is three weeks late and I have to email a client I like". This is the half people skip and the half that predicts switching.
  - name: motivation
    type: text
    required: true
    description: What they want to do in that moment, in their words and never in your feature's. "Get paid without damaging the relationship", not "send an automated reminder".
  - name: outcome
    type: text
    required: true
    description: The result they are after, functional and emotional together. The functional half explains what they bought; the emotional half explains why they finally switched after two years of coping.
  - name: success_metric
    type: text
    required: true
    description: How the customer knows the job is done - their signal, not your dashboard. If only you can see it, you have written a product metric and called it a job.
  - name: evidence_count
    type: integer
    required: true
    description: How many verbatim quotes from real switchers back this. Below three it is a hypothesis - write the number rather than an impression, and let the reader weigh it.
-->
## Job Statement: {{job_name}}

### Core Job
When {{situation}}
I want to {{motivation}}
So I can {{outcome}}

### Functional Dimension
- Goal: [Specific measurable outcome]
- Success metric: {{success_metric}}

### Emotional Dimension
- Desired feeling: [How they want to feel after]
- Avoided feeling: [What they want to stop feeling]

### Social Dimension
- Desired perception: [How they want others to see them]
- Status signal: [What success in this job signals to others]

### Key Circumstances
- When: {{situation}}
- Where: [Context or environment]
- Why now: [What changed that made this job active]

### Competitive Set (same job, different solutions)
- Direct: [Obvious competing products]
- Indirect: [Non-obvious — doing nothing, workarounds, adjacent products]
- Internal: [Existing habits, manual processes]

### Evidence ({{evidence_count}} verbatim quotes from real switchers; minimum 3)
1. "[Quote]" — interview [ID], [date]
2. "[Quote]" — interview [ID], [date]
3. "[Quote]" — interview [ID], [date]
