# GraphRAG LLM Prompts

## 1. Entity Extraction Prompts

### Basic Entity Extraction

```
You are an expert at extracting structured information from text.

Given the following text, extract all named entities and their types.

ENTITY TYPES:
- Person: Individual humans
- Organization: Companies, institutions, groups
- Location: Geographic places, addresses
- Product: Products, services, offerings
- Technology: Technologies, frameworks, tools
- Event: Notable occurrences, conferences, incidents
- Concept: Abstract ideas, topics, themes

TEXT:
{text}

OUTPUT FORMAT (JSON):
{
  "entities": [
    {
      "name": "entity name",
      "type": "entity type",
      "description": "brief description based on context",
      "aliases": ["alternative names if mentioned"]
    }
  ]
}

Extract ALL entities mentioned. Include a brief description derived from the context.
```

### Schema-Guided Entity Extraction

```
You are an expert knowledge graph builder. Extract entities from text following the provided schema.

SCHEMA:
{schema_json}

TEXT:
{text}

INSTRUCTIONS:
1. Extract only entities matching the schema types
2. Capture all properties defined in the schema
3. Use the exact entity type names from the schema
4. If a property is not mentioned, omit it (don't use null)
5. Resolve coreferences (he, she, it, they) to actual entity names

OUTPUT FORMAT (JSON):
{
  "entities": [
    {
      "name": "string",
      "type": "schema entity type",
      "properties": {
        "property_name": "value"
      }
    }
  ]
}
```

### Entity Extraction with Few-Shot Examples

```
You are an expert at extracting entities from text for knowledge graph construction.

ENTITY TYPES:
{entity_types}

EXAMPLES:

Input: "Elon Musk founded SpaceX in 2002. The company is headquartered in Hawthorne, California."
Output:
{
  "entities": [
    {"name": "Elon Musk", "type": "Person", "description": "Founder of SpaceX"},
    {"name": "SpaceX", "type": "Organization", "description": "Space exploration company founded in 2002"},
    {"name": "Hawthorne", "type": "Location", "description": "City in California, headquarters of SpaceX"},
    {"name": "California", "type": "Location", "description": "US state"}
  ]
}

Input: "Microsoft released Azure OpenAI Service, allowing developers to integrate GPT-4 into applications."
Output:
{
  "entities": [
    {"name": "Microsoft", "type": "Organization", "description": "Technology company"},
    {"name": "Azure OpenAI Service", "type": "Product", "description": "Cloud service for AI integration"},
    {"name": "GPT-4", "type": "Technology", "description": "Large language model"}
  ]
}

Now extract entities from this text:

TEXT:
{text}

OUTPUT (JSON only):
```

### Gleaning Prompt (Multi-Turn Extraction)

```
Review the text again and extract any entities that were missed in the previous extraction.

PREVIOUS EXTRACTION:
{previous_entities}

TEXT:
{text}

Are there any additional entities not captured above? Focus on:
- Implicit entities (referenced but not named directly)
- Technical terms or concepts
- Temporal references (dates, events)
- Relationships that imply entities

If no additional entities found, return: {"entities": []}

OUTPUT (JSON only):
```

## 2. Relationship Extraction Prompts

### Basic Relationship Extraction

```
You are an expert at identifying relationships between entities.

Given the entities and text below, extract all relationships.

ENTITIES:
{entities_json}

TEXT:
{text}

RELATIONSHIP TYPES:
- WORKS_FOR: Person works for Organization
- LOCATED_IN: Entity is located in Location
- PRODUCES: Organization produces Product
- USES: Entity uses Technology
- ACQUIRED: Organization acquired Organization
- FOUNDED: Person founded Organization
- PART_OF: Entity is part of Entity
- RELATED_TO: General relationship (specify type in description)

OUTPUT FORMAT (JSON):
{
  "relationships": [
    {
      "source": "source entity name",
      "target": "target entity name",
      "type": "relationship type",
      "description": "brief description of relationship",
      "properties": {
        "since": "date if mentioned",
        "role": "specific role if mentioned"
      }
    }
  ]
}

RULES:
1. Only create relationships between entities in the list
2. Ensure directionality is correct (source -> target)
3. Include temporal information when available
4. One relationship per distinct connection
```

