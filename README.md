
# Zecpath AI Microservices

Professional AI development environment and scalable project structure for the Zecpath platform.[cite: 1]

## Project Structure

- `data/`: Sample data and test documents.[cite: 1]
- `docs/`: Architecture reports and semantic matching accuracy tracking.
- `parsers/`: Resume text extraction (PDF/DOCX) and Job Description parsing routines.[cite: 1]
- `ats_engine/`: Candidate scoring and resume matching algorithms.[cite: 1]
- `screening_ai/`: Outbound voice call logic and eligibility evaluation.[cite: 1]
- `interview_ai/`: HR, technical, and machine test interview engines.[cite: 1]
- `scoring/`: Score aggregation, decision algorithms, and offer intelligence.[cite: 1]
- `utils/`: Shared utilities including the custom logging framework.[cite: 1]
- `tests/`: Automated unit tests for all microservices.[cite: 1]

## Core Features (Days 1 - 12)

* **Centralized Logging:** Custom logger outputting to both the console and local log files for robust debugging.[cite: 1]
* **Resume Extractor:** Extracts, cleans, and normalizes raw candidate text from unstructured PDF and DOCX files.[cite: 1]
* **Job Description Parser:** Translates unstructured job description paragraphs into structured, machine-readable JSON formats. Utilizes Regex and predefined tech dictionaries to normalize acronyms (e.g., "ML" to "machine learning") and extract exact experience/education requirements.[cite: 1]
* **Section Segmenter:** Intelligently divides unstructured resume text into distinct logical blocks (Skills, Experience, Education, Certifications).
* **Skills Parser:** Extracts technical skills and assigns confidence scores based on contextual text analysis.
* **Experience Relevance Engine:** Calculates exact employment durations, detects timeline gaps and overlapping roles, and uses NLP (TF-IDF Cosine Similarity) to calculate the relevance of past roles to target job descriptions.
* **Education & Certification Parser:** Normalizes diverse academic degrees (e.g., converting "BCA" to a standard "Bachelor's Degree") and tags certifications with relevance categories based on job requirements.
* **Semantic Matching Engine:** Utilizes the `sentence-transformers` library (`all-MiniLM-L6-v2` model) to generate dense vector embeddings. This allows for deep semantic resume-to-job matching, bypassing the limitations of exact keyword matching.

## How to Run

### 1. Activate Environment

Always ensure your virtual environment is active before running scripts or installing packages.[cite: 1]

```powershell
.\venv\Scripts\Activate.ps1
```
