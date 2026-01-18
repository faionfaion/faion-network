# M-PMT-005: GitLab Boards

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-005 |
| **Category** | PM Tools |
| **Difficulty** | Intermediate |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Teams using GitLab need to leverage its built-in project management without external tools:
- Issue boards that reflect development workflow
- Milestone planning for releases
- Epics for large initiatives (Premium/Ultimate)
- Integration with CI/CD pipelines

## Framework

### 1. GitLab Hierarchy

**Structure:**

```
Group (organization)
├── Subgroup (team/department)
│   └── Project (repository)
│       ├── Issues
│       ├── Milestones
│       ├── Boards
│       └── Epics (Premium+)
└── Group-level
    ├── Epics
    ├── Roadmaps
    └── Boards
```

**Project vs Group boards:**

| Level | Scope | Best For |
|-------|-------|----------|
| Project | Single repo | Small teams, focused work |
| Group | All projects in group | Cross-project planning |

### 2. Labels System

**Label hierarchy:**

```
Workflow Labels (scoped):
├── workflow::backlog
├── workflow::ready
├── workflow::in-progress
├── workflow::review
└── workflow::done

Priority Labels (scoped):
├── priority::critical
├── priority::high
├── priority::medium
└── priority::low

Type Labels:
├── bug
├── feature
├── documentation
├── tech-debt
└── security

Team Labels (scoped):
├── team::frontend
├── team::backend
├── team::devops
└── team::qa
```

**Scoped labels (::):**
- Only one label per scope can be applied
- Prevents conflicting states
- Auto-removes old label when new one added

**Label colors:**

| Type | Color | Example |
|------|-------|---------|
| Workflow | Blue shades | `#428BCA` |
| Priority | Red/Orange | Critical: `#FF0000` |
| Type | Green shades | Feature: `#5CB85C` |
| Team | Purple shades | `#9370DB` |

### 3. Board Configuration

**Basic board setup:**

```
Board: Development
├── Column: Open (no label)
├── Column: Backlog (workflow::backlog)
├── Column: Ready (workflow::ready)
├── Column: In Progress (workflow::in-progress)
├── Column: Review (workflow::review)
└── Column: Closed (closed issues)
```

**Multiple boards strategy:**

| Board | Purpose | Columns |
|-------|---------|---------|
| Development | Daily work | Backlog, Ready, In Progress, Review |
| Sprint | Current sprint | Sprint-specific labels |
| Bugs | Bug tracking | New, Triaged, Fixing, Testing |
| Release | Release planning | Planned, In Development, Ready, Released |

**Board scopes:**

```yaml
# Board: Frontend Team
scope:
  labels:
    - team::frontend
  milestone: "v2.0"
  assignee: null  # All assignees

# Board: Current Sprint
scope:
  milestone: "%Sprint-14"
  labels: []

# Board: My Work
scope:
  assignee: "@me"
```

### 4. Milestones

**Milestone structure:**

```
Project Milestones:
├── Sprint 14 (Jan 15-28)
│   ├── Due: Jan 28, 2026
│   ├── Issues: 15
│   └── Progress: 40%
├── Sprint 15 (Jan 29 - Feb 11)
└── v2.0 Release (Feb 28)
```

**Group milestones:**

```
Group: Product Team
├── Q1 2026
│   ├── Milestone: v2.0 (inherited to all projects)
│   ├── Milestone: v2.1
│   └── Milestone: v2.2
```

**Milestone types:**

| Type | Duration | Purpose |
|------|----------|---------|
| Sprint | 1-4 weeks | Iteration planning |
| Release | Variable | Version planning |
| Quarter | 3 months | Strategic planning |

### 5. Epics (Premium/Ultimate)

**Epic structure:**

```
Epic: User Authentication System
├── Description: Complete auth overhaul
├── Start: Jan 1, 2026
├── Due: Mar 31, 2026
├── Child Epics:
│   ├── Epic: OAuth Integration
│   └── Epic: 2FA Implementation
├── Issues:
│   ├── Issue: Design auth flow
│   ├── Issue: Implement login API
│   └── Issue: Add password reset
└── Progress: 25%
```

**Epic roadmap:**

```
Timeline View:
Q1 2026                                Q2 2026
|--Auth System----|
        |--Payment Integration--|
                    |--Mobile App--|
```

