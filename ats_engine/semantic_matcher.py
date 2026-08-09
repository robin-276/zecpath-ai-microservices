import json
from sentence_transformers import SentenceTransformer, util

class SemanticMatcher:
    def __init__(self):
        # Loads a lightweight, fast, and highly accurate embedding model
        # The first run will download an ~80MB model to your local machine
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Tuning similarity thresholds (Adjustable based on HR feedback)
        self.passing_threshold = 0.65

    def get_similarity(self, text1, text2):
        """Converts two text blocks into embeddings and calculates cosine similarity."""
        if not text1 or not text2:
            return 0.0
            
        # Convert text to dense vector embeddings
        embedding1 = self.model.encode(text1, convert_to_tensor=True)
        embedding2 = self.model.encode(text2, convert_to_tensor=True)
        
        # Calculate cosine similarity (-1.0 to 1.0)
        cosine_score = util.cos_sim(embedding1, embedding2).item()
        
        # Ensure it doesn't return negative values for completely unrelated text
        return round(max(0.0, cosine_score), 3)

    def match_profile(self, candidate_data, jd_data):
        """Measures semantic similarity across distinct resume sections."""
        
        # 1. Skill Matching
        cand_skills = " ".join(candidate_data.get("skills", []))
        jd_skills = " ".join(jd_data.get("required_skills", []))
        skill_score = self.get_similarity(cand_skills, jd_skills)

        # 2. Experience Matching
        cand_exp = " ".join([exp.get("role_snippet", "") for exp in candidate_data.get("experience", [])])
        jd_exp = jd_data.get("experience_requirements", "")
        exp_score = self.get_similarity(cand_exp, jd_exp)

        # 3. Project Matching
        cand_proj = " ".join(candidate_data.get("projects", []))
        # If JD doesn't specify project requirements, fallback to general experience requirements
        jd_proj = jd_data.get("project_requirements", jd_exp) 
        proj_score = self.get_similarity(cand_proj, jd_proj)

        # 4. Overall Weighted Score
        # Weighting: Skills (40%), Experience (40%), Projects (20%)
        overall_score = (skill_score * 0.4) + (exp_score * 0.4) + (proj_score * 0.2)

        return {
            "candidate_id": candidate_data.get("candidate_id", "unknown"),
            "scores": {
                "skills_match": skill_score,
                "experience_match": exp_score,
                "projects_match": proj_score,
                "overall_match": round(overall_score, 3)
            },
            "evaluation": {
                "threshold_passed": overall_score >= self.passing_threshold,
                "status": "Shortlisted" if overall_score >= self.passing_threshold else "Rejected"
            }
        }

# Test execution
if __name__ == "__main__":
    # Simulated structured data from previous pipeline steps
    sample_candidate = {
        "candidate_id": "cnd-001",
        "skills": ["Python", "TensorFlow", "scikit-learn", "Pandas"],
        "experience": [{"role_snippet": "Developed predictive machine learning models for semiconductor defect classification, achieving 96% accuracy using Random Forest."}],
        "projects": ["Built a fake news detection NLP pipeline handling large text datasets."]
    }

    sample_jd = {
        "required_skills": ["Python", "Machine Learning", "NLP", "Data Science"],
        "experience_requirements": "Looking for a data scientist with experience building and fine-tuning predictive models and handling text datasets.",
        "project_requirements": "Experience with natural language processing projects is a plus."
    }

    matcher = SemanticMatcher()
    result = matcher.match_profile(sample_candidate, sample_jd)
    
    print(json.dumps(result, indent=2))