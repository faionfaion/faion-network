// jscodeshift codemod: rename `user.email` -> `user.contact` repo-wide.
// Usage: npx jscodeshift -t templates/rename-property.ts --extensions=ts,tsx --parser=tsx 'src/**/*.{ts,tsx}'
// Idempotent: re-running on a clean tree produces no diff (validator assertion).

import type { API, FileInfo } from "jscodeshift";

export default function transform(file: FileInfo, api: API): string {
  const j = api.jscodeshift;
  const root = j(file.source);

  // 1. user.email -> user.contact (member access on identifier `user`)
  root
    .find(j.MemberExpression, {
      property: { type: "Identifier", name: "email" },
      object: { type: "Identifier", name: "user" },
    })
    .forEach(p => {
      (p.value.property as { name: string }).name = "contact";
    });

  // 2. { email } destructuring on user-typed objects -> { contact }
  root
    .find(j.ObjectPattern)
    .forEach(p => {
      p.value.properties.forEach(prop => {
        if (
          prop.type === "Property" &&
          prop.key.type === "Identifier" &&
          prop.key.name === "email" &&
          prop.shorthand
        ) {
          prop.key.name = "contact";
          if (prop.value.type === "Identifier") prop.value.name = "contact";
        }
      });
    });

  return root.toSource({ quote: "double" });
}
