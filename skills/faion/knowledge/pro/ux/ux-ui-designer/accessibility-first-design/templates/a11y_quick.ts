// a11y_quick.ts — WCAG contrast ratio calculator + touch-target validator
// No runtime dependencies. Import and call directly.

type RGB = [number, number, number];

/** Relative luminance per WCAG 2.x (IEC 61966-2-1 sRGB). */
function luminance([r, g, b]: RGB): number {
  const linearize = (v: number) => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b);
}

/** WCAG contrast ratio between two RGB colors. Range: 1–21. */
export function contrast(a: RGB, b: RGB): number {
  const [L1, L2] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (L1 + 0.05) / (L2 + 0.05);
}

type Level = "AA" | "AAA";
type Size = "body" | "large";

/** Check if a contrast ratio meets the WCAG threshold for level + text size. */
export function meetsWcag(ratio: number, level: Level, size: Size): boolean {
  const thresholds: Record<Level, Record<Size, number>> = {
    AA:  { body: 4.5, large: 3.0 },
    AAA: { body: 7.0, large: 4.5 },
  };
  return ratio >= thresholds[level][size];
}

/** Check WCAG 2.2 SC 2.5.8 touch target (44x44 CSS px minimum). */
export function targetOk(widthPx: number, heightPx: number): boolean {
  return widthPx >= 44 && heightPx >= 44;
}

// Example:
// const ratio = contrast([255, 255, 255], [117, 117, 117]); // → ~4.48
// meetsWcag(ratio, "AA", "body"); // → false (4.48 < 4.5 fails by 0.02)
// targetOk(44, 44); // → true