### Schema-Constrained Relationship Extraction

```
Extract relationships between entities following the provided schema.

SCHEMA:
{
  "relationships": [
    {"type": "WORKS_FOR", "source_types": ["Person"], "target_types": ["Organization"]},
    {"type": "LOCATED_IN", "source_types": ["Person", "Organization"], "target_types": ["Location"]},
    {"type": "PRODUCES", "source_types": ["Organization"], "target_types": ["Product"]},
    {"type": "USES", "source_types": ["Person", "Organization", "Product"], "target_types": ["Technology"]},
    {"type": "ACQUIRED", "source_types": ["Organization"], "target_types": ["Organization"]}
  ]
}

ENTITIES:
{entities_json}

TEXT:
{text}

INSTRUCTIONS:
1. Only extract relationships defined in the schema
2. Verify source/target entity types match schema constraints
3. Capture any mentioned properties (dates, amounts, roles)
4. If relationship direction is ambiguous, use most logical direction

OUTPUT (JSON):
{
  "relationships": [
    {
      "source": "entity name",
      "source_type": "entity type",
      "target": "entity name",
      "target_type": "entity type",
      "type": "relationship type from schema",
      "confidence": 0.0-1.0,
      "evidence": "quote from text supporting this relationship"
    }
  ]
}
```

### Combined Entity and Relationship Extraction

```
You are a knowledge graph extraction expert. Extract entities and relationships from text.

TEXT:
{text}

ENTITY TYPES: {entity_types}
RELATIONSHIP TYPES: {relationship_types}

OUTPUT FORMAT (JSON):
{
  "entities": [
    {
      "id": "unique_id",
      "name": "entity name",
      "type": "entity type",
      "description": "description from context"
    }
  ],
  "relationships": [
    {
      "source_id": "entity id",
      "target_id": "entity id",
      "type": "relationship type",
      "description": "relationship description"
    }
  ]
}

EXTRACTION GUIDELINES:
1. Assign unique IDs to entities (e.g., "e1", "e2")
2. Reference these IDs in relationships
3. Extract implicit relationships (e.g., "CEO of" implies WORKS_FOR)
4. Handle pronouns by resolving to actual entity names
5. Create bidirectional relationships only when explicitly bidirectional
```

## 3. Community Summarization Prompts

### Community Summary Generation

```
You are an expert at summarizing groups of related entities.

COMMUNITY INFORMATION:
Entities: {entities_list}
Relationships: {relationships_list}
Key facts: {facts_list}

Generate a comprehensive summary of this community that:
1. Identifies the main theme or topic
2. Highlights key entities and their roles
3. Explains important relationships
4. Notes any patterns or clusters within the community

FORMAT:
Title: [Descriptive title for this community]
Summary: [2-3 paragraph summary]
Key Entities: [Bulleted list of most important entities]
Key Relationships: [Bulleted list of most important relationships]
Themes: [Comma-separated list of themes]
```

### Hierarchical Community Summary

```
Create a summary for a high-level community composed of sub-communities.

SUB-COMMUNITY SUMMARIES:
{sub_community_summaries}

BRIDGING RELATIONSHIPS:
{bridging_relationships}

Generate a summary that:
1. Synthesizes the sub-community themes
2. Identifies overarching patterns
3. Highlights inter-community relationships
4. Provides a bird's-eye view suitable for answering global questions

OUTPUT:
{
  "title": "community title",
  "summary": "comprehensive summary paragraph",
  "themes": ["theme1", "theme2"],
  "key_insights": ["insight1", "insight2"],
  "sub_community_themes": ["sub-theme1", "sub-theme2"]
}
```

## 4. Query Processing Prompts

### Query Entity Extraction

