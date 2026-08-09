import re
import spacy

class ResumeSegmenter:
    def __init__(self):
        # Load lightweight NLP model for named entity recognition (NER)
        self.nlp = spacy.load("en_core_web_sm")
        
        # Rule-based keyword dictionary for standard headers
        self.section_keywords = {
            "experience": [r"\bexperience\b", r"\bemployment\b", r"\bwork history\b", r"\bcareer\b"],
            "education": [r"\beducation\b", r"\bacademic\b", r"\bqualifications\b", r"\bdegree\b"],
            "skills": [r"\bskills\b", r"\bcompetencies\b", r"\btechnologies\b", r"\btechnical\b"],
            "projects": [r"\bprojects\b", r"\bportfolio\b"],
            "certifications": [r"\bcertifications\b", r"\bcertificates\b", r"\blicenses\b"]
        }
        
    def _clean_line(self, line):
        return line.strip().lower()

    def _is_header(self, line):
        """Rule-based: Check if a line is likely a header based on keywords and length."""
        cleaned_line = self._clean_line(line)
        # Headers are usually short and don't contain much punctuation
        if len(cleaned_line) > 40 or len(cleaned_line) < 3:
            return None
            
        for section, patterns in self.section_keywords.items():
            for pattern in patterns:
                if re.search(pattern, cleaned_line):
                    return section
        return None

    def _nlp_fallback_classification(self, text_block):
        """NLP-based: If no header is found, guess the section based on entities."""
        doc = self.nlp(text_block)
        org_count = sum(1 for ent in doc.ents if ent.label_ == "ORG")
        date_count = sum(1 for ent in doc.ents if ent.label_ == "DATE")
        
        # Heuristic: Lots of dates and organizations usually means Experience
        if org_count > 1 and date_count > 1:
            return "experience"
        # Heuristic: Look for degree keywords
        if any(word in text_block.lower() for word in ["bachelor", "master", "phd", "bca", "university"]):
            return "education"
            
        return "summary_or_other"

    def segment(self, raw_text):
        """Main method to segment resume text into categorized blocks."""
        lines = raw_text.split('\n')
        
        segmented_data = {
            "summary_or_other": [],
            "experience": [],
            "education": [],
            "skills": [],
            "projects": [],
            "certifications": []
        }
        
        current_section = "summary_or_other"
        current_block = []

        for line in lines:
            if not line.strip():
                continue
                
            detected_header = self._is_header(line)
            
            if detected_header:
                # Save previous block before switching sections
                if current_block:
                    segmented_data[current_section].append("\n".join(current_block))
                    current_block = []
                current_section = detected_header
            else:
                current_block.append(line)

        # Append the final block
        if current_block:
            # If the block was unassigned, run NLP fallback
            if current_section == "summary_or_other" and len(current_block) > 3:
                guessed_section = self._nlp_fallback_classification(" ".join(current_block))
                segmented_data[guessed_section].append("\n".join(current_block))
            else:
                segmented_data[current_section].append("\n".join(current_block))

        # Clean up empty sections
        return {k: v for k, v in segmented_data.items() if v}

# Test execution
if __name__ == "__main__":
    sample_text = """
    ROBIN JOSE
    Innovative Software Developer
    
    SKILLS
    Python, TensorFlow, Django, SQL
    
    WORK EXPERIENCE
    AI & ML Intern - SINRO ROBOTICS
    Worked on machine learning models and data classification.
    
    EDUCATION
    Bachelor of Computer Applications
    SKCMS, Mahatma Gandhi University
    """
    
    segmenter = ResumeSegmenter()
    output = segmenter.segment(sample_text)
    
    import json
    print(json.dumps(output, indent=2))