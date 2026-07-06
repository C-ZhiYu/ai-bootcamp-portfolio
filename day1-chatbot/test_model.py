# Import
from litellm import completion

# Constants
MODEL = "ollama/gemma4:e2b"

# Create a completion
response = completion(
    model=MODEL,
    messages=[
        {"role": "user", "content": "Say hello in one sentence"}
    ],
    api_base="http://localhost:11434"
)

# Print the response
print(response.choices[0].message.content)