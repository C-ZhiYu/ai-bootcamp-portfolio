import { useState, ChangeEvent } from 'react';
import { analyzeScamText, analyzeScamImage, sendFollowUp } from './api';
import ReactMarkdown from 'react-markdown'
import './App.css';

type Mode = 'text' | 'image';

function App() {
  const [mode, setMode] = useState<Mode>('text');
  const [inputText, setInputText] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  
  const [result, setResult] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // NEW: State for backend session management and chat
  const [sessionId, setSessionId] = useState<string>("");
  const [chatHistory, setChatHistory] = useState<{role: string, text: string}[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
      setChatHistory([]);
    }
  };

  const handleAnalyze = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);
    setChatHistory([]); 

    // Generate a fresh session ID for the backend memory
    const newSessionId = crypto.randomUUID();
    setSessionId(newSessionId);

    try {
      if (mode === 'text') {
        if (!inputText.trim()) {
          throw new Error("Please enter a description or text message to analyze.");
        }
        const data = await analyzeScamText(inputText, newSessionId);
        setResult(data.analysis);
      } else {
        if (!selectedFile) {
          throw new Error("Please select or upload a screenshot to analyze.");
        }
        const data = await analyzeScamImage(selectedFile, newSessionId);
        setResult(data.analysis);
      }
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleChatSubmit = async () => {
    if (!chatInput.trim()) return;
    
    const userMsg = chatInput;
    setChatHistory(prev => [...prev, { role: 'user', text: userMsg }]);
    setChatInput("");
    setIsChatLoading(true);

    try {
      // Send only the sessionId and question; backend remembers the rest!
      const data = await sendFollowUp(sessionId, userMsg);
      setChatHistory(prev => [...prev, { role: 'model', text: data.reply }]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsChatLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "750px", margin: "40px auto", padding: "20px", fontFamily: "sans-serif" }}>
      <h1>ScamShield AI Assistant (SG)</h1>
      <p>Analyze suspicious messages, emails, or screenshots for potential scam risk.</p>

      {/* Mode Switcher */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <button
          onClick={() => { setMode('text'); setError(null); setResult(null); setChatHistory([]); }}
          style={{
            flex: 1,
            padding: "10px",
            backgroundColor: mode === 'text' ? '#007bff' : '#e0e0e0',
            color: mode === 'text' ? '#fff' : '#333',
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontWeight: "bold"
          }}
        >
          Text Input
        </button>
        <button
          onClick={() => { setMode('image'); setError(null); setResult(null); setChatHistory([]); }}
          style={{
            flex: 1,
            padding: "10px",
            backgroundColor: mode === 'image' ? '#007bff' : '#e0e0e0',
            color: mode === 'image' ? '#fff' : '#333',
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontWeight: "bold"
          }}
        >
          Upload Screenshot
        </button>
      </div>

      {/* Input Form */}
      {mode === 'text' ? (
        <textarea
          rows={6}
          style={{ width: "100%", padding: "12px", borderRadius: "8px", fontSize: "15px", boxSizing: "border-box" }}
          placeholder="e.g. Received a call from +65 81103107 claiming to be SPF asking for PayNow transfer..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          disabled={isLoading}
        />
      ) : (
        <div style={{ border: "2px dashed #ccc", padding: "20px", borderRadius: "8px", textAlign: "center" }}>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            disabled={isLoading}
            style={{ marginBottom: "10px" }}
          />
          {previewUrl && (
            <div style={{ marginTop: "15px" }}>
              <img
                src={previewUrl}
                alt="Upload preview"
                style={{ maxWidth: "100%", maxHeight: "300px", borderRadius: "8px" }}
              />
            </div>
          )}
        </div>
      )}

      {/* Submit Button */}
      <button
        onClick={handleAnalyze}
        disabled={isLoading}
        style={{
          marginTop: "16px",
          width: "100%",
          padding: "12px",
          fontSize: "16px",
          backgroundColor: "#28a745",
          color: "#fff",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
          fontWeight: "bold"
        }}
      >
        {isLoading ? "Analyzing..." : "Analyze Risk"}
      </button>

      {/* Error Alert */}
      {error && (
        <div style={{ marginTop: "20px", padding: "12px", backgroundColor: "#ffeeee", color: "#c00", borderRadius: "6px" }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Dynamic Results Rendering */}
      {result && (
        typeof result === 'object' && result.risk_score !== undefined ? (
          
          <div style={{ marginTop: "30px", padding: "24px", backgroundColor: "#f8f9fa", borderRadius: "12px", border: "1px solid #e0e0e0", textAlign: "left" }}>
            
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", borderBottom: "2px solid #dee2e6", paddingBottom: "15px", marginBottom: "20px" }}>
              <div style={{ paddingRight: "20px" }}>
                <h2 style={{ margin: 0, color: "#333" }}>Threat Assessment</h2>
                <p style={{ margin: "8px 0 0 0", color: "#555", fontSize: "15px", lineHeight: "1.5" }}>{result.summary || "No summary provided."}</p>
              </div>
              
              <div style={{ 
                backgroundColor: result.risk_score > 70 ? "#dc3545" : result.risk_score > 30 ? "#ffc107" : "#28a745",
                color: result.risk_score > 30 && result.risk_score <= 70 ? "#000" : "#fff",
                padding: "15px 25px",
                borderRadius: "50px",
                textAlign: "center",
                minWidth: "90px",
                boxShadow: "0 4px 6px rgba(0,0,0,0.1)"
              }}>
                <div style={{ fontSize: "28px", fontWeight: "900" }}>{result.risk_score}%</div>
                <div style={{ fontSize: "12px", fontWeight: "bold", letterSpacing: "1px", marginTop: "2px" }}>{result.risk_level || "UNKNOWN"}</div>
              </div>
            </div>

            <div style={{ display: "flex", gap: "25px" }}>
              <div style={{ flex: 1 }}>
                <h4 style={{ color: "#dc3545", margin: "0 0 10px 0" }}>🚩 Red Flags</h4>
                <ul style={{ paddingLeft: "20px", margin: 0, color: "#444" }}>
                  {Array.isArray(result.red_flags) && result.red_flags.length > 0 ? (
                    result.red_flags.map((flag: string, idx: number) => (
                      <li key={idx} style={{ marginBottom: "8px", lineHeight: "1.4" }}>{flag}</li>
                    ))
                  ) : (
                    <li>No specific red flags detected.</li>
                  )}
                </ul>
              </div>

              <div style={{ flex: 1 }}>
                <h4 style={{ color: "#28a745", margin: "0 0 10px 0" }}>🛡️ Recommended Actions</h4>
                <ol style={{ paddingLeft: "20px", margin: 0, color: "#444" }}>
                  {Array.isArray(result.next_steps) && result.next_steps.length > 0 ? (
                    result.next_steps.map((step: string, idx: number) => (
                      <li key={idx} style={{ marginBottom: "8px", lineHeight: "1.4" }}>{step}</li>
                    ))
                  ) : (
                    <li>No immediate action needed.</li>
                  )}
                </ol>
              </div>
            </div>

          </div>
        ) : (
          <div style={{ marginTop: "20px", padding: "16px", backgroundColor: "#f4f4f6", borderRadius: "8px", textAlign: "left" }}>
            <h3>Raw Output</h3>
            <pre style={{ whiteSpace: "pre-wrap", fontFamily: "inherit" }}>
              {typeof result === 'string' ? result : JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )
      )}

      {/* Follow-up Chat UI */}
      {result && typeof result === 'object' && (
        <div style={{ marginTop: "30px", borderTop: "2px solid #eee", paddingTop: "20px" }}>
          <h3>Ask a Follow-up Question</h3>
          
          {/* Chat History Messages */}
          <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginBottom: "15px" }}>
            {chatHistory.map((msg, idx) => (
              <div key={idx} style={{
                alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                backgroundColor: msg.role === 'user' ? '#007bff' : '#f1f1f1',
                color: msg.role === 'user' ? 'white' : 'black',
                padding: "10px 15px",
                borderRadius: "15px",
                maxWidth: "80%",
                textAlign: "left",
                fontSize: "15px",
                lineHeight: "1.5",
                boxShadow: "0 2px 5px rgba(0,0,0,0.05)",
              }}>
                {msg.role === 'model' ? (<ReactMarkdown>{msg.text}</ReactMarkdown>) : (msg.text)}
              </div>
            ))}
            {isChatLoading && <div style={{ alignSelf: "flex-start", color: "#888" }}>ScamShield AI is typing...</div>}
          </div>

          {/* Chat Input Box */}
          <div style={{ display: "flex", gap: "10px" }}>
            <input 
              type="text" 
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleChatSubmit()}
              placeholder="E.g. What should I tell the caller?"
              style={{ flex: 1, padding: "10px", borderRadius: "6px", border: "1px solid #ccc" }}
              disabled={isChatLoading}
            />
            <button 
              onClick={handleChatSubmit}
              disabled={isChatLoading}
              style={{ padding: "10px 20px", backgroundColor: "#333", color: "white", border: "none", borderRadius: "6px", cursor: "pointer" }}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;