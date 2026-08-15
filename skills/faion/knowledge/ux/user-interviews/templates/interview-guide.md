<!--
purpose: interview guide skeleton with neutrality checklist
consumes: research objectives + user-segment profile
produces: interview guide feeding the user-interviews artefact
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~400-1000 tokens once filled
variables:
  - name: research_topic
    type: string
    required: true
    description: What you are researching, in the participant's language. They hear this sentence in the first ten seconds and decide from it what kind of answers you want - so keep your product out of it.
  - name: project_name
    type: string
    required: true
    description: The project these interviews feed. Sessions get reused across projects and misattributed six months later; the name is what keeps a quote tied to the question it answered.
  - name: interviewer
    type: string
    required: true
    description: Who runs the session. Leading questions are personal habits - naming the interviewer is what makes the neutrality review at the end of this guide possible at all.
  - name: session_minutes
    type: integer
    required: true
    description: How long you tell the participant it will take. Say the true number; running over is the fastest way to lose the last ten minutes, which is where people stop performing.
  - name: research_objective_one
    type: text
    required: true
    description: The first thing you need to learn, phrased so an answer could disappoint you. If no possible response would change your plan, you are booking sessions to confirm something.
  - name: warmup_activity
    type: text
    required: true
    description: The routine activity you ask them to describe first - "how you usually plan your week". Ordinary and specific, to get them narrating rather than opining before the real questions.
-->
# User Interview Guide: {{research_topic}}

**Project:** {{project_name}}
**Interviewer:** {{interviewer}}

## Research Objectives (what we need to learn)
1. {{research_objective_one}}
2. [Objective 2]

## Introduction (5 min — verbatim)
"Hi, I'm {{interviewer}}. Thank you for speaking with me today. I'm researching {{research_topic}} to better understand how people work today. There are no right or wrong answers — I want to learn about your experiences. This will take about {{session_minutes}} minutes. Do you mind if I record this for my notes?"

## Warm-up (5 min)
1. Tell me a little about yourself and your role.
2. Walk me through {{warmup_activity}}.

## Main Questions (30 min)

### Topic 1: [Name]
1. [Open-ended question — "Tell me about the last time you..."]
   - Follow-up: [Probing question — "Why is that?", "Can you give an example?"]
2. [Question]

### Topic 2: [Name]
1. [Question]
2. [Question]

### Topic 3: [Name]
1. [Question]
2. [Question]

## Wrap-up (5 min)
1. Is there anything else about {{research_topic}} you'd like to share?
2. Do you have any questions for me?

"Thank you so much for your time. Your insights are valuable."

## Notes — flag these for review
- Leading questions detected: [list any flagged during prep]
- Pilot feedback: [from internal teammate run-through]
