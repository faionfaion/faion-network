// build-tokens.mjs — Style Dictionary pipeline
// Input:  tokens/primitive.json + tokens/semantic.json
// Output: dist/css/tokens.css, dist/js/tokens.js, dist/ios/Tokens.swift
import StyleDictionary from 'style-dictionary';

const sd = new StyleDictionary({
  source: ['tokens/primitive.json', 'tokens/semantic.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/css/',
      files: [{ destination: 'tokens.css', format: 'css/variables' }],
    },
    js: {
      transformGroup: 'js',
      buildPath: 'dist/js/',
      files: [{ destination: 'tokens.js', format: 'javascript/es6' }],
    },
    ios: {
      transformGroup: 'ios-swift',
      buildPath: 'dist/ios/',
      files: [{
        destination: 'Tokens.swift',
        format: 'ios-swift/class.swift',
        className: 'Tokens',
      }],
    },
  },
});

await sd.buildAllPlatforms();
