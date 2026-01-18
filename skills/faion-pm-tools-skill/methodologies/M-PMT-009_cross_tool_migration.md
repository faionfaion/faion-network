# M-PMT-009: Cross-Tool Migration

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-009 |
| **Category** | PM Tools |
| **Difficulty** | Intermediate |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Organizations need to migrate between PM tools when:
- Current tool no longer fits team needs
- Company standardizes on a single platform
- Tool costs become prohibitive
- Better alternatives emerge

Migration challenges:
- Data loss during transfer
- Broken workflows and automations
- Team resistance to change
- Downtime during transition
- Loss of historical context

---

## Framework

### 1. Migration Assessment

**Pre-migration checklist:**

```markdown
## Migration Readiness Assessment

### Current State
- [ ] Document all projects/boards
- [ ] List all users and roles
- [ ] Inventory custom fields and metadata
- [ ] Map current workflows
- [ ] Document automations
- [ ] List integrations in use
- [ ] Calculate data volume

### Target State
- [ ] Confirm target tool selection
- [ ] Verify feature parity
- [ ] Plan workflow adjustments
- [ ] Identify gaps to address

### Risks
- [ ] Data that cannot be migrated
- [ ] Features not available in target
- [ ] Timeline constraints
- [ ] Budget for migration tools
```

**Data inventory template:**

| Data Type | Source Format | Volume | Migrateable | Notes |
|-----------|---------------|--------|-------------|-------|
| Projects | JSON | 50 | Yes | Include archived |
| Tasks | CSV | 10,000 | Yes | With comments |
| Attachments | Files | 5GB | Partial | Size limits |
| Comments | JSON | 25,000 | Yes | Preserve timestamps |
| Custom Fields | JSON | 20 | Manual | Recreate in target |
| Automations | N/A | 30 | No | Rebuild required |
| Integrations | N/A | 5 | No | Reconfigure |

### 2. Field Mapping

**Common field mappings:**

```yaml
# Jira → GitHub Projects
field_mapping:
  - source: Summary
    target: Title
    transform: none

  - source: Description
    target: Body
    transform: markdown_convert

  - source: Issue Type
    target: Labels
    transform: |
      Bug → bug
      Story → enhancement
      Task → task

  - source: Priority
    target: Labels
    transform: |
      Highest → priority:critical
      High → priority:high
      Medium → priority:medium
      Low → priority:low

  - source: Status
    target: Status
    transform: |
      To Do → Todo
      In Progress → In Progress
      Done → Done

  - source: Assignee
    target: Assignees
    transform: user_mapping

  - source: Sprint
    target: Iteration
    transform: iteration_mapping

  - source: Story Points
    target: Custom Field (Effort)
    transform: none

  - source: Labels
    target: Labels
    transform: lowercase, spaces_to_hyphens

  - source: Comments
    target: Comments
    transform: preserve_author_timestamp
```

**User mapping table:**

| Source User | Source Email | Target User | Target Email |
|-------------|--------------|-------------|--------------|
| jsmith | john@company.com | john-smith | john@company.com |
| ajones | alice@company.com | alice-jones | alice@company.com |

### 3. Migration Strategies

**Strategy 1: Big Bang Migration**

```
Day 0: Freeze source tool (read-only)
Day 1: Export all data
Day 2: Transform and validate
Day 3: Import to target
Day 4: Verify and test
Day 5: Go live on target
```

Pros: Clean cutover, no sync issues
Cons: Higher risk, requires downtime

**Strategy 2: Phased Migration**

```
Phase 1: New projects in target tool
Phase 2: Migrate active projects
Phase 3: Migrate historical data
Phase 4: Decommission source
```

Pros: Lower risk, gradual learning
Cons: Dual tool maintenance, sync complexity

**Strategy 3: Parallel Run**

```
Week 1-2: Setup target, train team
Week 3-4: Run both tools in parallel
Week 5: Primary work moves to target
Week 6: Source becomes archive only
Week 8: Decommission source
```

Pros: Safety net, comparison period
Cons: Double work, confusion potential

### 4. Export Procedures

**Jira Export:**

