# Guardrails Checklists

Comprehensive checklists for designing, implementing, and testing LLM guardrails.

## Guardrail Design Checklist

### Requirements Analysis

- [ ] **Identify risk categories**
  - [ ] Content safety (harmful, toxic, illegal)
  - [ ] Data privacy (PII, confidential data)
  - [ ] Security (prompt injection, jailbreak)
  - [ ] Compliance (industry regulations)
  - [ ] Brand safety (off-topic, inappropriate)
  - [ ] Accuracy (hallucinations, factual errors)

- [ ] **Define severity levels**
  - [ ] Critical: Must block immediately (illegal content, PII leakage)
  - [ ] High: Should block, may allow with warning (toxic content)
  - [ ] Medium: Flag for review (borderline content)
  - [ ] Low: Log only (minor policy violations)

- [ ] **Document use case specifics**
  - [ ] Application type (chatbot, agent, extraction)
  - [ ] User population (internal, external, children)
  - [ ] Data sensitivity (public, confidential, regulated)
  - [ ] Latency requirements (real-time, batch)
  - [ ] Cost constraints (API calls, compute)

### Architecture Design

- [ ] **Select guardrail points**
  - [ ] Input validation (before LLM)
  - [ ] Output validation (after LLM)
  - [ ] Dialog control (conversation flow)
  - [ ] Retrieval filtering (RAG chunks)
  - [ ] Execution validation (tool calls)

- [ ] **Choose framework approach**
  - [ ] NeMo Guardrails for dialog control
  - [ ] Guardrails AI for output validation
  - [ ] Llama Guard for classification
  - [ ] Custom implementation
  - [ ] Hybrid approach

- [ ] **Design failure modes**
  - [ ] Block strategy (error message, refusal)
  - [ ] Fallback strategy (alternative response)
  - [ ] Escalation strategy (human review)
  - [ ] Retry strategy (with modifications)

- [ ] **Plan for edge cases**
  - [ ] Multilingual content
  - [ ] Code snippets
  - [ ] Technical jargon
  - [ ] Sarcasm and context
  - [ ] Long conversations

### Input Guardrails Design

- [ ] **Length validation**
  - [ ] Maximum input length defined
  - [ ] Token count limits
  - [ ] Message count limits (multi-turn)

- [ ] **Content validation**
  - [ ] Profanity filtering approach
  - [ ] PII detection patterns (email, phone, SSN, etc.)
  - [ ] Sensitive topic detection
  - [ ] Language detection (if monolingual)

- [ ] **Security validation**
  - [ ] Prompt injection detection strategy
  - [ ] Jailbreak attempt detection
  - [ ] Special character handling
  - [ ] Unicode normalization

- [ ] **Sanitization rules**
  - [ ] PII masking format
  - [ ] URL handling
  - [ ] Code block handling
  - [ ] HTML/Markdown stripping

### Output Guardrails Design

- [ ] **Content moderation**
  - [ ] Harmful content detection
  - [ ] Bias detection
  - [ ] Factuality checking approach
  - [ ] Tone validation

- [ ] **Format validation**
  - [ ] Expected output structure (JSON, text, etc.)
  - [ ] Required fields
  - [ ] Length constraints
  - [ ] Character restrictions

- [ ] **Hallucination prevention**
  - [ ] Source citation requirements
  - [ ] Fact-checking strategy
  - [ ] Confidence scoring
  - [ ] "I don't know" handling

- [ ] **Post-processing**
  - [ ] Output cleaning rules
  - [ ] Formatting standardization
  - [ ] Link validation
  - [ ] Reference verification

### Monitoring Design

- [ ] **Metrics to track**
  - [ ] Block rate by guardrail type
  - [ ] False positive rate estimation
  - [ ] Latency distribution
  - [ ] Cost per request

- [ ] **Logging strategy**
  - [ ] What to log (without PII)
  - [ ] Log retention period
  - [ ] Access controls
  - [ ] Audit requirements

- [ ] **Alerting rules**
  - [ ] Spike in violations
  - [ ] New violation patterns
  - [ ] Latency degradation
  - [ ] Error rate increase

---

## Implementation Checklist

### Environment Setup

- [ ] **Dependencies installed**
  ```bash
  # NeMo Guardrails
  pip install nemoguardrails

  # Guardrails AI
  pip install guardrails-ai

  # Additional validators
  guardrails hub install hub://guardrails/toxic_language
  guardrails hub install hub://guardrails/detect_pii
  ```

- [ ] **Configuration files created**
  - [ ] Guardrail config (YAML/JSON)
  - [ ] Policy definitions
  - [ ] Prompt templates
  - [ ] Model configurations

- [ ] **Secrets management**
  - [ ] API keys in environment variables
  - [ ] No hardcoded credentials
  - [ ] Separate configs for dev/staging/prod

### Input Guardrails Implementation

