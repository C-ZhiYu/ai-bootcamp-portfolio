# Import
from mem0 import Memory

# Constants
MODEL = "llama3.2:3b"
OLLAMA = "http://localhost:11434"

# memory: Mem0 + ChromaDB + nomic-embed-text
config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "path": "./chroma_db"
        }
    },
    "embedder":{
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "ollama_base_url": OLLAMA
        }
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": MODEL,
            "ollama_base_url": OLLAMA
        }
    }
}

# Create memory
memory = Memory.from_config(config)

# Add a test memory
memory.add(
    "My name is Alex and I study at DigiPen",
    user_id="student1"
)

# Search memory
results = memory.search(
    "What is my name?",
    filters={"user_id": "student1"}
)

print(results)