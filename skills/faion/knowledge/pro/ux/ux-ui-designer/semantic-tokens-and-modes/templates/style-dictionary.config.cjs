// purpose: Style Dictionary build config emitting CSS / Swift / Compose from DTCG tokens
// consumes: tokens/reference.json + tokens/semantic.json (per-mode values)
// produces: tokens.css ([data-theme] blocks), tokens.swift (Color.Theme), tokens.compose.kt
// depends-on: content/01-core-rules.xml dtcg-format rule
// token-budget-impact: ~400 tokens when loaded as context

module.exports = {
  source: ['tokens/reference.json', 'tokens/semantic.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/css/',
      files: [
        { destination: 'tokens.css', format: 'css/variables', options: { selector: ':root' } },
        { destination: 'tokens-dark.css', format: 'css/variables', options: { selector: '[data-theme="dark"]' }, filter: (t) => t.attributes && t.attributes.mode === 'dark' },
        { destination: 'tokens-hc.css', format: 'css/variables', options: { selector: '[data-theme="high-contrast"]' }, filter: (t) => t.attributes && t.attributes.mode === 'high-contrast' }
      ]
    },
    ios: {
      transformGroup: 'ios-swift',
      buildPath: 'dist/ios/',
      files: [
        { destination: 'Tokens.swift', format: 'ios-swift/class.swift', className: 'TokensTheme' }
      ]
    },
    android: {
      transformGroup: 'compose',
      buildPath: 'dist/android/',
      files: [
        { destination: 'Tokens.kt', format: 'compose/object', className: 'TokensTheme', packageName: 'com.example.tokens' }
      ]
    }
  }
};
