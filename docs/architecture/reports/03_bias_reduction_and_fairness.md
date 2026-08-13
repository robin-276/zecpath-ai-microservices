# Zecpath ATS: Bias Reduction & Fairness Strategy

**Date:** 2026-08-13
**Module:** `ats_engine/bias_reducer.py`

## 1. Masking Non-Essential Personal Attributes

To prevent both subconscious human bias and algorithmic bias, the Zecpath extraction pipeline utilizes a masking engine prior to semantic evaluation.

* **Redacted Data:** Email addresses, phone numbers, gendered pronouns, and explicit dates of birth are stripped and replaced with neutral bracketed tags (e.g., `[EMAIL_REDACTED]`).
* **Impact:** Ensures the candidate is judged strictly on their project history, skills, and experience rather than demographic identifiers.

## 2. Reducing Keyword Over-Dependence

Traditional ATS engines fail when candidates "keyword stuff" (pasting a block of invisible text containing buzzwords). Zecpath counters this by:

* **Relying on Semantic Matching:** Day 12's `sentence-transformers` evaluate the *context* of the experience, meaning exact keywords are no longer strictly necessary to score highly.
* **Density Penalties:** If the `bias_reducer.py` detects a keyword density exceeding 10% or 15% of the total word count, it assumes manipulation and applies a flat penalty (-5 or -15 points) to the normalized score.

## 3. Scoring Normalization

Scores across different job descriptions are normalized to a strict `0.00 - 100.00` scale. This standardizes resume evaluation, allowing recruiters to compare the relative strength of candidates across entirely different departments (e.g., comparing the strength of a Software Engineering applicant against a Data Analyst applicant).
