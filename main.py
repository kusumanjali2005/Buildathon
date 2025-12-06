from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

# Request model
class Query(BaseModel):
    user_query: str
    language: str = "hi"  # default Hindi

# System prompt
SYSTEM_PROMPT = """
You are an AI Legal Aid Assistant for Indian citizens.
- Explain legal rights in simple, non-technical language.
- Support English, Hindi, Telugu, Kannada.
- Provide general guidance only, not professional legal advice.
- Do not draft legal notices or FIRs.
- Always show steps the user should take.
"""

@app.get("/")
def home():
    return {"status": "Legal Aid API running"}

@app.post("/chat")
def ask_legal_ai(data: Query):
    try:
        user_text = f"Language: {data.language}. Query: {data.user_query}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            max_tokens=300
        )

        answer = response.choices[0].message.content
        return {"reply": answer}

    except Exception as e:
        return {"error": str(e)}
