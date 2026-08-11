import json

class ATSScoringEngine:
    def __init__(self):
        # Configurable weight system: Different roles prioritize different metrics.
        # Weights must always add up to 1.0 (100%)
        self.role_weights = {
            "Data Scientist": {
                "skill_match": 0.40, 
                "experience_relevance": 0.30, 
                "education_alignment": 0.10, 
                "semantic_similarity": 0.20
            },
            "Software Engineer": {
                "skill_match": 0.45, 
                "experience_relevance": 0.35, 
                "education_alignment": 0.05, 
                "semantic_similarity": 0.15
            },
            "Default": {
                "skill_match": 0.35, 
                "experience_relevance": 0.35, 
                "education_alignment": 0.10, 
                "semantic_similarity": 0.20
            }
        }

    def _get_weights(self, role):
        """Fetches the specific weight configuration for the target role."""
        return self.role_weights.get(role, self.role_weights["Default"])

    def calculate_score(self, candidate_id, role, metrics):
        """Generates a final explainable score out of 100."""
        weights = self._get_weights(role)
        
        explanation = []
        total_score = 0.0
        
        # Iterate through the expected metrics based on the weight config
        for category, weight in weights.items():
            # Get the candidate's score for this category
            raw_score = metrics.get(category)
            
            # Handle Missing Data: If a section wasn't found in the resume, penalize safely
            if raw_score is None:
                explanation.append(f"[ALERT] Missing data for '{category}'. Score set to 0.00.")
                raw_score = 0.0
            
            # Apply the weight multiplier
            weighted_score = raw_score * weight
            total_score += weighted_score
            
            # Build explainable, human-readable output
            category_name = category.replace('_', ' ').title()
            explanation.append(
                f"{category_name}: Scored {raw_score:.2f} (Weight: {weight*100:.0f}%) "
                f"-> Contributed {weighted_score:.3f} points."
            )

        # Convert to a clean 0-100 scale
        final_score_100 = round(total_score * 100, 2)
        
        # Categorize the final decision
        if final_score_100 >= 75:
            status = "Strong Match - Shortlist"
        elif final_score_100 >= 50:
            status = "Average Match - Review Required"
        else:
            status = "Weak Match - Reject"

        return {
            "candidate_id": candidate_id,
            "role_evaluated": role,
            "final_score_out_of_100": final_score_100,
            "decision_status": status,
            "explainable_breakdown": explanation,
            "weights_applied": weights
        }

# Test execution
if __name__ == "__main__":
    engine = ATSScoringEngine()
    
    # Simulated input from your Day 9-12 modules (Scores must be normalized to 0.0 - 1.0)
    # Notice that 'education_alignment' is completely missing from this candidate's data
    sample_candidate_metrics = {
        "skill_match": 0.88, 
        "experience_relevance": 0.74,
        "semantic_similarity": 0.81
    }
    
    # Generate the score for a Data Scientist role
    result = engine.calculate_score("cnd-002", "Data Scientist", sample_candidate_metrics)
    
    print(json.dumps(result, indent=2))