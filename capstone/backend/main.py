from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from services.scam_service import analyze_scam, save_session, handle_followup
from services.image_service import analyze_scam_image
from services.scraper import fetch_scam_alerts

load_dotenv()

app = FastAPI(title="ScamShield AI API")

# Allow requests from your Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScamRequest(BaseModel):
    text: str
    session_id: str  # Tracks the unique session for chat history

class FollowUpRequest(BaseModel):
    session_id: str  # Identifies which chat history to load
    question: str

@app.post("/api/analyze")
async def analyze(request: ScamRequest):
    """Endpoint to process scam analysis requests."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    result = analyze_scam(request.text)
    save_session(request.session_id, request.text, result)
    return {"analysis": result}

@app.post("/api/analyze-image")
async def analyze_image_endpoint(file: UploadFile = File(...), session_id: str = Form(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image (PNG, JPG, JPEG).")
    
    # Read the file bytes
    image_bytes = await file.read()
    
    # Send bytes to image service
    result = analyze_scam_image(image_bytes)
    save_session(session_id, "User uploaded a screenshot for analysis.", result)
    
    return {"analysis": result}

@app.post("/api/chat")
async def chat_endpoint(request: FollowUpRequest):
    reply = handle_followup(request.session_id, request.question)
    return {"reply": reply}

@app.get("/api/alerts")
async def get_alerts():
    """Returns the latest threat intelligence alerts for the frontend banner."""
    alerts = fetch_scam_alerts()
    return {"alerts": alerts}