# EU AI Act Compliance Examples

Practical examples of compliance implementation by use case.

## Example 1: Customer Service Chatbot (Limited Risk)

### Classification

- **Risk Level:** Limited
- **Article:** 50 (Transparency)
- **Deadline:** August 2026

### Requirements

1. Disclose AI nature to users
2. No emotion recognition without consent
3. Clear escalation to human

### Implementation

```python
# Chatbot disclosure implementation

class ChatbotService:
    DISCLOSURE_MESSAGE = (
        "You are chatting with an AI assistant. "
        "Type 'human' at any time to speak with a person."
    )

    def start_conversation(self, user_id: str) -> dict:
        """Start conversation with required disclosure."""
        return {
            "type": "disclosure",
            "message": self.DISCLOSURE_MESSAGE,
            "timestamp": datetime.utcnow().isoformat(),
            "user_acknowledged": False
        }

    def process_message(self, user_id: str, message: str) -> dict:
        if message.lower() == "human":
            return self._escalate_to_human(user_id)
        return self._generate_response(message)
```

### Documentation Required

- System description
- Disclosure mechanism
- Escalation procedures
- User consent records

---

## Example 2: Resume Screening AI (High Risk)

### Classification

- **Risk Level:** High (Annex III - Employment)
- **Articles:** 9-15, 17, 43
- **Deadline:** August 2026

### Requirements

Full compliance including:
- Risk management system
- Bias testing and mitigation
- Human oversight
- Technical documentation
- Conformity assessment

### Implementation

```python
# Resume screening with EU AI Act compliance

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CandidateEvaluation:
    candidate_id: str
    score: float
    confidence: float
    features_used: list[str]
    explanation: str
    bias_metrics: dict
    human_review_required: bool
    timestamp: datetime

class ResumeScreener:
    def __init__(self):
        self.risk_manager = RiskManager()
        self.bias_detector = BiasDetector()
        self.logger = ComplianceLogger()

    def evaluate(self, resume: dict, job_req: dict) -> CandidateEvaluation:
        """Evaluate resume with full compliance logging."""

        # Article 12: Automatic logging
        self.logger.log_input(resume, job_req)

        # Article 9: Risk assessment
        risk_check = self.risk_manager.assess(resume)
        if risk_check.requires_intervention:
            return self._flag_for_human_review(resume, risk_check)

        # Core evaluation
        score, features, confidence = self._score_resume(resume, job_req)

        # Article 10: Bias detection
        bias_metrics = self.bias_detector.analyze(
            score=score,
            features=features,
            protected_attributes=["gender", "age", "ethnicity"]
        )

        # Article 14: Human oversight threshold
        human_review = (
            confidence < 0.7 or
            bias_metrics["disparity_score"] > 0.1
        )

        # Article 13: Explainability
        explanation = self._generate_explanation(features)

        evaluation = CandidateEvaluation(
            candidate_id=resume["id"],
            score=score,
            confidence=confidence,
            features_used=features,
            explanation=explanation,
            bias_metrics=bias_metrics,
            human_review_required=human_review,
            timestamp=datetime.utcnow()
        )

        # Article 12: Log output
        self.logger.log_output(evaluation)

        return evaluation

class BiasDetector:
    """Article 10: Data governance and bias detection."""

    PROTECTED_ATTRIBUTES = ["gender", "age", "ethnicity", "disability"]

    def analyze(self, score: float, features: list,
                protected_attributes: list) -> dict:
        """Detect potential bias in evaluation."""
        return {
            "disparity_score": self._calculate_disparity(features),
            "protected_correlation": self._check_correlation(
                features, protected_attributes
            ),
            "fairness_metrics": self._compute_fairness_metrics(score)
        }

class ComplianceLogger:
    """Article 12: Automatic event logging."""

    def log_input(self, resume: dict, job_req: dict):
        """Log inputs with PII protection."""
        self._store_event({
            "type": "input",
            "timestamp": datetime.utcnow().isoformat(),
            "resume_hash": self._hash_pii(resume),
            "job_id": job_req["id"]
        })

    def log_output(self, evaluation: CandidateEvaluation):
        """Log outputs for traceability."""
        self._store_event({
            "type": "output",
            "timestamp": evaluation.timestamp.isoformat(),
            "candidate_id": evaluation.candidate_id,
            "score": evaluation.score,
            "human_review": evaluation.human_review_required
        })
```

### Bias Testing Results (Example)

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Gender parity | 0.95 | > 0.8 | Pass |
| Age correlation | 0.02 | < 0.1 | Pass |
| Ethnicity disparity | 0.08 | < 0.1 | Pass |

### Human Oversight Protocol

1. All candidates scoring 70-85 reviewed by HR
2. All rejections require human confirmation
3. Weekly bias audit reports
4. Quarterly external audit

---

## Example 3: Medical Diagnosis AI (High Risk)

### Classification

- **Risk Level:** High (CE-marked medical device)
- **Articles:** 9-15, 17, 43
- **Deadline:** August 2027 (extended for regulated products)

### Requirements

- Medical device regulation compliance
- Clinical validation
- Full technical documentation
- Notified body conformity assessment

### Implementation Architecture

```
Patient Data
    |
    v
[De-identification] --> [Compliance Logger]
    |
    v
[Risk Assessment]
    |
    v
[AI Diagnosis Model]
    |
    v
[Confidence Check] ---> [Human Review Queue]
    |                          |
    v                          v
[Explanation Engine]     [Physician Review]
    |                          |
    v                          v
[Final Diagnosis] <------------+
    |
    v
[Audit Trail]
```

