<!--
purpose: .aidocs/memory/mistakes.md skeleton — recurring-error entries with frequency, root cause, fix, detection method, first/last seen.
consumes: nothing beyond the repo's own code-review and post-mortem history
produces: mistakes-file artefact (project-local memory, sibling to this methodology's pattern entries — not validated by content/02-output-contract.xml, which shapes patterns not mistakes)
depends-on: nothing
token-budget-impact: ~250-450 tokens when loaded as context
-->

# Mistakes: <project_name>

Project: <project_name>
Updated: <updated>

<!-- This file captures recurring errors and how to prevent them.
     Add entries after code review cycles and post-mortems.
     Each entry should include the detection method so future reviews catch it early.
     Resolved mistakes (not seen in 3+ features) can be archived. -->

## <mistake_name>

**Frequency:** rare / occasional / frequent
**Root cause:** {why this mistake happens}
**Impact:** {what goes wrong when this occurs}

**Fix:**
{What to do instead — be specific}

```{lang}
{Correct version — max 5 lines}
```

**Detection:**
{How to catch this in code review or automated checks}

**First seen:** <feature_nnn_name>
**Last seen:** {feature-NNN-name or "not recurred"}

---

## {mistake-name}

**Frequency:** {frequency}
**Root cause:** {root cause}
**Impact:** {impact}

**Fix:** <fix_description>

**Detection:** <detection_method>

**First seen:** <feature_nnn_name>