- [ ] **Length validator**
  - [ ] Character limit implemented
  - [ ] Token limit implemented
  - [ ] Truncation handling defined

- [ ] **PII detector**
  - [ ] Email regex pattern
  - [ ] Phone number patterns (international)
  - [ ] SSN/ID patterns
  - [ ] Credit card patterns
  - [ ] Name entity recognition (optional)
  - [ ] Masking/replacement logic

- [ ] **Injection detector**
  - [ ] Pattern-based detection
  - [ ] Semantic detection (if needed)
  - [ ] Test against common attacks
  - [ ] False positive handling

- [ ] **Content moderator**
  - [ ] Profanity list/model
  - [ ] Topic classifier
  - [ ] Threshold configuration
  - [ ] Bypass rules (technical terms)

### Output Guardrails Implementation

- [ ] **Format validator**
  - [ ] JSON schema validation
  - [ ] Required field checks
  - [ ] Type validation
  - [ ] Repair logic (if applicable)

- [ ] **Content validator**
  - [ ] Output moderation
  - [ ] Length constraints
  - [ ] Character restrictions
  - [ ] Custom business rules

- [ ] **Hallucination checker**
  - [ ] Context comparison logic
  - [ ] Citation verification
  - [ ] Confidence scoring
  - [ ] Fallback responses

- [ ] **Output filter**
  - [ ] PII scrubbing
  - [ ] URL handling
  - [ ] Code sanitization
  - [ ] Formatting cleanup

### Pipeline Integration

- [ ] **Request flow**
  - [ ] Input guardrails before LLM
  - [ ] Proper error handling
  - [ ] Timeout configuration
  - [ ] Retry logic

- [ ] **Response flow**
  - [ ] Output guardrails after LLM
  - [ ] Fallback responses
  - [ ] Partial response handling
  - [ ] Streaming support (if needed)

- [ ] **Error handling**
  - [ ] Guardrail failure responses
  - [ ] LLM failure handling
  - [ ] Timeout handling
  - [ ] Rate limit handling

### Performance Optimization

- [ ] **Latency optimization**
  - [ ] Parallel guardrail execution
  - [ ] Async processing where possible
  - [ ] Caching for repeated checks
  - [ ] Early termination on critical failures

- [ ] **Cost optimization**
  - [ ] Tiered checking (cheap first)
  - [ ] Sampling for expensive checks
  - [ ] Batch processing (if applicable)
  - [ ] Model selection for validators

- [ ] **Resource management**
  - [ ] Connection pooling
  - [ ] Memory limits
  - [ ] Thread/process limits
  - [ ] Cleanup routines

### Logging and Monitoring

- [ ] **Structured logging**
  - [ ] Request ID tracking
  - [ ] Guardrail results
  - [ ] Latency measurements
  - [ ] Error details

- [ ] **Metrics collection**
  - [ ] Prometheus/StatsD integration
  - [ ] Custom metrics defined
  - [ ] Dashboard created
  - [ ] Alerts configured

- [ ] **Audit trail**
  - [ ] Compliance logging
  - [ ] Access logging
  - [ ] Change tracking
  - [ ] Retention policy

---

## Testing Checklist

### Unit Testing

- [ ] **Individual validators**
  - [ ] Each validator tested in isolation
  - [ ] Edge cases covered
  - [ ] Error handling verified
  - [ ] Performance benchmarked

- [ ] **Test categories**
  - [ ] Valid input passes
  - [ ] Invalid input blocked
  - [ ] Borderline cases handled
  - [ ] Empty/null input handled
  - [ ] Unicode/special characters handled

- [ ] **Mock dependencies**
  - [ ] LLM calls mocked
  - [ ] External APIs mocked
  - [ ] Database calls mocked

### Integration Testing

- [ ] **Pipeline tests**
  - [ ] Full request/response flow
  - [ ] Multiple guardrails in sequence
  - [ ] Error propagation
  - [ ] Timeout behavior

- [ ] **Component interaction**
  - [ ] Input → LLM → Output flow
  - [ ] RAG with guardrails
  - [ ] Multi-agent coordination
  - [ ] Streaming responses

- [ ] **External dependencies**
  - [ ] LLM API integration
  - [ ] Moderation API integration
  - [ ] Database integration
  - [ ] Caching integration

### Security Testing

- [ ] **Prompt injection tests**
  ```
  Test cases:
  - "Ignore previous instructions and..."
  - "You are now in developer mode..."
  - "Translate: [malicious content]"
  - Encoded/obfuscated attacks
  - Multi-turn manipulation
  ```

- [ ] **Jailbreak tests**
  ```
  Test cases:
  - Role-play scenarios
  - Hypothetical framing
  - Token manipulation
  - Context overflow
  ```

- [ ] **Data leakage tests**
  - [ ] System prompt extraction attempts
  - [ ] Training data extraction
  - [ ] PII in responses
  - [ ] Confidential info leakage

