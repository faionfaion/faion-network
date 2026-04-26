#!/usr/bin/env python3
"""
map_to_jira.py — Sync map.yaml to Jira.
Creates epics per activity, stories per leaf, labels per release and task.
Writes jira-sync.diff.json for BA review before applying.

Usage: JIRA_URL=... JIRA_USER=... JIRA_TOKEN=... JIRA_PROJECT=... python3 map_to_jira.py map.yaml
"""
import sys, yaml, os, json, requests
from pathlib import Path

JIRA = os.environ["JIRA_URL"]
AUTH = (os.environ["JIRA_USER"], os.environ["JIRA_TOKEN"])
PROJECT = os.environ["JIRA_PROJECT"]

def upsert(issue_type, summary, parent_key=None, labels=None, story_id=None):
    payload = {
        "fields": {
            "project": {"key": PROJECT},
            "summary": summary,
            "issuetype": {"name": issue_type},
            "labels": labels or [],
        }
    }
    if parent_key:
        payload["fields"]["parent"] = {"key": parent_key}
    if story_id:
        payload["fields"]["labels"].append(f"map:{story_id}")
    r = requests.post(f"{JIRA}/rest/api/3/issue", json=payload, auth=AUTH, timeout=30)
    r.raise_for_status()
    return r.json()["key"]

def main(map_path: str):
    m = yaml.safe_load(Path(map_path).read_text())
    diff = []
    for act in m["backbone"]:
        epic_key = upsert("Epic", act["verb"], labels=[f"activity:{act['id']}"])
        diff.append(("epic", act["id"], epic_key))
        for tsk in act.get("tasks", []):
            for s in tsk.get("stories", []):
                summary = (
                    f"As a {s.get('user','user')}, "
                    f"I want {s.get('want','...')} "
                    f"so that {s.get('so_that','...')}"
                )
                key = upsert(
                    "Story", summary,
                    parent_key=epic_key,
                    labels=[f"task:{tsk['id']}", f"release:{s.get('release','TBD')}"],
                    story_id=s["id"],
                )
                diff.append(("story", s["id"], key))
    Path("jira-sync.diff.json").write_text(json.dumps(diff, indent=2))
    print(f"Wrote jira-sync.diff.json — {len(diff)} items. Review before applying.")

if __name__ == "__main__":
    main(sys.argv[1])
