import re
import json

class BiasReducer:
    def __init__(self):
        # Regex patterns to identify and mask personal attributes that could trigger subconscious or algorithmic bias
        self.patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
            "phone": r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
            "pronouns": r'\b(he|him|his|she|her|hers)\b',
            "dob_format": r'\b(19|20)\d{2}[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12][0-9]|3[01])\b'
        }

    def mask_personal_info(self, raw_text):
        """Replaces identifying personal data with neutral tags."""
        if not raw_text:
            return ""
        
        masked_text = raw_text
        masked_text = re.sub(self.patterns['email'], '[EMAIL_REDACTED]', masked_text)
        masked_text = re.sub(self.patterns['phone'], '[PHONE_REDACTED]', masked_text)
        masked_text = re.sub(self.patterns['pronouns'], '[PRONOUN]', masked_text, flags=re.IGNORECASE)
        masked_text = re.sub(self.patterns['dob_format'], '[DOB_REDACTED]', masked_text)
        
        return masked_text

    def detect_keyword_stuffing(self, total_word_count, target_keyword_count):
        """
        Calculates keyword density to reduce over-dependence on keywords.
        Returns a penalty score if the candidate is attempting to 'game' the ATS.
        """
        if total_word_count == 0:
            return 0.0
            
        density = target_keyword_count / total_word_count
        
        # If keywords make up an unnaturally high percentage of the resume
        if density > 0.15: # > 15% density
            return 15.0    # 15 point penalty
        elif density > 0.10: # > 10% density
            return 5.0     # 5 point penalty
            
        return 0.0

    def normalize_score(self, raw_score, text_length, matched_keywords):
        """Applies fairness normalization and outputs a standard 0-100 score."""
        # 1. Cap raw score at 100 maximum
        normalized = min(float(raw_score), 100.0)
        
        # 2. Evaluate and apply keyword stuffing penalties
        penalty = self.detect_keyword_stuffing(text_length, matched_keywords)
        normalized = max(0.0, normalized - penalty)
        
        return {
            "original_score": round(raw_score, 2),
            "keyword_stuffing_penalty": penalty,
            "final_normalized_score": round(normalized, 2)
        }

# Test execution
if __name__ == "__main__":
    reducer = BiasReducer()
    
    # 1. Test Masking Logic
    sample_text = "Contact candidate at test.candidate@email.com or +91-9876543210. She is an experienced developer born on 1998-04-20."
    masked_output = reducer.mask_personal_info(sample_text)
    
    # 2. Test Normalization & Keyword Stuffing Logic
    # Scenario: Candidate achieved a 98.5 score, but their 200-word resume contained 35 target keywords (17.5% density).
    fairness_results = reducer.normalize_score(raw_score=98.5, text_length=200, matched_keywords=35)
    
    output = {
        "masking_engine": {
            "original_text": sample_text,
            "masked_text": masked_output
        },
        "scoring_normalization": fairness_results
    }
    
    print(json.dumps(output, indent=2))