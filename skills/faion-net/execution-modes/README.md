# Execution Modes

Two execution modes for different task types and user preferences.

---

## YOLO Mode (Autonomous)

**Agent:** `faion-task-YOLO-executor-opus-agent`

**Behavior:**
- Execute tasks completely without asking questions
- Make decisions autonomously using best practices
- Use appropriate methodologies from 605 available
- Document assumptions in code/comments
- Complete tasks or report blockers with details

**When to use:**
- Clear, well-defined tasks
- Tasks with SDD documentation (spec, design)
- User trusts AI judgment
- User wants speed over control

**Execution:**
```python
Task(
    prompt="Execute task: {task_description}",
    subagent_type="faion-task-YOLO-executor-opus-agent"
)
```

---

## Interactive Mode (Dialogue)

**Skill:** `faion-communicator` (10 methodologies)

**Behavior:**
- Execute directly in main conversation flow
- Ask clarifying questions before proceeding
- Validate understanding at each step
- Use communication techniques:
  - **Interview:** Gather requirements with probing questions
  - **Brainstorm:** Generate options collaboratively
  - **Clarification:** Resolve ambiguity
  - **Validation:** Confirm before implementing
  - **Socratic:** Deep exploration through questions

**When to use:**
- Vague or incomplete requirements
- User wants to learn/understand
- Complex decisions needing input
- User prefers control over speed

---

## Communication Protocol

### For new feature requests → Interview

```
"I'd like to understand your requirements:
1. What problem are you solving?
2. Who are the users?
3. What's the success criteria?
4. Any constraints?"
```

### For design decisions → Brainstorm + Validate

```
"Let's explore options:
- Option A: [pros/cons]
- Option B: [pros/cons]
Which direction feels right?"
```

### For ambiguous requirements → Clarification

```
"When you say 'fast', do you mean:
a) Response time < 100ms?
b) Quick to implement?
c) Fast user experience?"
```

### Before implementation → Validation

```
"Here's my understanding: [summary]
Is this correct? Shall I proceed?"
```

---

## Execution in Interactive Mode

- Use tools directly in conversation
- Ask questions via AskUserQuestion or text
- Provide step-by-step visibility
- Confirm before significant changes

---

*Execution modes for faion-net orchestrator*
