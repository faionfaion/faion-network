#!/usr/bin/env python3
"""sdd-sync.py — reconcile a feature's SDD task files against a tracker
snapshot through a hash ledger, and emit only the changes.

The lifecycle here is directory-as-status: a task lives in todo/, in-progress/
or done/ and moving the file is the status change. Nothing off the shelf knows
that, so this is the part of the pack no vendor ships.

The ledger is what makes it idempotent. `--map` persists task-file to
remote-id to last-hash for both sides, so a second run UPDATES rather than
duplicating. An agent improvising this reconcile has no ledger, cannot tell a
task it already pushed from a new one, and creates the whole task set again on
run two, every time. It is also what lets the tool tell local-ahead from
remote-ahead from a genuine conflict instead of silently picking a winner: a
conflict is reported and exits 1, never merged.

It makes no network call at all. api-call.py is the only networking code in
the pack, so the remote side arrives as `--remote` rows from it and the push
side leaves as a `--plan` it executes. That split is why the idempotence proof
runs offline in --self-test over a fixture tree.

Input:  --aidocs feature dir, --map ledger, --remote rows, --profile
Output: one summary line on stdout; the change set and findings on stderr.

Exit: 0 in sync or applied - 1 a conflict, drift, or a failed self-test - 2
      the tool could not run - 5 changes were refused for want of --yes.
Zero model calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

NAME = "sdd-sync"
STATUSES = ("todo", "in-progress", "done")
KEY = re.compile(r"TASK-(?:[0-9]+-)*[0-9]+")
UNIT = "\x1f"

# How each tracker names the three fields this reconcile needs, and which
# state string means finished. Data, so a fourth tracker is a dict entry.
FIELDS = {
    "github": {"id": "number", "title": "title", "state": "state",
               "done": "closed"},
    "linear": {"id": "id", "title": "title", "state": "state",
               "done": "done"},
    "clickup": {"id": "id", "title": "name", "state": "status",
                "done": "complete"},
}

# Fixture tree for --self-test: three tasks over the three status dirs, and
# the remote as api-call --select would hand it over. BAD is the mistake a
# caller actually makes — running a second time and expecting no duplicates.
OK_TASKS = {
    "todo/TASK-049-001-spec-deltas.md":
        "# TASK-049-001: Spec deltas\n\nWrite the delta spec.\n",
    "in-progress/TASK-049-002-bdd-cli.md":
        "---\ntitle: BDD for the CLI\nstatus: todo\n---\n\n# TASK-049-002\n\nBDD.\n",
    "done/TASK-049-003-close-out.md":
        "# TASK-049-003: Close out\n\nDone already.\n",
}
BAD_REMOTE = (
    '{"number": 7, "title": "TASK-049-003 Close out", "state": "open"}\n'
)


def read_rows(text: str) -> list[dict] | str:
    """JSONL rows, or one error string."""
    rows: list[dict] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            return f"remote line {lineno}: not JSON: {exc}"
        if not isinstance(obj, dict):
            return f"remote line {lineno}: not a JSON object"
        rows.append(obj)
    return rows


def task_key(name: str) -> str:
    """The stable identity of a task file: its TASK-nnn-nnn prefix."""
    found = KEY.search(name)
    return found.group(0) if found else Path(name).stem


def split_front_matter(text: str) -> tuple[dict, str]:
    """YAML front matter as flat key to string, plus the body after it.

    Deliberately not a YAML parser: the reconcile reads `title` and nothing
    else, and `status` is the directory, never the field."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    front: dict = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        front[key.strip()] = value.strip().strip('"').strip("'")
    return front, text[end + 4:].lstrip("\n")


def title_of(front: dict, body: str, key: str) -> str:
    """The task's title: the front matter field, else the H1 after the key."""
    if front.get("title"):
        return front["title"]
    for line in body.splitlines():
        if line.startswith("# "):
            heading = line[2:].strip()
            if ":" in heading:
                heading = heading.split(":", 1)[1].strip()
            heading = heading.replace(key, "").strip(" :-")
            return heading or key
    return key


def normalise(text: str) -> str:
    """Whitespace-canonical body, so a trailing newline is not a change."""
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def digest(*parts: str) -> str:
    """The hash both sides are compared through."""
    return hashlib.sha256(UNIT.join(parts).encode("utf-8")).hexdigest()


