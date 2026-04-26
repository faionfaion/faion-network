# Checklist

## Planning Phase

- [ ] Choose CSS-in-JS library (styled-components, Emotion, vanilla-extract)
- [ ] Design component styling strategy
- [ ] Plan theming approach (light/dark mode)
- [ ] Identify design system tokens (colors, spacing, typography)
- [ ] Plan global styles vs component styles
- [ ] Design responsive breakpoints

## Setup Phase

- [ ] Install chosen CSS-in-JS library
- [ ] Configure styled-components/Emotion in tsconfig
- [ ] Create theme definitions (light and dark)
- [ ] Set up ThemeProvider wrapper
- [ ] Create global styles file
- [ ] Configure Babel/build tools if needed

## Theme Definition Phase

- [ ] Define color palette (primitives and semantic)
- [ ] Define typography scale (font sizes, weights)
- [ ] Define spacing scale (margins, padding)
- [ ] Define border radius values
- [ ] Define shadow values
- [ ] Define breakpoints for responsive design
- [ ] Create TypeScript theme type definitions

## Component Styling Phase

- [ ] Create base styled components
- [ ] Implement variant patterns (size, color, state)
- [ ] Use theme values consistently
- [ ] Extract common styles to styled utilities
- [ ] Implement pseudo-selectors (:hover, :focus, :disabled)
- [ ] Add responsive styles with media queries
- [ ] Test theme switching works without page reload

## Theming Phase

- [ ] Implement light theme
- [ ] Implement dark theme with proper contrast
- [ ] Create theme toggle mechanism
- [ ] Store theme preference (localStorage/cookie)
- [ ] Support prefers-color-scheme media query
- [ ] Test all components in both themes

## Performance Phase

- [ ] Verify no styles are created in render functions
- [ ] Extract variant styles outside components
- [ ] Use css`` utility for reusable styles
- [ ] Check bundle size impact
- [ ] Use zero-runtime library if static styles only
- [ ] Implement server-side style extraction if SSR

## Testing Phase

- [ ] Test styled components render correctly
- [ ] Test responsive breakpoints work
- [ ] Test theme values apply correctly
- [ ] Test variant combinations
- [ ] Test disabled/active states
- [ ] Accessibility testing for color contrast

## Deployment

- [ ] Document theming API for team
- [ ] Create component style guide
- [ ] Document design token usage
- [ ] Monitor bundle size