import re
import json

class SkillExtractor:
    def __init__(self):
        # 1. Master Skill Dictionary (Aliases mapping to Normalized Standard)
        self.skill_aliases = {
            "js": "JavaScript",
            "reactjs": "React",
            "react.js": "React",
            "node.js": "Node.js",
            "nodejs": "Node.js",
            "ml": "Machine Learning",
            "ai": "Artificial Intelligence",
            "tf": "TensorFlow",
            "scikit learn": "scikit-learn",
            "sklearn": "scikit-learn",
            "postgres": "PostgreSQL"
        }
        
        # 2. Skill Stacks (Unwraps acronyms into individual standard skills)
        self.skill_stacks = {
            "mern": ["MongoDB", "Express.js", "React", "Node.js"],
            "mean": ["MongoDB", "Express.js", "Angular", "Node.js"],
            "lamp": ["Linux", "Apache", "MySQL", "PHP"]
        }
        
        # 3. Standard Core Skills (Used for direct matching)
        # In production, this would be loaded from a larger JSON or database
        self.core_skills = [
            "python", "java", "c++", "ruby", "aws", "docker", "kubernetes", 
            "tensorflow", "sql", "django", "pandas", "numpy", "javascript", 
            "machine learning", "artificial intelligence", "react", "postgresql"
        ]

    def extract_skills(self, text):
        """Main method to extract, normalize, and score skills."""
        text_lower = text.lower()
        extracted_skills = {}

        # Helper function to add/update skills with the highest confidence score
        def add_skill(skill_name, confidence):
            if skill_name not in extracted_skills or extracted_skills[skill_name] < confidence:
                extracted_skills[skill_name] = confidence

        # A. Check for Direct Core Skills (Confidence: 1.0)
        for skill in self.core_skills:
            # Use regex boundaries \b to prevent matching "java" inside "javascript"
            if re.search(rf"\b{re.escape(skill)}\b", text_lower):
                # Capitalize nicely based on our dictionary if possible, else title case
                standard_name = next((v for k, v in self.skill_aliases.items() if v.lower() == skill), skill.title())
                if skill == "sql": standard_name = "SQL" # edge case formatting
                add_skill(standard_name, 1.0)

        # B. Check for Aliases and Synonyms (Confidence: 0.9)
        for alias, standard_name in self.skill_aliases.items():
            if re.search(rf"\b{re.escape(alias)}\b", text_lower):
                add_skill(standard_name, 0.90)

        # C. Check for Skill Stacks (Confidence: 0.85 - inferred)
        for stack, stack_skills in self.skill_stacks.items():
            if re.search(rf"\b{re.escape(stack)}\b", text_lower):
                # Add the stack name itself
                add_skill(stack.upper(), 1.0)
                # Add inferred skills from the stack
                for inferred_skill in stack_skills:
                    add_skill(inferred_skill, 0.85)

        # Format output
        final_output = [
            {"skill": name, "confidence_score": score} 
            for name, score in sorted(extracted_skills.items(), key=lambda x: x[1], reverse=True)
        ]
        
        return {
            "total_skills_found": len(final_output),
            "skills": final_output
        }

# Test execution
if __name__ == "__main__":
    sample_resume_text = """
    I am a backend developer with experience in python and Django. 
    Previously worked with the MERN stack and deployed apps using AWS. 
    Strong background in ML, specifically using sklearn and tf.
    """
    
    extractor = SkillExtractor()
    result = extractor.extract_skills(sample_resume_text)
    print(json.dumps(result, indent=2))