# 🛡️ ScamShield AI (SG)

ScamShield AI is an intelligent, localized threat-assessment dashboard designed to protect Singaporeans from phishing, social engineering, and fraudulent messages. 

Built with a highly resilient **multi-LLM fallback architecture**, it analyzes text messages and screenshots to detect red flags, assign risk scores, and provide actionable next steps. It also features a real-time web scraper that pulls live threat intelligence directly from the official ScamShield government portal.

## ✨ Key Features

*   **Multimodal Threat Analysis:** Upload suspicious SMS texts, emails, or screenshots. The AI extracts the context and evaluates the scam probability.
*   **Two-Column Desktop Dashboard:** A responsive, modern UI built with Tailwind CSS v4, featuring a comfortable input area that expands into a side-by-side analytics view.
*   **Live Threat Intel Ticker:** A custom Python web scraper (BeautifulSoup) fetches real-time scam bulletins from `scamshield.gov.sg` and displays them in a scrolling marquee. Includes a graceful cache fallback if the government firewall blocks the request.
*   **AI Investigator Chat:** A session-aware chat interface allowing users to ask follow-up questions about their specific threat assessment (e.g., *"What should I say if the caller rings back?"*).
*   **Dark / Light Mode:** Fully supported manual toggle for comfortable reading.
*   **Universal Image Support:** Automatically converts unsupported image formats (like `.avif` or `.webp`) into standard JPEGs in-memory using `Pillow` before sending them to the Vision APIs.

## 🧠 Enterprise-Grade AI Fallback Architecture

To ensure high availability and prevent rate-limit crashes, this application implements a **3-Tier AI Fallback Chain**:

1.  **Primary:** Google Gemini 3.5 Flash / 3.6 Flash (Fast, multimodal, high accuracy).
2.  **Secondary (Fallback 1):** OpenAI GPT-4o-mini (Takes over if Gemini hits quota limits or fails).
3.  **Tertiary (Fallback 2):** Groq LLaMA 3 8B (Takes over text processing if both proprietary APIs experience an outage).

The backend automatically translates universal chat histories into provider-specific formats on the fly, ensuring a seamless user experience even during a live failover.

---

## 🛠️ Tech Stack

**Frontend:**
*   React 18 + TypeScript
*   Vite
*   Tailwind CSS (v4)
*   React Markdown

**Backend:**
*   Python 3 + FastAPI
*   Uvicorn
*   BeautifulSoup4 + Requests (Web Scraping)
*   Pillow (Image Processing)
*   Google Generative AI SDK, OpenAI SDK, Groq SDK

---

## 🚀 Getting Started

### Prerequisites
*   Node.js (v18+)
*   Python (3.10+)
*   API Keys for Gemini, OpenAI, and Groq.

### 1. Backend Setup
Navigate to the `backend` directory and set up your Python environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install fastapi uvicorn google-generativeai openai groq pillow requests beautifulsoup4 python-multipart