"""
Zod schema generator from a field spec list.

Input: list of field dicts with keys:
  name (str), type (str: email|phone|integer|string|date|enum),
  required (bool, default True), min (int), max (int),
  enum_values (list[str] for enum type)

Output: TypeScript Zod schema string

Usage:
    fields = [
        {"name": "email", "type": "email"},
        {"name": "age", "type": "integer", "min": 18, "max": 120},
        {"name": "country", "type": "enum", "enum_values": ["US", "UK", "CA"]},
    ]
    print(generate_zod_schema(fields))
"""


def generate_zod_schema(fields: list[dict]) -> str:
    lines = ["import { z } from 'zod';", "", "export const formSchema = z.object({"]
    for f in fields:
        name = f["name"]
        ftype = f.get("type", "string")
        required = f.get("required", True)

        if ftype == "email":
            rule = "z.string().email('Invalid email format')"
        elif ftype == "phone":
            rule = "z.string().regex(/^[+]?[\\d\\s\\-().]{7,15}$/, 'Invalid phone format')"
        elif ftype == "integer":
            mn = f.get("min", 1)
            mx = f.get("max", 999)
            rule = f"z.number().int().min({mn}, 'Min {mn}').max({mx}, 'Max {mx}')"
        elif ftype == "date":
            rule = "z.string().regex(/^\\d{4}-\\d{2}-\\d{2}$/, 'Use YYYY-MM-DD format')"
        elif ftype == "enum":
            values = f.get("enum_values", [])
            vals_str = ", ".join(f'"{v}"' for v in values)
            rule = f"z.enum([{vals_str}])"
        else:
            max_len = f.get("max", 255)
            rule = f"z.string().min(1, 'Required').max({max_len})"

        if not required:
            rule += ".optional()"

        lines.append(f"  {name}: {rule},")

    lines.extend(["});", "", "export type FormData = z.infer<typeof formSchema>;"])
    return "\n".join(lines)


# NOTE: Cross-field validation (end date after start date, password matches
# confirmation) cannot be generated from individual field specs.
# Add .refine() or .superRefine() manually for any cross-field rules.
# Example:
#   formSchema.refine(data => data.endDate > data.startDate, {
#     message: "End date must be after start date",
#     path: ["endDate"],
#   })
