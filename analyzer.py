# analyzer.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Use the correct model path (v1 syntax)
model = genai.GenerativeModel(model_name="models/gemini-pro")

def get_feedback_from_model(resume_text, job_text):
    prompt = f"""
You are an AI resume expert.

Analyze the following RESUME in the context of the JOB DESCRIPTION.

Give a structured and specific feedback report with:
1. Skill match score (0–100)
2. ✅ Matching hard/soft skills
3. ❌ Missing key skills
4. 📌 Suggestions to improve experience/projects/skills section
5. Example bullet points the candidate can add

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_text}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error from Gemini API: {str(e)}"
