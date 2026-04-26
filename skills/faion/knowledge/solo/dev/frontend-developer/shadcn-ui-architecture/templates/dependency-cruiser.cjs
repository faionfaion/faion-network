// .dependency-cruiser.cjs
// Enforce shadcn/ui layer contract:
// 1. Primitives (ui/) must not import feature components
// 2. Feature components cannot import across feature boundaries
module.exports = {
  forbidden: [
    {
      name: 'primitives-pure',
      comment: 'ui/ primitives must not import from feature components',
      severity: 'error',
      from: { path: '^src/components/ui' },
      to:   { path: '^src/components/(?!ui)' },
    },
    {
      name: 'no-cross-feature',
      comment: 'Feature dirs cannot import from sibling feature dirs',
      severity: 'error',
      from: { path: '^src/components/([^/]+)/' },
      to:   { path: '^src/components/(?!\\1|ui|layout)/[^/]+/' },
    },
  ],
  options: {
    doNotFollow: { path: 'node_modules' },
    moduleSystems: ['es6', 'cjs'],
    tsPreCompilationDeps: true,
  },
};
