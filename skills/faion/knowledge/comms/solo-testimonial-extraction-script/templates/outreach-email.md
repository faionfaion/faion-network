<!--
purpose: 3-question testimonial outreach skeleton
consumes: Customer record
produces: Outreach email
depends-on: content/01-core-rules.xml
token-budget-impact: ~200 tokens when loaded
variables:
  - name: first_name
    type: string
    required: true
    description: The customer's first name as they sign their own emails - the short form if that is what they use. Get it wrong and the rest reads like a mail merge, which it is.
  - name: recent_project
    type: text
    required: true
    description: The specific thing you built or fixed for them, named the way they name it internally. "Your project" tells them this went to fifty people and none of them owed you a reply.
  - name: your_name
    type: string
    required: true
    description: How you sign off - the name they already know you by, not your legal name and not your company's. This is a favour being asked between two people.
  - name: publish_surface
    type: string
    required: true
    default: "the site"
    description: Where the quote would actually appear - "the site", "the case-study page", "LinkedIn". Consent is specific; naming the surface is the difference between permission and a guess.
-->

Subject: Quick favour — 3 questions about your experience

Hi {{first_name}},

Hope {{recent_project}} is still humming along. I'm collecting customer stories and would love 3 quick answers if you have 5 minutes:

1. **Before we started, what hesitation did you have?**
2. **What happened that made it worth it?**
3. **Who would you NOT recommend this to?** (this one is actually the most helpful — it tells future buyers if they're a fit)

If you reply with a few sentences, can I publish your words + name + role on {{publish_surface}}?
- [ ] Yes, quote + name + role
- [ ] Yes, quote only (no name)
- [ ] No publication

Thanks,
{{your_name}}