def local_state(status: str) -> str:
    """Every tracker this pack speaks to is binary, so todo and in-progress
    both mean open. Losing that distinction remotely is deliberate: inventing
    a status per tracker is a mapping nobody can verify."""
    return "done" if status == "done" else "open"


def load_tasks(root: Path) -> list[dict] | str:
    """Every task file under the three status dirs, or one error string."""
    tasks: list[dict] = []
    if not any((root / status).is_dir() for status in STATUSES):
        return (f"{root} holds none of todo/, in-progress/, done/ — point "
                "--aidocs at one feature directory")
    for status in STATUSES:
        folder = root / status
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.md")):
            if not path.name.upper().startswith("TASK"):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                return f"cannot read {path}: {exc}"
            front, body = split_front_matter(text)
            key = task_key(path.name)
            title = title_of(front, body, key)
            tasks.append({
                "key": key,
                "path": str(path),
                "status": status,
                "title": title,
                "body": normalise(body),
                "hash": digest(key, title, local_state(status),
                               normalise(body)),
            })
    return tasks


def remote_state(row: dict, fields: dict) -> str:
    """The tracker's state folded to open or done. A nested state object is
    read by name, because that is the shape Linear and ClickUp return."""
    value = row.get(fields["state"])
    if isinstance(value, dict):
        value = value.get("name") or value.get("status") or value.get("type")
    text = str(value or "").strip().lower()
    return "done" if text == fields["done"] else "open"


def index_remote(rows: list[dict], fields: dict) -> tuple[dict, list[str]]:
    """Remote rows keyed by the task key in their title. A row whose title
    carries no key is not this feature's business and is ignored."""
    out: dict = {}
    problems: list[str] = []
    for row in rows:
        title = str(row.get(fields["title"]) or "")
        found = KEY.search(title)
        if not found:
            continue
        key = found.group(0)
        clean = title.replace(key, "").strip(" :-")
        entry = {"id": str(row.get(fields["id"]) or ""),
                 "title": clean or title,
                 "state": remote_state(row, fields)}
        entry["hash"] = digest(key, entry["title"], entry["state"])
        if key in out:
            problems.append(f"{key}: two remote items claim it "
                            f"({out[key]['id']} and {entry['id']})")
        out[key] = entry
    return out, problems


def duplicate_keys(tasks: list[dict]) -> list[str]:
    """Two files sharing a task key cannot be synced to one remote item."""
    seen: dict = {}
    problems: list[str] = []
    for task in tasks:
        if task["key"] in seen:
            problems.append(f"{task['key']}: two local files claim it "
                            f"({seen[task['key']]} and {task['path']})")
        seen[task["key"]] = task["path"]
    return problems


