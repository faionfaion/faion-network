<!-- purpose: Feature-usage-triggered upsell email offering a free trial of the next plan tier. -->
<!-- consumes: customer name + feature usage count + current plan limit -->
<!-- produces: Markdown email template -->
<!-- depends-on: content/01-core-rules.xml (r1-trigger-from-usage-signals-not-calendar, r2-frame-with-customers-own-usage-data) -->
<!-- token-budget-impact: ~200-350 tokens when loaded as context -->

Subject: You've been using [Feature] — here's what Pro unlocks

Hi <name>,

I noticed you've used [FEATURE] [X] times in the last [30] days — nice work.

On <current_plan>, [Feature] is limited to <current_limit>. With <pro_next_plan>, you can:
- [Enhanced capability — specific, concrete]
- [Related feature that complements their usage]
- [Time or effort saving tied to their current pattern]

Teams similar to yours typically save <x_hours_month> after upgrading.

**Try Pro free for 14 days — no credit card changes until you decide:**

[Start 14-Day Pro Trial]

[Your name]

---
*Based on your [Feature] activity on <plan>. <manage_preferences>*
