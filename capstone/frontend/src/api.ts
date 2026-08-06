export interface ScamAnalysisResponse {
  analysis: any; 
}

const BACKEND_URL = "http://localhost:8000";

export async function analyzeScamText(text: string, sessionId: string): Promise<ScamAnalysisResponse> {
  const response = await fetch(`${BACKEND_URL}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: text, session_id: sessionId }),
  });
  if (!response.ok) throw new Error("Failed to analyze text.");
  return response.json();
}

export async function analyzeScamImage(file: File, sessionId: string): Promise<ScamAnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("session_id", sessionId); 

  const response = await fetch(`${BACKEND_URL}/api/analyze-image`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) throw new Error("Failed to analyze image.");
  return response.json();
}

export async function sendFollowUp(sessionId: string, question: string): Promise<{ reply: string }> {
  const response = await fetch(`${BACKEND_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, question: question }),
  });
  
  if (!response.ok) throw new Error("Failed to send message.");
  return response.json();
}