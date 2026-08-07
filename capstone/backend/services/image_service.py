# services/image_service.py
import os
import io
import json
import base64
from PIL import Image
import google.generativeai as genai
from openai import OpenAI
from config import SYSTEM_PROMPT

def analyze_scam_image(image_bytes: bytes) -> dict:
    """Processes image bytes and sends the image to Gemini for vision analysis with an OpenAI fallback."""
    
    # 1. Try Gemini Vision
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            image = Image.open(io.BytesIO(image_bytes))
            genai.configure(api_key=api_key)
            
            model = genai.GenerativeModel(
                model_name="gemini-3.6-flash", 
                system_instruction=SYSTEM_PROMPT,
                generation_config={"response_mime_type": "application/json"} 
            )
            
            response = model.generate_content([
                image, 
                "Analyze this screenshot or image carefully for scam indicators, fake branding, suspicious phone numbers, or phishing links."
            ])
            
            return json.loads(response.text)
    except Exception as e:
        print(f"⚠️ Gemini Vision failed: {e}. Falling back to OpenAI Vision...")

    # 2. Try OpenAI Vision Fallback
    try:
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            # Convert ANY image format (AVIF, BMP, etc.) to standard JPEG for OpenAI
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            clean_jpeg_bytes = buffer.getvalue()

            # Base64 encode the clean JPEG bytes
            base64_image = base64.b64encode(clean_jpeg_bytes).decode('utf-8')
            
            client = OpenAI(api_key=openai_key)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": "Analyze this screenshot or image carefully for scam indicators, fake branding, suspicious phone numbers, or phishing links. Provide the response in JSON format."
                            },
                            {
                                "type": "image_url", 
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ]
            )
            
            return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"❌ OpenAI Vision failed: {e}.")
        
    # 3. Return a valid fail-safe dictionary if everything goes wrong
    return {
        "risk_score": 0, 
        "risk_level": "ERROR", 
        "summary": "Service unavailable. Both Gemini and OpenAI vision analysis failed.", 
        "red_flags": [], 
        "next_steps": []
    }