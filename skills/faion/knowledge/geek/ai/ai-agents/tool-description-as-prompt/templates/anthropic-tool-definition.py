tools = [
    {
        "name": "search_docs",
        "description": (
            "Search the indexed documentation for passages matching a query. "
            "Use this when the user asks a how-to or reference question and you don't already have the answer. "
            "Do NOT use this for code search — use `grep_repo` instead. "
            "Returns up to 10 passages ranked by relevance; each includes title, path, and a 200-char excerpt."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural-language question."},
                "max_results": {"type": "integer", "default": 10, "description": "1-50."},
            },
            "required": ["query"],
        },
    },
]
