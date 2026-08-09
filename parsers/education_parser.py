import re
import json

class EducationParser:
    def __init__(self):
        # 1. Normalization dictionaries to standardize degree naming
        self.degree_mapping = {
            r"\b(bachelor|b\.?a\.?|b\.?sc\.?|b\.?tech\.?|bca)\b": "Bachelor's Degree",
            r"\b(master|m\.?a\.?|m\.?sc\.?|m\.?tech\.?|mca|mba)\b": "Master's Degree",
            r"\b(ph\.?d|doctorate)\b": "Doctorate",
            r"\b(associate)\b": "Associate's Degree",
            r"\b(diploma|certificat(e|ion))\b": "Diploma/Certificate"
        }
        
        # Simple ranking to determine the highest degree achieved
        self.degree_rank = {
            "Doctorate": 5,
            "Master's Degree": 4,
            "Bachelor's Degree": 3,
            "Associate's Degree": 2,
            "Diploma/Certificate": 1,
            "Unknown": 0
        }
        
        # 2. Certification categorization
        self.cert_categories = {
            "cloud": [r"aws", r"azure", r"gcp", r"google cloud"],
            "data_science": [r"machine learning", r"data science", r"ai", r"artificial intelligence"],
            "development": [r"full stack", r"frontend", r"backend", r"web", r"software"]
        }

    def _normalize_degree(self, text):
        text_lower = text.lower()
        for pattern, standard_degree in self.degree_mapping.items():
            if re.search(pattern, text_lower):
                return standard_degree
        return "Unknown"

    def _extract_year(self, text):
        # FIXED: Added ?: for a non-capturing group so it returns the full 4 digits
        years = re.findall(r'\b(?:19|20)\d{2}\b', text)
        if years:
            return int(years[-1]) # Graduation year is usually the last date listed
        return None

    def evaluate_relevance(self, extracted_items, jd_keywords):
        """Tags items as High or Low relevance based on Job Description overlap."""
        jd_lower = jd_keywords.lower()
        for item in extracted_items:
            # Check if words in the certification title exist in the JD
            item['relevance'] = "High" if any(word in jd_lower for word in item['title'].lower().split() if len(word) > 2) else "Low"
        return extracted_items

    def parse_education(self, edu_blocks):
        education_list = []
        for block in edu_blocks:
            degree = self._normalize_degree(block)
            year = self._extract_year(block)
            
            # Heuristic: Find the institution by looking for common academic keywords
            institution = "Unknown"
            for line in block.split('\n'):
                if re.search(r'(university|college|institute|school|skcms)', line, re.IGNORECASE):
                    institution = line.strip()
                    break
            
            education_list.append({
                "raw_text": block.strip().replace('\n', ' '),
                "degree_level": degree,
                "institution": institution,
                "graduation_year": year
            })
        return education_list

    def parse_certifications(self, cert_blocks, jd_keywords):
        cert_list = []
        for block in cert_blocks:
            category = "General"
            for cat, patterns in self.cert_categories.items():
                if any(re.search(p, block.lower()) for p in patterns):
                    category = cat
                    break
            
            year = self._extract_year(block)
            
            cert_list.append({
                "title": block.split('\n')[0].strip(), # Assumes the first line is the certificate name
                "category": category,
                "year": year
            })
            
        return self.evaluate_relevance(cert_list, jd_keywords)

    def process_academic_profile(self, segmented_data, jd_requirements):
        """Main method to compile the Day 11 Deliverable Object."""
        edu_blocks = segmented_data.get("education", [])
        cert_blocks = segmented_data.get("certifications", [])
        
        education_data = self.parse_education(edu_blocks)
        certification_data = self.parse_certifications(cert_blocks, jd_requirements)
        
        # Calculate highest degree
        highest_degree = "Unknown"
        if education_data:
            highest_degree = max(education_data, key=lambda x: self.degree_rank.get(x['degree_level'], 0))['degree_level']
        
        return {
            "academic_summary": {
                "highest_degree": highest_degree,
                "total_certifications": len(certification_data)
            },
            "education": education_data,
            "certifications": certification_data
        }

# Test execution
if __name__ == "__main__":
    # Simulated input from Day 8 Section Segmenter
    sample_segmented_data = {
        "education": [
            "Bachelor of Computer Applications (BCA)\nSKCMS, Kuruppampady (Mahatma Gandhi University)\nMarch 2022 - March 2025"
        ],
        "certifications": [
            "Data Science and Artificial Intelligence\nAVODHA, Ernakulam\n2025"
        ]
    }
    
    target_jd = "Looking for a Data Scientist with a Bachelor's degree and AI/ML experience."
    
    parser = EducationParser()
    result = parser.process_academic_profile(sample_segmented_data, target_jd)
    
    print(json.dumps(result, indent=2))