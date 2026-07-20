import os
import sys
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("MODEL_NAME", "gemini-flash-latest")
DB_NAME = os.getenv("DB_NAME", "review_history.db")

if not GEMINI_API_KEY:
    print("Security Error: GEMINI_API_KEY is missing from your .env file!")
    print("Please generate a key at https://aistudio.google.com/ and add it to .env")
    sys.exit(1)