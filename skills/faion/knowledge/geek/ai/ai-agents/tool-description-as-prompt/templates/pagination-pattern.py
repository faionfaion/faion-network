# purpose: paginated-tool pattern with per-page + max-page cap
# consumes: tool name + function signature + side-effect class
# produces: tool definition (Python dict) conforming to content/02-output-contract.xml schema constraints
# depends-on: 01-core-rules.xml (structured-description-required, under-200-tokens, anti-trigger-required-on-overlap, mutating-marker-required, latency-and-pagination-caps, description-matches-schema)
# token-budget-impact: ~80-180 tokens per tool description
{
    "name": "list_issues",
    "description": (
        "List GitHub issues in the current repo. "
        "Use this to find context for a bug fix or feature. "
        "Returns 30 per page; pass `cursor` from the previous response to paginate. "
        "Do NOT loop more than 5 pages — narrow the query if you need more."
    ),
}
