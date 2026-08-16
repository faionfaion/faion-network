<!-- purpose: worked example demonstrating one full detection cycle -->
<!-- consumes: PR diff with fabricated resource type -->
<!-- produces: rendered report matching content/02-output-contract.xml -->
<!-- depends-on: content/04-procedure.xml -->
<!-- token-budget-impact: ~400 tokens -->

# Worked example: catching `aws_dynamodb_globaltable`

Diff under review:

```hcl
resource "aws_dynamodb_globaltable" "main" {
  name = "orders"
}
```

Run:

```bash
terraform init -backend=false
terraform providers schema -json > schema.json
python scripts/validate-ai-iac-hallucination-detector.py --plan plan.json --schema schema.json
```

Output:

```json
{
  "scanned_files": ["main.tf"],
  "hallucinations": [
    {
      "category": "resource-type",
      "file": "main.tf",
      "line": 1,
      "fabricated_name": "aws_dynamodb_globaltable",
      "suggestion": "aws_dynamodb_global_table"
    }
  ],
  "verdict": "fail"
}
```

PR check fails. Author fixes to `aws_dynamodb_global_table`, validator re-runs, verdict=pass.
