from parsers.skill_extractor import SkillExtractor

def test_direct_skill_extraction():
    extractor = SkillExtractor()
    # Test if it finds exact matches, even with weird capitalization
    result = extractor.extract_skills("I have 3 years of experience with pYtHoN and JAVA.")
    
    # Extract just the names into a simple list to check them
    skill_names = [s["skill"] for s in result["skills"]]
    
    assert "Python" in skill_names
    assert "Java" in skill_names

def test_synonym_translation():
    extractor = SkillExtractor()
    # Test if it translates "ML" and "tf" properly
    result = extractor.extract_skills("I built models using ML and tf.")
    
    skill_names = [s["skill"] for s in result["skills"]]
    
    assert "Machine Learning" in skill_names
    assert "TensorFlow" in skill_names

def test_skill_stack_unpacking():
    extractor = SkillExtractor()
    # Test if "MERN" gets unpacked into MongoDB, React, etc.
    result = extractor.extract_skills("Full stack developer using MERN.")
    
    skill_names = [s["skill"] for s in result["skills"]]
    
    assert "MERN" in skill_names
    assert "React" in skill_names
    assert "MongoDB" in skill_names