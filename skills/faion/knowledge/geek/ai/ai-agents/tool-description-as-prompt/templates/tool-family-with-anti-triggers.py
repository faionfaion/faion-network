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
