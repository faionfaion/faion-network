# Accessibility & Semantic HTML Reference

## WCAG 2.2 Compliance Levels

| Level | Description | Requirement |
|-------|-------------|-------------|
| **A** | Minimum | Must meet for basic accessibility |
| **AA** | Standard | Required by most laws (EAA 2025) |
| **AAA** | Enhanced | Best practice, not always achievable |

---

## Semantic HTML Structure

### Correct Document Outline

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title | Site Name</title>
  <meta name="description" content="Page description for SEO">
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <header role="banner">
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/" aria-current="page">Home</a></li>
        <li><a href="/about/">About</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main id="main-content" role="main">
    <article>
      <h1>Single H1 - Main Page Title</h1>
      <p>Introduction paragraph...</p>

      <section aria-labelledby="section1-heading">
        <h2 id="section1-heading">Section 1</h2>
        <p>Content...</p>

        <h3>Subsection 1.1</h3>
        <p>More content...</p>
      </section>

      <section aria-labelledby="section2-heading">
        <h2 id="section2-heading">Section 2</h2>
        <p>Content...</p>
      </section>
    </article>

    <aside aria-label="Related articles">
      <h2>Related Articles</h2>
      <ul>
        <li><a href="/related1/">Related Article 1</a></li>
      </ul>
    </aside>
  </main>

  <footer role="contentinfo">
    <nav aria-label="Footer navigation">
      <ul>
        <li><a href="/privacy/">Privacy Policy</a></li>
        <li><a href="/terms/">Terms of Service</a></li>
      </ul>
    </nav>
    <p>&copy; 2026 Company Name</p>
  </footer>
</body>
</html>
```

---

## HTML5 Semantic Elements

| Element | Purpose | ARIA Equivalent |
|---------|---------|-----------------|
| `<header>` | Page or section header | `role="banner"` (top-level only) |
| `<nav>` | Navigation links | `role="navigation"` |
| `<main>` | Main content (one per page) | `role="main"` |
| `<article>` | Self-contained content | `role="article"` |
| `<section>` | Thematic grouping | `role="region"` (with label) |
| `<aside>` | Tangentially related | `role="complementary"` |
| `<footer>` | Page or section footer | `role="contentinfo"` (top-level) |
| `<figure>` | Self-contained media | |
| `<figcaption>` | Caption for figure | |
| `<time>` | Date/time | |
| `<mark>` | Highlighted text | |
| `<details>` | Disclosure widget | |
| `<summary>` | Summary for details | |

---

## Heading Hierarchy

### Correct

```html
<h1>Main Page Title</h1>
  <h2>Section 1</h2>
    <h3>Subsection 1.1</h3>
    <h3>Subsection 1.2</h3>
  <h2>Section 2</h2>
    <h3>Subsection 2.1</h3>
      <h4>Sub-subsection</h4>
```

### Incorrect

```html
<!-- ❌ Multiple H1s -->
<h1>Title</h1>
<h1>Another Title</h1>

<!-- ❌ Skipping levels -->
<h1>Title</h1>
<h3>Jumped to H3</h3>

<!-- ❌ Using headings for styling -->
<h4>This should be a paragraph</h4>
```

---

## Images & Alt Text

### Guidelines

| Image Type | Alt Text |
|------------|----------|
| Informative | Describe content and function |
| Decorative | `alt=""` (empty) |
| Functional (link/button) | Describe action |
| Complex (charts, graphs) | Brief alt + detailed description |
| Text in image | Include all text |

### Examples

```html
<!-- Informative -->
<img src="chart.png" alt="Sales increased 40% from Q1 to Q4 2025">

<!-- Decorative -->
<img src="decorative-line.png" alt="">

<!-- Functional (in link) -->
<a href="/home/">
  <img src="logo.png" alt="Company Name - Go to homepage">
</a>

<!-- Complex with long description -->
<figure>
  <img src="flowchart.png" alt="SDD workflow diagram" aria-describedby="flow-desc">
  <figcaption id="flow-desc">
    The SDD workflow begins with idea validation, moves through specification,
    design, implementation, and ends with deployment...
  </figcaption>
</figure>
```

---

## Links

### Descriptive Link Text

```html
<!-- ❌ Bad -->
<a href="/guide/">Click here</a>
<a href="/guide/">Read more</a>
<a href="/guide/">Learn more</a>

