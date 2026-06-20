import json
import streamlit as st
from groq import Groq

def evaluate_answer(question, answer):
    """
    Evaluates an interview response using Llama-3, returning a structured JSON object.
    """
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    prompt = f"""
    You are a Senior Technical Interviewer. Evaluate the candidate's response to the given question.

    Interview Question:
    {question}

    Candidate Answer:
    {answer}

    You must evaluate the response and return ONLY a valid JSON object with the following structural keys:
    "technical_score": (integer out of 10),
    "communication_score": (integer out of 10),
    "strengths": (list of strings),
    "weaknesses": (list of strings),
    "missing_concepts": (list of strings),
    "improved_answer": (string providing a perfect response model),
    "feedback": (string containing summary recommendations)

    Do not output any introductory or conversational text, markdown text formatting, or backticks outside of the pure JSON object payload.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert technical interviewer that scores engineering responses strictly in a valid JSON schema data structure."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)