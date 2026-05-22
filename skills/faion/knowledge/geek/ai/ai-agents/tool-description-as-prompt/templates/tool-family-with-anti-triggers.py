# purpose: tool family pattern with mutual anti-triggers
# consumes: tool name + function signature + side-effect class
# produces: tool definition (Python dict) conforming to content/02-output-contract.xml schema constraints
# depends-on: 01-core-rules.xml (structured-description-required, under-200-tokens, anti-trigger-required-on-overlap, mutating-marker-required, latency-and-pagination-caps, description-matches-schema)
# token-budget-impact: ~80-180 tokens per tool description
read_file = {
    "name": "read_file",
    "description": (
        "Read a file's contents from the local repo. "
        "Use this when you need to inspect specific code/text. "
        "Do NOT use this for searching across files — use `grep_repo`. "
        "Do NOT use this on files larger than 50KB without `offset`/`limit`."
    ),
}

grep_repo = {
    "name": "grep_repo",
    "description": (
        "Search the repository for a regex pattern. "
        "Use this when you need to find where something appears across many files. "
        "Do NOT use this if you already know the file path — use `read_file`. "
        "Returns matches grouped by file, max 200 lines."
    ),
}
