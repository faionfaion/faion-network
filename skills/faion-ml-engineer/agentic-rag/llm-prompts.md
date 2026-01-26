# Agentic RAG LLM Prompts

Production-ready prompts for agentic RAG components.

## 1. Query Router Prompts

### Basic Router

```
You are a query router. Analyze the query and route to the best data source.

Available sources:
- vectorstore: Internal documentation, knowledge base, domain-specific content
- web_search: Current events, recent news, real-time information, public facts
- direct_response: General knowledge, definitions, simple calculations
- api: User-specific data (email, calendar, CRM, personal accounts)

Consider:
1. Does the query require specific domain knowledge? → vectorstore
2. Does it ask about recent events or current state? → web_search
3. Is it a simple factual question or definition? → direct_response
4. Does it reference personal/user-specific data? → api

Query: {query}

Respond with JSON:
{
  "datasource": "<source>",
  "reasoning": "<why this source>",
  "confidence": <0.0-1.0>
}
```

### Multi-Source Router

```
You are an intelligent query router. Determine which data sources to query.

Sources:
- vectorstore: Internal docs, product info, company knowledge
- web: Current events, public information, recent updates
- api: User data (email, calendar, CRM)
- calculator: Math, conversions, calculations
- code: Code search, documentation

Query: {query}

Analyze what information types are needed. Route to one or more sources.

Respond with JSON:
{
  "sources": ["<source1>", "<source2>"],
  "primary_source": "<main source>",
  "reasoning": "<explanation>",
  "parallel": true/false
}
```

### Complexity-Aware Router

```
Analyze query complexity and determine retrieval strategy.

Complexity levels:
- SIMPLE: Factual, single-fact answer, no retrieval needed
- MODERATE: Requires 1-2 document lookups, single topic
- COMPLEX: Multi-hop reasoning, multiple sources, synthesis required

Query: {query}

Consider:
1. How many distinct facts are needed?
2. Does answering require combining information?
3. Is domain expertise required?
4. Could multiple sources provide different perspectives?

Respond with JSON:
{
  "complexity": "SIMPLE|MODERATE|COMPLEX",
  "requires_retrieval": true/false,
  "estimated_hops": <1-5>,
  "recommended_sources": ["<source1>"],
  "reasoning": "<explanation>"
}
```

## 2. Document Grading Prompts

### Binary Relevance Grader

```
You are a relevance grader. Assess if a document helps answer the question.

STRICT CRITERIA:
- YES: Document contains information directly relevant to answering the question
- NO: Document is off-topic, tangentially related, or lacks needed information

Question: {question}

Document:
{document}

Think step by step:
1. What information does the question seek?
2. Does this document provide that information?
3. Would removing this document hurt the answer quality?

Respond with JSON:
{
  "binary_score": "yes|no",
  "reasoning": "<brief explanation>"
}
```

### Graded Relevance with Key Info Extraction

```
Grade this document's relevance to the question and extract key information.

Question: {question}

Document:
{document}

Evaluation criteria:
- 0.0-0.3: Not relevant, different topic
- 0.4-0.6: Partially relevant, some useful context
- 0.7-0.8: Relevant, contains needed information
- 0.9-1.0: Highly relevant, directly answers the question

Respond with JSON:
{
  "relevance_score": <0.0-1.0>,
  "binary_score": "yes|no",
  "reasoning": "<why this score>",
  "key_information": "<extracted relevant facts if any>"
}
```

### Batch Document Grader

```
Grade multiple documents for relevance to the question.

Question: {question}

Documents:
{documents}

For each document, provide:
- Document index (0-based)
- Relevance score (0.0-1.0)
- Keep recommendation (yes/no)

Then provide overall assessment.

Respond with JSON:
{
  "grades": [
    {"index": 0, "score": 0.8, "keep": "yes", "reason": "..."},
    {"index": 1, "score": 0.3, "keep": "no", "reason": "..."}
  ],
  "overall_quality": "high|medium|low",
  "recommendation": "proceed|rewrite_query|web_search",
  "reasoning": "<overall assessment>"
}
```

## 3. Query Rewriting Prompts

### Basic Query Rewriter

```
Rewrite this query to improve retrieval results.

Original query: {original_query}
Current query: {current_query}
Retrieved context (insufficient): {context}
Attempt number: {attempt}

Rewriting strategies:
1. SYNONYM_EXPANSION: Add related terms and synonyms
2. SPECIFICITY_ADJUST: Make more specific or broader
3. DECOMPOSITION: Break into sub-queries
4. REPHRASING: Different sentence structure

Choose the best strategy based on why retrieval may have failed.

Respond with JSON:
{
  "rewritten_query": "<improved query>",
  "strategy": "<strategy used>",
  "sub_queries": ["<sub1>", "<sub2>"],
  "reasoning": "<why this approach>"
}
```

