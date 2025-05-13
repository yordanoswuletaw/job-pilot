from langchain_together import ChatTogether
from reader import ResumeReader
import os
from dotenv import load_dotenv

load_dotenv()
prompt = """
**Task**:  
You are an expert resume parser. Convert the following raw resume text into a structured JSON format. Extract and categorize all key details accurately, even if the resume format is unconventional.

**Instructions**:
1. Analyze the text carefully. Identify sections even if they aren't explicitly labeled.
2. Infer missing context (e.g., if dates are partial, assume reasonable formatting).
3. Handle abbreviations (e.g., "Jan 2020" → "2020-01") and normalize data.
4. If a field is missing, leave it as `None`.
5. Extract dates in YYYY-MM or Month YYYY format.
6. Use natural interpretation even if the formatting is non-standard.


**Output Format**:  
```json
{{
  "personal_info": {{
    "full_name": "string (e.g., 'John Doe')",
    "email": "string (must be valid format)",
    "phone": "string (e.g., '+1-123-456-7890')",
    "location": "string (e.g., 'San Francisco, CA')",
    "linkedin": "string (URL or username)",
    "website": "string (URL)",
    "github": "string (URL)",
    "summary": "string (e.g., 'Experienced software engineer with 5 years of experience in full-stack development.')"
  }},
  "education": [
    {{
      "degree": "string (e.g., 'BSc, MSc, PhD')",
      "field_of_study": "string (e.g., 'Computer Science')",
      "institution": "string",
      "location": "string",
      "start_date": "string (YYYY-MM-DD or YYYY)",
      "end_date": "string (YYYY-MM-DD, YYYY, or 'present')",
      "gpa": "string (if mentioned)"
    }}
  ],
  "work_experience": [
    {{
      "job_title": "string (e.g., 'Software Engineer')",
      "company": "string (e.g., 'Tech Company')",
      "location": "string (e.g., 'San Francisco, CA')",
      "start_date": "string (YYYY-MM-DD or YYYY)",
      "end_date": "string (YYYY-MM-DD, YYYY, or 'present')",
      "description": "array of strings",
      "link": "string (URL)"
    }}
  ],
  "skills": "array of strings (e.g., ['Python', 'SQL', 'Leadership', 'Communication'])",
  "projects": [
    {{
      "name": "string (e.g., 'Project Name')",
      "description": "array of strings (e.g., ['Description 1', 'Description 2'])",
      "technologies": "array of strings (e.g., ['Python', 'SQL'])",
      "link": "string (URL)",
      "start_date": "string (YYYY-MM-DD or YYYY)",
      "end_date": "string (YYYY-MM-DD, YYYY, or 'present')"
    }}
  ],
  "certifications": [
    {{
      "name": "string (e.g., 'AWS Certified Solutions Architect - Associate')",
      "issuer": "string (e.g., 'AWS')",
      "date_earned": "string (YYYY-MM-DD or YYYY)"
    }}  
  ],
  "languages": "array of strings (e.g., ['English (Fluent)', 'Spanish (Intermediate)'])"
}}
```

**Raw Resume Text to Parse:**
{resume_raw_text}
"""

model = ChatTogether(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
)

if __name__ == '__main__':
    # Get the absolute path to the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    test_file = os.path.join(project_root, 'data', 'fake_resume.pdf')
    
    print('started...')
    reader = ResumeReader()
    try:
        resume_data = reader.read_resume_data(test_file)
        res = model.invoke(prompt.format(resume_raw_text=resume_data))
        print(res)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"Please make sure there is a PDF file at: {test_file}")
    print('ended...')
