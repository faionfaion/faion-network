# M-PMT-008: Trello Kanban

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-008 |
| **Category** | PM Tools |
| **Difficulty** | Beginner |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Teams need simple, visual project management that:
- Shows work status at a glance
- Requires minimal setup and learning curve
- Works for any workflow (dev, marketing, operations)
- Enables quick collaboration without complexity

---

## Framework

### 1. Board Architecture

**Trello hierarchy:**

```
Workspace (team)
├── Board (project/workflow)
│   ├── List (status column)
│   │   ├── Card (task/item)
│   │   │   ├── Checklist
│   │   │   ├── Attachments
│   │   │   ├── Comments
│   │   │   └── Custom Fields
```

**Workspace organization:**

```
Workspace: Acme Inc
├── Board: Product Development
├── Board: Marketing Campaigns
├── Board: Customer Support
├── Board: Team Meetings
└── Board: Company OKRs
```

### 2. Board Setup

**Standard Kanban lists:**

```
Board: Sprint Board
├── Backlog           # Prioritized work queue
├── To Do             # Committed for this sprint
├── In Progress       # Currently being worked on
├── In Review         # Awaiting review/approval
├── Done              # Completed work
└── Blocked           # Waiting on dependencies
```

**Alternative workflows:**

```
# Marketing Campaign
├── Ideas
├── Research
├── Creating
├── Review
├── Scheduled
├── Published

# Customer Support
├── New
├── Assigned
├── In Progress
├── Waiting on Customer
├── Resolved

# Content Pipeline
├── Ideas
├── Outline
├── Draft
├── Editing
├── Design
├── Published
```

### 3. Card Structure

**Card anatomy:**

```yaml
Card:
  title: "Implement OAuth login"
  description: |
    Add social login support for Google and GitHub.
    See spec: [link]

  labels:
    - name: "Feature"
      color: green
    - name: "Backend"
      color: blue
    - name: "P1"
      color: red

  members:
    - @alice

  due_date: "2026-01-25"
  start_date: "2026-01-20"

  checklist:
    name: "Acceptance Criteria"
    items:
      - "[ ] Google OAuth works"
      - "[ ] GitHub OAuth works"
      - "[ ] Error handling"
      - "[ ] Tests written"

  attachments:
    - spec.pdf
    - mockup.png

  custom_fields:
    - Story Points: 5
    - Sprint: "Sprint 14"
    - Epic: "Authentication"
```

**Card templates:**

```markdown
## Bug Report Card

**Environment:** [Production/Staging/Dev]
**Browser:** [Chrome/Firefox/Safari]
**Steps to Reproduce:**
1. Step 1
2. Step 2

**Expected:** What should happen
**Actual:** What actually happens

**Screenshots:** [attach]

---

## Feature Card

**User Story:**
As a [user type], I want [goal] so that [benefit].

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Technical Notes:**
- Implementation detail 1
- Implementation detail 2

**Resources:**
- Design: [link]
- Spec: [link]
```

### 4. Labels Strategy

**Recommended label system:**

| Category | Labels | Colors |
|----------|--------|--------|
| Type | Feature, Bug, Task, Spike | Green, Red, Yellow, Purple |
| Priority | P0, P1, P2, P3 | Red, Orange, Yellow, Gray |
| Team | Frontend, Backend, Design, QA | Blue, Sky, Pink, Lime |
| Status | Blocked, Needs Review, Ready | Red, Purple, Green |

**Label configuration:**

```yaml
Labels:
  # Type
  - name: Feature
    color: green
  - name: Bug
    color: red
  - name: Task
    color: yellow
  - name: Spike
    color: purple
  - name: Tech Debt
    color: orange

  # Priority
  - name: P0-Critical
    color: red
  - name: P1-High
    color: orange
  - name: P2-Medium
    color: yellow
  - name: P3-Low
    color: sky

  # Blocking
  - name: Blocked
    color: red
  - name: Needs Review
    color: purple
```

### 5. Power-Ups

**Essential Power-Ups:**

| Power-Up | Purpose | Use Case |
|----------|---------|----------|
| Calendar | Due date visualization | Sprint planning |
| Custom Fields | Extended metadata | Story points, sprints |
| Card Aging | Identify stale cards | Backlog grooming |
| Voting | Prioritization | Feature voting |
| List Limits | WIP limits | Kanban flow |

