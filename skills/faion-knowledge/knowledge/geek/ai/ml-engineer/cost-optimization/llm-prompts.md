# LLM Prompts for Cost Optimization

Prompts for analyzing, auditing, and optimizing LLM costs.

## Cost Audit Prompts

### Analyze Cost Report

```
Analyze this LLM cost report and provide optimization recommendations:

<cost_report>
{{COST_REPORT_JSON}}
</cost_report>

Evaluate:
1. Model distribution - are expensive models overused?
2. Cache hit rate - is caching effective?
3. Token efficiency - input vs output ratio
4. Cost per feature - which features are most expensive?
5. Anomalies - any unexpected patterns?

Provide:
- Top 3 cost reduction opportunities with estimated savings
- Risk assessment for each recommendation
- Implementation priority (quick wins vs long-term)

Format as structured analysis with tables where appropriate.
```

### Identify Routing Opportunities

```
Review these LLM requests and identify routing optimization opportunities:

<requests>
{{SAMPLE_REQUESTS}}
</requests>

For each request type, recommend:
1. Current model used
2. Recommended model (cheapest that maintains quality)
3. Estimated cost reduction percentage
4. Quality risk assessment (low/medium/high)

Output as a routing rules table:
| Request Pattern | Current | Recommended | Savings | Risk |
```

### Prompt Efficiency Analysis

```
Analyze these prompts for token efficiency:

<prompts>
{{PROMPTS}}
</prompts>

For each prompt:
1. Current token count
2. Optimization suggestions (remove filler, compress, restructure)
3. Optimized version
4. Estimated token reduction

Focus on:
- Removing unnecessary politeness phrases
- Condensing verbose instructions
- Using structured formats
- Eliminating redundant context

Maintain semantic meaning while reducing tokens.
```

## Optimization Prompts

### Generate Compressed System Prompt

```
Compress this system prompt while preserving all essential instructions:

<original>
{{SYSTEM_PROMPT}}
</original>

Requirements:
- Preserve all behavioral instructions
- Maintain output format requirements
- Keep critical constraints
- Remove filler phrases and redundancy
- Target 50% token reduction

Output:
1. Compressed prompt
2. Token count comparison (before/after)
3. List of removed elements (verify none are critical)
```

### Create Model Routing Classifier

```
Based on these example queries and their ideal model assignments:

<examples>
{{QUERY_MODEL_PAIRS}}
</examples>

Generate:
1. Classification rules as regex patterns
2. Keyword lists for each complexity tier
3. Python code for a classify_complexity() function
4. Edge cases to watch for

Target routing distribution:
- Simple (nano): 40% of requests
- Medium (mini): 50% of requests
- Complex (full): 10% of requests
```

### Design Caching Strategy

```
Design a caching strategy for this LLM application:

<application_description>
{{APP_DESCRIPTION}}
</application_description>

<request_patterns>
{{COMMON_REQUEST_TYPES}}
</request_patterns>

Determine for each request type:
1. Cacheable: yes/no
2. Cache key components
3. Recommended TTL
4. Invalidation triggers
5. Expected hit rate

Output a caching configuration with:
- Cache key generation logic
- TTL by request type
- Estimated cost savings
- Memory/Redis storage estimates
```

## Monitoring Prompts

### Anomaly Detection Analysis

```
Analyze this cost time series for anomalies:

<metrics>
{{DAILY_COSTS_ARRAY}}
</metrics>

Identify:
1. Sudden spikes (>2x normal)
2. Gradual increases (trending up)
3. Unusual patterns (weekday vs weekend)
4. Correlation with request volume

For each anomaly:
- Timestamp/period
- Magnitude
- Possible causes
- Recommended investigation steps
```

### Generate Cost Forecast

```
Based on this historical cost data:

<history>
{{MONTHLY_COSTS}}
</history>

<growth_factors>
- Expected traffic growth: {{TRAFFIC_GROWTH}}%
- New features planned: {{FEATURES}}
- Model price changes: {{PRICE_CHANGES}}
</growth_factors>

Forecast:
1. Next month projected cost
2. Next quarter projected cost
3. Cost if no optimization
4. Cost with recommended optimizations
5. Break-even analysis for optimization investment
```

## Code Generation Prompts

### Generate Cost Tracker

```
Generate a production-ready cost tracking module for {{LANGUAGE}} with:

Requirements:
- Real-time cost calculation per request
- Aggregation by model, feature, user
- Budget limit enforcement
- Prometheus metrics export
- Thread-safe operations

Include:
- Main CostTracker class
- Pricing configuration
- Metrics exporter
- Budget alert system
- Unit tests

Use current 2025 pricing for OpenAI and Anthropic models.
```

### Generate Caching Layer

```
Create a multi-tier caching layer for LLM responses:

Stack:
- L1: In-memory LRU cache
- L2: Redis with TTL
- L3: Optional S3 for long-term

Features needed:
- Semantic similarity matching (optional)
- Cache warming from logs
- Automatic invalidation
- Hit rate metrics
- Configurable TTL by model

Language: {{LANGUAGE}}
Framework: {{FRAMEWORK}}
```

### Generate Batch Processor

```
Create an async batch processor for LLM requests:

Requirements:
- Configurable batch size
- Concurrent request limit
- Rate limiting
- Progress callbacks
- Error handling with retries
- Support for OpenAI and Anthropic APIs

Interface:
```python
processor = BatchProcessor(config)
results = await processor.process(prompts, model="gpt-4.1-mini")
```

Include cancellation support and graceful shutdown.
```

## Analysis Prompts

### Compare Provider Costs

```
Compare costs across LLM providers for this workload:

<workload>
Monthly requests: {{REQUEST_COUNT}}
Average input tokens: {{AVG_INPUT}}
Average output tokens: {{AVG_OUTPUT}}
Required features: {{FEATURES}}
Latency requirement: {{LATENCY_MS}}ms
</workload>

Compare:
- OpenAI (GPT-4.1 family)
- Anthropic (Claude 4 family)
- Google (Gemini 2 family)
- Mistral

For each:
1. Monthly cost estimate
2. Best model for workload
3. Pros/cons
4. Migration effort if switching

Recommend optimal provider/model mix.
```

### ROI Analysis for Optimization

```
Calculate ROI for implementing these cost optimizations:

<current_state>
Monthly cost: ${{CURRENT_COST}}
Request volume: {{REQUESTS}}
Cache hit rate: {{CACHE_RATE}}%
Model distribution: {{MODEL_DIST}}
</current_state>

<proposed_optimizations>
{{OPTIMIZATIONS}}
</proposed_optimizations>

For each optimization calculate:
1. Implementation cost (engineering hours)
2. Monthly savings
3. Payback period
4. 12-month ROI
5. Risk factors

Prioritize by ROI and ease of implementation.
```

## Quick Reference Prompts

### Summarize Cost Report (Short)

```
Summarize this cost report in 3 bullet points:
<report>{{REPORT}}</report>

Focus on: total spend, biggest cost driver, top saving opportunity.
```

### Quick Prompt Compression

```
Compress, preserve meaning, target 50% reduction:
<prompt>{{PROMPT}}</prompt>
```

### Classify Request Complexity

```
Classify as SIMPLE/MEDIUM/COMPLEX:
<request>{{REQUEST}}</request>
Output only the classification.
```
