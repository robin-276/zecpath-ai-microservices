from parsers.jd_parser import JobDescriptionParser

# Sample Job Description
sample_jd = """
We are looking for a Data Scientist to join our team. 
You should have 2+ years of experience building predictive models.
Required skills include Python, SQL, and ML. Experience with Pandas and NLP is a huge plus.
Candidates must have a Bachelor degree in Computer Science or related field.
"""

# Initialize Parser
parser = JobDescriptionParser()

# Parse the JD
structured_jd = parser.parse(role_name="Data Scientist", jd_text=sample_jd)

# Print the AI-Friendly JSON Output
print(parser.to_json(structured_jd))