def reconcile(tasks: list[dict], remote: dict, ledger: dict,
              mode: str) -> tuple[list[dict], list[str]]:
    """The whole decision. Pure: no I/O, no exits, no clock.

    Three-way against the ledger, which is the only thing that can tell a
    local edit from a remote one: local hash moved and remote did not is
    local-ahead, the reverse is remote-ahead, both moved is a conflict that
    is reported and never merged."""
    actions: list[dict] = []
    findings: list[str] = []
    entries = ledger.get("tasks") or {}
    for task in sorted(tasks, key=lambda t: t["key"]):
        key = task["key"]
        entry = entries.get(key) or {}
        item = remote.get(key)
        if not item:
            if not entry:
                actions.append({"action": "create", "key": key,
                                "title": task["title"], "path": task["path"],
                                "status": task["status"],
                                "hash": task["hash"]})
            elif entry.get("pending"):
                findings.append(f"{key}: the create is still planned and not "
                                "applied — run the plan through api-call")
            else:
                findings.append(f"{key}: was linked to remote "
                                f"{entry.get('remote_id')} and is gone from "
                                "the snapshot")
            continue
        if entry.get("pending") and entry.get("want_hash"):
            # An update was planned. Whether it ran is readable from the
            # snapshot, so a plan the caller never executed is reported
            # instead of being recorded as synced.
            if item["hash"] == entry["want_hash"]:
                actions.append({"action": "record", "key": key,
                                "remote_id": item["id"], "hash": task["hash"],
                                "remote_hash": item["hash"]})
            elif item["hash"] == entry.get("remote_hash"):
                findings.append(f"{key}: the update is still planned and not "
                                "applied — run the plan through api-call")
            else:
                findings.append(f"{key}: an update was pending on "
                                f"{entry.get('remote_id')} and the tracker "
                                "moved somewhere else")
            continue
        if not entry or entry.get("pending"):
            actions.append({"action": "adopt", "key": key,
                            "remote_id": item["id"], "hash": task["hash"],
                            "remote_hash": item["hash"]})
            continue
        local_moved = entry.get("hash") != task["hash"]
        remote_moved = entry.get("remote_hash") != item["hash"]
        want_hash = digest(key, task["title"], local_state(task["status"]))
        if local_moved and remote_moved:
            findings.append(f"{key}: conflict — both sides changed since "
                            f"{entry.get('remote_id')} was last synced")
        elif local_moved:
            if mode != "push":
                findings.append(f"{key}: local-ahead, and pull would discard "
                                "it")
            elif want_hash == item["hash"]:
                # The edit does not reach anything the tracker holds — the
                # body is not synced — so there is nothing to send.
                actions.append({"action": "record", "key": key,
                                "remote_id": entry.get("remote_id"),
                                "hash": task["hash"],
                                "remote_hash": item["hash"]})
            else:
                actions.append({"action": "update", "key": key,
                                "remote_id": entry.get("remote_id"),
                                "title": task["title"], "path": task["path"],
                                "status": task["status"],
                                "hash": task["hash"],
                                "remote_hash": item["hash"],
                                "want_hash": want_hash})
        elif remote_moved:
            if mode != "pull":
                findings.append(f"{key}: remote-ahead on "
                                f"{entry.get('remote_id')}, and push would "
                                "overwrite it")
            else:
                want = "done" if item["state"] == "done" else "todo"
                if local_state(task["status"]) != item["state"]:
                    # The recorded hash is the one the file will have AFTER
                    # the move, or the next run reads its own move as a local
                    # edit and plans a pointless push back.
                    actions.append({"action": "move", "key": key,
                                    "path": task["path"],
                                    "from": task["status"], "to": want,
                                    "hash": digest(key, task["title"],
                                                   item["state"],
                                                   task.get("body", "")),
                                    "remote_hash": item["hash"]})
                else:
                    findings.append(f"{key}: remote-ahead in text only; the "
                                    "title changed and pull moves files, not "
                                    "prose")
    local_keys = {task["key"] for task in tasks}
    for key in sorted(set(remote) - local_keys):
        findings.append(f"{key}: on the tracker as {remote[key]['id']} and "
                        "in no status directory")
    return actions, findings


def changes(actions: list[dict]) -> int:
    """Actions that alter a side. adopt and record only write the ledger."""
    return sum(1 for a in actions if a["action"] not in ("adopt", "record"))


def apply_ledger(ledger: dict, actions: list[dict], profile: str) -> dict:
    """The ledger after these actions. Pure, and sorted, so the file is
    byte-stable across runs.

    A create or an update is recorded `pending` with the hash the remote is
    expected to carry once the plan runs. That is what lets the next run tell
    "already applied" from "planned and never executed" instead of assuming
    the caller did their half."""
    out = {"version": 1, "profile": profile,
           "tasks": dict(ledger.get("tasks") or {})}
    for action in actions:
        key = action["key"]
        entry = dict(out["tasks"].get(key) or {})
        entry["hash"] = action["hash"]
        if action["action"] == "create":
            entry["remote_id"] = None
            entry["pending"] = True
            entry.pop("want_hash", None)
        elif action["action"] == "update":
            entry["pending"] = True
            entry["want_hash"] = action["want_hash"]
            if action.get("remote_id") is not None:
                entry["remote_id"] = action["remote_id"]
            if action.get("remote_hash"):
                entry["remote_hash"] = action["remote_hash"]
        else:
            entry.pop("pending", None)
            entry.pop("want_hash", None)
            if action.get("remote_id") is not None:
                entry["remote_id"] = action["remote_id"]
            if action.get("remote_hash"):
                entry["remote_hash"] = action["remote_hash"]
        out["tasks"][key] = entry
    out["tasks"] = {k: out["tasks"][k] for k in sorted(out["tasks"])}
    return out


