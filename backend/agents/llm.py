from crewai import LLM
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

llm_model = LLM(
    model='gemini/gemini-2.0-flash',
    api_key=api_key
)