<!--
purpose: Launch-day email to an existing list, pointing at the Product Hunt listing
consumes: product name + PH listing URL + the day's offer
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~200 tokens when loaded as context
variables:
  - name: product_name
    type: string
    required: true
    description: The product as this list already knows it. If you renamed it since they signed up, use the old name once and the new one after - a launch email is not the place to introduce a rebrand.
  - name: url
    type: string
    required: true
    description: The full Product Hunt listing URL, live before this sends. Every hour this email sits with a dead link is votes going to whoever launched at midnight PT.
  - name: sender_name
    type: string
    required: true
    description: The person signing this - a human they have heard from before, not the company. Launch-day asks work on relationship, and nobody has a relationship with a brand.
  - name: launch_offer
    type: text
    required: true
    description: What the Product Hunt crowd gets today and only today. Be exact about the discount and its expiry; a vague "special offer" reads as a discount you have not decided on yet.
  - name: audience_relationship
    type: text
    required: true
    description: In one clause, who these people are to you - "you have been on the beta since March". It replaces the generic flattery and is the reason they open a launch email at all.
-->
# Launch Day Email Template

Subject: We're live on Product Hunt today

Hi [First Name],

Big day — {{product_name}} just launched on Product Hunt!

{{url}}

You are getting this because {{audience_relationship}}. If {{product_name}} has been useful, an upvote
and a comment would mean a lot. It helps us reach more people like you.

How to support us (2 minutes):
1. Click the link above
2. Hit the upvote button (the orange triangle)
3. Leave a comment about your experience or what you're most excited about

No pressure at all — but if you've gotten value from {{product_name}}, this is the best way to
help us grow.

We're also running something for the PH community today: {{launch_offer}}

Thank you for being part of this from the beginning.

{{sender_name}}

P.S. — I'll be replying to every comment on the listing all day. Come say hi.
