// alt-input-matrix.ts — spatial accessibility: alternative input modality auditor
// Input: list of spatial interactions with their supported modalities
// Output: pass count + gaps (interactions missing required alternative count)

type Modality = "gaze" | "voice" | "hand" | "controller" | "switch";

interface Interaction {
  name: string;
  primary: Modality;
  supports: Modality[];
  seatedCompatible: boolean;
}

interface AuditResult {
  passing: number;
  gaps: { name: string; missing: number; seatedIssue: boolean }[];
}

const REQUIRED_MODALITIES = 2; // minimum distinct input paths per interaction

export function audit(interactions: Interaction[]): AuditResult {
  const gaps: AuditResult["gaps"] = [];

  for (const interaction of interactions) {
    const allModalities = new Set([interaction.primary, ...interaction.supports]);
    const modalityCount = allModalities.size;
    const modalityGap = Math.max(0, REQUIRED_MODALITIES - modalityCount);
    const seatedIssue = !interaction.seatedCompatible;

    if (modalityGap > 0 || seatedIssue) {
      gaps.push({
        name: interaction.name,
        missing: modalityGap,
        seatedIssue,
      });
    }
  }

  return {
    passing: interactions.length - gaps.length,
    gaps,
  };
}

// Example usage:
// const result = audit([
//   { name: "Select object", primary: "gaze", supports: ["voice", "controller"], seatedCompatible: true },
//   { name: "Grab item", primary: "hand", supports: [], seatedCompatible: false },
// ]);
// console.log(result);
// → { passing: 1, gaps: [{ name: "Grab item", missing: 1, seatedIssue: true }] }