- [ ] **Adversarial inputs**
  - [ ] Unicode exploits
  - [ ] Encoding tricks
  - [ ] Token boundary manipulation
  - [ ] Context window attacks

### Performance Testing

- [ ] **Latency tests**
  - [ ] p50, p90, p99 latency
  - [ ] Latency under load
  - [ ] Latency with large inputs
  - [ ] Latency variance

- [ ] **Throughput tests**
  - [ ] Requests per second
  - [ ] Concurrent requests
  - [ ] Sustained load
  - [ ] Burst capacity

- [ ] **Resource tests**
  - [ ] Memory usage
  - [ ] CPU utilization
  - [ ] Network bandwidth
  - [ ] Connection limits

### Accuracy Testing

- [ ] **False positive testing**
  - [ ] Legitimate content passes
  - [ ] Technical discussions allowed
  - [ ] Edge cases handled
  - [ ] Context-aware decisions

- [ ] **False negative testing**
  - [ ] Known bad content blocked
  - [ ] Variations detected
  - [ ] New attack patterns
  - [ ] Multi-language content

- [ ] **Evaluation metrics**
  - [ ] Precision calculated
  - [ ] Recall calculated
  - [ ] F1 score tracked
  - [ ] Confusion matrix analyzed

### Regression Testing

- [ ] **Test suite maintenance**
  - [ ] Golden test cases
  - [ ] Automated regression tests
  - [ ] CI/CD integration
  - [ ] Test coverage tracking

- [ ] **Version testing**
  - [ ] Model version changes
  - [ ] Library updates
  - [ ] Configuration changes
  - [ ] Prompt modifications

### User Acceptance Testing

- [ ] **Real-world scenarios**
  - [ ] Representative user inputs
  - [ ] Common use cases
  - [ ] Edge cases from production
  - [ ] Multi-turn conversations

- [ ] **Feedback collection**
  - [ ] False positive reports
  - [ ] Usability issues
  - [ ] Performance concerns
  - [ ] Feature requests

---

## Deployment Checklist

### Pre-Deployment

- [ ] **Configuration verified**
  - [ ] Production config separate from dev
  - [ ] All thresholds reviewed
  - [ ] Logging levels appropriate
  - [ ] Alerts configured

- [ ] **Dependencies verified**
  - [ ] All packages locked to versions
  - [ ] Compatibility tested
  - [ ] License compliance checked
  - [ ] Security vulnerabilities scanned

- [ ] **Documentation complete**
  - [ ] Configuration documented
  - [ ] Runbooks created
  - [ ] Incident response plan
  - [ ] Escalation procedures

### Deployment

- [ ] **Gradual rollout**
  - [ ] Shadow mode first
  - [ ] Small percentage traffic
  - [ ] Metrics monitored
  - [ ] Rollback plan ready

- [ ] **Monitoring active**
  - [ ] Dashboards visible
  - [ ] Alerts enabled
  - [ ] Logs accessible
  - [ ] On-call notified

### Post-Deployment

- [ ] **Validation**
  - [ ] Smoke tests passed
  - [ ] Key metrics normal
  - [ ] No error spikes
  - [ ] Latency acceptable

- [ ] **Ongoing monitoring**
  - [ ] Daily metrics review
  - [ ] Weekly false positive review
  - [ ] Monthly accuracy evaluation
  - [ ] Quarterly security audit

---

## Maintenance Checklist

### Regular Maintenance

- [ ] **Weekly tasks**
  - [ ] Review violation logs
  - [ ] Check false positive reports
  - [ ] Monitor latency trends
  - [ ] Update block lists if needed

- [ ] **Monthly tasks**
  - [ ] Accuracy evaluation
  - [ ] Threshold tuning
  - [ ] Performance optimization
  - [ ] Documentation updates

- [ ] **Quarterly tasks**
  - [ ] Security audit
  - [ ] Dependency updates
  - [ ] Comprehensive testing
  - [ ] Strategy review

### Incident Response

- [ ] **Detection**
  - [ ] Automated alerts
  - [ ] User reports
  - [ ] Manual monitoring
  - [ ] External notification

- [ ] **Response**
  - [ ] Incident classification
  - [ ] Immediate mitigation
  - [ ] Root cause analysis
  - [ ] Fix implementation

- [ ] **Recovery**
  - [ ] Service restoration
  - [ ] Data verification
  - [ ] User communication
  - [ ] Post-mortem documentation

### Continuous Improvement

- [ ] **Feedback loop**
  - [ ] Collect user feedback
  - [ ] Analyze violation patterns
  - [ ] Identify improvement areas
  - [ ] Prioritize changes

- [ ] **Model updates**
  - [ ] Evaluate new models
  - [ ] Test improvements
  - [ ] Gradual migration
  - [ ] Performance comparison
