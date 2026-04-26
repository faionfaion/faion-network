#!/usr/bin/env python3
"""Create an Azure DevOps User Story and link it to a Feature parent.

Usage:
  ADO_PAT=<token> python ado-create-story.py \
    "Story title" "Description HTML" "Acceptance criteria HTML" 5 \
    "MyProject\\Release 1\\Sprint 1" <parent_feature_id>

Outputs: created User Story ID.
"""
import json
import os
import sys

import requests

ORG = os.environ.get("ADO_ORG", "myorg")
PROJECT = os.environ.get("ADO_PROJECT", "MyProject")
PAT = os.environ["ADO_PAT"]
AUTH = ("", PAT)
HDR = {"Content-Type": "application/json-patch+json"}
BASE = f"https://dev.azure.com/{ORG}/{PROJECT}/_apis"


def create_story(title: str, desc: str, ac: str, points: int,
                 iteration: str, parent_id: int) -> int:
    url = f"{BASE}/wit/workitems/$User%20Story?api-version=7.0"
    body = [
        {"op": "add", "path": "/fields/System.Title", "value": title},
        {"op": "add", "path": "/fields/System.Description", "value": desc},
        {"op": "add",
         "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
         "value": ac},
        {"op": "add",
         "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints",
         "value": points},
        {"op": "add",
         "path": "/fields/System.IterationPath",
         "value": iteration},
        {"op": "add", "path": "/relations/-", "value": {
            "rel": "System.LinkTypes.Hierarchy-Reverse",
            "url": f"{BASE}/wit/workItems/{parent_id}",
        }},
    ]
    r = requests.post(url, headers=HDR, auth=AUTH, data=json.dumps(body))
    r.raise_for_status()
    result = r.json()
    # Validate — ADO can return 200 with a ValidationError
    if result.get("message"):
        raise RuntimeError(f"ADO ValidationError: {result['message']}")
    return result["id"]


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(__doc__)
        sys.exit(2)
    story_id = create_story(
        title=sys.argv[1],
        desc=sys.argv[2],
        ac=sys.argv[3],
        points=int(sys.argv[4]),
        iteration=sys.argv[5],
        parent_id=int(sys.argv[6]),
    )
    print(f"Created User Story id={story_id}")
