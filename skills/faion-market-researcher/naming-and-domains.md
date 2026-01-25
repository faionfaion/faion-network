# Naming and Domain Methods

Reference for project naming and domain availability methodologies.

---

## Table of Contents

1. [project-naming](#project-naming)
2. [domain-availability](#domain-availability)

---

## project-naming

### Problem
Entrepreneurs struggle to find memorable, available names.

### Framework

**Naming Strategies:**

| Strategy | Description | Examples |
|----------|-------------|----------|
| **Descriptive** | What it does | Dropbox, YouTube |
| **Invented** | Made-up word | Spotify, Kodak |
| **Compound** | Two words combined | Facebook, Snapchat |
| **Metaphor** | Symbolic meaning | Amazon, Apple |
| **Portmanteau** | Blended words | Pinterest, Instagram |
| **Alliteration** | Same sound | PayPal, Coca-Cola |
| **Acronym** | Letters | IBM, NASA |

**Good Name Criteria:**
- Easy to spell
- Easy to pronounce
- Memorable
- Domain available (.com preferred)
- No trademark conflicts
- Works internationally

**Generation Process:**
1. Define brand attributes (3-5 adjectives)
2. List keywords (product, benefit, emotion)
3. Apply each strategy to keywords
4. Generate 20+ candidates
5. Check availability
6. Test with target audience

### Templates

**Naming Brief:**
```markdown
## Project: {Description}

### Brand Attributes
- {attribute 1}
- {attribute 2}
- {attribute 3}

### Keywords
- Product: {words}
- Benefits: {words}
- Emotions: {words}

### Name Candidates

| Name | Strategy | .com | Meaning |
|------|----------|------|---------|
| {name} | Descriptive | Y/N | {why} |
| {name} | Invented | Y/N | {why} |
| {name} | Compound | Y/N | {why} |

### Top 3 Recommendations
1. {name}: {reasoning}
2. {name}: {reasoning}
3. {name}: {reasoning}
```

### Examples

**Task Management Tool:**
- Attributes: Simple, fast, powerful
- Candidates: TaskFlow (compound), Tasko (invented), QuickTask (descriptive)
- Winner: TaskFlow (.com available, memorable)

### Agent
faion-research-agent (mode: names)

---

## domain-availability

### Problem
Great names are unusable due to domain/handle unavailability.

### Framework

**Check Priority:**

| Type | Priority | Importance |
|------|----------|------------|
| .com | 1 | Essential for credibility |
| .io | 2 | Acceptable for tech |
| .co | 3 | Alternative |
| GitHub | 1 | Essential for open source |
| Twitter/X | 2 | Important for marketing |
| LinkedIn | 3 | Nice to have |

**Availability Actions:**

| Status | Action |
|--------|--------|
| Available | Register immediately |
| Premium ($X) | Consider if <$5K |
| Taken (parked) | Check price, usually overpriced |
| Taken (active) | Move to next name |

**Alternative Strategies:**
- Add "get", "try", "use" prefix: getTaskFlow.com
- Add "app", "hq" suffix: taskflowhq.com
- Different TLD: taskflow.io
- Creative spelling: taskflw.com

### Templates

**Domain Check Report:**
```markdown
## Name: {name}

### Domain Availability

| Domain | Status | Price | Notes |
|--------|--------|-------|-------|
| {name}.com | Available | $12/yr | Register now |
| {name}.io | Taken | - | Active site |
| {name}.co | Premium | $2,500 | Parked |

### Social Handles

| Platform | Handle | Status |
|----------|--------|--------|
| Twitter | @{name} | Available |
| GitHub | {name} | Taken |
| LinkedIn | /company/{name} | Available |

### Trademark Check
- USPTO: No conflicts found
- Note: Not legal advice, consult attorney

### Recommendation
**Register {name}.com and @{name} immediately**

### Alternatives if Unavailable
1. get{name}.com
2. {name}app.com
3. {name}.io
```

### Examples

**TaskFlow Availability:**
- taskflow.com: Taken (active SaaS)
- gettaskflow.com: Available
- taskflow.io: Available
- @taskflow: Taken
- @gettaskflow: Available
- Recommendation: gettaskflow.com + @gettaskflow

### Agent
faion-domain-checker-agent

---

*Naming and Domain Methods Reference | 2 methodologies*