```bash
# Via REST API
curl -u email:api_token \
  "https://your-domain.atlassian.net/rest/api/3/search?jql=project=PROJ&maxResults=1000" \
  -H "Accept: application/json" > jira_export.json

# Bulk export (Admin)
# Administration → System → Backup Manager → Create Backup
# Downloads XML backup of entire instance
```

```python
from jira import JIRA

def export_jira_project(server, email, token, project_key):
    jira = JIRA(server=server, basic_auth=(email, token))

    issues = []
    start = 0
    max_results = 100

    while True:
        batch = jira.search_issues(
            f"project={project_key}",
            startAt=start,
            maxResults=max_results,
            expand="changelog,comments,attachments"
        )
        if not batch:
            break
        issues.extend([issue.raw for issue in batch])
        start += max_results

    return {
        "project": project_key,
        "exported_at": datetime.now().isoformat(),
        "total_issues": len(issues),
        "issues": issues
    }
```

**Trello Export:**

```python
import requests

def export_trello_board(api_key, token, board_id):
    url = f"https://api.trello.com/1/boards/{board_id}"
    params = {
        "key": api_key,
        "token": token,
        "fields": "all",
        "cards": "all",
        "card_attachments": "true",
        "lists": "all",
        "members": "all",
        "checklists": "all",
        "labels": "all",
        "actions": "all",
        "actions_limit": 1000
    }

    response = requests.get(url, params=params)
    return response.json()
```

**Linear Export:**

```graphql
# Via GraphQL API
query ExportProject($projectId: String!) {
  project(id: $projectId) {
    id
    name
    issues {
      nodes {
        id
        title
        description
        state {
          name
        }
        priority
        estimate
        assignee {
          name
          email
        }
        labels {
          nodes {
            name
          }
        }
        comments {
          nodes {
            body
            user {
              name
            }
            createdAt
          }
        }
        attachments {
          nodes {
            url
            title
          }
        }
        createdAt
        updatedAt
      }
    }
  }
}
```

**ClickUp Export:**

```python
import requests

def export_clickup_space(api_token, space_id):
    headers = {"Authorization": api_token}
    base_url = "https://api.clickup.com/api/v2"

    # Get folders and lists
    folders = requests.get(
        f"{base_url}/space/{space_id}/folder",
        headers=headers
    ).json()

    tasks = []
    for folder in folders.get("folders", []):
        for list_item in folder.get("lists", []):
            list_tasks = requests.get(
                f"{base_url}/list/{list_item['id']}/task",
                headers=headers,
                params={"include_closed": True}
            ).json()
            tasks.extend(list_tasks.get("tasks", []))

    return {
        "space_id": space_id,
        "folders": folders,
        "tasks": tasks
    }
```

### 5. Transform Data

**Python transformation framework:**

```python
import json
from dataclasses import dataclass
from typing import Dict, List, Any, Callable
from datetime import datetime

@dataclass
class FieldMapping:
    source_field: str
    target_field: str
    transform: Callable[[Any], Any] = lambda x: x
    required: bool = False
    default: Any = None

class MigrationTransformer:
    def __init__(self, mappings: List[FieldMapping],
                 user_map: Dict[str, str] = None):
        self.mappings = {m.source_field: m for m in mappings}
        self.user_map = user_map or {}
        self.errors = []

    def transform_item(self, source_item: Dict) -> Dict:
        """Transform single item from source to target format"""
        target_item = {}

        for source_field, mapping in self.mappings.items():
            try:
                value = source_item.get(source_field, mapping.default)

                if value is None and mapping.required:
                    self.errors.append(
                        f"Missing required field: {source_field}"
                    )
                    continue

                if value is not None:
                    target_item[mapping.target_field] = mapping.transform(value)
            except Exception as e:
                self.errors.append(
                    f"Error transforming {source_field}: {str(e)}"
                )

        return target_item

    def transform_all(self, source_items: List[Dict]) -> List[Dict]:
        """Transform all items"""
        return [self.transform_item(item) for item in source_items]

    def map_user(self, source_user: str) -> str:
        """Map source user to target user"""
        return self.user_map.get(source_user, source_user)


# Example: Jira to GitHub transformation
def jira_to_github_transform(jira_issues: List[Dict],
                              user_map: Dict[str, str]) -> List[Dict]:

    def transform_description(desc):
        # Convert Jira markup to Markdown
        if not desc:
            return ""
        # Basic conversions
        desc = desc.replace("{code}", "```")
        desc = desc.replace("h1.", "#")
        desc = desc.replace("h2.", "##")
        desc = desc.replace("*bold*", "**bold**")
        return desc

    def transform_priority(priority):
        mapping = {
            "Highest": "priority:critical",
            "High": "priority:high",
            "Medium": "priority:medium",
            "Low": "priority:low",
            "Lowest": "priority:low"
        }
        return mapping.get(priority, "")

    def transform_status(status):
        mapping = {
            "To Do": "Todo",
            "In Progress": "In Progress",
            "In Review": "In Progress",
            "Done": "Done",
            "Closed": "Done"
        }
        return mapping.get(status, "Todo")

    mappings = [
        FieldMapping("summary", "title", required=True),
        FieldMapping("description", "body", transform_description),
        FieldMapping("priority", "labels", transform_priority),
        FieldMapping("status", "status", transform_status),
        FieldMapping("assignee", "assignees",
                    lambda x: [user_map.get(x, x)] if x else []),
        FieldMapping("labels", "labels",
                    lambda labels: [l.lower().replace(" ", "-")
                                   for l in labels]),
        FieldMapping("created", "created_at"),
        FieldMapping("updated", "updated_at"),
    ]

    transformer = MigrationTransformer(mappings, user_map)
    return transformer.transform_all(jira_issues)
