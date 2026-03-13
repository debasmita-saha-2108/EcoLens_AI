import os
from groq import Groq
from dotenv import load_dotenv

# Load API Key from root .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

def get_esg_analysis(company_data, initiatives):
    """
    Connects to Groq API to generate a professional ESG summary.
    """
    if not api_key:
        return "Error: GROQ_API_KEY not found in .env file."

    client = Groq(api_key=api_key)

    prompt = f"""
    You are an expert ESG Consultant for 'EcoLens AI'. 
    Analyze the following data:
    - Carbon Data: {company_data}
    - Initiatives: {initiatives}
    
    Provide a professional ESG Report Summary with:
    1. Executive Summary
    2. Environmental Impact Analysis
    3. ROI & Strategic Recommendations
    
    Tone: Professional, Green-Tech focused, and concise.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional ESG analyst."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Groq API Error: {str(e)}"