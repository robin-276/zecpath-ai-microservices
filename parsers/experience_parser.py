import re
import json
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ExperienceAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def _parse_dates(self, date_string):
        """Extracts start and end years/months from a string."""
        years = [int(y) for y in re.findall(r'\b(20\d{2})\b', date_string)]
        
        start_year = years[0] if len(years) > 0 else datetime.now().year
        
        if "present" in date_string.lower() or "current" in date_string.lower():
            end_year = datetime.now().year
        else:
            end_year = years[1] if len(years) > 1 else start_year
            
        return start_year, end_year

    def calculate_relevance(self, role_description, jd_text):
        """Calculates how closely the past role matches the new job requirements."""
        if not role_description or not jd_text:
            return 0.0
            
        try:
            tfidf_matrix = self.vectorizer.fit_transform([role_description, jd_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return round(similarity, 2)
        except ValueError:
            return 0.0

    def analyze_timeline(self, roles):
        """Detects gaps, overlaps, and calculates total unique experience."""
        if not roles:
            return 0, False, False

        # Sort roles by start year
        roles.sort(key=lambda x: x['start_year'])
        
        total_years = 0
        has_gaps = False
        has_overlaps = False
        
        current_end = roles[0]['start_year']
        
        for role in roles:
            start = role['start_year']
            end = role['end_year']
            
            if start < current_end:
                has_overlaps = True
                # Add only the non-overlapping portion
                if end > current_end:
                    total_years += (end - current_end)
                    current_end = end
            else:
                if start > current_end:
                    has_gaps = True
                total_years += (end - start)
                current_end = end
                
        # Handle cases where duration is less than a year
        if total_years == 0 and len(roles) > 0:
            total_years = 0.5 
            
        return total_years, has_gaps, has_overlaps

    def process_experience(self, extracted_roles, target_jd):
        """Main method to compile the Day 10 Deliverable Object."""
        processed_roles = []
        
        for role in extracted_roles:
            start_year, end_year = self._parse_dates(role.get('date_string', ''))
            
            # Combine title and description for NLP scoring
            role_text = f"{role.get('title', '')} {role.get('description', '')}"
            relevance = self.calculate_relevance(role_text, target_jd)
            
            processed_roles.append({
                "company": role.get('company', 'Unknown'),
                "job_title": role.get('title', 'Unknown'),
                "start_year": start_year,
                "end_year": end_year,
                "duration_years": end_year - start_year if end_year > start_year else 0.5,
                "relevance_score": relevance
            })

        total_exp, has_gaps, has_overlaps = self.analyze_timeline(processed_roles)
        
        # Calculate adjusted relevant experience (Weighting years by relevance score)
        adjusted_years = sum(r['duration_years'] * r['relevance_score'] for r in processed_roles)

        return {
            "summary": {
                "total_experience_years": total_exp,
                "adjusted_relevant_years": round(adjusted_years, 2),
                "has_gaps": has_gaps,
                "has_overlaps": has_overlaps
            },
            "roles": processed_roles
        }

# Test execution
if __name__ == "__main__":
    sample_roles = [
        {
            "company": "SINRO ROBOTICS",
            "title": "AI & ML Intern",
            "date_string": "Jan 2026 - Feb 2026",
            "description": "Worked on machine learning models and data classification."
        },
        {
            "company": "Freelance",
            "title": "Python Developer",
            "date_string": "2025 - Present",
            "description": "Built backend APIs using Django and Python."
        }
    ]
    
    target_job = "Looking for a Data Scientist with Machine Learning experience. Python skills required."
    
    analyzer = ExperienceAnalyzer()
    output = analyzer.process_experience(sample_roles, target_job)
    
    print(json.dumps(output, indent=2))