#!/usr/bin/env python3
"""seed_labels.py — create scoped labels on a GitLab project.

Usage:
    GITLAB_URL=https://gitlab.com GITLAB_TOKEN=<token> python3 seed_labels.py <project_id>

project_id: numeric ID or URL-encoded path (e.g. mygroup%2Fmyproject)
"""
from __future__ import annotations

import os
import sys
import requests

GL = os.environ["GITLAB_URL"].rstrip("/")
TOKEN = os.environ["GITLAB_TOKEN"]
PROJECT = sys.argv[1]  # numeric id or url-encoded path

LABELS = [
    ("workflow::backlog", "#6699cc"),
    ("workflow::ready", "#3399cc"),
    ("workflow::in-progress", "#ddaa00"),
    ("workflow::review", "#aa66cc"),
    ("workflow::testing", "#cc6600"),
    ("workflow::done", "#33aa55"),
    ("priority::critical", "#cc0000"),
    ("priority::high", "#ee5500"),
    ("priority::medium", "#cc9900"),
    ("priority::low", "#888888"),
    ("type::feature", "#33aa66"),
    ("type::bug", "#cc3333"),
    ("type::tech-debt", "#996699"),
    ("type::docs", "#5577aa"),
]

s = requests.Session()
s.headers["PRIVATE-TOKEN"] = TOKEN
for name, color in LABELS:
    r = s.post(
        f"{GL}/api/v4/projects/{PROJECT}/labels",
        data={"name": name, "color": color},
    )
    if r.status_code not in (201, 409):  # 409 = already exists
        r.raise_for_status()
    print(f"{r.status_code:3d}  {name}")
