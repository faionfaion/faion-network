# LLM Prompts for Architecture Decisions

Prompts for using LLMs to assist with LLM architecture decisions.

## Prompt 1: Requirements Analysis

```
You are an ML architect helping to analyze requirements for an LLM-powered system.

Given the following system description:
<system_description>
{description}
</system_description>

Analyze and extract:

1. **Data Requirements**
   - What data sources are needed?
   - How often does data change?
   - What is the data volume?
   - Are there privacy/compliance concerns?

2. **Performance Requirements**
   - What latency is acceptable?
   - What accuracy is required?
   - What is the expected query volume?
   - Is real-time response critical?

3. **Functional Requirements**
   - Are citations/sources needed?
   - What output format is required?
   - What reasoning complexity is involved?
   - Are there multi-turn conversation needs?

4. **Constraints**
   - Budget limitations?
   - Team expertise?
   - Timeline constraints?
   - Infrastructure constraints?

Output as a structured analysis with recommendations for the LLM enhancement approach (Prompt Engineering, RAG, Fine-tuning, or Hybrid).
```

## Prompt 2: Approach Recommendation

```
You are an ML architect specializing in LLM systems.

Given these requirements:
<requirements>
- Data freshness: {freshness}
- Data volume: {volume}
- Latency requirement: {latency}
- Accuracy requirement: {accuracy}
- Citations needed: {citations}
- Budget: {budget}
- Team expertise: {expertise}
- Timeline: {timeline}
</requirements>

Recommend the optimal LLM enhancement approach:

1. **Primary Recommendation**: [Prompt Engineering | RAG | Fine-tuning | RAFT]
   - Explain why this is the best fit
   - List key benefits for this use case

2. **Alternative Consideration**: [Second-best option]
   - When to consider this instead
   - Trade-offs vs primary recommendation

3. **Implementation Outline**:
   - Key components needed
   - Estimated complexity
   - Critical success factors

4. **Risks and Mitigations**:
   - Top 3 risks with this approach
   - Mitigation strategies

5. **Cost-Benefit Analysis**:
   - Setup investment
   - Operational costs
   - Expected ROI timeline
```

## Prompt 3: RAG Architecture Design

```
You are a senior ML engineer designing RAG systems.

Design a RAG architecture for:
<use_case>
{description}
</use_case>

Data sources:
{data_sources}

Requirements:
- Latency: {latency}
- Accuracy: {accuracy}
- Scale: {scale}

Provide a complete RAG architecture including:

1. **Ingestion Pipeline**
   - Document processing strategy
   - Chunking approach (size, overlap, method)
   - Metadata extraction

2. **Embedding Strategy**
   - Recommended embedding model
   - Dimensionality considerations
   - Batch processing approach

3. **Vector Database Selection**
   - Recommended database with rationale
   - Index configuration
   - Scaling considerations

4. **Retrieval Strategy**
   - Search method (vector, hybrid, multi-stage)
   - Top-k and filtering approach
   - Reranking strategy

5. **Generation Configuration**
   - LLM selection
   - Prompt template
   - Context window management

6. **Production Considerations**
   - Caching strategy
   - Fallback handling
   - Monitoring and evaluation

Output as a technical specification document.
```

## Prompt 4: Fine-tuning Feasibility

```
You are an ML engineer evaluating fine-tuning feasibility.

Evaluate whether fine-tuning is appropriate for:
<use_case>
{description}
</use_case>

Available data:
- Dataset size: {size}
- Data quality: {quality}
- Data format: {format}

Analyze:

1. **Data Sufficiency**
   - Is the dataset size adequate? (minimum recommendations)
   - Is the data quality sufficient?
   - What data augmentation might help?

2. **Fine-tuning Approach**
   - Recommended method (SFT, LoRA, QLoRA, DPO)
   - Base model selection
   - Hyperparameter recommendations

3. **Alternative Analysis**
   - Could prompt engineering achieve similar results?
   - Would RAG be more appropriate?
   - Cost-benefit comparison

4. **Implementation Plan**
   - Data preparation steps
   - Training infrastructure needs
   - Evaluation strategy

5. **Risk Assessment**
   - Overfitting risks
   - Maintenance burden
   - Knowledge cutoff concerns

Conclude with a clear recommendation: Fine-tune / Don't fine-tune / Hybrid approach
```

## Prompt 5: Cost Optimization Analysis