```

### 6. Import Procedures

**GitHub Projects Import:**

```python
import requests
from typing import List, Dict

class GitHubProjectsImporter:
    def __init__(self, token: str, owner: str, repo: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"

    def create_issue(self, title: str, body: str = "",
                     labels: List[str] = None,
                     assignees: List[str] = None) -> Dict:
        """Create GitHub issue"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues"
        data = {
            "title": title,
            "body": body,
            "labels": labels or [],
            "assignees": assignees or []
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def add_to_project(self, issue_id: int, project_id: str):
        """Add issue to GitHub Project (v2)"""
        # GraphQL mutation for Projects v2
        query = """
        mutation($projectId: ID!, $contentId: ID!) {
          addProjectV2ItemById(input: {
            projectId: $projectId,
            contentId: $contentId
          }) {
            item {
              id
            }
          }
        }
        """
        # Implementation via GraphQL API
        pass

    def import_batch(self, items: List[Dict],
                     batch_size: int = 50) -> List[Dict]:
        """Import items in batches with rate limiting"""
        results = []
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            for item in batch:
                try:
                    result = self.create_issue(
                        title=item["title"],
                        body=item.get("body", ""),
                        labels=item.get("labels", []),
                        assignees=item.get("assignees", [])
                    )
                    results.append({"success": True, "issue": result})
                except Exception as e:
                    results.append({"success": False, "error": str(e),
                                   "item": item})

            # Rate limit: 5000 requests/hour for authenticated
            time.sleep(0.1)  # ~10 requests/second

        return results
```

**Linear Import:**

```python
import requests

class LinearImporter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.linear.app/graphql"
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

    def create_issue(self, team_id: str, title: str, **kwargs) -> Dict:
        """Create Linear issue"""
        query = """
        mutation IssueCreate($input: IssueCreateInput!) {
          issueCreate(input: $input) {
            success
            issue {
              id
              identifier
              title
              url
            }
          }
        }
        """

        variables = {
            "input": {
                "teamId": team_id,
                "title": title,
                "description": kwargs.get("description", ""),
                "priority": kwargs.get("priority", 3),
                "estimate": kwargs.get("estimate"),
                "assigneeId": kwargs.get("assignee_id"),
                "labelIds": kwargs.get("label_ids", []),
                "projectId": kwargs.get("project_id"),
                "cycleId": kwargs.get("cycle_id")
            }
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            json={"query": query, "variables": variables}
        )
        return response.json()

    def import_from_jira(self, jira_issues: List[Dict],
                         team_id: str,
                         field_mapping: Dict) -> List[Dict]:
        """Import Jira issues to Linear"""
        results = []

        for issue in jira_issues:
            try:
                linear_issue = self.create_issue(
                    team_id=team_id,
                    title=issue.get("summary"),
                    description=self._convert_description(
                        issue.get("description")
                    ),
                    priority=self._map_priority(
                        issue.get("priority")
                    ),
                    estimate=issue.get("customfield_10016")  # Story points
                )
                results.append({
                    "jira_key": issue.get("key"),
                    "linear_id": linear_issue.get("data", {})
                                            .get("issueCreate", {})
                                            .get("issue", {})
                                            .get("identifier"),
                    "success": True
                })
            except Exception as e:
                results.append({
                    "jira_key": issue.get("key"),
                    "success": False,
                    "error": str(e)
                })

        return results
```

### 7. Validation

**Post-migration validation checklist:**

```markdown
## Migration Validation

### Data Integrity
- [ ] Total item count matches source
- [ ] All required fields populated
- [ ] Attachments accessible
- [ ] Comments preserved with timestamps
- [ ] User assignments correct

### Workflows
- [ ] Status transitions work
- [ ] Automations trigger correctly
- [ ] Notifications functioning
- [ ] Permissions enforced

### Integrations
- [ ] Slack notifications working
- [ ] GitHub/GitLab links functional
- [ ] Webhooks firing
- [ ] API endpoints responding

### User Acceptance
- [ ] Key users verified their data
- [ ] Workflows tested end-to-end
- [ ] Training completed
- [ ] Documentation updated
```

**Validation script:**

```python
class MigrationValidator:
    def __init__(self, source_data: List[Dict], target_data: List[Dict]):
        self.source = source_data
        self.target = target_data
        self.issues = []

    def validate_count(self):
        """Verify item counts match"""
        source_count = len(self.source)
        target_count = len(self.target)

        if source_count != target_count:
            self.issues.append(
                f"Count mismatch: {source_count} source, {target_count} target"
            )
            return False
        return True

    def validate_required_fields(self, required_fields: List[str]):
        """Verify required fields have values"""
        for item in self.target:
            for field in required_fields:
                if not item.get(field):
                    self.issues.append(
                        f"Missing {field} in item {item.get('id', 'unknown')}"
                    )

    def validate_mapping(self, id_field: str):
        """Verify all source items have target counterparts"""
        source_ids = {item[id_field] for item in self.source}
        target_source_refs = {
            item.get("source_id") for item in self.target
            if item.get("source_id")
        }

        missing = source_ids - target_source_refs
        if missing:
            self.issues.append(f"Missing migrations: {missing}")

    def generate_report(self) -> Dict:
        """Generate validation report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "source_count": len(self.source),
            "target_count": len(self.target),
            "issues_found": len(self.issues),
            "issues": self.issues,
            "status": "PASS" if not self.issues else "FAIL"
        }
