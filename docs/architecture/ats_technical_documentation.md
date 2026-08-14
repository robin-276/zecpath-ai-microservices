# Zecpath ATS: Technical Documentation & Developer Guide

**Version:** 1.0.0
**Last Updated:** 2026-08-14

## 1. System Overview

The Zecpath ATS Engine is an AI-powered microservice designed to automate the extraction, semantic evaluation, and ranking of candidate resumes. It utilizes natural language processing (`sentence-transformers`) to score candidates based on contextual relevance rather than rigid keyword matching.

## 2. Developer Setup Guide

### Prerequisites

* Python 3.9+
* Virtual Environment (venv)
* Git

### Installation

1. Clone the repository and navigate to the project root.
2. Activate the virtual environment:
   `venv\Scripts\Activate.ps1` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies:
   `pip install sentence-transformers PyPDF2 scikit-learn`

## 3. Scoring Logic Explanation

The final candidate score is a weighted composite, normalized on a 0-100 scale.

* **Semantic Match (60%):** Vector embeddings of the candidate's experience are compared to the job description using cosine similarity.
* **Experience & Education Formatting (20%):** Validates the structural integrity of the resume (e.g., parsable timelines, explicit degree mentions).
* **Bias Reduction Penalty (Negative Weighting):** If the candidate's resume contains a target keyword density exceeding 15%, the system assumes "keyword stuffing" and deducts 15.0 points from the final score.

## 4. Troubleshooting Notes

* **Issue: Out of Memory (OOM) / RAM Spikes**
  * *Cause:* The `SentenceTransformer` model is loading multiple times.
  * *Fix:* Ensure the `ATSOptimizer.get_model()` Singleton pattern is being utilized instead of instantiating a new model class directly.
* **Issue: Poor Model Performance on First Run**
  * *Cause:* Cold start / Caching missing.
  * *Fix:* The first execution of an embedding requires compiling. Subsequent runs utilize the `@functools.lru_cache`, dropping execution time to microseconds.
* **Issue: Text Sanitization Failing on PDFs**
  * *Cause:* Heavily formatted graphical resumes returning broken unicode (e.g., `\u25E6`).
  * *Fix:* Update the regex patterns in `performance_optimizer.py -> clean_noisy_text()` to strip the newly discovered artifacts.