def plan_line(action: dict, profile: str) -> dict:
    """One action as an api-call payload, ready to pipe through --body.

    The body carries only what this tool can map without guessing: the
    tracker's own title field, and for GitHub the open/closed state, which is
    the one status vocabulary that is not workspace-specific. Linear wants a
    stateId and ClickUp a status name defined per list, so both arrive as the
    `status` field for the caller to map rather than as an invented value."""
    fields = FIELDS.get(profile, FIELDS["github"])
    ops = {"github": ("create-issue", "update-issue"),
           "linear": ("create-issue", "update-issue"),
           "clickup": ("create-task", "update-task")}
    create_op, update_op = ops.get(profile, ops["github"])
    if action["action"] == "move":
        return {"action": "move", "key": action["key"],
                "from": action.get("from"), "to": action.get("to"),
                "path": action.get("path")}
    state = local_state(action["status"])
    body = {fields["title"]: f"{action['key']} {action.get('title', '')}".strip()}
    line = {"action": action["action"], "key": action["key"], "status": state,
            "op": create_op if action["action"] == "create" else update_op,
            "body": body}
    if action["action"] == "update":
        line["remote_id"] = action.get("remote_id")
        if profile == "github":
            body["state"] = fields["done"] if state == "done" else "open"
    return line


def describe(action: dict) -> str:
    """The change set line a caller reads before saying --yes."""
    if action["action"] == "move":
        return (f"move {action['key']}: {action['from']} -> {action['to']} "
                f"({action['path']})")
    if action["action"] == "adopt":
        return f"adopt {action['key']}: link to remote {action['remote_id']}"
    if action["action"] == "record":
        return (f"record {action['key']}: the edit does not reach the tracker, "
                "ledger only")
    target = action.get("remote_id") or "a new item"
    return f"{action['action']} {action['key']} -> {target}"


def move_paths(action: dict, root: Path) -> tuple[Path, Path]:
    """Where a pull moves a task file. Inside the feature dir, by construction."""
    source = Path(action["path"])
    return source, root / action["to"] / source.name


def simulate(remote: dict, actions: list[dict], start: int) -> dict:
    """What the tracker looks like once the plan has been executed. Used by
    --self-test to prove the second run creates nothing."""
    out = dict(remote)
    number = start
    for action in actions:
        if action["action"] != "create":
            continue
        state = local_state(action["status"])
        out[action["key"]] = {
            "id": str(number), "title": action["title"], "state": state,
            "hash": digest(action["key"], action["title"], state)}
        number += 1
    return out