### 6. GitLab API

**Authentication:**

```bash
# Personal Access Token
curl --header "PRIVATE-TOKEN: glpat-xxxxxxxxxxxx" \
  "https://gitlab.com/api/v4/projects"

# OAuth2 Token
curl --header "Authorization: Bearer ACCESS_TOKEN" \
  "https://gitlab.com/api/v4/projects"
```

**Common operations:**

```python
import requests

class GitLabClient:
    def __init__(self, url: str, token: str):
        self.url = url.rstrip('/')
        self.headers = {"PRIVATE-TOKEN": token}

    def _get(self, endpoint: str, params: dict = None):
        response = requests.get(
            f"{self.url}/api/v4{endpoint}",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: dict):
        response = requests.post(
            f"{self.url}/api/v4{endpoint}",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def _put(self, endpoint: str, data: dict):
        response = requests.put(
            f"{self.url}/api/v4{endpoint}",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    # Issues
    def get_issues(self, project_id: int, **filters):
        """Get project issues with filters"""
        return self._get(f"/projects/{project_id}/issues", filters)

    def create_issue(self, project_id: int, title: str, **kwargs):
        """Create new issue"""
        data = {"title": title, **kwargs}
        return self._post(f"/projects/{project_id}/issues", data)

    def update_issue(self, project_id: int, issue_iid: int, **updates):
        """Update issue"""
        return self._put(
            f"/projects/{project_id}/issues/{issue_iid}",
            updates
        )

    # Labels
    def get_labels(self, project_id: int):
        """Get project labels"""
        return self._get(f"/projects/{project_id}/labels")

    def create_label(self, project_id: int, name: str, color: str, **kwargs):
        """Create label"""
        data = {"name": name, "color": color, **kwargs}
        return self._post(f"/projects/{project_id}/labels", data)

    # Milestones
    def get_milestones(self, project_id: int, state: str = "active"):
        """Get project milestones"""
        return self._get(
            f"/projects/{project_id}/milestones",
            {"state": state}
        )

    def create_milestone(self, project_id: int, title: str, **kwargs):
        """Create milestone"""
        data = {"title": title, **kwargs}
        return self._post(f"/projects/{project_id}/milestones", data)

    # Boards
    def get_boards(self, project_id: int):
        """Get project boards"""
        return self._get(f"/projects/{project_id}/boards")

    def get_board_lists(self, project_id: int, board_id: int):
        """Get board lists (columns)"""
        return self._get(
            f"/projects/{project_id}/boards/{board_id}/lists"
        )

# Usage
client = GitLabClient("https://gitlab.com", "glpat-xxxx")

# Get issues in milestone
issues = client.get_issues(
    project_id=123,
    milestone="Sprint 14",
    state="opened",
    labels="workflow::in-progress"
)

# Create issue
new_issue = client.create_issue(
    project_id=123,
    title="Implement OAuth login",
    description="Add Google and GitHub OAuth",
    labels="feature,team::backend",
    milestone_id=5,
    assignee_ids=[42]
)

# Update issue status
client.update_issue(
    project_id=123,
    issue_iid=456,
    labels="workflow::review"
)
```

**GraphQL API (for epics):**

```graphql
# Get group epics
query GetEpics($groupPath: ID!) {
  group(fullPath: $groupPath) {
    epics(first: 20) {
      nodes {
        id
        iid
        title
        state
        startDate
        dueDate
        descendantCounts {
          openedIssues
          closedIssues
        }
        children {
          nodes {
            title
          }
        }
      }
    }
  }
}

# Create epic
mutation CreateEpic($groupPath: ID!, $title: String!) {
  createEpic(input: {
    groupPath: $groupPath
    title: $title
  }) {
    epic {
      id
      iid
      title
    }
    errors
  }
}
```

### 7. CI/CD Integration

**Auto-close issues on merge:**

```yaml
# .gitlab-ci.yml
deploy:
  stage: deploy
  script:
    - ./deploy.sh
  environment:
    name: production
  only:
    - main
```

**Issue closing patterns:**

```markdown
<!-- In merge request description -->
Closes #123
Fixes #456
Resolves #789
```

**Auto-update issue on pipeline:**

