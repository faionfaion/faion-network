# purpose: Step Functions state machine for multi-step orchestration
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (config)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~350 tokens when loaded

resource "aws_sfn_state_machine" "main" {
  name     = "${var.project}-orchestrator"
  role_arn = aws_iam_role.sfn.arn
  definition = jsonencode({
    Comment = "Order processing"
    StartAt = "Validate"
    States = {
      Validate = { Type = "Task", Resource = module.lambda.lambda_function_arn, Next = "Process", Retry = [{ ErrorEquals = ["States.ALL"], MaxAttempts = 3 }] }
      Process  = { Type = "Task", Resource = module.lambda.lambda_function_arn, End = true }
    }
  })
}
