## Technical Debt Register: {Product}

### Summary
- **Total items:** {X}
- **High priority (score > 6):** {X}
- **Est. total fix effort:** {X} person-days
- **Last reviewed:** {Date}

---

#### TD-001: {Name}
**Type:** Deliberate / Accidental / Bit-rot / Design / Documentation / Test
**Created:** {Date}
**Location:** {file path or module/system}

**Description:**
{What the debt is — specific, not vague}

**Why it exists:**
{How it was created — ship-fast decision, learned better pattern, etc.}

**Impact:**
- Time tax: {X dev-hours per sprint slowed}
- Risk: {What could break if not addressed}
- Blocked work: {Features that cannot be built safely}

**Fix effort:** XS / S / M / L / XL
**Interest score (1-5):** {X}
**Contagion score (1-5):** {X}
**Alignment score (1-5):** {X — proximity to planned roadmap features}
**Priority score:** {(Interest x Alignment) / Effort}

**Fix approach:**
{Concrete approach — not "refactor", but what specific change}

**Related roadmap work:** {Upcoming feature that touches this code, or "none"}

---

#### TD-002: {Name}
{repeat pattern}
