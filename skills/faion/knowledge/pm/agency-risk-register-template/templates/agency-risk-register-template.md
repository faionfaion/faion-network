<!-- purpose: agency risk register for the Monday refresh — 30-minute timebox, 90-day concentration recompute, 8-column rows across the six agency classes with quantified details, responses on rows at 15 or more, closed tab -->
<!-- consumes: trailing-90-day billing export, CRM stage-weighted pipeline, ledger by currency, contractor list, credential inventory, regulatory obligations -->
<!-- produces: filled artefact for validate-agency-risk-register-template.py -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~700 tokens when fully filled -->

# Agency Risk Register — <company_name> — Monday <artefact_date>

- headcount: <3 to 25>
- owner of the refresh: <owner_full_name>

## Refresh (30 minutes)
- minutes: scores_update <5>, top5_walk <15>, action_note <10>, total <at most 30>
- consecutive_overruns: <n>, split_or_prune_required: <true after two overruns>
- action_note: <what changed, who does what by when>

## Concentration (billing export, trailing 90 days, recomputed today)

| client | share of trailing-90-day revenue |
|---|---|
| <every client; above 20 percent gets a row, 40 percent or more scores 15+> | <0.xx> |

## Register (8 columns; agency classes only)

| id | class | description | likelihood | impact | score | owner | trigger |
|---|---|---|---|---|---|---|---|
| R-01 | <revenue_concentration, key_person, fx_currency, contractor_classification, pipeline_thinness, regulatory> | <the risk> | <1-5> | <1-5> | <likelihood x impact> | <a named person> | <observable event that flips it to actioned> |

### Details per class
- revenue_concentration: client <name>, share <0.xx>
- key_person: item <credential, system, relationship, skill>, holder <person>, remediation_owner <person>, deadline <YYYY-MM-DD>
- fx_currency: revenue_share_by_currency <USD 0.6, EUR 0.4>, cost_share_by_currency <EUR 0.9, USD 0.1>
- contractor_classification: contractors <name, jurisdiction, test, outcome (contractor, employee_risk, unresolved), fix_due when unresolved>
- pipeline_thinness: weighted_pipeline <n>, monthly_cost_base <n>, months_of_coverage <weighted / cost>, trigger_below_months <n>
- regulatory: regulation <what applies>

### Responses (every row at 15 or more)

| row | kind | action / signed_by | owner | due_date / signed_on |
|---|---|---|---|---|
| <R-xx> | <mitigation | acceptance> | <the action, or the founder's name> | <person> | <inside this week, or the signing date> |

## Closed tab (never deleted; read at annual planning)

| id | class | description | closed_on | lesson |
|---|---|---|---|---|
| <R-xx> | <class> | <the risk> | <YYYY-MM-DD> | <one line> |
