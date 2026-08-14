# ATS Engine: Improvement Backlog

**Date:** 2026-08-14

Based on the Day 17 system testing, the following items have been added to the engineering backlog for future optimization:

## High Priority

1. **Implicit Skill Extraction:** Currently, if a candidate lists "Django and PHP" but forgets to explicitly write "Python", the keyword engine might penalize them. The engine needs to understand that Django implies Python.
2. **Creative Resume OCR Failures:** Highly designed, multi-column PDF resumes (often used by designers and marketers) occasionally cause the `section_segmenter.py` to mix up the Skills and Experience blocks. Implement a more robust layout-aware PDF parser.

## Medium Priority

3. **Non-Tech Metric Tuning:** Sales and HR roles rely heavily on soft skills and quantifiable metrics (e.g., "Increased revenue by 30%"). The Semantic Matcher needs specific weights to prioritize these metrics over strict timeline gaps for non-tech roles.
4. **Handling Typographical Errors:** Improve robustness against misspelled technical terms (e.g., "TensorFlow" vs "TenorFlow" or "scikit-learn" vs "SKlearn").

## Low Priority

5. **Dynamic Thresholds:** Instead of hardcoding the `75.0` shortlist threshold, allow the API to dynamically lower the threshold to `65.0` if a job post receives very few applicants.
