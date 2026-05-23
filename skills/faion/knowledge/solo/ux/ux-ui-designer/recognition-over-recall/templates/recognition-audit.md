<!--
purpose: recognition audit report skeleton (Nielsen H#6)
consumes: UI surface inventory + icon allowlist + clickable prototype
produces: a recognition-over-recall artefact validating against scripts/validate-recognition-over-recall.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~600-1500 tokens once filled
-->
# Recognition Audit: [Feature / Screen]

**Date:** [Date]
**Reviewer:** [Name]

## Recall Requirements

| Task | Recall Required | Recognition Alternative | Priority |
|------|-----------------|------------------------|----------|
| [Task] | [What user must remember] | [How to show instead] | H/M/L |

## Hidden Information

| Information | Where Hidden | Should Be Visible? | Notes |
|-------------|--------------|-------------------|-------|
| [Info] | [Location] | Y/N | [Context] |

## Icons Without Labels

| Icon | Meaning | Label Needed? | Tooltip Acceptable? |
|------|---------|---------------|---------------------|
| [Icon] | [Meaning] | Y/N | Y/N |

## Multi-step Context Failures

| Step | Information from Prior Step | Still Visible? | Fix |
|------|-----------------------------|----------------|-----|
| [Step] | [Prior info needed] | Y/N | [How to show] |

## Recommendations

| Issue | Recall Burden | Recognition Alternative | Priority |
|-------|---------------|------------------------|----------|
| [Issue] | [What must be recalled] | [Recognition fix] | H/M/L |
