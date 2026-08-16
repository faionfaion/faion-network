<!--
purpose: 5-question MVP sanity check plus a capacity check against build budget — fast gut-check before the full scope doc.
consumes: a candidate MVP feature list, build capacity estimate (see Prerequisites)
produces: an MVP quick-check verdict
depends-on: content/01-core-rules.xml (riskiest-assumption + build-capacity rules the quick check screens for)
token-budget-impact: ~180 tokens when filled
-->

# MVP Quick Check: <feature_list>

## The 5 Questions

1. **Does it solve ONE problem completely?**
   [ ] Yes [ ] No
   Problem: [State it]

2. **Can user get value TODAY (without future features)?**
   [ ] Yes [ ] No
   Value: <what_they_get>

3. **What is the MINIMUM to prove this works?**
   Features needed: <list>

4. **What can wait until v1.1?**
   Deferred: <list>

5. **Can you build this in [X] weeks with [N] devs?**
   [ ] Yes [ ] No — Cut: [What to cut]

## Capacity Check
Must-Have days: [X] / Budget (60% of <weeks_devs_5>): <y>
[ ] Within budget [ ] Over budget — cut <items>

## Verdict
[ ] Scope is right
[ ] Too big — cut these: [X]
[ ] Too small — add: [X]
[ ] Missing hypothesis — write it first
