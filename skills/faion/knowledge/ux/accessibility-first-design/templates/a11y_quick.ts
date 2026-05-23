// purpose: TypeScript contrast calc + token-pair checker
// consumes: color pair (fg, bg)
// produces: {ratio, pass}
// depends-on: stdlib only
// token-budget-impact: ~150 imported

export function relativeLuminance(hex: string): number {
  const c = hex.replace('#', '');
  const rgb = [parseInt(c.slice(0,2),16), parseInt(c.slice(2,4),16), parseInt(c.slice(4,6),16)].map(v => v/255);
  const lin = rgb.map(v => v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4));
  return 0.2126*lin[0] + 0.7152*lin[1] + 0.0722*lin[2];
}
export function contrast(fg: string, bg: string): number {
  const [l1, l2] = [relativeLuminance(fg), relativeLuminance(bg)].sort((a,b)=>b-a);
  return (l1+0.05)/(l2+0.05);
}
export function pass(fg: string, bg: string, kind: 'body'|'large'|'non-text'): boolean {
  const r = contrast(fg, bg);
  return kind === 'body' ? r >= 4.5 : r >= 3;
}
