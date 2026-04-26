// ds-coverage.mjs — AST-based design system adoption scanner
// Counts system-package component usages vs locally-implemented snowflake primitives
// Install: npm i -D ts-morph
// Usage: SYSTEM_PKG=@org/ui node ds-coverage.mjs [tsconfig.json]
import { Project, SyntaxKind } from 'ts-morph';
import { writeFileSync } from 'node:fs';

const SYSTEM_PKG = process.env.SYSTEM_PKG ?? '@org/ui';
const PRIMITIVES = ['button', 'input', 'select', 'textarea', 'modal', 'dialog', 'card'];
const tsConfigPath = process.argv[2] ?? 'tsconfig.json';

const project = new Project({ tsConfigFilePath: tsConfigPath, skipAddingFilesFromTsConfig: false });
const coverage = {};

for (const sf of project.getSourceFiles('apps/**/*.{ts,tsx}')) {
  const appKey = sf.getFilePath().replace(process.cwd(), '').split('/')[2] ?? 'root';
  if (!coverage[appKey]) coverage[appKey] = { system_uses: 0, snowflake_uses: 0 };

  const importsSystem = sf.getImportDeclarations()
    .some(d => d.getModuleSpecifierValue() === SYSTEM_PKG);

  for (const el of sf.getDescendantsOfKind(SyntaxKind.JsxOpeningElement)) {
    const tag = el.getTagNameNode().getText().toLowerCase();
    if (PRIMITIVES.includes(tag)) {
      if (importsSystem) coverage[appKey].system_uses++;
      else coverage[appKey].snowflake_uses++;
    }
  }
}

const report = Object.entries(coverage).map(([app, { system_uses, snowflake_uses }]) => ({
  app,
  system_uses,
  snowflake_uses,
  coverage_pct: system_uses + snowflake_uses === 0
    ? null
    : +(system_uses / (system_uses + snowflake_uses) * 100).toFixed(1),
}));

const output = JSON.stringify(report, null, 2);
console.log(output);
writeFileSync('ds-coverage.json', output);
