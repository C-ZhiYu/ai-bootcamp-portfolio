# Day 1 Chatbot — Local AI Chatbot with Memory

A local chatbot using Llama (via Ollama), Mem0 + ChromaDB for long-term memory, and an Streamlit UI. Runs entirely on your machine.

## Setup

```
python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # macOS / Linux

pip install litellm mem0ai chromadb streamlit ollama

ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

## Run

Make sure Ollama is running (`ollama serve` in a separate terminal if needed), then:

```
python chatbot.py
```

Or launch the web UI:

```
streamlit run app.py
```

Type `quit` or `exit` to stop the CLI version.