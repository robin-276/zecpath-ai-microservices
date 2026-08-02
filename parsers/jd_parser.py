import re
import json

class JobDescriptionParser:
    def __init__(self):
        # A foundational dictionary to map skill abbreviations to standard names
        self.skill_synonyms = {
            "js": "javascript",
            "ml": "machine learning",
            "aws": "amazon web services",
            "nlp": "natural language processing",
            "db": "database"
        }
        
        # A master list of trackable skills (this can later be moved to a Postgres DB)
        self.known_skills = {
            "python", "javascript", "react", "fastapi", "django", 
            "machine learning", "deep learning", "mongodb", "postgresql", 
            "amazon web services", "docker", "kubernetes", "natural language processing", 
            "sql", "pandas", "numpy"
        }
        
        # Education indicators
        self.edu_keywords = ["bachelor", "bachelors", "master", "masters", "phd", "bca", "b.tech", "degree"]

    def normalize_text(self, text: str) -> str:
        """Cleans jd text and normalizes skill synonyms."""
        text = text.lower()
        # Remove special characters but keep plus signs (e.g., C++) and spaces
        text = re.sub(r'[^a-z0-9\s\+]', ' ', text)
        
        # Replace synonyms
        words = text.split()
        normalized_words = [self.skill_synonyms.get(w, w) for w in words]
        return ' '.join(normalized_words)

    def extract_skills(self, normalized_text: str) -> list:
        """Finds known skills within the JD text."""
        found_skills = set()
        for skill in self.known_skills:
            if re.search(rf'\b{skill}\b', normalized_text):
                found_skills.add(skill)
        return list(found_skills)

    def extract_experience(self, text: str) -> str:
        """Uses Regex to find experience requirements like '3-5 years' or '2+ years'."""
        match = re.search(r'(\d+)\s*[-+to]*\s*(\d+)?\s*(years|yrs)\s*(?:of experience)?', text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
        return "Not explicitly specified"

    def extract_education(self, text: str) -> list:
        """Extracts required education levels."""
        found_edu = set()
        for edu in self.edu_keywords:
            if re.search(rf'\b{edu}\b', text, re.IGNORECASE):
                found_edu.add(edu.capitalize())
        return list(found_edu)

    def parse(self, role_name: str, jd_text: str) -> dict:
        """Compiles all extractions into a structured AI-friendly object."""
        normalized_jd = self.normalize_text(jd_text)
        
        job_profile = {
            "role_name": role_name,
            "raw_text_length": len(jd_text),
            "requirements": {
                "experience": self.extract_experience(jd_text),
                "education": self.extract_education(jd_text),
                "skills": self.extract_skills(normalized_jd)
            }
        }
        return job_profile

    def to_json(self, job_profile: dict) -> str:
        """Converts the python dictionary to a JSON string for the AI or Database."""
        return json.dumps(job_profile, indent=4)