```

### 8. Rollback Plan

**Rollback procedure:**

```markdown
## Rollback Plan

### Triggers for Rollback
- Critical data loss discovered
- Major workflow broken
- Team unable to work
- Integration failures blocking work

### Rollback Steps

1. **Communicate** (5 min)
   - Notify team of rollback
   - Set source tool to read-write

2. **Restore Source** (15 min)
   - Remove read-only flags
   - Restore from backup if needed
   - Verify source accessibility

3. **Sync Changes** (30 min)
   - Export changes made in target
   - Manually apply critical changes to source
   - Document what needs re-migration

4. **Disable Target** (5 min)
   - Set target to read-only
   - Update documentation
   - Notify team source is primary

5. **Post-Mortem** (1 hour)
   - Document what went wrong
   - Plan fixes
   - Schedule retry
```

---

## Templates

### Migration Plan Template

```markdown
# PM Tool Migration Plan

## Overview
- **Source:** [Current tool]
- **Target:** [New tool]
- **Timeline:** [Start] - [End]
- **Migration Lead:** [Name]

## Scope
- Projects: [List]
- Users: [Count]
- Data volume: [Size]

## Strategy
[ ] Big Bang / [ ] Phased / [ ] Parallel Run

## Timeline

| Phase | Dates | Activities |
|-------|-------|------------|
| Planning | Week 1 | Assessment, mapping |
| Preparation | Week 2 | Setup target, create scripts |
| Migration | Week 3 | Export, transform, import |
| Validation | Week 4 | Testing, fixes |
| Go-Live | Week 5 | Cutover, training |

