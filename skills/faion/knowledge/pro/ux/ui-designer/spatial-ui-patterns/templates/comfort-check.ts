// comfort_check.ts — flag spatial panels outside the ergonomic envelope
// Input: Panel spec. Output: array of violation strings (empty = pass).

type Panel = {
  id: string;
  distance_m: number;
  eccentricity_deg: number;  // degrees off forward gaze axis
  size_m: [number, number];  // [width, height] in meters
  anchor: "world" | "head" | "body" | "hand";
};

const RULES = {
  distance_m: [0.5, 2.0] as [number, number],
  eccentricity_deg: 30,
  min_size_m: 0.04,           // 4 cm — touch target floor in spatial
  hand_distance_m: [0.25, 0.5] as [number, number],
};

export function checkComfort(p: Panel): string[] {
  const issues: string[] = [];
  const [lo, hi] = RULES.distance_m;

  if (p.anchor !== "hand") {
    if (p.distance_m < lo || p.distance_m > hi) {
      issues.push(`distance:${p.distance_m}m (expected ${lo}-${hi}m)`);
    }
  } else {
    const [hl, hh] = RULES.hand_distance_m;
    if (p.distance_m < hl || p.distance_m > hh) {
      issues.push(`hand-range:${p.distance_m}m (expected ${hl}-${hh}m)`);
    }
  }

  if (p.eccentricity_deg > RULES.eccentricity_deg) {
    issues.push(`fov-edge:${p.eccentricity_deg}deg (max ${RULES.eccentricity_deg}deg)`);
  }

  if (Math.min(...p.size_m) < RULES.min_size_m) {
    issues.push(`too-small:${p.size_m}m (min ${RULES.min_size_m}m)`);
  }

  return issues;
}

// Example usage:
// const issues = checkComfort({ id: "nav-menu", distance_m: 0.3, eccentricity_deg: 15,
//   size_m: [0.3, 0.2], anchor: "body" });
// console.log(issues); // ["distance:0.3m (expected 0.5-2m)"]
