<!-- purpose: Resolution-response email closing out a support ticket with root cause and fix steps. -->
<!-- consumes: ticket root cause + fix steps + customer name -->
<!-- produces: Markdown email template -->
<!-- depends-on: none -->
<!-- token-budget-impact: ~100-250 tokens when loaded as context -->

# Email: Resolution Response

Subject: Re: <original_subject>

Hi <name>,

Good news — I've figured out <issue_summary>.

Here's what was happening:
[1-2 sentence explanation of root cause — honest and clear]

Here's how to fix it:
1. <step_1>
2. <step_2>
3. <step_3>

[If a bug: "I've also filed this as a bug (ticket #X) so we can prevent it for others."]
[If a feature request: "I've added this to our feature request list — I'll let you know if we build it."]

Let me know if this resolves things or if you have other questions.

Best,
[Your name]
<product_name> Support
