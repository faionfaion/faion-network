"""
purpose: Pydantic models for Entity + Relation.
consumes: see AGENTS.md ## Prerequisites
produces: spec
depends-on: content/02-output-contract.xml schema for graph-rag
token-budget-impact: ≤500 tokens to fill
"""

# Generic entity/relationship schema for GraphRAG pipelines

GENERIC_SCHEMA = {
    "entities": [
        {"name": "Person", "properties": ["name", "title", "affiliation"]},
        {"name": "Organization", "properties": ["name", "type", "industry", "location"]},
        {"name": "Location", "properties": ["name", "type", "country"]},
        {"name": "Product", "properties": ["name", "type", "manufacturer"]},
        {"name": "Technology", "properties": ["name", "type", "version"]},
        {"name": "Event", "properties": ["name", "date", "location"]},
        {"name": "Concept", "properties": ["name", "domain"]},
    ],
    "relationships": [
        {"name": "WORKS_FOR", "source": "Person", "target": "Organization"},
        {"name": "LOCATED_IN", "source": ["Person", "Organization"], "target": "Location"},
        {"name": "PRODUCES", "source": "Organization", "target": "Product"},
        {"name": "USES", "source": ["Person", "Organization"], "target": "Technology"},
        {"name": "ACQUIRED", "source": "Organization", "target": "Organization"},
        {"name": "RELATED_TO", "source": "*", "target": "*", "properties": ["type", "strength"]},
    ],
}

# Domain-specific: Technical documentation
TECH_DOCS_SCHEMA = {
    "entities": [
        {"name": "API", "properties": ["name", "version", "type"]},
        {"name": "Function", "properties": ["name", "signature", "module"]},
        {"name": "Class", "properties": ["name", "module", "parent_class"]},
        {"name": "Module", "properties": ["name", "package", "version"]},
        {"name": "ErrorType", "properties": ["name", "code", "severity"]},
    ],
    "relationships": [
        {"name": "CONTAINS", "source": "Module", "target": ["Function", "Class"]},
        {"name": "CALLS", "source": "Function", "target": "Function"},
        {"name": "INHERITS", "source": "Class", "target": "Class"},
        {"name": "RAISES", "source": "Function", "target": "ErrorType"},
        {"name": "DEPENDS_ON", "source": "Module", "target": "Module"},
    ],
}
