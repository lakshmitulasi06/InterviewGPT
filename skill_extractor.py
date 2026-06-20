import json
import streamlit as st
from groq import Groq

def extract_skills(resume_text):
    """
    Uses Llama-3 to parse the resume text and return structured profile details.
    """
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        prompt = f"""
        Analyze the following resume text and extract technical skills.
        You must return ONLY a valid JSON object with exactly these four keys:
        "languages", "frameworks", "tools", "experience_level".
        Do not include any conversational text, markdown formatting, or triple backticks.

        Resume Text:
        {resume_text[:3000]}
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": f"Failed to parse skills: {str(e)}"}