**Custom Fields setup:**

```yaml
Custom Fields:
  - name: Story Points
    type: number
    show_badge: true

  - name: Sprint
    type: dropdown
    options:
      - Sprint 14
      - Sprint 15
      - Sprint 16
      - Backlog

  - name: Epic
    type: dropdown
    options:
      - Authentication
      - Dashboard
      - API v2
      - Infrastructure

  - name: Estimate Hours
    type: number

  - name: Actual Hours
    type: number
```

**List Limits (WIP):**

```
In Progress: Max 3 cards per person
In Review: Max 5 cards total
```

### 6. Butler Automation

**Common automation rules:**

```yaml
# Auto-assign on move to In Progress
Rule: "Auto-assign"
Trigger: "when a card is moved into list 'In Progress'"
Action: "add me to the card"

# Due date reminder
Rule: "Due date warning"
Trigger: "when a card is due in 1 day"
Actions:
  - "add the yellow 'Due Soon' label to the card"
  - "@mention all members of the card"

# Complete checklist = move to Done
Rule: "Auto-complete"
Trigger: "when all the checklists on a card are completed"
Actions:
  - "move the card to list 'Done'"
  - "remove all labels from the card"

# Archive old Done cards
Rule: "Auto-archive"
Trigger: "every day at 9:00 AM"
Action: "archive all cards in list 'Done' that have been in the list for more than 7 days"

# Create recurring task
Rule: "Weekly standup"
Trigger: "every Monday at 9:00 AM"
Actions:
  - "create a new card in list 'To Do'"
  - "set the card name to 'Weekly Team Standup'"
  - "add checklist 'Agenda' to the card"
```

**Button automations:**

```yaml
# Quick actions on cards
Card Button: "Start Work"
Actions:
  - "move the card to list 'In Progress'"
  - "add me to the card"
  - "set start date to today"

Card Button: "Request Review"
Actions:
  - "move the card to list 'In Review'"
  - "add the 'Needs Review' label"
  - "@mention @tech-lead"

Card Button: "Mark Blocked"
Actions:
  - "add the red 'Blocked' label"
  - "move the card to list 'Blocked'"
  - "add comment 'Blocked: [describe blocker]'"
```

### 7. Trello API

**Authentication:**

```bash
# Get API key from https://trello.com/app-key
# Generate token with your API key

curl "https://api.trello.com/1/boards/BOARD_ID?key=API_KEY&token=TOKEN"
```

**Python client:**

