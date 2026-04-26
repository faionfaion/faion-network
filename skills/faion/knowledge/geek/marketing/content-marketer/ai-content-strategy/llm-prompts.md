# AI Content Strategy - LLM Prompts

## Content Differentiation Analysis Prompt

```markdown
# Evaluate Content Differentiation

You are evaluating whether a piece of content is differentiated or generic.
Analyze the content below and provide specific feedback.

## Content to Analyze
[INSERT CONTENT HERE]

## Analysis Framework

1. **Generic Signals** (Rate 1-10: Higher = more generic)
   - Aggregates top 10 search results without new insights
   - "Best practices" language without specific examples
   - No data, statistics, or original research
   - No author experience or perspective
   - No contrarian viewpoint

2. **Differentiation Signals** (Rate 1-10: Higher = more differentiated)
   - Contains proprietary data or research
   - Shares first-hand experience or failures
   - Includes expert interviews or quotes
   - Takes a specific stance or opinion
   - Provides specific examples with outcomes
   - Reveals what doesn't work

## Evaluation
- Generic score: ___ / 10
- Differentiation score: ___ / 10
- E-E-A-T signals present: [ ] None [ ] Some [ ] Strong

## Recommendations
1. What makes this differentiated?
2. What generic elements to remove?
3. Specific additions to increase differentiation
4. E-E-A-T signals to add

## Verdict
[ ] Publish as-is (strong differentiation)
[ ] Revise (add specific elements below)
[ ] Reject (too generic, start over)
```

## E-E-A-T Enhancement Prompt

```markdown
# Add E-E-A-T to Content

You are enhancing content with E-E-A-T signals to improve Google ranking potential.

## Original Content
[INSERT CONTENT HERE]

## Task
Suggest specific additions for each E-E-A-T signal:

### Experience
- Author experience: "In my [years] years of [role]..."
- Audience experience: "When we tested this with [customers]..."
- Real-world testing: "We measured [specific metric]..."

### Expertise
- Credentials: "As a [credential/background]..."
- Methodology: "We used [specific framework/process]..."
- Research: "Our research across [sample size]..."

### Authoritativeness
- Industry recognition: "Recognized by [authority]..."
- Original research: "Our proprietary data shows..."
- Supporting sources: "As [Authority] confirmed..."

### Trustworthiness
- Transparency: "Our methodology: [details]..."
- Limitations: "This doesn't work for [specific cases]..."
- Honesty: "What we got wrong: [failure]..."

## Output
For each section: Suggest 2-3 specific additions that feel natural and authentic.
```

## AI + Human Collaboration Workflow Prompt

```markdown
# Design Content for AI + Human Collaboration

You are designing a content brief that optimizes for AI strengths and human oversight.

## Content Topic
[TOPIC]

## Task
Create a detailed brief that shows:

1. **What AI Will Do**
   - Research phase: [specific tasks]
   - Initial draft: [specific approach]
   - Optimization: [specific tools]

2. **What Human Will Add**
   - Experience/cases: [specific types]
   - Data/insights: [proprietary elements]
   - Voice/opinion: [specific stance]
   - QA/verification: [specific checks]

3. **Workflow Design**
   - Stage 1: AI research
   - Stage 2: Human review & expansion
   - Stage 3: AI first draft
   - Stage 4: Human edit for brand voice
   - Stage 5: AI optimization
   - Stage 6: Human final QA

4. **Differentiation Strategy**
   - Proprietary data to include: ___
   - Expert perspectives: ___
   - First-hand examples: ___
   - Contrarian elements: ___

5. **E-E-A-T Integration**
   - Experience signals: ___
   - Expertise signals: ___
   - Authority signals: ___
   - Trust signals: ___

## Output Format
Detailed workflow with specific prompts for each AI task.
```

## Content Repurposing Prompt

```markdown
# Generate Multi-Channel Content Variations

You are creating variations of core content for different platforms/formats.

## Core Content Topic
[TOPIC/TITLE]

## Core Content Summary
[BRIEF SUMMARY OF KEY POINTS]

## Task
Create variations for each format:

### 1. LinkedIn Article (400 words)
- Target: C-level professionals
- Tone: Professional, authoritative
- Include: 3 key insights, 1 data point
- CTA: [Link to blog]

### 2. Twitter Thread (8 tweets)
- Format: 1 insight per tweet
- Include: Statistics, questions to engage
- CTA: "Thread about [topic]"

### 3. Email Newsletter (250 words)
- Subject line: Curiosity hook
- Opening: Personal relevance
- Include: 1-2 key insights
- CTA: "Read full post"

### 4. TikTok/Short Video Script (90 seconds)
- Hook: First 3 seconds critical
- Visuals: Describe key moments
- Include: 2-3 key points
- CTA: "Link in bio"

### 5. Podcast Talking Points (5 minutes)
- Introduction: Context setting
- Main points: 3-4 key ideas
- Stories: Specific examples
- Closing: Takeaways

## Output
Complete text/scripts for each format, ready to adapt.
```

## Content Brief Generation Prompt

```markdown
# Generate Content Brief for AI Content Creation

You are creating a detailed content brief for a blog post/article.

## Topic
[TOPIC]

## ICP Context
- Role: [Target role]
- Company size: [Size]
- Pain point: [Specific pain]
- Desired outcome: [Desired result]

## Task
Create a detailed brief including:

1. **Target Keyword & Intent**
   - Primary keyword: [keyword]
   - Search volume: [volume]
   - Intent: [Informational/Commercial/Transactional]
   - Secondary keywords: [keywords]

2. **Differentiation Angle**
   - Our perspective: [Unique angle]
   - Why we're different: [Specific reason]
   - Proprietary insight: [Insight to include]
   - Contrarian element: [Opinion to share]

3. **Content Outline**
   - H2: [Section]
     - H3: [Subsection]
     - Key point: [Point]
     - Needs data/example: [ ]
   - [Repeat for each section]

4. **Examples & Data**
   - Proprietary data: [Data to include]
   - Case study: [Case to share]
   - Expert quote: [Who to interview]
   - Real example: [Example to use]

5. **E-E-A-T Integration**
   - Experience: [Author experience to share]
   - Expertise: [Credentials/methodology]
   - Authority: [Research/sources]
   - Trust: [Transparency/limitations]

6. **Format & Publishing**
   - Length: [Word count]
   - Visuals: [Images/diagrams needed]
   - Internal links: [Existing posts to link]
   - CTA: [Call to action]

## Output
Comprehensive brief ready for AI draft generation.
```

## Competitive Content Analysis Prompt

```markdown
# Analyze Competitor Content & Find Gaps

You are analyzing competitor content to find differentiation opportunities.

## Competitors
1. [Competitor A]
2. [Competitor B]
3. [Competitor C]

## Topic
[Your topic]

## Task

### Top 3 Competitors Current Approach
For each competitor's top ranking article:
- Headline: [Headline]
- Main angle: [Angle]
- Strengths: [What they do well]
- Gaps: [What's missing]
- Outdated elements: [What's old]

### Aggregated Competitor Strategy
- Common themes: [Themes]
- Expected structure: [Structure]
- Typical depth: [Depth level]

### Opportunities for Differentiation
- Angle nobody covers: [Angle]
- Data nobody has: [Data you can provide]
- Perspective nobody takes: [Perspective]
- Format nobody uses: [Format]

### Our Content Strategy
- Our differentiation: [How we'll be different]
- Unique data/insight: [What only we know]
- Author perspective: [Our specific view]
- Enhanced E-E-A-T: [Our signals]

## Output
Detailed competitive analysis with specific differentiation recommendations.
```
