---
# Zecpath Storage Structure

This document outlines where and how different types of data are stored across the Zecpath microservices platform.

## 1. Raw Resumes & Documents (Blob Storage)
*   **Format:** Binary files (`.pdf`, `.docx`).
*   **Storage Location:** `data/raw/` (Development) -> AWS S3 / Cloud Storage (Production).
*   **Purpose:** Immutable original source of truth. These files are never modified after the initial upload.

## 2. Parsed Profiles & Job Descriptions (Document Storage)
*   **Format:** `.json` or NoSQL documents (e.g., MongoDB).
*   **Storage Location:** `data/parsed/` -> Document Database.
*   **Purpose:** Fast, flexible reading for the AI engines. Contains normalized text, arrays of skills, and extracted work history ready for AI consumption.

## 3. ATS Scores (Relational Storage)
*   **Format:** Relational tables (PostgreSQL/MySQL).
*   **Data Points:** Weighted scores (0.0 to 1.0) for skills match, experience match, and overall suitability.
*   **Purpose:** Fast querying, sorting, and filtering for human recruiters to view top candidates instantly on a leaderboard.

## 4. Screening Reports & Interview Results
*   **Format:** `.json` containing conversational transcripts and NLP sentiment scores. Associated audio files saved to Blob Storage.
*   **Purpose:** Complete audit trail of the AI's conversation and technical evaluation of the candidate.

---