```python
import requests
from typing import Optional, List, Dict

class TrelloClient:
    BASE_URL = "https://api.trello.com/1"

    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.BASE_URL}/{endpoint}"
        params = kwargs.get("params", {})
        params.update({"key": self.api_key, "token": self.token})
        kwargs["params"] = params
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    # Boards
    def get_boards(self):
        """Get all boards for authenticated user"""
        return self._request("GET", "members/me/boards")

    def get_board(self, board_id: str):
        """Get board details"""
        return self._request("GET", f"boards/{board_id}")

    def get_board_lists(self, board_id: str):
        """Get all lists on a board"""
        return self._request("GET", f"boards/{board_id}/lists")

    def get_board_cards(self, board_id: str):
        """Get all cards on a board"""
        return self._request("GET", f"boards/{board_id}/cards")

    # Lists
    def create_list(self, board_id: str, name: str, pos: str = "bottom"):
        """Create a new list"""
        return self._request("POST", "lists", params={
            "name": name,
            "idBoard": board_id,
            "pos": pos
        })

    def get_list_cards(self, list_id: str):
        """Get all cards in a list"""
        return self._request("GET", f"lists/{list_id}/cards")

    # Cards
    def create_card(self, list_id: str, name: str, **kwargs):
        """Create a new card"""
        params = {"name": name, "idList": list_id}
        params.update(kwargs)
        return self._request("POST", "cards", params=params)

    def update_card(self, card_id: str, **kwargs):
        """Update card properties"""
        return self._request("PUT", f"cards/{card_id}", params=kwargs)

    def move_card(self, card_id: str, list_id: str):
        """Move card to another list"""
        return self.update_card(card_id, idList=list_id)

    def add_label(self, card_id: str, label_id: str):
        """Add label to card"""
        return self._request("POST", f"cards/{card_id}/idLabels",
                           params={"value": label_id})

    def add_member(self, card_id: str, member_id: str):
        """Add member to card"""
        return self._request("POST", f"cards/{card_id}/idMembers",
                           params={"value": member_id})

    def add_comment(self, card_id: str, text: str):
        """Add comment to card"""
        return self._request("POST", f"cards/{card_id}/actions/comments",
                           params={"text": text})

    def archive_card(self, card_id: str):
        """Archive (close) a card"""
        return self.update_card(card_id, closed=True)

    # Checklists
    def create_checklist(self, card_id: str, name: str):
        """Create checklist on card"""
        return self._request("POST", "checklists", params={
            "idCard": card_id,
            "name": name
        })

    def add_checklist_item(self, checklist_id: str, name: str):
        """Add item to checklist"""
        return self._request("POST", f"checklists/{checklist_id}/checkItems",
                           params={"name": name})

    # Labels
    def get_board_labels(self, board_id: str):
        """Get all labels on a board"""
        return self._request("GET", f"boards/{board_id}/labels")

    def create_label(self, board_id: str, name: str, color: str):
        """Create a new label"""
        return self._request("POST", "labels", params={
            "idBoard": board_id,
            "name": name,
            "color": color
        })

    # PM-specific methods
    def get_sprint_metrics(self, board_id: str, done_list_id: str):
        """Calculate sprint metrics"""
        cards = self.get_board_cards(board_id)
        done_cards = self.get_list_cards(done_list_id)

        return {
            "total_cards": len(cards),
            "completed": len(done_cards),
            "completion_rate": len(done_cards) / len(cards) if cards else 0
        }

    def find_blocked_cards(self, board_id: str, blocked_label_id: str):
        """Find all blocked cards"""
        cards = self.get_board_cards(board_id)
        return [c for c in cards if blocked_label_id in c.get("idLabels", [])]


# Usage
trello = TrelloClient(
    api_key="your_api_key",
    token="your_token"
)

# Get boards
boards = trello.get_boards()

# Create card
card = trello.create_card(
    list_id="list_id",
    name="Implement feature X",
    desc="Full description here",
    due="2026-01-25"
)

# Move card to In Progress
trello.move_card(card["id"], "in_progress_list_id")

# Add comment
trello.add_comment(card["id"], "Started working on this")
```

**Webhook setup:**

```python
# Register webhook
webhook = trello._request("POST", "webhooks", params={
    "callbackURL": "https://your-server.com/trello/webhook",
    "idModel": "board_id",
    "description": "Board webhook"
})

# Webhook handler (Flask example)
from flask import Flask, request

app = Flask(__name__)

@app.route("/trello/webhook", methods=["POST", "HEAD"])
def trello_webhook():
    if request.method == "HEAD":
        return "", 200  # Trello verification

    data = request.json
    action_type = data.get("action", {}).get("type")

    if action_type == "updateCard":
        # Card was moved
        list_after = data["action"]["data"].get("listAfter", {})
        card_name = data["action"]["data"]["card"]["name"]
        print(f"Card '{card_name}' moved to {list_after.get('name')}")

    return "", 200
```

### 8. Integrations

**Slack integration:**

```
/trello add [card name]     # Quick add to default list
/trello search [query]      # Search cards
/trello link [url]          # Link card to channel
```

**GitHub integration:**

```yaml
# Attach commits and PRs to cards
GitHub → Trello:
  - Include card URL in commit message
  - Card shows commits/PRs automatically

# Automation
Power-Up: GitHub
Actions:
  - PR merged → Move card to Done
  - PR opened → Move card to In Review
```

**Slack notifications via Butler:**

```yaml
Rule: "Notify Slack on Done"
Trigger: "when a card is moved into list 'Done'"
Action: "post command '/notify Card {card name} completed'"
```

---

## Templates

### Board Setup Checklist

