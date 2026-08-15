<!--
purpose: Pre-filled Mom-Test interview script with question slots
consumes: HYPOTHESIS, PERSONA
produces: Interview template
depends-on: content/01-core-rules.xml
token-budget-impact: ~250 tokens when loaded
variables:
  - name: general_area
    type: text
    required: true
    description: The broad area you open with, in the interviewee's language - "keeping track of client invoices", not "financial workflow optimisation". They have to hear their own life in it.
  - name: specific_topic
    type: text
    required: true
    description: The narrower topic you steer into after the opener. Narrow enough to trigger the memory of one particular occasion, because a general answer is a compliment in disguise.
  - name: did_thing
    type: text
    required: true
    description: The past action you will ask them to walk through - "chased an overdue invoice". Past tense and specific: the Mom Test works because memory is harder to flatter with than opinion.
  - name: signal_scale
    type: enum
    required: true
    default: "strong-weak-none"
    options: [strong-weak-none, pain-scale-1-5, currency-committed]
    description: How you will score each answer afterwards. strong-weak-none is the default; currency-committed only if you are asking for money or a calendar slot in this same conversation.
-->

# Customer Discovery Interview

## Opening (2 min)
"I'm trying to understand how people deal with {{general_area}}. Can you tell me about your experience with {{specific_topic}}?"

Do NOT mention your idea here.

## Exploration (15 min)
- "Walk me through the last time you {{did_thing}}."
- "What was hardest about that?"
- "How did you solve it?"
- "What else have you tried?"
- "How much time or money does this currently cost you?"

## Digging (5 min)
- "Why is that important?"
- "Can you give me a specific example?"
- "What would happen if you didn't solve this?"

## Closing (3 min)
- "Who else should I talk to about this?"
- "What should I have asked that I didn't?"

---
Post-interview: write exact quotes within 10 minutes.
Rate each signal on the {{signal_scale}} scale.
