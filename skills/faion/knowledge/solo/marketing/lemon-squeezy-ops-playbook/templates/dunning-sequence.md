<!--
purpose: 3-email dunning sequence for failed renewals
consumes: failed_renewal event + customer first name
produces: 3 emails scheduled in LS automation
depends-on: content/01-core-rules.xml
token-budget-impact: ~300 tokens when loaded as context
-->
# Dunning sequence — REPLACE-PRODUCT

## T+1 — soft reminder

Subject: Quick payment hiccup on your REPLACE-PRODUCT subscription

Hi REPLACE-FIRST_NAME,

Your card on file just declined a renewal charge. Banks do this for all sorts of reasons — usually no action needed. We'll retry tomorrow. If you want to update your card now:

REPLACE-CARD-UPDATE-LINK

Thanks,
REPLACE-FOUNDER-NAME

## T+4 — update CTA

Subject: Still can't bill your card — quick fix

Hi REPLACE-FIRST_NAME,

Still no luck on the renewal. The fastest fix is updating your card directly:

REPLACE-CARD-UPDATE-LINK

If you'd rather pause or cancel, just hit reply.

REPLACE-FOUNDER-NAME

## T+8 — final + grace

Subject: Final notice on REPLACE-PRODUCT — grace period offer

Hi REPLACE-FIRST_NAME,

After T+10 your subscription auto-cancels. If you're in a rough spot but want to keep access, hit reply — I'll extend you a grace period.

Otherwise, update your card here: REPLACE-CARD-UPDATE-LINK

REPLACE-FOUNDER-NAME