```
Extract entities mentioned in the user query for knowledge graph search.

QUERY: {query}

AVAILABLE ENTITY TYPES: {entity_types}

Extract:
1. Explicit entities (directly named)
2. Implicit entities (described but not named)
3. Entity types being asked about

OUTPUT (JSON):
{
  "explicit_entities": ["entity1", "entity2"],
  "implicit_entities": [
    {"description": "entity description", "probable_type": "type"}
  ],
  "target_entity_types": ["types being queried about"],
  "relationship_focus": ["relationship types relevant to query"]
}
```

### Query Classification

```
Classify the query to determine the best retrieval strategy.

QUERY: {query}

CLASSIFICATION CATEGORIES:

LOCAL QUERY - Specific entity/relationship questions
- "What is X?"
- "Who founded Y?"
- "How are A and B related?"

GLOBAL QUERY - Broad theme/summary questions
- "What are the main themes?"
- "Summarize the key topics"
- "What patterns exist across..."

HYBRID QUERY - Requires both specific facts and broader context
- "How does X compare to similar entities?"
- "What role does Y play in the broader context?"

OUTPUT (JSON):
{
  "classification": "LOCAL" | "GLOBAL" | "HYBRID",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation",
  "suggested_traversal_depth": 1-3,
  "suggested_community_level": 0-N
}
```

## 5. Response Synthesis Prompts

### Local Search Synthesis

```
Generate a response using the retrieved subgraph context.

QUERY: {query}

CONTEXT:
Entities: {entities}
Relationships: {relationships}
Text chunks: {relevant_chunks}

INSTRUCTIONS:
1. Answer the query using ONLY the provided context
2. Cite specific entities and relationships
3. If information is incomplete, state what is known and what is missing
4. Do not make up information not in the context

RESPONSE FORMAT:
[Direct answer to the query]

Supporting evidence:
- [Entity/relationship citations]

Confidence: [HIGH/MEDIUM/LOW based on context coverage]
```

### Global Search Synthesis (Map-Reduce)

#### Map Phase

```
Based on this community summary, provide a partial answer to the query.

QUERY: {query}

COMMUNITY SUMMARY:
{community_summary}

If this community is relevant to the query:
- Provide specific information from the summary
- Note key entities or themes that address the query
- Rate relevance: HIGH/MEDIUM/LOW

If not relevant, respond: "NOT_RELEVANT"

PARTIAL ANSWER:
```

#### Reduce Phase

```
Combine these partial answers into a comprehensive response.

QUERY: {query}

PARTIAL ANSWERS:
{partial_answers}

INSTRUCTIONS:
1. Synthesize all relevant partial answers
2. Identify common themes across communities
3. Note any contradictions or different perspectives
4. Provide a comprehensive, well-structured response

RESPONSE:
[Comprehensive answer synthesizing all partial answers]

Sources: [List of communities/themes that contributed]
```

### Hybrid Search Synthesis

```
Generate a response using both vector-retrieved content and graph context.

QUERY: {query}

VECTOR SEARCH RESULTS (semantic similarity):
{vector_results}

GRAPH CONTEXT (entity relationships):
{graph_context}

INSTRUCTIONS:
1. Prioritize graph context for relationship questions
2. Use vector results for detailed textual information
3. Combine both for comprehensive answers
4. Cite sources appropriately

RESPONSE:
[Answer combining both sources]

Graph-derived facts:
- [Facts from entity relationships]

Text-derived details:
- [Details from vector search]
```

## 6. Entity Resolution Prompts

### Deduplication

```
Identify if these entities refer to the same real-world entity.

ENTITY A:
{entity_a}

ENTITY B:
{entity_b}

CONTEXT A: {context_a}
CONTEXT B: {context_b}

Analyze:
1. Name similarity (including aliases, abbreviations)
2. Type consistency
3. Contextual clues (descriptions, relationships)
4. Distinguishing features

OUTPUT (JSON):
{
  "same_entity": true/false,
  "confidence": 0.0-1.0,
  "reasoning": "explanation",
  "canonical_name": "preferred name if same entity",
  "merged_properties": {} // combined properties if same entity
}
```

### Coreference Resolution

