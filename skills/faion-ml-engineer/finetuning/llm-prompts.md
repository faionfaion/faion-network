# LLM Prompts for Fine-tuning Tasks

Prompts for using LLMs to assist with fine-tuning workflows.

---

## Table of Contents

1. [Data Preparation Prompts](#data-preparation-prompts)
2. [Data Quality Assessment](#data-quality-assessment)
3. [Configuration Generation](#configuration-generation)
4. [Evaluation Prompts](#evaluation-prompts)
5. [Debugging Prompts](#debugging-prompts)
6. [Documentation Prompts](#documentation-prompts)

---

## Data Preparation Prompts

### Generate Training Examples

```
I need to create training data for fine-tuning an LLM on [TASK DESCRIPTION].

Requirements:
- Format: [alpaca/sharegpt/openai chat]
- Domain: [DOMAIN]
- Tone: [formal/casual/technical]
- Output length: [short/medium/long]

Generate [N] diverse, high-quality training examples that:
1. Cover various edge cases
2. Demonstrate the desired behavior
3. Include both simple and complex scenarios
4. Maintain consistent formatting

Each example should follow this structure:
[PROVIDE FORMAT TEMPLATE]
```

### Convert Data Formats

```
Convert the following data from [SOURCE FORMAT] to [TARGET FORMAT] suitable for fine-tuning:

Source format example:
[EXAMPLE]

Target format requirements:
- [REQUIREMENT 1]
- [REQUIREMENT 2]

Ensure:
1. No information is lost
2. Formatting is consistent
3. Special characters are properly escaped
4. JSON is valid
```

### Augment Training Data

```
I have the following training example for [TASK]:

[EXAMPLE]

Generate [N] variations that:
1. Preserve the core task/response relationship
2. Vary the input phrasing
3. Include different complexity levels
4. Maintain output quality standards

Variations should not:
- Change the fundamental meaning
- Introduce errors or inconsistencies
- Be trivially similar to each other
```

### Clean and Standardize Data

```
Review and clean this training data for LLM fine-tuning:

[DATA SAMPLE]

Check for and fix:
1. Inconsistent formatting
2. Grammatical errors (unless intentional)
3. Incomplete responses
4. Duplicate or near-duplicate entries
5. Instructions that don't match outputs
6. PII or sensitive information

Output the cleaned version with a brief summary of changes made.
```

---

## Data Quality Assessment

### Evaluate Training Data Quality

```
Evaluate the quality of this fine-tuning dataset:

[SAMPLE OF 10-20 EXAMPLES]

Assess each example on:
1. Instruction clarity (1-5)
2. Response quality (1-5)
3. Instruction-response alignment (1-5)
4. Factual accuracy (1-5)
5. Format consistency (1-5)

Provide:
- Overall quality score
- Distribution analysis
- Specific examples of issues
- Recommendations for improvement
```

### Check for Data Leakage

```
Review this training/validation data split for potential data leakage:

Training examples (sample):
[TRAINING SAMPLE]

Validation examples:
[VALIDATION SAMPLE]

Check for:
1. Exact duplicates
2. Near-duplicates (paraphrased versions)
3. Overlapping source material
4. Sequential data that should be together
5. Contamination from evaluation benchmarks

Report any issues found with specific examples.
```

### Analyze Data Distribution

```
Analyze the distribution of this fine-tuning dataset:

Dataset summary:
- Total examples: [N]
- Categories: [LIST]
- Sample:
[REPRESENTATIVE SAMPLES]

Analyze:
1. Category balance
2. Input length distribution
3. Output length distribution
4. Complexity distribution
5. Topic coverage gaps

Recommend adjustments to improve training effectiveness.
```

---

## Configuration Generation

### Generate Training Configuration

```
Generate an optimal fine-tuning configuration for:

Base model: [MODEL NAME]
Task: [TASK DESCRIPTION]
Dataset size: [N EXAMPLES]
Available GPU: [GPU TYPE AND MEMORY]
Framework: [unsloth/axolotl/trl]

Consider:
1. Memory constraints
2. Training stability
3. Quality vs speed tradeoffs
4. Overfitting prevention

Output a complete configuration file with comments explaining each choice.
```

### Optimize Hyperparameters

```
Given these training results:

Run 1: lr=2e-4, rank=16, epochs=3
- Final train loss: 0.45
- Final val loss: 0.52
- Observations: [OBSERVATIONS]

Run 2: lr=1e-4, rank=32, epochs=3
- Final train loss: 0.38
- Final val loss: 0.58
- Observations: [OBSERVATIONS]

[MORE RUNS...]

Recommend:
1. Optimal hyperparameter combination
2. Additional experiments to try
3. Signs of overfitting/underfitting
4. Estimated improvement potential
```

### Select LoRA Target Modules

```
For fine-tuning [MODEL NAME] on [TASK TYPE]:

Task characteristics:
- [CHARACTERISTIC 1]
- [CHARACTERISTIC 2]
- [CHARACTERISTIC 3]

Current configuration:
- Rank: [RANK]
- Target modules: [CURRENT MODULES]

Recommend optimal target modules considering:
1. Task requirements
2. Memory constraints: [MEMORY]
3. Quality requirements: [high/medium/acceptable]

Explain the reasoning for each recommendation.
```

---

## Evaluation Prompts

### Evaluate Model Output Quality

```
Compare outputs from the base model and fine-tuned model:

Input: [INPUT]

Base model output:
[BASE OUTPUT]

Fine-tuned model output:
[FINETUNED OUTPUT]

Expected output (if available):
[EXPECTED]

Evaluate on:
1. Task completion accuracy
2. Response quality
3. Format adherence
4. Factual correctness
5. Style/tone match

Score each dimension 1-5 and provide overall recommendation.
```

### Generate Evaluation Test Cases

```
Generate [N] evaluation test cases for a model fine-tuned on [TASK]:

Requirements:
1. Cover edge cases
2. Include adversarial examples
3. Test boundary conditions
4. Verify format compliance
5. Check for common failure modes

For each test case provide:
- Input
- Expected output (or acceptable output criteria)
- What aspect it tests
- Difficulty level (easy/medium/hard)
```

### Analyze Training Metrics

```
Analyze these training metrics and diagnose any issues:

Epoch 1: train_loss=2.1, val_loss=2.3
Epoch 2: train_loss=1.5, val_loss=1.8
Epoch 3: train_loss=0.9, val_loss=1.4
Epoch 4: train_loss=0.5, val_loss=1.6
Epoch 5: train_loss=0.3, val_loss=1.9

Configuration:
- Learning rate: [LR]
- Batch size: [BATCH]
- LoRA rank: [RANK]

Diagnose:
1. Is overfitting occurring? When?
2. Should training stop early? At which epoch?
3. What configuration changes might help?
4. Is the learning rate appropriate?
```

---

## Debugging Prompts

### Diagnose Training Issues

```
Help diagnose this fine-tuning issue:

Problem: [DESCRIBE PROBLEM]

Configuration:
[CONFIG]

Error/symptoms:
[ERROR OR OBSERVED BEHAVIOR]

Training log (last 50 lines):
[LOG EXCERPT]

Hardware:
- GPU: [GPU]
- VRAM: [VRAM]
- System RAM: [RAM]

Provide:
1. Most likely cause(s)
2. Diagnostic steps to confirm
3. Solution(s) to try
4. Prevention for future runs
```

### Fix Data Format Issues

```
My training is failing with this error:
[ERROR MESSAGE]

Data sample that causes the issue:
[DATA SAMPLE]

Expected format:
[EXPECTED FORMAT]

Help me:
1. Identify what's wrong with the data
2. Provide a corrected version
3. Write a validation script to catch similar issues
4. Explain how to prevent this in data collection
```

### Debug Memory Issues

```
I'm getting OOM errors during fine-tuning:

Configuration:
- Model: [MODEL]
- GPU: [GPU WITH VRAM]
- Batch size: [BATCH]
- Sequence length: [SEQ LEN]
- LoRA rank: [RANK]
- Gradient checkpointing: [yes/no]
- Quantization: [none/4bit/8bit]

Error occurs at: [STEP/PHASE]

Recommend changes to fit training in memory, prioritized by:
1. Quality impact (least impact first)
2. Implementation difficulty
3. Training speed impact
```

---

## Documentation Prompts

### Generate Training Report

```
Generate a training report for this fine-tuning run:

Configuration:
[FULL CONFIG]

Results:
- Final train loss: [LOSS]
- Final val loss: [LOSS]
- Training time: [TIME]
- Best checkpoint: [CHECKPOINT]

Evaluation results:
[EVAL METRICS]

Sample outputs:
[SAMPLE OUTPUTS]

Generate a professional report including:
1. Executive summary
2. Configuration details
3. Training analysis
4. Evaluation results
5. Recommendations for improvement
6. Deployment considerations
```

### Create Model Card

```
Generate a model card for my fine-tuned model:

Base model: [BASE MODEL]
Fine-tuning task: [TASK]
Dataset: [DATASET DESCRIPTION]
Training configuration: [KEY CONFIG]
Evaluation results: [RESULTS]
Known limitations: [LIMITATIONS]
Intended use: [USE CASE]

Follow Hugging Face model card format with sections for:
1. Model description
2. Intended uses
3. Training data
4. Training procedure
5. Evaluation
6. Limitations and biases
7. How to use
```

### Document Data Collection Process

```
Document the data collection process for fine-tuning:

Task: [TASK]
Data sources: [SOURCES]
Collection method: [METHOD]
Quality criteria: [CRITERIA]
Volume: [N EXAMPLES]

Create documentation covering:
1. Data collection methodology
2. Quality assurance process
3. Data format specification
4. Known biases or limitations
5. Reproduction instructions
6. Ethical considerations
```

---

## Best Practices for Using These Prompts

1. **Be specific** - Provide concrete examples and context
2. **Iterate** - Refine prompts based on output quality
3. **Verify outputs** - Always validate LLM-generated data/configs
4. **Document changes** - Track what prompts produced useful results
5. **Combine approaches** - Use multiple prompts for comprehensive coverage

---

*Last updated: 2026-01-25*
