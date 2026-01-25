# Execution Patterns

Task execution patterns for marketing workflows.

---

## GTM Manifest Creation

```python
# Strategy questions
AskUserQuestion(
    questions=[
        {
            "question": "Sales model?",
            "options": [
                {"label": "PLG", "description": "Product-Led Growth"},
                {"label": "Sales-Led", "description": "Enterprise sales"},
                {"label": "Hybrid", "description": "PLG + Sales"}
            ]
        },
        {
            "question": "Launch timeline?",
            "options": [
                {"label": "MVP", "description": "3-6 months"},
                {"label": "Full", "description": "6-12 months"}
            ]
        }
    ]
)

# Generate sections
for section in SECTIONS:
    Task(
        subagent_type="general-purpose",
        prompt=f"""
PROJECT: {project}
SECTION: {section.name}
RESEARCH: {research_data}
OUTPUT: product_docs/gtm-manifest/{section.file}

Write {section.name} section using research data.
"""
    )
```

---

## Landing Page Creation

```python
# Copywriting
Task(subagent_type="faion-landing-agent (mode: copy)",
     prompt=f"PRODUCT: {p}, AUDIENCE: {a}, FRAMEWORK: AIDA")

# Design
Task(subagent_type="faion-landing-agent (mode: design)",
     prompt=f"COPY: {copy}, STYLE: {modern|minimal|bold}")

# Analysis
Task(subagent_type="faion-landing-agent (mode: analyze)",
     prompt=f"Analyze {url_or_code} for conversion")
```

---

## Content Marketing

```python
Task(subagent_type="faion-content-agent",
     prompt=f"Create content plan for {topic} targeting {audience}")

Task(subagent_type="faion-content-agent",
     prompt=f"Write blog post: {title}")
```

---

## Growth Experiments

```python
Task(subagent_type="faion-growth-agent",
     prompt=f"Design experiment to test {hypothesis}")

Task(subagent_type="faion-growth-agent",
     prompt=f"Analyze experiment results: {data}")
```

---

*Execution Patterns for Marketing Workflows*
*Part of faion-marketing-manager skill*