<!-- ✅ Good -->
<a href="/guide/">Read the complete SDD methodology guide</a>
<a href="/guide/">SDD Methodology Guide</a>
```

### External Links

```html
<a href="https://external.com" target="_blank" rel="noopener noreferrer">
  External Site
  <span class="visually-hidden">(opens in new tab)</span>
</a>
```

### Skip Links

```html
<style>
  .skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #000;
    color: #fff;
    padding: 8px;
    z-index: 100;
  }
  .skip-link:focus {
    top: 0;
  }
</style>

<a href="#main-content" class="skip-link">Skip to main content</a>
```

---

## Forms

### Proper Labeling

```html
<!-- Method 1: Explicit label -->
<label for="email">Email address</label>
<input type="email" id="email" name="email" required>

<!-- Method 2: Implicit label -->
<label>
  Email address
  <input type="email" name="email" required>
</label>

<!-- With helper text -->
<label for="password">Password</label>
<input type="password" id="password" aria-describedby="password-help">
<p id="password-help">Must be at least 8 characters</p>

<!-- Required field -->
<label for="name">
  Name <span aria-hidden="true">*</span>
  <span class="visually-hidden">(required)</span>
</label>
<input type="text" id="name" required aria-required="true">

<!-- Error state -->
<label for="email">Email</label>
<input type="email" id="email" aria-invalid="true" aria-describedby="email-error">
<p id="email-error" role="alert">Please enter a valid email address</p>
```

---

## ARIA Landmarks

```html
<header role="banner">...</header>
<nav role="navigation" aria-label="Main">...</nav>
<main role="main">...</main>
<aside role="complementary">...</aside>
<footer role="contentinfo">...</footer>
```

### Multiple Navigation

```html
<nav aria-label="Main navigation">...</nav>
<nav aria-label="Breadcrumb">...</nav>
<nav aria-label="Footer navigation">...</nav>
```

---

## Color Contrast

### WCAG Requirements

| Text Size | Level AA | Level AAA |
|-----------|----------|-----------|
| Normal text (< 18pt) | 4.5:1 | 7:1 |
| Large text (≥ 18pt or 14pt bold) | 3:1 | 4.5:1 |
| UI components & graphics | 3:1 | 3:1 |

### Testing Tools

- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- Chrome DevTools → Elements → Styles → Color picker
- [Accessible Colors](https://accessible-colors.com/)

---

## Keyboard Navigation

### Requirements

1. **All interactive elements focusable** - links, buttons, inputs
2. **Visible focus indicator** - outline or other visual change
3. **Logical tab order** - follows visual order
4. **No keyboard traps** - can always navigate away
5. **Skip links** - bypass repetitive content

### Focus Styles

```css
/* Don't remove outline without replacement */
/* ❌ Bad */
:focus { outline: none; }

/* ✅ Good - Custom focus style */
:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

/* For mouse users (optional) */
:focus:not(:focus-visible) {
  outline: none;
}

:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}
```

---

## Screen Reader Text

### Visually Hidden Class

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### Usage

```html
<button>
  <svg aria-hidden="true">...</svg>
  <span class="visually-hidden">Close menu</span>
</button>

<a href="/cart/">
  Cart
  <span class="visually-hidden">(3 items)</span>
</a>
```

---

## Tables

### Accessible Tables

```html
<table>
  <caption>Pricing Plans Comparison</caption>
  <thead>
    <tr>
      <th scope="col">Plan</th>
      <th scope="col">Price</th>
      <th scope="col">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Free</th>
      <td>$0/mo</td>
      <td>5 methodologies, 2 agents</td>
    </tr>
    <tr>
      <th scope="row">Pro</th>
      <td>$35/mo</td>
      <td>All methodologies, all agents</td>
    </tr>
  </tbody>
</table>
```

---

## Testing Checklist

- [ ] Keyboard navigation works (Tab, Enter, Escape, Arrow keys)
- [ ] All interactive elements have focus indicators
- [ ] Skip link present and functional
- [ ] Headings form logical hierarchy
- [ ] All images have appropriate alt text
- [ ] Links have descriptive text
- [ ] Form inputs have labels
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Page works without CSS
- [ ] Screen reader announces content correctly
- [ ] No ARIA errors (use axe DevTools)

## Tools

- [WAVE](https://wave.webaim.org/) - Web accessibility evaluator
- [axe DevTools](https://www.deque.com/axe/) - Browser extension
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/) - Built into Chrome
- [NVDA](https://www.nvaccess.org/) - Free screen reader (Windows)
- [VoiceOver](https://www.apple.com/accessibility/vision/) - Built into macOS/iOS