## Field Mapping
[Include mapping table]

## User Mapping
[Include user mapping table]

## Risk Mitigation
| Risk | Mitigation |
|------|------------|
| Data loss | Full backup before migration |
| Downtime | Weekend migration window |
| User confusion | Training sessions, documentation |

## Rollback Criteria
- [Criterion 1]
- [Criterion 2]

## Success Criteria
- [ ] 100% data migrated
- [ ] All users can access target
- [ ] Key workflows functional
- [ ] Integrations working
```

### Communication Template

```markdown
# Migration Communication Plan

## Pre-Migration (1 week before)

**Subject:** PM Tool Migration Scheduled

Team,

We will be migrating from [Source] to [Target] on [Date].

**What's happening:**
- All projects will move to [Target]
- Your data will be preserved

**What you need to do:**
- Complete urgent work by [Date]
- Attend training on [Date/Time]
- Review your assignments after migration

**Timeline:**
- [Date] 5pm: [Source] becomes read-only
- [Date] - [Date]: Migration in progress
- [Date] 9am: [Target] goes live

Questions? Contact [Migration Lead]

---

## Migration Day

**Subject:** Migration In Progress

Migration is underway. [Source] is now read-only.

Expected completion: [Time]
Status updates: [Slack channel]

---

## Post-Migration

**Subject:** Migration Complete - Action Required

Migration to [Target] is complete!

**Next steps:**
1. Log in: [Target URL]
2. Verify your projects and tasks
3. Report issues: [Channel/Form]

**Training resources:**
- Quick start guide: [Link]
- Video walkthrough: [Link]
- Office hours: [Date/Time]

Welcome to [Target]!
```

---

## Examples

### Example 1: Jira to Linear

**Scenario:** 100-person engineering team migrating 50,000 issues

**Approach:** Phased migration over 4 weeks

```python
# Migration script outline
migration_config = {
    "source": {
        "type": "jira",
        "url": "https://company.atlassian.net",
        "projects": ["PROJ1", "PROJ2", "PROJ3"]
    },
    "target": {
        "type": "linear",
        "team_id": "team_xxx"
    },
    "field_mapping": {
        "summary": "title",
        "description": "description",
        "priority": {"Highest": 1, "High": 2, "Medium": 3, "Low": 4},
        "status": {"To Do": "todo", "In Progress": "inProgress", "Done": "done"}
    },
    "phases": [
        {"name": "Active sprints", "jql": "sprint in openSprints()"},
        {"name": "Recent issues", "jql": "updated > -30d"},
        {"name": "Historical", "jql": "updated <= -30d"}
    ]
}
```

### Example 2: Trello to ClickUp

**Scenario:** Marketing team moving 20 boards

**Approach:** Big bang over weekend

```yaml
Migration Weekend Schedule:
  Friday 5pm:
    - Set all Trello boards to read-only
    - Final backup export

  Saturday:
    - Transform data
    - Import to ClickUp
    - Configure automations

  Sunday:
    - Validation testing
    - Fix critical issues
    - Prepare training materials

  Monday 9am:
    - Team training session
    - Go live on ClickUp
    - Support available all day
```

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| No field mapping | Data in wrong places | Document mapping before starting |
| Skipping validation | Discover issues late | Validate after each phase |
| No rollback plan | Stuck if migration fails | Plan rollback before starting |
| Insufficient training | Low adoption | Train before and after |
| Migrating everything | Unnecessary work | Archive old data first |
| Ignoring attachments | Lost files | Plan attachment migration |
| No communication | Team confusion | Over-communicate |

---

## Next Steps

1. Assess current tool data and workflows
2. Select migration strategy
3. Create field and user mappings
4. Build and test migration scripts
5. Plan communication and training
6. Execute migration with validation
7. Monitor and support post-migration

---

## Related Methodologies

- M-PMT-010: PM Tool Selection
- M-PMT-001: Jira Workflow Management
- M-PMT-002: ClickUp Setup
- M-PMT-003: Linear Issue Tracking
- M-PMT-004: GitHub Projects