```markdown
## Trello Board Setup

### Structure
- [ ] Board created with clear name
- [ ] Board description added
- [ ] Lists created (Backlog, To Do, In Progress, Review, Done)
- [ ] WIP limits configured via Power-Up

### Labels
- [ ] Type labels (Feature, Bug, Task)
- [ ] Priority labels (P0-P3)
- [ ] Team labels if needed
- [ ] Blocking labels (Blocked, Needs Review)

### Power-Ups
- [ ] Custom Fields enabled
- [ ] Calendar enabled
- [ ] Card Aging enabled (optional)
- [ ] List Limits enabled (optional)

### Custom Fields
- [ ] Story Points field
- [ ] Sprint field
- [ ] Epic/Project field

### Automations (Butler)
- [ ] Auto-assign on In Progress
- [ ] Due date reminders
- [ ] Auto-archive Done cards
- [ ] Recurring tasks

### Card Templates
- [ ] Feature template
- [ ] Bug template
- [ ] Task template

### Integrations
- [ ] Slack connected
- [ ] GitHub connected (if applicable)
- [ ] Calendar sync
```

### Sprint Board Template

```yaml
Board: "[Team] Sprint [Number]"
Description: "Sprint [Start] - [End]. Goal: [Sprint goal]"

Lists:
  - name: "Sprint Backlog"
    description: "Committed for this sprint"
  - name: "In Progress (WIP: 3)"
    description: "Currently being worked on"
  - name: "In Review"
    description: "Awaiting code review"
  - name: "Testing"
    description: "QA verification"
  - name: "Done"
    description: "Completed and accepted"

Labels:
  - Feature (green)
  - Bug (red)
  - Tech Debt (orange)
  - P1 (red)
  - P2 (yellow)
  - Blocked (red)

Custom Fields:
  - Story Points (number)
  - Epic (dropdown)
```

---

## Examples

### Example 1: Development Team

**Board structure:**

```
Board: Product Development
├── Backlog (sorted by priority)
├── Sprint Backlog
├── In Progress [WIP: 3/person]
├── Code Review
├── QA Testing
├── Done
└── Shipped to Production
```

**Workflow automation:**

```yaml
# PR opened → Move to Review
Rule: GitHub PR Opened
Trigger: "when a Pull Request is opened"
Action: "move the card to list 'Code Review'"

# PR merged → Move to QA
Rule: GitHub PR Merged
Trigger: "when a Pull Request is merged"
Action: "move the card to list 'QA Testing'"

# QA passed → Move to Done
Rule: QA Complete
Card Button: "QA Passed"
Action: "move the card to list 'Done'"
```

### Example 2: Marketing Team

**Board structure:**

```
Board: Content Calendar
├── Ideas
├── Research
├── Writing
├── Design
├── Review
├── Scheduled
└── Published
```

**Card template:**

```markdown
## Content: [Title]

**Type:** Blog / Social / Email / Video
**Target Date:** [Date]
**Author:** @name

### Brief
- Audience:
- Goal:
- Key message:

### Assets Needed
- [ ] Hero image
- [ ] Social graphics
- [ ] Video (if applicable)

### Distribution
- [ ] Blog
- [ ] Twitter
- [ ] LinkedIn
- [ ] Newsletter
```

### Example 3: Personal Kanban

**Simple board:**

```
Board: Personal Tasks
├── Inbox (capture everything)
├── This Week
├── Today (max 3 items)
├── Waiting (blocked/delegated)
└── Done

Weekly Review:
1. Archive Done cards
2. Review Inbox
3. Plan This Week
4. Select Today items
```

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Too many lists | Confusion, slow drag | Max 7 lists per board |
| No WIP limits | Multitasking, delays | Set In Progress limits |
| Labels overload | Visual noise | Max 2 labels per card |
| Ignoring due dates | Missed deadlines | Always set due dates |
| No archiving | Slow board, clutter | Weekly archive Done cards |
| No card templates | Inconsistent info | Create templates |
| No automation | Manual work | Setup Butler rules |

---

## Next Steps

1. Create board with standard Kanban lists
2. Set up labels for type and priority
3. Enable Custom Fields Power-Up
4. Create card templates
5. Configure Butler automations
6. Connect Slack notifications
7. Train team on workflow

---

## Related Methodologies

- M-PMT-002: ClickUp Setup
- M-PMT-007: Notion PM
- M-PMT-010: PM Tool Selection
- M-PMT-011: Agile Ceremonies Setup
- M-PMT-012: Reporting & Dashboards