```
You are an ML cost optimization specialist.

Current LLM system:
<current_system>
{system_description}
</current_system>

Current costs:
- LLM API: ${llm_cost}/month
- Infrastructure: ${infra_cost}/month
- Other: ${other_cost}/month

Query patterns:
- Volume: {volume}/day
- Avg input tokens: {input_tokens}
- Avg output tokens: {output_tokens}
- Cache hit rate: {cache_rate}%

Analyze cost optimization opportunities:

1. **Model Optimization**
   - Could a smaller model handle some queries?
   - Model routing strategy
   - Batch processing opportunities

2. **Caching Strategy**
   - Semantic caching potential
   - Query deduplication
   - Response caching

3. **Prompt Optimization**
   - Token reduction techniques
   - System prompt optimization
   - Few-shot example optimization

4. **Infrastructure Optimization**
   - Right-sizing recommendations
   - Reserved capacity benefits
   - Self-hosting considerations

5. **Cost Projections**
   | Optimization | Current | Optimized | Savings |
   |--------------|---------|-----------|---------|
   | [Category]   | $X      | $X        | $X      |

6. **Implementation Priority**
   - Quick wins (< 1 week)
   - Medium-term (1-4 weeks)
   - Strategic (1-3 months)

Provide specific, actionable recommendations with estimated savings.
```

## Prompt 6: Architecture Review

```
You are a senior ML architect reviewing an LLM system design.

Review this architecture:
<architecture>
{architecture_description}
</architecture>

Evaluate against these criteria:

1. **Correctness**
   - Does the architecture meet stated requirements?
   - Are there logical gaps or inconsistencies?

2. **Scalability**
   - Will it handle projected load?
   - What are the bottlenecks?
   - Horizontal vs vertical scaling approach

3. **Reliability**
   - Failure modes and handling
   - Fallback strategies
   - Data consistency

4. **Performance**
   - Latency analysis
   - Throughput considerations
   - Optimization opportunities

5. **Cost Efficiency**
   - Cost drivers identification
   - Optimization opportunities
   - TCO analysis

6. **Maintainability**
   - Operational complexity
   - Monitoring and debugging
   - Update and retraining strategy

7. **Security**
   - Data privacy considerations
   - Access control
   - Audit requirements

Provide:
- Overall assessment (1-5 rating)
- Critical issues (must fix)
- Recommendations (should fix)
- Nice-to-haves (could improve)
```

## Prompt 7: Migration Planning

```
You are an ML engineer planning a migration between LLM approaches.

Current state:
<current>
{current_approach}
</current>

Target state:
<target>
{target_approach}
</target>

Motivation:
{motivation}

Create a migration plan:

1. **Gap Analysis**
   - What's missing in current approach?
   - What new components are needed?
   - What can be reused?

2. **Risk Assessment**
   - Migration risks
   - Rollback strategy
   - Data migration concerns

3. **Phased Migration Plan**

   Phase 1: [Preparation]
   - Tasks and duration
   - Dependencies
   - Success criteria

   Phase 2: [Parallel Running]
   - Shadow mode testing
   - Performance comparison
   - Gradual traffic shift

   Phase 3: [Cutover]
   - Full migration
   - Monitoring
   - Cleanup

4. **Resource Requirements**
   - Team effort
   - Infrastructure needs
   - Timeline estimate

5. **Success Metrics**
   - How to measure successful migration?
   - Acceptance criteria
   - Rollback triggers
```

## Prompt 8: Evaluation Framework Design

```
You are an ML evaluation specialist.

Design an evaluation framework for:
<system>
{system_description}
</system>

Requirements:
- Primary use case: {use_case}
- Critical metrics: {metrics}
- Evaluation frequency: {frequency}

Create a comprehensive evaluation framework:

1. **Metric Definitions**

   | Metric | Definition | Target | Measurement Method |
   |--------|------------|--------|-------------------|
   | [Metric 1] | [How calculated] | [Target value] | [How measured] |

2. **Automated Evaluation**
   - LLM-as-judge prompts for quality assessment
   - Automated accuracy checks
   - Format compliance validation

3. **Human Evaluation Protocol**
   - Sampling strategy
   - Evaluation criteria
   - Inter-rater reliability

4. **Benchmark Suite**
   - Standard test cases
   - Edge cases
   - Regression tests

5. **Continuous Monitoring**
   - Real-time metrics
   - Alerting thresholds
   - Drift detection

6. **Reporting Template**
   - Dashboard components
   - Report frequency
   - Stakeholder communication

Provide implementation details including specific prompts for LLM-as-judge evaluations.
```

---

## Usage Guidelines

1. **Customize placeholders:** Replace `{placeholder}` with actual values
2. **Iterate on outputs:** Use follow-up prompts to refine recommendations
3. **Validate with experts:** LLM suggestions should be reviewed by ML engineers
4. **Document decisions:** Capture LLM-assisted analysis in ADRs

---

*LLM Prompts for Architecture Decisions v2.0*
