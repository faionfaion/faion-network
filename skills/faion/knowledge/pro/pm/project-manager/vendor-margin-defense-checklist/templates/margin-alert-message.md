<!-- purpose: Diplomatic client message body for any bleed > 5% of margin -->
<!-- consumes: alert entry with pattern_id + evidence -->
<!-- produces: drafted message; human reviews before sending -->
<!-- depends-on: content/01-core-rules.xml#r3-bleed-alert-threshold -->
<!-- token-budget-impact: ~120 tokens -->

Subject: Quick check on [project] scope vs SOW — week of [YYYY-MM-DD]

Hi [client first name],

Quick housekeeping note while reviewing progress against our SOW.

This week I logged [hours] hours on [scope item not in original SOW]. The exchange where this came up was [link/quote/date]. To keep the numbers clean (and not surprise either of us at invoice time) I'd like to capture this as a small change order — [hours × rate = $X], adding [N] days to the [milestone] window.

Want me to send the CR over for a quick YES, or shall we hop on a 15-min call Thursday to talk through it?

— [vendor name]

<!--
Diplomacy rules:
- Concrete numbers in body (hours, $, days). No "minor", "small", "just".
- Reference the exact message/thread that requested the work.
- Offer a low-friction next step (reply YES) AND a higher-touch fallback (call).
- Send within 48 business hours of the alert.
-->
