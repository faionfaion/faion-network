{
    "name": "apply_patch",
    "description": (
        "MUTATING: Apply a unified-diff patch to the repo. "
        "Use this AFTER you have validated the patch with `dry_run_patch`. "
        "Do NOT use this on a dirty working tree. "
        "Returns: {applied: bool, conflicts: list[str]}."
    ),
}
