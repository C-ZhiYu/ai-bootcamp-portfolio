# services/image_service.py
import os
import io
import json # 1. Added json import
from PIL import Image
import google.generativeai as genai
from config import SYSTEM_PROMPT

def analyze_scam_image(image_bytes: bytes) -> dict: # 2. Updated return type to dict
    """Processes image bytes and sends the image to Gemini for vision analysis."""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("Error: GEMINI_API_KEY is missing in backend .env.")

    try:
        image = Image.open(io.BytesIO(image_bytes))
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel(
            model_name="gemini-3.6-flash", # Updated to the latest model
            system_instruction=SYSTEM_PROMPT,
            generation_config={"response_mime_type": "application/json"} # 3. Force JSON output
        )
        
        # Pass both the image object and a prompt instruction
        response = model.generate_content([
            image, 
            "Analyze this screenshot or image carefully for scam indicators, fake branding, suspicious phone numbers, or phishing links."
        ])
        
        # 4. Parse the text string into a Python dictionary
        return json.loads(response.text)

    except Exception as e:
        # 5. Return a valid fail-safe dictionary if something goes wrong
        return {
            "risk_score": 0, 
            "risk_level": "ERROR", 
            "summary": f"An error occurred while analyzing the image: {str(e)}", 
            "red_flags": [], 
            "next_steps": []
        }