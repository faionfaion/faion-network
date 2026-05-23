#!/usr/bin/env bash
# gen-compound.sh <ComponentName> [Sub1,Sub2,Sub3]
# Scaffolds a compound component skeleton with context + sub-components
set -euo pipefail

NAME="${1:?Usage: gen-compound.sh <Name> [Header,Content,Footer]}"
SUBS="${2:-Header,Content,Footer}"
DIR="src/components/composite/${NAME}"
mkdir -p "$DIR"

cat > "$DIR/${NAME}.tsx" <<EOF
import { createContext, useContext, ReactNode } from 'react';

interface ${NAME}ContextValue { /* add shared state */ }
const ${NAME}Context = createContext<${NAME}ContextValue | null>(null);

export function use${NAME}Context() {
  const ctx = useContext(${NAME}Context);
  if (!ctx) throw new Error('${NAME} sub-components must be used inside <${NAME}>');
  return ctx;
}

interface ${NAME}Props { children: ReactNode; className?: string; }
function ${NAME}Root({ children, className }: ${NAME}Props) {
  return (
    <${NAME}Context.Provider value={{}}>
      <div data-component="${NAME}" className={className}>{children}</div>
    </${NAME}Context.Provider>
  );
}
EOF

IFS=',' read -ra PARTS <<< "$SUBS"
for P in "${PARTS[@]}"; do
  cat >> "$DIR/${NAME}.tsx" <<EOF

export function ${NAME}${P}({ children }: { children: ReactNode }) {
  return <div data-part="${P}">{children}</div>;
}
EOF
done

# Object.assign export + named re-export
ASSIGN=$(IFS=','; echo "${PARTS[*]}" | sed 's/\([^,]*\)/\1: '${NAME}'\1/g')
echo "" >> "$DIR/${NAME}.tsx"
echo "export const ${NAME} = Object.assign(${NAME}Root, { ${ASSIGN} });" >> "$DIR/${NAME}.tsx"
echo "export * from './${NAME}';" > "$DIR/index.ts"
echo "Scaffolded ${DIR}/${NAME}.tsx"
