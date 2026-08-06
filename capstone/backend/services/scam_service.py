import os
import json
import google.generativeai as genai
from config import SYSTEM_PROMPT, CHAT_SYSTEM_PROMPT

chat_histories = {}

def save_session(session_id: str, user_input: str, ai_response: dict):
    """Saves the initial JSON analysis into the backend memory."""
    chat_histories[session_id] = [
        {"role": "user", "parts": [f"Analyze this suspicious input: {user_input}"]},
        {"role": "model", "parts": [json.dumps(ai_response)]}
    ]

def analyze_scam(user_input: str) -> dict:
    """Sends user input to the Gemini API and returns JSON analysis."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing.")

    if not user_input.strip():
        raise ValueError("Please provide a valid description or text to analyze.")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-3.5-flash",
            system_instruction=SYSTEM_PROMPT,
            generation_config={"response_mime_type": "application/json"}
        )
        response = model.generate_content(user_input)
        return json.loads(response.text)

    except Exception as e:
        return {"risk_score": 0, "risk_level": "ERROR", "summary": str(e), "red_flags": [], "next_steps": []}

def handle_followup(session_id: str, new_question: str) -> str:
    """Retrieves the session history and asks a follow-up question."""
    api_key = os.getenv("GEMINI_API_KEY")
    if session_id not in chat_histories:
        return "Error: Chat session expired or not found. Please start a new analysis."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-3.5-flash",
            system_instruction=CHAT_SYSTEM_PROMPT
        )
        
        history = chat_histories[session_id]
        chat = model.start_chat(history=history)
        
        response = chat.send_message(new_question)
        
        chat_histories[session_id] = chat.history
        return response.text

    except Exception as e:
        return f"Sorry, I couldn't process that: {str(e)}"