# purpose: side-effect tool pattern with MUTATING: marker + dry-run pair
# consumes: tool name + function signature + side-effect class
# produces: tool definition (Python dict) conforming to content/02-output-contract.xml schema constraints
# depends-on: 01-core-rules.xml (structured-description-required, under-200-tokens, anti-trigger-required-on-overlap, mutating-marker-required, latency-and-pagination-caps, description-matches-schema)
# token-budget-impact: ~80-180 tokens per tool description
{
    "name": "apply_patch",
    "description": (
        "MUTATING: Apply a unified-diff patch to the repo. "
        "Use this AFTER you have validated the patch with `dry_run_patch`. "
        "Do NOT use this on a dirty working tree. "
        "Returns: {applied: bool, conflicts: list[str]}."
    ),
}
