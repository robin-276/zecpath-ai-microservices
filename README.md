# Zecpath AI Microservices

Professional AI development environment and scalable project structure for the Zecpath platform.

## Project Structure

- `data/`: Sample data and test documents.
- `parsers/`: Resume text extraction and parsing routines.
- `ats_engine/`: Candidate scoring and resume matching algorithms.
- `screening_ai/`: Outbound voice call logic and eligibility evaluation.
- `interview_ai/`: HR, technical, and machine test interview engines.
- `scoring/`: Score aggregation, decision algorithms, and offer intelligence.
- `utils/`: Shared utilities including the logging framework.
- `tests/`: Automated unit tests.

## How to Run

1. **Activate Environment:**

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
2. # Zecpath AI Microservices

   Professional AI development environment and scalable project structure for the Zecpath platform.

   ## Project Structure


   - `data/`: Sample data and test documents.
   - `parsers/`: Resume text extraction (PDF/DOCX) and Job Description parsing routines.
   - `ats_engine/`: Candidate scoring and resume matching algorithms.
   - `screening_ai/`: Outbound voice call logic and eligibility evaluation.
   - `interview_ai/`: HR, technical, and machine test interview engines.
   - `scoring/`: Score aggregation, decision algorithms, and offer intelligence.
   - `utils/`: Shared utilities including the custom logging framework.
   - `tests/`: Automated unit tests for all microservices.

   ## Core Features

   * **Centralized Logging:** Custom logger outputting to both the console and local log files for robust debugging.
   * **Resume Extractor:** Extracts, cleans, and normalizes raw candidate text from unstructured PDF and DOCX files.
   * **Job Description Parser:** Translates unstructured job description paragraphs into structured, machine-readable JSON formats. Utilizes Regex and predefined tech dictionaries to normalize acronyms (e.g., "ML" to "machine learning") and extract exact experience/education requirements.

   ## How to Run

   ### 1. Activate Environment

   Always ensure your virtual environment is active before running scripts or installing packages.

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
