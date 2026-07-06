# Libraries import
from litellm import completion
from mem0 import Memory

# Constants
MODEL = "gemma4:e2b"
MODEL_PATH = f"ollama/{MODEL}"
OLLAMA = "http://localhost:11434"

# Config | memory: Mem0 + ChromaDB + nomic-embed-text
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

# Function
def chat(user_message, history) :
    # Search memory for relevant context
    relevant = memory.search(user_message, filters={"user_id": "student1"})
    
    # Search Results (turn into plain text for the prompt)
    results = relevant["results"]
    memories_text = "\n".join(m["memory"] for m in results)
    
    # System Prompt
    system_prompt = (
        "You are a helpful assistant. Use these known facts about the user "
        "if relevant:\n" + (memories_text if memories_text else "No known facts yet.")
    )
    
    messages = [{"role": "system", "content": system_prompt}] + history + [
        {"role": "user", "content": user_message}
    ]

    # Call

    # Create a completion
    response = completion(
        model=MODEL_PATH,
        messages=messages,
        api_base=OLLAMA # localhost:11434
    )
    reply = response.choices[0].message.content

    # Save this turn to memory
    memory.add(
        [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": reply}
        ],
        user_id="student1"
    )

    return reply

# Main
if __name__ == "__main__":
    print("Chatbot ready. Type 'quit' to exit.")
    history = []
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue
        reply = chat(user_input, history)
        print(reply)
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": reply})