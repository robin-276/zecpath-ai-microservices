# Semantic Matching Engine Accuracy Report

**Date:** 2026-08-09
**Model:** `all-MiniLM-L6-v2` (Sentence-Transformers)
**Methodology:** Dense Vector Embeddings + Cosine Similarity

## Tuning Similarity Thresholds

* **0.80 - 1.00:** Near-perfect match (Often indicates copied JD text).
* **0.65 - 0.79:** Strong match (Conceptually aligned skills and experience).
* **0.40 - 0.64:** Partial match (Has some overlapping concepts, lacks depth).
* **0.00 - 0.39:** Poor match (Irrelevant background).

*Current Platform Passing Threshold set to: **0.65***

## Validation Across Job Types

| Job Category             | Candidate Background      | Overall Match Score | Engine Decision | Human Review Alignment             |
| :----------------------- | :------------------------ | :------------------ | :-------------- | :--------------------------------- |
| **Data Scientist** | ML, Python, TensorFlow    | 0.725               | Shortlisted     | Yes - Concepts align perfectly     |
| **Backend Dev**    | Node.js, Express, MongoDB | 0.210               | Rejected        | Yes - Completely different stack   |
| **Data Analyst**   | Excel, Tableau, SQL       | 0.540               | Rejected        | Yes - Close, but lacks advanced ML |

## Next Steps

* Monitor production data to see if the `0.65` threshold is too strict (rejecting good candidates) or too loose (passing unqualified candidates).
