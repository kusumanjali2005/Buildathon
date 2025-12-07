from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()


# CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model - flexible to accept both 'question' and 'user_query'
class Query(BaseModel):
    user_query: Optional[str] = None
    question: Optional[str] = None
    language: str = "hi"  # default Hindi
    
    def get_query(self):
        """Get the query from either field"""
        return self.user_query or self.question or ""

# System prompt
SYSTEM_PROMPT = """
You are an AI Legal Aid Assistant for Indian citizens.
- Explain legal rights in simple, non-technical language.
- Support multiple Indian languages: English, Hindi, Telugu, Kannada, Tamil, Marathi, Gujarati, Bengali, Malayalam, Punjabi, Odia.
- CRITICAL: Always respond in the EXACT language specified by the user's language selection.
- If user selects Kannada, respond ONLY in Kannada. If they select Tamil, respond ONLY in Tamil.
- NEVER mix languages in your response. Use only the selected language.
- Provide general guidance only, not professional legal advice.
- Do not draft legal notices or FIRs.
- Always show clear, numbered steps the user should take.
- Be culturally sensitive and use simple words that common people can understand.
- Write in a conversational, helpful tone appropriate for the selected language.
"""

@app.get("/")
def home():
    return {"status": "Legal Aid API running"}

# Add this function before the @app.post("/ask") decorator
def detect_language(text):
    """Simple heuristic to detect if text contains non-English characters"""
    # Check for common Indian language scripts
    scripts = {
        'hi': ['\u0900-\u097F'],  # Devanagari (Hindi, Marathi)
        'kn': ['\u0C80-\u0CFF'],  # Kannada
        'te': ['\u0C00-\u0C7F'],  # Telugu
        'ta': ['\u0B80-\u0BFF'],  # Tamil
        'gu': ['\u0A80-\u0AFF'],  # Gujarati
        'bn': ['\u0980-\u09FF'],  # Bengali
        'ml': ['\u0D00-\u0D7F'],  # Malayalam
        'pa': ['\u0A00-\u0A7F'],  # Gurmukhi (Punjabi)
        'or': ['\u0B00-\u0B7F'],  # Odia
    }
    import re
    for lang, pattern in scripts.items():
        if re.search(pattern, text):
            return lang
    return 'en'

@app.post("/ask")
def ask_legal_ai(data: Query):
    try:
        user_query = data.get_query()
        
        if not user_query:
            return {"error": "No query provided", "reply": ""}
        
        # Language mapping for better AI understanding
        language_name_map = {
            "en": "English",
            "hi": "Hindi",
            "kn": "Kannada", 
            "te": "Telugu",
            "ta": "Tamil",
            "mr": "Marathi",
            "gu": "Gujarati",
            "bn": "Bengali",
            "ml": "Malayalam",
            "pa": "Punjabi",
            "or": "Odia"
        }
        
        language_name = language_name_map.get(data.language, "English")
        
        # More explicit prompt to ensure response in the correct language
        user_text = f"""The user has selected {language_name} as their preferred language.
The user's query is: {user_query}

IMPORTANT: 
- You MUST respond ENTIRELY in {language_name} language.
- Do NOT mix languages. Use ONLY {language_name}.
- If the user wrote in {language_name}, respond in {language_name}.
- If the user wrote in a different language but selected {language_name}, still respond in {language_name}.
- Use simple, clear {language_name} words that common people can understand.
- Write your complete response in {language_name} only."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            max_tokens=500,
            temperature=0.7  # Slightly higher for more natural language responses
        )

        answer = response.choices[0].message.content
        
        # Return both 'reply' and 'answer' for compatibility
        return {"reply": answer, "answer": answer}

    except Exception as e:
        return {"error": str(e), "reply": "", "answer": ""}