def self_test() -> list[str]:
    """Prove the reconcile, and prove it is idempotent: the second run over
    the same tree creates nothing. No network, no temp files."""
    failures: list[str] = []
    tasks = []
    for rel, text in sorted(OK_TASKS.items()):
        status, name = rel.split("/")
        front, body = split_front_matter(text)
        key = task_key(name)
        title = title_of(front, body, key)
        tasks.append({"key": key, "path": rel, "status": status,
                      "title": title, "body": normalise(body),
                      "hash": digest(key, title, local_state(status),
                                     normalise(body))})
    if [t["key"] for t in tasks] != ["TASK-049-003", "TASK-049-002",
                                     "TASK-049-001"]:
        failures.append(f"fixture keys parsed wrong: {[t['key'] for t in tasks]}")
    if tasks[1]["title"] != "BDD for the CLI":
        failures.append("front matter title was not preferred")
    if tasks[0]["status"] != "done":
        failures.append("directory-as-status was not read from the directory")

    ledger: dict = {}
    first, findings = reconcile(tasks, {}, ledger, "push")
    if changes(first) != 3:
        failures.append(f"first run planned {changes(first)} changes, wanted 3")
    if findings:
        failures.append(f"first run found problems it should not: {findings}")

    # Run two, having applied the plan. This is the whole value proposition.
    ledger = apply_ledger(ledger, first, "github")

    # Sharpest form: the snapshot is stale and shows nothing, so only the
    # ledger stands between this run and a duplicate task set.
    stale, stale_findings = reconcile(tasks, {}, ledger, "push")
    if changes(stale) != 0:
        failures.append("A STALE SNAPSHOT RE-CREATED THE WHOLE TASK SET")
    if len(stale_findings) != 3:
        failures.append(f"the unapplied plan was not reported: {stale_findings}")

    remote = simulate({}, first, 101)
    second, second_findings = reconcile(tasks, remote, ledger, "push")
    if changes(second) != 0:
        failures.append(f"SECOND RUN WOULD DUPLICATE: {[a['action'] for a in second]}")
    if second_findings:
        failures.append(f"second run found problems: {second_findings}")
    ledger = apply_ledger(ledger, second, "github")
    third, third_findings = reconcile(tasks, remote, ledger, "push")
    if third or third_findings:
        failures.append(f"third run was not silent: {third} {third_findings}")

    # Without a ledger the same inputs create the whole set again — the
    # failure this tool exists to prevent.
    naive, _ = reconcile(tasks, {}, {}, "push")
    if changes(naive) != 3:
        failures.append("the no-ledger control did not duplicate, so the "
                        "idempotence assertion proves nothing")

    edited = [dict(t) for t in tasks]
    edited[2]["hash"] = digest("TASK-049-001", "Spec deltas", "open", "edited")
    body_only, _ = reconcile(edited, remote, ledger, "push")
    if [a["action"] for a in body_only] != ["record"] or changes(body_only):
        failures.append(f"a body-only edit planned a pointless call: {body_only}")

    retitled = [dict(t) for t in tasks]
    retitled[2] = dict(retitled[2], title="Spec deltas, rescoped",
                       hash=digest("TASK-049-001", "Spec deltas, rescoped",
                                   "open", "rescoped"))
    ahead, _ = reconcile(retitled, remote, ledger, "push")
    if [a["action"] for a in ahead] != ["update"]:
        failures.append(f"local-ahead did not plan an update: {ahead}")
    if reconcile(retitled, remote, ledger, "pull")[0]:
        failures.append("pull acted on a local-ahead task instead of reporting")

    # An update the caller never executed must not be recorded as synced.
    pending = apply_ledger(ledger, ahead, "github")
    if not any("still planned" in f
               for f in reconcile(retitled, remote, pending, "push")[1]):
        failures.append("an unexecuted update was recorded as synced")
    ran = dict(remote)
    ran["TASK-049-001"] = {
        "id": "101", "title": "Spec deltas, rescoped", "state": "open",
        "hash": digest("TASK-049-001", "Spec deltas, rescoped", "open")}
    recorded, _ = reconcile(retitled, ran, pending, "push")
    if [a["action"] for a in recorded] != ["record"]:
        failures.append(f"an executed update was not recorded: {recorded}")

    moved = dict(remote)
    moved["TASK-049-001"] = {"id": "103", "title": "Spec deltas",
                             "state": "done",
                             "hash": digest("TASK-049-001", "Spec deltas",
                                            "done")}
    pull, _ = reconcile(tasks, moved, ledger, "pull")
    if [a["action"] for a in pull] != ["move"] or pull[0]["to"] != "done":
        failures.append(f"remote-ahead did not plan a move: {pull}")
    push_back, push_findings = reconcile(tasks, moved, ledger, "push")
    if push_back or not any("remote-ahead" in f for f in push_findings):
        failures.append("push overwrote a remote-ahead task instead of "
                        "reporting it")

    conflict, conflict_findings = reconcile(edited, moved, ledger, "push")
    if conflict or not any("conflict" in f for f in conflict_findings):
        failures.append("a two-sided change was not reported as a conflict")

    rows = read_rows(BAD_REMOTE)
    if isinstance(rows, str):
        failures.append(f"the remote fixture does not parse: {rows}")
    else:
        indexed, problems = index_remote(rows, FIELDS["github"])
        if problems or indexed["TASK-049-003"]["state"] != "open":
            failures.append("a reopened remote item was not read as open")
        drift, _ = reconcile(tasks, indexed, ledger, "push")
        if drift:
            failures.append("an unledgered remote item was acted on rather "
                            "than adopted")
    if remote_state({"status": {"status": "complete"}},
                    FIELDS["clickup"]) != "done":
        failures.append("a nested state object was not read")
    if duplicate_keys(tasks + [dict(tasks[0], path="other.md")]) == []:
        failures.append("two files sharing a key were not reported")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--aidocs", help="one feature dir holding todo/, "
                                     "in-progress/ and done/")
    ap.add_argument("--map", dest="ledger",
                    help="hash ledger JSON, created on the first apply")
    ap.add_argument("--remote", help="tracker rows as JSONL from api-call")
    ap.add_argument("--profile", default="github",
                    help="tracker field map: github, linear, clickup")
    ap.add_argument("--plan", help="write the api-call change set here as JSONL")
    ap.add_argument("--push", action="store_true",
                    help="plan the local side onto the tracker")
    ap.add_argument("--pull", action="store_true",
                    help="move task files to match the tracker's state")
    ap.add_argument("--report", action="store_true",
                    help="reconcile and change nothing (the default)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the change set and write nothing")
    ap.add_argument("--yes", action="store_true",
                    help="apply: write the ledger, the plan and any moves")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit, offline")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=27 failures={len(failures)}")
        return 1 if failures else 0

    if args.push and args.pull:
        print(f"{NAME}: --push and --pull are opposite directions",
              file=sys.stderr)
        return 2
    mode = "push" if args.push else ("pull" if args.pull else "report")
    if not args.aidocs or not args.ledger:
        print(f"{NAME}: --aidocs and --map are required", file=sys.stderr)
        return 2
    if args.profile not in FIELDS:
        print(f"{NAME}: no field map for {args.profile!r}; known: "
              f"{', '.join(sorted(FIELDS))}", file=sys.stderr)
        return 2
    if mode != "report" and not args.remote:
        print(f"{NAME}: --remote is required for {mode}; take the snapshot "
              "with api-call first", file=sys.stderr)
        return 2

    root = Path(args.aidocs)
    tasks = load_tasks(root)
    if isinstance(tasks, str):
        print(f"{NAME}: {tasks}", file=sys.stderr)
        return 2
    problems = duplicate_keys(tasks)

    rows: list[dict] = []
    if args.remote:
        try:
            parsed = read_rows(Path(args.remote).read_text(encoding="utf-8"))
        except OSError as exc:
            print(f"{NAME}: cannot read the remote rows: {exc}",
                  file=sys.stderr)
            return 2
        if isinstance(parsed, str):
            print(f"{NAME}: {parsed}", file=sys.stderr)
            return 2
        rows = parsed
    remote, remote_problems = index_remote(rows, FIELDS[args.profile])
    problems += remote_problems

    ledger: dict = {}
    if Path(args.ledger).is_file():
        try:
            ledger = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"{NAME}: cannot read the ledger: {exc}", file=sys.stderr)
            return 2
    if ledger.get("profile") and ledger["profile"] != args.profile:
        print(f"{NAME}: the ledger belongs to {ledger['profile']}, not "
              f"{args.profile}", file=sys.stderr)
        return 2

    actions, findings = reconcile(tasks, remote, ledger, mode)
    findings = problems + findings
    if problems:
        actions = []
    for action in actions:
        print(f"{NAME}: {describe(action)}", file=sys.stderr)
    for finding in findings:
        print(f"{NAME}: {finding}", file=sys.stderr)

    applied = 0
    if mode != "report" and actions and not args.dry_run and args.yes:
        try:
            if args.plan:
                Path(args.plan).write_text("".join(
                    json.dumps(plan_line(a, args.profile), sort_keys=True)
                    + "\n" for a in actions
                    if a["action"] in ("create", "update", "move")),
                    encoding="utf-8")
            for action in actions:
                if action["action"] != "move":
                    continue
                source, target = move_paths(action, root)
                target.parent.mkdir(parents=True, exist_ok=True)
                os.replace(source, target)
                applied += 1
            Path(args.ledger).write_text(
                json.dumps(apply_ledger(ledger, actions, args.profile),
                           indent=2, sort_keys=True) + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot apply: {exc}", file=sys.stderr)
            return 2

    print(f"{NAME}: mode={mode} tasks={len(tasks)} remote={len(remote)} "
          f"changes={changes(actions)} applied={applied} "
          f"findings={len(findings)}")
    if findings:
        return 1
    if mode != "report" and changes(actions) and not args.yes \
            and not args.dry_run:
        return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
