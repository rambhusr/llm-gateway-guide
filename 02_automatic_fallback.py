# OpenAI had a 4-hour outage in November 2023. Apps that hard-coded gpt-4 went completely dark.
# With a gateway, if one provider fails, we automatically fall back to another. Production apps must have this.

import os
from dotenv import load_dotenv
load_dotenv()
from litellm import completion

# Define a fallback chain: try llama-3.3 first, then Gemini, then allam-2-7b model
response = completion(
    model="groq/llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "What is an LLM Gateway?"}],
    fallbacks=[
        "gemini/gemini-2.5-flash",
        "groq/allam-2-7b"
    ]
)

print("Response:", response.choices[0].message.content[:200], "...")
print("\nWhich model actually answered?", response.model)