### Iterative Query Refinement

```
The initial retrieval did not find sufficient information. Refine the query.

Original question: {original_query}
Previous queries tried: {query_history}
Context retrieved so far: {context}
What's still missing: {missing_info}

Generate a refined query that:
1. Targets the missing information specifically
2. Uses different keywords than previous attempts
3. May broaden or narrow scope as needed

Respond with JSON:
{
  "refined_query": "<new query>",
  "targeting": "<what missing info this targets>",
  "approach_change": "<how this differs from previous attempts>"
}
```

### Query Decomposition

```
Decompose this complex query into simpler sub-queries.

Complex query: {query}

Break down into independent questions that:
1. Each can be answered with a single retrieval
2. Together provide complete answer to original query
3. Have minimal overlap

Specify execution order and dependencies.

Respond with JSON:
{
  "original_query": "<original>",
  "sub_queries": [
    {"id": 0, "query": "<sub1>", "purpose": "<what it retrieves>"},
    {"id": 1, "query": "<sub2>", "purpose": "<what it retrieves>"}
  ],
  "execution_order": [0, 1],
  "dependencies": {"1": [0]},
  "synthesis_strategy": "<how to combine answers>"
}
```

## 4. Sufficiency Check Prompts

### Context Sufficiency Assessment

```
Assess if the retrieved context is sufficient to answer the question.

Question: {question}

Retrieved context:
{context}

Consider:
1. Does context contain the main facts needed?
2. Are there obvious gaps in information?
3. Is the context relevant to the question?
4. Could an accurate, complete answer be generated?

Respond with JSON:
{
  "is_sufficient": true/false,
  "confidence": <0.0-1.0>,
  "missing_information": ["<gap1>", "<gap2>"],
  "recommendation": "generate|retrieve_more|rewrite_query|web_search",
  "reasoning": "<explanation>"
}
```

### Multi-Hop Sufficiency

```
For this multi-hop question, assess if we have enough information.

Question: {question}
Information hops completed: {hop_count}/{max_hops}

Retrieved information by hop:
{hop_context}

Evaluate:
1. Have all required facts been retrieved?
2. Can the facts be connected to form an answer?
3. Is additional retrieval needed?

Respond with JSON:
{
  "is_sufficient": true/false,
  "facts_found": ["<fact1>", "<fact2>"],
  "facts_missing": ["<missing1>"],
  "next_hop_query": "<query for next retrieval if needed>",
  "reasoning": "<explanation>"
}
```

## 5. Generation Prompts

### Grounded Answer Generation

```
Generate an answer based ONLY on the provided context. Do not use prior knowledge.

Question: {question}

Context:
{context}

Instructions:
1. Answer using only information from the context
2. If context doesn't fully answer, acknowledge limitations
3. Cite which part of context supports each claim
4. Be concise but complete

If the context is insufficient, say: "Based on the available information, I can only partially answer..."

Answer:
```

### Answer with Citations

```
Answer the question using the provided sources. Include citations.

Question: {question}

Sources:
[1] {source_1}
[2] {source_2}
[3] {source_3}

Format your answer with inline citations [1], [2], etc.
Only make claims supported by the sources.
If sources conflict, acknowledge the discrepancy.

Answer:
```

### Synthesis from Multiple Sources

```
Synthesize information from multiple sources to answer the question.

Question: {question}

Source A (Internal Docs): {source_a}
Source B (Web Search): {source_b}
Source C (API Data): {source_c}

Instructions:
1. Integrate information from all relevant sources
2. Prioritize more authoritative/recent sources when they conflict
3. Note source of key claims
4. Highlight any inconsistencies between sources

Synthesized Answer:
```

## 6. Verification Prompts

### Grounding Verification

```
Verify that this answer is fully grounded in the source context.

Generated Answer: {answer}

Source Context:
{context}

For each claim in the answer:
1. Is it directly supported by the context?
2. Is it a reasonable inference from the context?
3. Is it potentially hallucinated (not in context)?

Respond with JSON:
{
  "is_grounded": true/false,
  "grounding_score": <0.0-1.0>,
  "claims": [
    {"claim": "<claim text>", "status": "supported|inferred|unsupported", "source": "<context snippet if supported>"}
  ],
  "unsupported_claims": ["<claim1>"],
  "verified_answer": "<answer with unsupported claims removed or caveated>"
}
```

### Hallucination Detection

```
Check this response for hallucinations (claims not in sources).

Response: {response}

Available Sources:
{sources}

Hallucination types:
1. FACTUAL: Claims facts not in sources
2. ATTRIBUTION: Wrong source attribution
3. EXTRAPOLATION: Over-extends source information
4. FABRICATION: Completely made-up information

Respond with JSON:
{
  "has_hallucination": true/false,
  "severity": "none|minor|major|critical",
  "hallucinations": [
    {"type": "<type>", "claim": "<hallucinated text>", "explanation": "<why it's hallucinated>"}
  ],
  "corrected_response": "<response with hallucinations removed>"
}
```

