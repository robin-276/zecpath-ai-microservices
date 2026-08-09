# Section Detection Accuracy Report - v1.0

**Date:** 2026-08-04
**Model Version:** Rule-based Regex + spaCy NER fallback

## Test Dataset

* Total Resumes Tested: 10
* Formats Included: Standard one-column, Two-column tables, No-header narratives.

## Results Breakdown

| Section Category     | Expected | Successfully Extracted | Accuracy | Notes                                                                     |
| :------------------- | :------- | :--------------------- | :------- | :------------------------------------------------------------------------ |
| **Skills**     | 10       | 9                      | 90%      | Failed on a table-based format where skills were in the left margin.      |
| **Experience** | 10       | 10                     | 100%     | NLP fallback successfully caught 1 resume missing an "Experience" header. |
| **Education**  | 10       | 9                      | 90%      |                                                                           |
| **Projects**   | 6        | 5                      | 83%      |                                                                           |

## Known Limitations & Next Steps

1. **Tables & Columns:** `pdfplumber` sometimes reads across columns horizontally instead of vertically.
   * *Fix Action:* Update `extractor.py` to use `layout=True` or bounding box extraction before passing text to the `section_segmenter.py`.
2. **Missing Headings:** spaCy NER struggles if dates are completely missing from the experience block.