```
Resolve pronouns and references to their actual entities.

TEXT: {text}

IDENTIFIED ENTITIES: {entities}

For each pronoun or reference (he, she, it, they, the company, etc.):
1. Identify what it refers to
2. Map to an entity from the list
3. If no match, identify as new implicit entity

OUTPUT (JSON):
{
  "resolutions": [
    {
      "reference": "the pronoun/reference",
      "position": "character position in text",
      "resolved_to": "entity name or NEW",
      "confidence": 0.0-1.0
    }
  ]
}
```

## 7. Domain-Specific Prompts

### Technical Documentation

```
Extract technical entities and relationships from documentation.

TEXT: {text}

ENTITY TYPES:
- API: API endpoints or interfaces
- Function: Functions or methods
- Class: Classes or types
- Parameter: Function/API parameters
- Module: Packages or modules
- ErrorType: Exceptions or error codes

RELATIONSHIP TYPES:
- CONTAINS: Module contains Function/Class
- CALLS: Function calls another Function
- INHERITS: Class inherits from Class
- ACCEPTS: Function/API accepts Parameter
- RETURNS: Function returns type
- RAISES: Function raises ErrorType
- DEPENDS_ON: Module depends on Module

OUTPUT (JSON):
{
  "entities": [...],
  "relationships": [...]
}

Focus on:
- Method signatures and their parameters
- Class hierarchies
- Module dependencies
- Error handling patterns
```

### Legal Documents

```
Extract legal entities and relationships.

TEXT: {text}

ENTITY TYPES:
- Case: Legal cases with citations
- Statute: Laws, regulations, codes
- Party: Plaintiffs, defendants, appellants
- Judge: Judges and justices
- Court: Courts and tribunals
- LegalConcept: Legal doctrines, principles

RELATIONSHIP TYPES:
- CITES: Case cites Case/Statute
- OVERRULES: Case overrules Case
- AFFIRMS: Case affirms Case
- INTERPRETS: Case interprets Statute
- INVOLVES: Case involves Party
- DECIDED_BY: Case decided by Judge
- HEARD_IN: Case heard in Court
- ESTABLISHES: Case establishes LegalConcept

OUTPUT (JSON):
{
  "entities": [...],
  "relationships": [...]
}

Focus on:
- Case citations and their relationships
- Legal precedents and their authority
- Statutory interpretations
```

## 8. Quality Improvement Prompts

### Extraction Critique

```
Review the entity and relationship extraction for quality issues.

ORIGINAL TEXT:
{text}

EXTRACTION:
{extraction_json}

Check for:
1. Missing entities (important nouns not captured)
2. Incorrect types (entity assigned wrong type)
3. Duplicate entities (same entity extracted twice)
4. Missing relationships (obvious connections not captured)
5. Incorrect directionality (relationship direction wrong)
6. Hallucinated entities (entities not in text)

OUTPUT (JSON):
{
  "issues": [
    {
      "type": "MISSING_ENTITY|WRONG_TYPE|DUPLICATE|MISSING_RELATIONSHIP|WRONG_DIRECTION|HALLUCINATION",
      "description": "description of issue",
      "suggestion": "how to fix"
    }
  ],
  "quality_score": 0.0-1.0
}
```

### Extraction Refinement

```
Refine the extraction based on identified issues.

ORIGINAL EXTRACTION:
{extraction_json}

ISSUES:
{issues_json}

Provide a corrected extraction addressing all issues.

CORRECTED OUTPUT (JSON):
{
  "entities": [...],
  "relationships": [...]
}
```

## Usage Notes

1. **Temperature**: Use temperature=0 for extraction (deterministic), 0.3-0.5 for summarization
2. **Context Window**: Chunk text to fit within context limits, with overlap for continuity
3. **Few-Shot Examples**: Domain-specific examples significantly improve extraction quality
4. **Validation**: Always validate JSON output and retry on parse errors
5. **Batching**: Process multiple chunks in parallel for efficiency
6. **Caching**: Cache extraction results for incremental updates
