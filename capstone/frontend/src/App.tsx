import { useState, useEffect, useRef, ChangeEvent } from 'react';
import { analyzeScamText, analyzeScamImage, sendFollowUp } from './api';
import ReactMarkdown from 'react-markdown';
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

  const [sessionId, setSessionId] = useState<string>("");
  const [chatHistory, setChatHistory] = useState<{role: string, text: string}[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);

  const [isDarkMode, setIsDarkMode] = useState(false);
  const [liveAlerts, setLiveAlerts] = useState<string[]>([]);

  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  useEffect(() => {
    fetch('http://localhost:8000/api/alerts')
      .then(res => res.json())
      .then(data => setLiveAlerts(data.alerts))
      .catch(err => console.error("Failed to fetch alerts:", err));
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, isChatLoading]);

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

    const newSessionId = crypto.randomUUID();
    setSessionId(newSessionId);

    try {
      if (mode === 'text') {
        if (!inputText.trim()) throw new Error("Please enter a description or text message to analyze.");
        const data = await analyzeScamText(inputText, newSessionId);
        setResult(data.analysis);
      } else {
        if (!selectedFile) throw new Error("Please select or upload a screenshot to analyze.");
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
      const data = await sendFollowUp(sessionId, userMsg);
      setChatHistory(prev => [...prev, { role: 'model', text: data.reply }]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsChatLoading(false);
    }
  };

  const getRiskColorClasses = (score: number) => {
    if (score > 70) return "bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 border-red-200 dark:border-red-800/50";
    if (score > 30) return "bg-yellow-50 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400 border-yellow-200 dark:border-yellow-800/50";
    return "bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 border-green-200 dark:border-green-800/50";
  };

  return (
    <div className="w-full min-h-screen bg-gray-100 dark:bg-gray-950 py-10 px-4 font-sans text-gray-900 dark:text-gray-100 transition-colors duration-300 flex justify-center items-start">
      <div className={`w-full transition-all duration-500 ${result ? 'max-w-[1450px]' : 'max-w-3xl'} bg-white dark:bg-gray-900 rounded-3xl shadow-xl border border-gray-200 dark:border-gray-800 p-8 md:p-12`}>
        
        {/* LIVE ALERT Header */}
        {liveAlerts.length > 0 && (
          <div className="absolute top-0 left-0 w-full bg-red-600 text-white text-xs font-bold py-2 overflow-hidden flex items-center">
            <div className="px-4 bg-red-700 h-full absolute left-0 z-10 flex items-center shadow-[10px_0_15px_-3px_rgba(220,38,38,1)]">
              🚨 LIVE THREAT INTEL
            </div>
            <div className="animate-marquee whitespace-nowrap pl-32">
              {liveAlerts.map((alert, idx) => (
                <span key={idx} className="mx-8">
                  • {alert}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Header */}
        <div className="text-center mb-10 relative">
          <button 
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="absolute top-0 right-0 p-3 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors cursor-pointer"
            title="Toggle Dark Mode"
          >
            {isDarkMode ? '☀️' : '🌙'}
          </button>
          
          <div className="text-6xl mb-4">🛡️</div>
          <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-2">
            ScamShield AI
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            Instant threat analysis for messages, emails, and screenshots.
          </p>
        </div>

        {/* Dynamic Layout Grid */}
        <div className={`grid grid-cols-1 ${result ? 'lg:grid-cols-12' : 'grid-cols-1'} gap-8 items-start`}>
          
          {/* LEFT COLUMN: Input Source (Top) + Threat Assessment (Bottom) */}
          <div className={`w-full ${result ? 'lg:col-span-6' : 'max-w-2xl mx-auto'} flex flex-col gap-6`}>
            
            {/* Input Card */}
            <div className="bg-gray-50 dark:bg-gray-950 p-6 rounded-3xl border border-gray-200 dark:border-gray-800 shadow-sm">
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Input Threat Source</h3>
              
              <div className="flex bg-gray-200 dark:bg-gray-800 p-1.5 rounded-2xl mb-6 transition-colors">
                <button
                  onClick={() => { setMode('text'); setError(null); setResult(null); setChatHistory([]); }}
                  className={`flex-1 py-3 px-4 rounded-xl font-semibold text-sm transition-all duration-200 cursor-pointer ${
                    mode === 'text' 
                      ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm' 
                      : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
                  }`}
                >
                  📝 Text
                </button>
                <button
                  onClick={() => { setMode('image'); setError(null); setResult(null); setChatHistory([]); }}
                  className={`flex-1 py-3 px-4 rounded-xl font-semibold text-sm transition-all duration-200 cursor-pointer ${
                    mode === 'image' 
                      ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm' 
                      : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
                  }`}
                >
                  📸 Image
                </button>
              </div>

              {mode === 'text' ? (
                <textarea
                  rows={5}
                  className="w-full p-4 rounded-2xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-base focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-y transition-all"
                  placeholder="Paste the suspicious message, phone number, or email content here..."
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  disabled={isLoading}
                />
              ) : (
                <div className="border-2 border-dashed border-gray-300 dark:border-gray-700 p-6 rounded-2xl text-center bg-white dark:bg-gray-900 transition-colors">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    disabled={isLoading}
                    className="mb-4 text-sm w-full text-gray-600 dark:text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 dark:file:bg-blue-900/30 file:text-blue-700 dark:file:text-blue-400 hover:file:bg-blue-100 transition-colors cursor-pointer"
                  />
                  {previewUrl && (
                    <div className="mt-4 flex justify-center">
                      <img
                        src={previewUrl}
                        alt="Upload preview"
                        className="max-w-full max-h-36 rounded-xl shadow-md object-contain"
                      />
                    </div>
                  )}
                </div>
              )}

              <button
                onClick={handleAnalyze}
                disabled={isLoading}
                className={`w-full mt-6 py-4 px-6 text-lg font-bold rounded-2xl text-white transition-all duration-200 cursor-pointer ${
                  isLoading 
                    ? 'bg-gray-400 dark:bg-gray-700 cursor-not-allowed' 
                    : 'bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-600/30 dark:shadow-blue-900/20'
                }`}
              >
                {isLoading ? "Running Analysis..." : "Analyze Risk"}
              </button>

              {error && (
                <div className="mt-6 p-4 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 border border-red-200 dark:border-red-800/50 rounded-xl flex items-center gap-3 text-sm">
                  <span className="text-xl">⚠️</span>
                  <strong>Error:</strong> {error}
                </div>
              )}
            </div>

            {/* Threat Assessment Card (Bottom Left) */}
            {result && typeof result === 'object' && result.risk_score !== undefined && (
              <div className="p-6 bg-gray-50 dark:bg-gray-950 rounded-3xl border border-gray-200 dark:border-gray-800 shadow-sm transition-colors animate-fadeIn">
                
                <div className="flex flex-col sm:flex-row items-start justify-between border-b border-gray-200 dark:border-gray-800 pb-5 mb-5 gap-4">
                  <div className="flex-1">
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-1">Threat Assessment</h2>
                    <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                      {result.summary || "No summary provided."}
                    </p>
                  </div>
                  
                  <div className={`border-2 px-5 py-3 rounded-2xl min-w-[110px] flex flex-col items-center justify-center shadow-sm ${getRiskColorClasses(result.risk_score)}`}>
                    <div className="text-2xl font-black leading-none">{result.risk_score}%</div>
                    <div className="text-[10px] font-bold tracking-widest mt-1 uppercase text-center">
                      {result.risk_level || "UNKNOWN"}
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-red-50/50 dark:bg-red-900/10 p-4 rounded-2xl border border-red-100 dark:border-red-900/30">
                    <h4 className="text-red-700 dark:text-red-400 font-bold mb-2 flex items-center gap-2 text-xs uppercase tracking-wider">
                      <span>🚩</span> Red Flags
                    </h4>
                    <ul className="space-y-1.5 text-xs">
                      {Array.isArray(result.red_flags) && result.red_flags.length > 0 ? (
                        result.red_flags.map((flag: string, idx: number) => (
                          <li key={idx} className="text-gray-700 dark:text-gray-300 flex items-start gap-1.5">
                            <span className="text-red-500">•</span> 
                            <span>{flag}</span>
                          </li>
                        ))
                      ) : (
                        <li className="text-gray-500 italic">No specific red flags detected.</li>
                      )}
                    </ul>
                  </div>

                  <div className="bg-green-50/50 dark:bg-green-900/10 p-4 rounded-2xl border border-green-100 dark:border-green-900/30">
                    <h4 className="text-green-700 dark:text-green-400 font-bold mb-2 flex items-center gap-2 text-xs uppercase tracking-wider">
                      <span>🛡️</span> Actions
                    </h4>
                    <ul className="space-y-1.5 text-xs">
                      {Array.isArray(result.next_steps) && result.next_steps.length > 0 ? (
                        result.next_steps.map((step: string, idx: number) => (
                          <li key={idx} className="text-gray-700 dark:text-gray-300 flex items-start gap-1.5">
                            <span className="text-green-600 font-bold">{idx + 1}.</span> 
                            <span>{step}</span>
                          </li>
                        ))
                      ) : (
                        <li className="text-gray-500 italic">No immediate action needed.</li>
                      )}
                    </ul>
                  </div>
                </div>

              </div>
            )}

          </div>

          {/* RIGHT COLUMN: Fully Expanded AI Investigator Chat Panel */}
          {result && (
            <div className="w-full lg:col-span-6 flex flex-col animate-fadeIn">
              <div className="p-6 bg-gray-50 dark:bg-gray-950 rounded-3xl border border-gray-200 dark:border-gray-800 shadow-sm transition-colors flex flex-col h-full">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                  <span>💬</span> AI Investigator Chat
                </h3>
                
                {/* Taller, Expanded Chat Container for maximum history viewing */}
                <div className="h-[520px] flex flex-col gap-3 mb-4 overflow-y-auto pr-2 border border-gray-200 dark:border-gray-800 p-4 rounded-2xl bg-white dark:bg-gray-900">
                  {chatHistory.length === 0 && (
                    <div className="m-auto text-center text-gray-400 dark:text-gray-500 text-sm italic">
                      Ask follow-up questions about this threat analysis below.
                    </div>
                  )}
                  {chatHistory.map((msg, idx) => (
                    <div key={idx} className={`p-4 max-w-[85%] shadow-sm text-sm ${
                      msg.role === 'user' 
                        ? 'self-end bg-blue-600 text-white rounded-2xl rounded-tr-sm' 
                        : 'self-start bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-2xl rounded-tl-sm border border-gray-200 dark:border-gray-700 [&>p]:mb-2 last:[&>p]:mb-0 [&>ul]:list-disc [&>ul]:ml-4 [&>ol]:list-decimal [&>ol]:ml-4 [&_strong]:text-gray-900 dark:[&_strong]:text-white'
                    }`}>
                      {msg.role === 'model' ? (
                        <ReactMarkdown>{msg.text}</ReactMarkdown>
                      ) : (
                        <p className="whitespace-pre-wrap m-0">{msg.text}</p>
                      )}
                    </div>
                  ))}
                  {isChatLoading && (
                    <div className="self-start bg-gray-100 dark:bg-gray-800 text-gray-500 p-4 rounded-2xl rounded-tl-sm text-xs border border-gray-200 dark:border-gray-700 flex items-center gap-2">
                      <span className="animate-pulse">●</span>
                      <span className="animate-pulse animation-delay-200">●</span>
                      <span className="animate-pulse animation-delay-400">●</span>
                    </div>
                  )}
                  <div ref={chatEndRef} />
                </div>

                <div className="flex gap-2">
                  <input 
                    type="text" 
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleChatSubmit()}
                    placeholder="Ask a follow-up question..."
                    className="flex-1 p-3.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                    disabled={isChatLoading}
                  />
                  <button 
                    onClick={handleChatSubmit}
                    disabled={isChatLoading || !chatInput.trim()}
                    className={`px-6 font-bold rounded-xl transition-all text-sm cursor-pointer ${
                      chatInput.trim() 
                        ? 'bg-gray-900 dark:bg-white text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-gray-200' 
                        : 'bg-gray-300 dark:bg-gray-800 text-gray-500 dark:text-gray-600 cursor-not-allowed'
                    }`}
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

export default App;