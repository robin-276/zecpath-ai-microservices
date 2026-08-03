---
### File 4: `04_retraining_lifecycle.md`
**Location:** `docs/architecture/04_retraining_lifecycle.md`
**Content:** Copy and paste everything below.

```markdown
# AI Data Lifecycle & Retraining Strategy

This document defines how candidate data flows from ingestion to a final decision, and how the platform learns from those decisions over time.

## 1. Ingestion & Transformation
Data enters the system as unstructured text (PDF/DOCX). The parsing microservices immediately assign a `candidate_id` and convert the document to structured JSON. The raw file is archived securely.

## 2. Evaluation Pipeline
Candidate data moves sequentially through the ATS Engine, Screening AI, and Interview AI. Each microservice appends its findings to the candidate's master JSON record and logs its specific `model_version` in the metadata.

## 3. Decision & Archival
The scoring module aggregates the pipeline data. The final output is flagged as `Hired`, `Rejected`, or `Talent Pool`.

## 4. Retraining Strategy (The Feedback Loop)
To ensure continuous improvement, Zecpath utilizes a feedback loop:
*   **Data Collection:** The system aggregates discrepancies (e.g., candidates scored highly by the ATS AI but rejected by human HR post-interview).
*   **Versioning:** Datasets are snapshotted monthly (e.g., `dataset_v2026_08`). 
*   **Retraining:** Models are periodically fine-tuned on this discrepancy data to improve accuracy and reduce bias. 
*   **Deployment:** Updated models are deployed with a new semantic version number, ensuring all future predictions are trackable against the new version.
---