```yaml
# Using GitLab API in CI
update-issue:
  stage: notify
  script:
    - |
      curl --request PUT \
        --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        --data "labels=workflow::deployed" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/issues/$ISSUE_IID"
  only:
    - tags
```

---

## Templates

### Project Setup Checklist

```markdown
## GitLab Project Setup

### Labels
- [ ] Workflow labels created (scoped)
- [ ] Priority labels created (scoped)
- [ ] Type labels created
- [ ] Team labels created (if needed)

### Boards
- [ ] Development board configured
- [ ] Sprint board created
- [ ] Bug tracking board (optional)

### Milestones
- [ ] Current sprint milestone
- [ ] Next sprint milestone
- [ ] Release milestones

### Issue Templates
- [ ] Bug report template
- [ ] Feature request template
- [ ] Task template

### Integrations
- [ ] Slack notifications
- [ ] CI/CD pipeline triggers
- [ ] Auto-close on merge
```

### Issue Templates

**.gitlab/issue_templates/Bug.md:**

```markdown
## Summary

<!-- Brief description of the bug -->

## Steps to Reproduce

1.
2.
3.

## Expected Behavior

<!-- What should happen -->

## Actual Behavior

<!-- What actually happens -->

## Environment

- GitLab version:
- Browser:
- OS:

## Possible Fix

<!-- Optional: suggest a fix -->

/label ~bug ~"priority::medium" ~"workflow::backlog"
```

**.gitlab/issue_templates/Feature.md:**

```markdown
## Summary

<!-- Brief description of the feature -->

## Problem Statement

<!-- What problem does this solve? -->

## Proposed Solution

<!-- How should it work? -->

## User Stories

- As a [user], I want [feature] so that [benefit]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Technical Notes

<!-- Implementation considerations -->

/label ~feature ~"priority::medium" ~"workflow::backlog"
```

### Quick Commands

```markdown
## GitLab Quick Actions

### Labels
/label ~bug ~"priority::high"
/unlabel ~"workflow::backlog"
/relabel ~"workflow::in-progress"

### Assignment
/assign @username
/unassign
/assign_reviewer @reviewer

### Milestone
/milestone %"Sprint 14"
/remove_milestone

### Time
/estimate 4h
/spend 2h

### Status
/close
/reopen
/lock
/unlock

### Relationships
/relate #123
/blocks #456
/clones #789

### Epic (Premium)
/epic &epic-title
/remove_epic
```

---

## Examples

### Example 1: Small Development Team

**Project:** acme-app

**Labels:**
```
workflow::backlog, workflow::ready, workflow::in-progress,
workflow::review, workflow::testing
priority::critical, priority::high, priority::medium, priority::low
bug, feature, tech-debt, documentation
```

**Board: Development**
| Open | Backlog | Ready | In Progress | Review | Testing |
|------|---------|-------|-------------|--------|---------|
| Triage | Prioritized | Sprint | Active | PR/MR | QA |

**Milestones:**
- Sprint 14 (current)
- Sprint 15 (next)
- v1.5 Release

### Example 2: Multi-Project Group

**Group:** product-team

**Subgroups:**
```
product-team/
├── frontend/
│   ├── web-app
│   └── mobile-app
├── backend/
│   ├── api
│   └── workers
└── infrastructure/
    └── terraform
```

**Group-level boards:**
- Cross-Project Roadmap (by milestone)
- All Bugs (filtered by ~bug)
- Release Board (by ~release label)

**Group milestones:**
- Q1 2026 Release
- Q2 2026 Release

**Epics:**
- Epic: Authentication Overhaul (spans api + web-app)
- Epic: Performance Optimization (spans all)

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Non-scoped labels | Multiple states | Use :: scoped labels |
| Too many boards | Confusion | 2-4 boards per project |
| Missing milestones | No time tracking | Create sprints + releases |
| No issue templates | Inconsistent issues | Create templates |
| Manual label updates | Overhead | Use quick actions |

---

## Next Steps

1. Create scoped labels for workflow
2. Set up Development board with label columns
3. Create sprint milestones
4. Add issue templates
5. Configure CI/CD integration
6. Set up group-level planning (if Premium)

---

## Related Methodologies

- M-PMT-004: GitHub Projects
- M-PMT-006: Azure DevOps Boards
- M-PMT-009: Cross-Tool Migration
- M-PMT-011: Agile Ceremonies Setup
