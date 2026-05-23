/**
 * Style Dictionary v3 configuration.
 * Emits: CSS custom properties, SCSS variables, JS/TS modules, JSON.
 *
 * Pin the major version: v3 uses formatter: function({dictionary, file})
 * v4 uses format: ({dictionary, options}) => string — do NOT mix.
 *
 * Run: npx style-dictionary build --config style-dictionary.config.js
 */
const StyleDictionary = require("style-dictionary");

module.exports = {
  source: [
    "tokens/primitives/**/*.json",
    "tokens/semantic/**/*.json",
    "tokens/modes/light.json",  // extend per build target
  ],
  platforms: {
    css: {
      transformGroup: "css",
      prefix: "--",
      buildPath: "dist/css/",
      files: [
        {
          destination: "variables.css",
          format: "css/variables",
          selector: ":root",
          filter: (token) => token.attributes.category !== "private",
          options: {
            outputReferences: true,  // emit var(--alias) not resolved value
          },
        },
      ],
    },
    scss: {
      transformGroup: "scss",
      buildPath: "dist/scss/",
      files: [
        {
          destination: "_variables.scss",
          format: "scss/variables",
          options: { outputReferences: true },
        },
      ],
    },
    js: {
      transformGroup: "js",
      buildPath: "dist/js/",
      files: [
        {
          destination: "tokens.js",
          format: "javascript/es6",
        },
        {
          destination: "tokens.d.ts",
          format: "typescript/es6-declarations",
        },
      ],
    },
    json: {
      transformGroup: "js",
      buildPath: "dist/json/",
      files: [
        {
          destination: "tokens.json",
          format: "json/nested",
        },
      ],
    },
  },
};
