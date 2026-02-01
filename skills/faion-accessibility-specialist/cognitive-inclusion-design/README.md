# Cognitive Inclusion Design

## Problem

Traditional accessibility focuses on visual/motor impairments. Cognitive disabilities (ADHD, autism, dyslexia, anxiety, learning disabilities) are often overlooked, affecting 15-20% of the population.

## Solution: Design for Cognitive Inclusion

### Cognitive Load Reduction

| Aspect | Challenge | Best Practice |
|--------|-----------|---------------|
| **Information structure** | Too much at once | Clear hierarchy, chunked content (5-7 items) |
| **Notifications** | Intrusive, overwhelming | Non-intrusive, user-controllable, pause option |
| **Navigation** | Unpredictable, complex | Predictable, consistent patterns, breadcrumbs |
| **Reading** | Small text, dense paragraphs | Dyslexia-friendly fonts, 1.5 line spacing, short paragraphs |
| **Focus** | Too many distractions | Distraction-free modes, focus indicators |
| **Time limits** | Stressful, exclusionary | Extended or eliminated, warnings |
| **Error messages** | Blame, unclear | Clear, non-blaming, actionable solutions |
| **Forms** | Long, complex | Break into steps, save progress, clear labels |

### ADHD-Friendly Design

**Characteristics:** Attention difficulties, impulsivity, distractibility, working memory challenges

**Design strategies:**

**Progress Indicators:**
```
Multi-step tasks need clear progress:
→ Step 1 of 5: Account details
→ Progress bar showing completion
→ Ability to bookmark and return
→ Auto-save all progress
```

**Auto-Save Functionality:**
- Save drafts automatically every 30 seconds
- "All changes saved" indicator
- Restore unsaved work on return
- No data loss from distraction

**Bookmark/Resume Capabilities:**
- "Save and continue later" button
- Email resume link
- Quick access to in-progress items
- Remember scroll position

**Reduced Motion Options:**
- Respect `prefers-reduced-motion`
- Disable auto-playing animations
- Pauseable carousels
- Static alternatives to animated content

**Focus Modes:**
- Hide non-essential UI elements
- Reduce notifications
- Minimize distractions
- "Do Not Disturb" option

### Autism-Friendly Design

**Characteristics:** Sensory sensitivities, preference for predictability, literal thinking, visual processing strengths

**Design strategies:**

**Predictable Interactions:**
- Consistent button placement
- Same action always same result
- No unexpected popups
- Clear cause and effect

**Clear Visual Boundaries:**
- Defined sections with borders
- Visual separation of content areas
- Clear start and end points
- Avoid cluttered layouts

**Literal Language:**
```
Avoid:
→ "Piece of cake" (unclear idiom)
→ "Click here" (where?)
→ "Think outside the box"

Use:
→ "This is easy"
→ "Submit your application"
→ "Consider alternative solutions"
```

**Sensory-Friendly Color Palettes:**
- Avoid overly bright colors
- Provide muted color options
- High contrast mode
- No harsh color combinations

**Transition Warnings:**
- "You will now leave this page"
- Countdown before auto-redirect
- Confirmation before destructive actions
- Clear navigation cues

### Dyslexia-Friendly Design

**Characteristics:** Reading difficulties, letter/word reversal, processing speed challenges

**Design strategies:**

**Font Selection:**
```
Recommended fonts:
→ OpenDyslexic (free, designed for dyslexia)
→ Comic Sans (surprisingly helpful)
→ Arial, Verdana (clean sans-serif)
→ Avoid serif fonts (harder to read)
→ Never use decorative fonts for body text
```

**Line Height and Spacing:**
```css
/* Dyslexia-friendly spacing */
body {
  line-height: 1.5; /* Minimum */
  letter-spacing: 0.12em;
  word-spacing: 0.16em;
}

p {
  margin-bottom: 2em; /* Space between paragraphs */
  max-width: 70ch; /* Optimal line length */
}
```

**Text Alignment:**
- Left-aligned text (never justified)
- Ragged right edge helps tracking
- Avoid center-aligned body text
- Consistent margins