### Completeness Check

```
Evaluate if this answer completely addresses the question.

Question: {question}

Answer: {answer}

Check:
1. Are all parts of the question addressed?
2. Is the answer specific enough?
3. Are there important caveats missing?
4. Would a user be satisfied with this response?

Respond with JSON:
{
  "is_complete": true/false,
  "completeness_score": <0.0-1.0>,
  "addressed_aspects": ["<aspect1>"],
  "missing_aspects": ["<aspect1>"],
  "suggested_additions": "<what should be added>",
  "final_assessment": "<brief evaluation>"
}
```

## 7. Error Recovery Prompts

### Retrieval Failure Handler

```
Retrieval failed for this query. Determine the best recovery strategy.

Query: {query}
Error: {error}
Retrieval attempts: {attempts}

Recovery options:
1. RETRY: Transient error, retry same query
2. REWRITE: Query may be malformed, rewrite it
3. FALLBACK: Use alternative data source
4. DIRECT: Answer from LLM knowledge if possible
5. CLARIFY: Ask user for clarification

Respond with JSON:
{
  "recovery_strategy": "<strategy>",
  "reasoning": "<why this strategy>",
  "rewritten_query": "<if strategy is REWRITE>",
  "fallback_source": "<if strategy is FALLBACK>",
  "clarification_question": "<if strategy is CLARIFY>"
}
```

### Insufficient Results Handler

```
Retrieved results are insufficient. Determine next action.

Question: {question}
Current query: {query}
Results found: {result_count}
Relevance scores: {scores}
Retries remaining: {retries}

Options:
1. Broaden the query
2. Try different keywords
3. Search web instead
4. Generate partial answer with caveat
5. Ask for clarification

Respond with JSON:
{
  "action": "<chosen action>",
  "new_query": "<if rewriting>",
  "partial_answer": "<if generating partial>",
  "reasoning": "<explanation>"
}
```

## 8. Orchestration Prompts

### Agent Selector

```
Select the best agent(s) to handle this query.

Query: {query}

Available agents:
- knowledge_agent: Internal documentation, product info
- web_agent: Current events, public information
- api_agent: User-specific data (email, calendar)
- code_agent: Code search, technical docs
- math_agent: Calculations, data analysis

Consider:
1. What type of information is needed?
2. Should multiple agents work in parallel?
3. Is there an optimal order of execution?

Respond with JSON:
{
  "selected_agents": ["<agent1>", "<agent2>"],
  "primary_agent": "<main agent>",
  "parallel_execution": true/false,
  "execution_order": ["<agent1>", "<agent2>"],
  "reasoning": "<explanation>"
}
```

### Result Aggregation

```
Aggregate results from multiple agents into a coherent response.

Question: {question}

Agent Results:
- knowledge_agent: {knowledge_result}
- web_agent: {web_result}
- api_agent: {api_result}

Instructions:
1. Combine relevant information from all agents
2. Resolve any conflicts (prefer more authoritative sources)
3. Maintain source attribution
4. Produce a unified, coherent answer

Aggregated Response:
```

## 9. Prompt Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{query}` | User's question | "What is RAG?" |
| `{question}` | Same as query | "What is RAG?" |
| `{context}` | Retrieved documents joined | "RAG is..." |
| `{documents}` | List of documents | "[Doc1, Doc2]" |
| `{document}` | Single document | "RAG stands for..." |
| `{answer}` | Generated answer | "RAG is a technique..." |
| `{original_query}` | Initial user query | "Explain RAG" |
| `{current_query}` | Possibly rewritten | "retrieval augmented generation explanation" |
| `{attempt}` | Current attempt number | 2 |
| `{retries}` | Remaining retries | 1 |
| `{query_history}` | Previous query attempts | ["q1", "q2"] |
| `{hop_count}` | Current retrieval hop | 2 |
| `{max_hops}` | Maximum allowed hops | 5 |
| `{scores}` | Relevance scores | [0.8, 0.6, 0.4] |
| `{error}` | Error message | "Connection timeout" |

## 10. Prompt Engineering Tips

### For Grading Prompts

- Use binary decisions when possible (yes/no)
- Provide clear criteria for each grade level
- Ask for reasoning before the decision
- Include edge cases in instructions

### For Rewriting Prompts

- Show what was tried before
- Explain why previous attempts failed
- Provide multiple strategy options
- Limit rewrite count to prevent loops

### For Generation Prompts

- Emphasize grounding in sources
- Request citations/attribution
- Handle insufficient context gracefully
- Be specific about format requirements

### For Verification Prompts

- Check each claim independently
- Distinguish supported vs inferred
- Require corrected version output
- Use structured JSON for parsing
