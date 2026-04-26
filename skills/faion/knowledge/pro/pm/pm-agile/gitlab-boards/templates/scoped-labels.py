#!/usr/bin/env python3
"""scoped-labels.py — reference template for GitLab scoped label definitions.

Copy this file and adjust LABELS for your project's workflow.
Run via: GITLAB_URL=... GITLAB_TOKEN=... python3 scoped-labels.py <project_id>
"""
from __future__ import annotations

LABELS = [
    # Workflow — mutually exclusive via "::" scoping
    ("workflow::backlog",     "#6699cc"),
    ("workflow::ready",       "#3399cc"),
    ("workflow::in-progress", "#ddaa00"),
    ("workflow::review",      "#aa66cc"),
    ("workflow::testing",     "#cc6600"),
    ("workflow::done",        "#33aa55"),
    # Priority — mutually exclusive
    ("priority::critical",    "#cc0000"),
    ("priority::high",        "#ee5500"),
    ("priority::medium",      "#cc9900"),
    ("priority::low",         "#888888"),
    # Type — mutually exclusive
    ("type::feature",         "#33aa66"),
    ("type::bug",             "#cc3333"),
    ("type::tech-debt",       "#996699"),
    ("type::docs",            "#5577aa"),
]