**High Contrast Modes:**
- Black text on white background
- Or cream/beige backgrounds (easier on eyes)
- Avoid low contrast (gray on gray)
- User-selectable contrast levels

**Text-to-Speech Integration:**
- Built-in read-aloud functionality
- Highlight text as it's read
- Adjustable reading speed
- Pause and resume

### Anxiety-Friendly Design

**Characteristics:** Overwhelm from too many choices, fear of making mistakes, need for reassurance

**Design strategies:**

**Error Prevention:**
- Inline validation (immediate feedback)
- Clear field requirements upfront
- Undo functionality
- Confirmation before destructive actions

**Reassuring Feedback:**
```
Positive, clear messages:
→ "Great! Your email is valid"
→ "All changes saved"
→ "Your password is strong"
→ "No action needed right now"
```

**Progress Indicators:**
- Show how far through process
- Estimate time remaining
- "You're almost done!"
- Celebrate completion

**Clear Exit Points:**
- Obvious "Cancel" or "Go Back" buttons
- Save draft and exit
- No traps or dead ends
- Breadcrumb navigation

### Learning Disabilities Support

**Multi-modal Content:**
- Text + images + video
- Audio alternatives to reading
- Visual diagrams for concepts
- Interactive demonstrations

**Scaffolding:**
- Break complex tasks into simple steps
- Provide examples and templates
- Show worked examples
- Offer hints and tips

**Flexible Pacing:**
- No time limits on learning
- Ability to pause and resume
- Repeat sections unlimited times
- Progress at own speed

### Implementation Checklist

**Content and Structure:**
- [ ] Clear heading hierarchy (H1 → H2 → H3)
- [ ] Short paragraphs (3-4 sentences max)
- [ ] Bullet points for lists
- [ ] Visual breaks between sections
- [ ] Important information highlighted
- [ ] Plain language (no jargon)

**Interaction:**
- [ ] Predictable navigation
- [ ] Consistent patterns throughout
- [ ] Auto-save functionality
- [ ] Undo/redo capabilities
- [ ] Confirmation for destructive actions
- [ ] Multiple input methods (keyboard, mouse, voice)

**Visual Design:**
- [ ] Adequate spacing (not cramped)
- [ ] Readable fonts (14-16px minimum)
- [ ] High contrast text
- [ ] Color not sole indicator
- [ ] Reduced motion option
- [ ] Focus indicators visible

**Timing:**
- [ ] No time limits (or adjustable)
- [ ] Warnings before timeout
- [ ] Ability to extend time
- [ ] Auto-save prevents data loss
- [ ] Pauseable media

**Feedback:**
- [ ] Clear error messages
- [ ] Positive reinforcement
- [ ] Progress indicators
- [ ] Loading states
- [ ] Success confirmations
- [ ] Non-blaming language

### Testing with Users

**Include people with:**
- ADHD
- Autism
- Dyslexia
- Anxiety disorders
- Learning disabilities
- Memory impairments
- Processing speed differences

**Test for:**
- Task completion success
- Cognitive load (subjective)
- Error rates
- Time on task
- User confidence
- Stress levels

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement cognitive-inclusion-design pattern | haiku | Straightforward implementation |
| Review cognitive-inclusion-design implementation | sonnet | Requires code analysis |
| Optimize cognitive-inclusion-design design | opus | Complex trade-offs |

## Sources

- [W3C: Cognitive Accessibility Guidance](https://www.w3.org/WAI/WCAG2/supplemental/objectives/o3-clear/)
- [WebAIM: Cognitive Disabilities](https://webaim.org/articles/cognitive/)
- [ADHD Foundation: Digital Accessibility](https://www.adhdfoundation.org.uk/)
- [National Autistic Society: Website Accessibility](https://www.autism.org.uk/what-we-do/help-and-support/accessibility)
- [British Dyslexia Association: Style Guide](https://www.bdadyslexia.org.uk/advice/employers/creating-a-dyslexia-friendly-workplace/dyslexia-friendly-style-guide)
