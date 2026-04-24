# Interview Methods

Structured interviewing, behavioral questions, scorecards, assessments.

---

## Interviewing & Selection Methodologies

### structured-interview-design

**Problem:** Inconsistent, biased interviews.

**Framework:**
| Component | Implementation |
|-----------|----------------|
| Competencies | 4-6 key skills for role |
| Questions | Same questions for all candidates |
| Scoring | 1-5 scale with rubric |
| Panel | Multiple interviewers |
| Debrief | Structured discussion |

**Agent:** faion-recruiter-agent

### star-interview-method

**Problem:** Vague, unhelpful interview answers.

**Framework:**
| Component | Prompt |
|-----------|--------|
| **S**ituation | "Tell me about a time when..." |
| **T**ask | "What was your responsibility?" |
| **A**ction | "What did you do?" |
| **R**esult | "What was the outcome?" |

**Follow-ups:**
- "What would you do differently?"
- "What did you learn?"

**Agent:** faion-recruiter-agent

### behavioral-interview-questions

**Problem:** Wrong questions, wrong hires.

**Framework by competency:**
| Competency | Question |
|------------|----------|
| Leadership | "Tell me about leading a team through change" |
| Problem-solving | "Describe solving a complex problem" |
| Collaboration | "Give an example of cross-functional work" |
| Communication | "Describe delivering difficult feedback" |
| Adaptability | "Tell me about adjusting to major change" |

**Agent:** faion-recruiter-agent

### interview-scorecard

**Problem:** Subjective, undocumented evaluations.

**Framework:**
```markdown
## Interview Scorecard: [Candidate] - [Role]

### Competency Ratings (1-5)
| Competency | Score | Notes |
|------------|-------|-------|
| Technical skills | 4 | Strong Python, weak SQL |
| Communication | 5 | Articulate, clear examples |
| Problem-solving | 3 | Needed prompting |
| Culture fit | 4 | Values aligned |

### Overall: Hire / No Hire / Maybe

### Key Strengths:
### Areas of Concern:
### Questions for Next Round:
```

**Agent:** faion-recruiter-agent

### technical-assessment-design

**Problem:** Can't verify technical skills.

**Framework:**
| Type | Best For |
|------|----------|
| Take-home project | Deep evaluation, async |
| Live coding | Problem-solving, thinking |
| Code review | Real-world skills |
| System design | Senior roles |
| Pair programming | Collaboration |

**Best practices:**
- Time-box (2-4 hours max)
- Real-world scenarios
- Clear evaluation criteria
- Compensate candidate time

**Agent:** faion-recruiter-agent

### culture-fit-assessment

**Problem:** Technical match, culture mismatch.

**Framework:**
| Approach | Implementation |
|----------|----------------|
| Values interview | Questions on values alignment |
| Team lunch/coffee | Informal culture assessment |
| Work simulation | Day-in-the-life scenario |
| Reference questions | "How did they handle X?" |

**Warning:** "Culture fit" ≠ "like us". Focus on values, not personality.

**Agent:** faion-recruiter-agent

### reference-check-framework

**Problem:** References don't reveal real performance.

**Framework:**
| Question | Purpose |
|----------|---------|
| "What was their role?" | Verify claims |
| "What did they excel at?" | Strengths |
| "Where could they improve?" | Development areas |
| "How did they handle pressure?" | Stress response |
| "Would you rehire them?" | Ultimate question |

**Agent:** faion-recruiter-agent

### interviewer-training

**Problem:** Interviewers introduce bias.

**Framework:**
| Topic | Training Content |
|-------|-----------------|
| Structured interviews | Why and how |
| Bias awareness | Common biases to avoid |
| Legal compliance | What you can't ask |
| Evaluation | Using scorecards |
| Candidate experience | Creating positive interaction |

**Agent:** faion-recruiter-agent

### hiring-committee-debrief

**Problem:** Loudest voice wins hiring decision.

**Framework:**
1. Submit scorecards before debrief
2. No discussion until all submitted
3. Review discrepancies first
4. Focus on evidence, not impressions
5. Decide: Hire / No hire / More info needed

**Agent:** faion-recruiter-agent

---

*Interview Methods Methodologies | faion-hr-recruiter*

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Format job description, update HRIS data, send offer | haiku | Content formatting and data updates |
| Evaluate resume fit for role requirements | sonnet | Assessment and analysis |
| Provide STAR interview feedback on candidates | sonnet | Qualitative evaluation and scoring |
| Design interview process and rubrics | opus | Systematic process design |
| Create onboarding program for new team | sonnet | Planning and documentation |
| Plan compensation strategy and salary bands | opus | Complex organizational decisions |
| Analyze retention data and recommend interventions | sonnet | Data analysis and recommendations |

---

## Sources

- [Google re:Work Structured Interviewing](https://rework.withgoogle.com/guides/hiring-use-structured-interviewing/steps/introduction/)
- [SHRM Interview Guide](https://www.shrm.org/topics-tools/tools/toolkits/conducting-effective-interviews)
- [Harvard Business Review Interview Techniques](https://hbr.org/topic/subject/interviewing)
