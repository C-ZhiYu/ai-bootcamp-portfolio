import os
import json
import google.generativeai as genai
from openai import OpenAI
from groq import Groq
from config import SYSTEM_PROMPT, CHAT_SYSTEM_PROMPT

# In-memory database for sessions
chat_histories = {}

def save_session(session_id: str, user_input: str, ai_response: dict):
    """Saves the initial JSON analysis into the backend memory in a universal format."""
    chat_histories[session_id] = [
        {"role": "user", "content": f"Original Suspicious Input: {user_input}"},
        {"role": "assistant", "content": f"Threat Analysis: {json.dumps(ai_response)}"}
    ]

def analyze_scam(user_input: str) -> dict:
    """Sends user input to the API and returns JSON analysis with fallback."""
    if not user_input.strip():
        raise ValueError("Please provide a valid description or text to analyze.")

    # 1. Try Gemini
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="gemini-3.5-flash", 
                system_instruction=SYSTEM_PROMPT,
                generation_config={"response_mime_type": "application/json"}
            )
            response = model.generate_content(user_input)
            return json.loads(response.text)
    except Exception as e:
        print(f"⚠️ Gemini failed: {e}. Trying OpenAI...")

    # 2. Try OpenAI
    try:
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"⚠️ OpenAI failed: {e}. Trying Groq...")

    # 3. Try Groq
    try:
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            client = Groq(api_key=groq_key)
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"❌ Groq failed: {e}")
        
    # If everything fails, return safe fallback JSON
    return {
        "risk_score": 0, 
        "risk_level": "ERROR", 
        "summary": "Service unavailable. All AI providers failed.", 
        "red_flags": [], 
        "next_steps": []
    }

def handle_followup(session_id: str, new_question: str) -> str:
    """Handles chat follow-ups using a universal history and fallback chain."""
    if session_id not in chat_histories:
        return "Error: Chat session expired or not found. Please start a new analysis."

    # Append new user question to universal history
    chat_histories[session_id].append({"role": "user", "content": new_question})
    
    universal_history = chat_histories[session_id]

    # 1. Try Gemini
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            # Convert universal history to Gemini's specific format
            gemini_history = []
            for msg in universal_history[:-1]: # Exclude the latest question for history setup
                role = "model" if msg["role"] == "assistant" else "user"
                gemini_history.append({"role": role, "parts": [msg["content"]]})
                
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="gemini-3.5-flash",
                system_instruction=CHAT_SYSTEM_PROMPT
            )
            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(new_question)
            
            chat_histories[session_id].append({"role": "assistant", "content": response.text})
            return response.text
    except Exception as e:
        print(f"⚠️ Gemini chat failed: {e}. Trying OpenAI...")

    # 2. Try OpenAI
    try:
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            client = OpenAI(api_key=openai_key)
            messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}] + universal_history
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            reply = response.choices[0].message.content
            chat_histories[session_id].append({"role": "assistant", "content": reply})
            return reply
    except Exception as e:
        print(f"⚠️ OpenAI chat failed: {e}. Trying Groq...")

    # 3. Try Groq
    try:
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            client = Groq(api_key=groq_key)
            messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}] + universal_history
            
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages
            )
            reply = response.choices[0].message.content
            chat_histories[session_id].append({"role": "assistant", "content": reply})
            return reply
    except Exception as e:
        # Remove the unanswered user question so they can try asking again
        chat_histories[session_id].pop()
        return "Sorry, I couldn't process that due to an API outage. Please try again."