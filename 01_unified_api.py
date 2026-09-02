# The biggest pain point: every provider has a different SDK.
# LiteLLM gives you one function — completion() — that works with all of them
# Same code, three different providers. This alone is huge — you can switch providers with a string change.


import warnings
warnings.filterwarnings("ignore")

import logging
logging.getLogger("LiteLLM").setLevel(logging.ERROR)

# Now import LiteLLM normally
from litellm import completion

import litellm
litellm.suppress_debug_info = True

import os
from dotenv import load_dotenv
load_dotenv()

# Quick check
print("OpenAI key loaded:    ", "✅" if os.getenv("OPENAI_API_KEY") else "❌")
print("Anthropic key loaded: ", "✅" if os.getenv("ANTHROPIC_API_KEY") else "❌")
print("Groq key loaded:      ", "✅" if os.getenv("GROQ_API_KEY") else "❌")
print("Gemini key loaded:      ", "✅" if os.getenv("GEMINI_API_KEY") else "❌")

#import completion which is unified API offered by LiteLLM
from litellm import completion

# Same code, different providers — just change the `model` string!

# Call OpenAI
response_gemini = completion(
    model="gemini/gemini-2.5-flash",
    messages=[{"role": "user", "content": "Explain RAG in one sentence."}]
)
print("🔵 Gemini:    ", response_gemini.choices[0].message.content)

# Call Groq (super fast inference)
response_groq = completion(
    model="groq/allam-2-7b",
    messages=[{"role": "user", "content": "Explain RAG in one sentence."}]
)
print("🟢 Groq:      ", response_groq.choices[0].message.content)