### Key Compliance Features

```python
class MedicalDiagnosisAI:
    # Article 15: Accuracy requirements
    MINIMUM_ACCURACY = 0.95
    CONFIDENCE_THRESHOLD = 0.85

    # Article 14: Mandatory human oversight
    ALWAYS_REQUIRE_PHYSICIAN_REVIEW = True

    def diagnose(self, patient_data: dict) -> DiagnosisResult:
        """Generate diagnosis with mandatory human oversight."""

        # Never provide diagnosis without physician review
        result = self._model_inference(patient_data)

        return DiagnosisResult(
            suggestion=result.diagnosis,
            confidence=result.confidence,
            explanation=self._generate_clinical_explanation(result),
            status="pending_physician_review",
            disclaimer=(
                "This AI-generated suggestion requires review and "
                "confirmation by a qualified healthcare professional."
            )
        )
```

---

## Example 4: Content Moderation AI (Limited Risk)

### Classification

- **Risk Level:** Limited
- **Key Requirement:** Transparency when AI makes decisions

### Implementation

```python
class ContentModerator:
    def moderate(self, content: dict) -> ModerationResult:
        """Moderate content with transparency."""

        result = self._analyze_content(content)

        if result.action in ["remove", "restrict"]:
            # Transparency: Inform user of AI decision
            return ModerationResult(
                action=result.action,
                reason=result.reason,
                ai_disclosure=(
                    "This content was flagged by an automated system. "
                    "You may appeal this decision for human review."
                ),
                appeal_available=True
            )

        return result
```

---

## Example 5: Deepfake / Synthetic Content (Limited Risk)

### Classification

- **Risk Level:** Limited
- **Article:** 50.4 (Synthetic content labeling)

### Requirements

1. Machine-readable watermarks
2. Human-perceptible disclosure
3. Content authenticity metadata

### Implementation

```python
from PIL import Image
import hashlib

class SyntheticContentLabeler:
    """Article 50.4: Label AI-generated content."""

    WATERMARK_KEY = "EU_AI_ACT_SYNTHETIC"

    def label_image(self, image: Image, metadata: dict) -> Image:
        """Add compliant watermark to AI-generated image."""

        # Machine-readable watermark (C2PA standard)
        watermarked = self._add_c2pa_manifest(image, {
            "ai_generated": True,
            "generator": metadata.get("model"),
            "timestamp": datetime.utcnow().isoformat(),
            "organization": metadata.get("org")
        })

        # Visual disclosure (optional but recommended)
        if metadata.get("add_visual_label"):
            watermarked = self._add_visual_label(
                watermarked,
                "AI Generated"
            )

        return watermarked

    def label_text(self, text: str, metadata: dict) -> dict:
        """Label AI-generated text content."""
        return {
            "content": text,
            "metadata": {
                "ai_generated": True,
                "model": metadata.get("model"),
                "timestamp": datetime.utcnow().isoformat(),
                "hash": hashlib.sha256(text.encode()).hexdigest()
            }
        }
```

---

## Example 6: Credit Scoring AI (High Risk)

### Classification

- **Risk Level:** High (Essential services)
- **Additional:** Consumer protection laws apply

### Implementation

```python
class CreditScoringAI:
    """High-risk credit scoring with full compliance."""

    def score(self, applicant: dict) -> CreditScore:
        # Article 10: No prohibited data sources
        clean_data = self._remove_prohibited_features(applicant, [
            "ethnicity",
            "religion",
            "political_affiliation",
            "sexual_orientation"
        ])

        # Core scoring
        score = self._calculate_score(clean_data)

        # Article 13: Mandatory explanation
        explanation = self._generate_explanation(
            score=score,
            factors=self._get_top_factors(clean_data),
            adverse_reasons=self._get_adverse_reasons(score)
        )

        # Article 14: Human review for edge cases
        human_review = score.confidence < 0.8 or score.is_edge_case

        return CreditScore(
            value=score.value,
            explanation=explanation,
            factors=score.factors,
            human_review_required=human_review,
            appeal_instructions=self._get_appeal_instructions()
        )
```

---

## Anti-Patterns to Avoid

### 1. Hidden AI Use

```python
# WRONG: No disclosure
def respond_to_customer(message):
    return ai_model.generate(message)

# CORRECT: With disclosure
def respond_to_customer(message):
    response = ai_model.generate(message)
    return {
        "message": response,
        "disclosure": "This response was generated by an AI assistant."
    }
```

### 2. Emotion Recognition Without Consent

```python
# WRONG: Silent emotion detection
def analyze_call(audio):
    transcript = transcribe(audio)
    sentiment = detect_emotions(audio)  # Violation!
    return {"transcript": transcript, "sentiment": sentiment}

# CORRECT: With explicit consent
def analyze_call(audio, consent_given: bool):
    transcript = transcribe(audio)
    if consent_given:
        sentiment = detect_emotions(audio)
        return {"transcript": transcript, "sentiment": sentiment}
    return {"transcript": transcript}
```

### 3. No Human Oversight

```python
# WRONG: Fully automated high-stakes decision
def auto_reject_application(application):
    if score(application) < 0.5:
        reject(application)  # Violation!

# CORRECT: Human in the loop
def evaluate_application(application):
    score = calculate_score(application)
    if score < 0.5:
        queue_for_human_review(application, reason="low_score")
    return score
```

---

*ML Engineer Methodology - faion-network*
