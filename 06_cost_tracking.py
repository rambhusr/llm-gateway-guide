# LiteLLM automatically calculates the cost of every call using its built-in pricing database.

from litellm import completion, completion_cost
import os
from dotenv import load_dotenv
load_dotenv()

response = completion(
    model="gemini/gemini-2.5-flash",
    messages=[{"role": "user", "content": "Write about LLM Gateway."}]
)

# Get the exact USD cost of this single call
cost = completion_cost(completion_response=response)

print("Response:    ", response.choices[0].message.content)
print("\nInput tokens: ", response.usage.prompt_tokens)
print("Output tokens:", response.usage.completion_tokens)
print(f"Cost:         ${cost:.8f}")