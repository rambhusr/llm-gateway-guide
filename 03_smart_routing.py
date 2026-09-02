import os
from dotenv import load_dotenv
load_dotenv()
from litellm import Router

model_list = [
    {
        "model_name": "fast-cheap",
        "litellm_params": {
            "model": "groq/allam-2-7b",
            "api_key": os.getenv("GROQ_API_KEY")
        }
    },
    {
        "model_name": "smart-coding",                              # 👈 alias kept
        "litellm_params": {
            "model": "gemini/gemini-2.5-flash",                                      # 👈 mapped to OpenAI instead
            "api_key": os.getenv("GEMINI_API_KEY")
        }
    }
]

router = Router(model_list=model_list)

fast_response = router.completion(
    model="fast-cheap",
    messages=[{"role": "user", "content": "Summarize: LLM Gateway."}]
)

code_response = router.completion(
    model="smart-coding",
    messages=[{"role": "user", "content": "Write a Python function to reverse a string."}]
)

print("⚡ Fast/cheap (Groq): ", fast_response.choices[0].message.content[:150])
print("\n🧠 Smart/coding (Gemini):\n", code_response.choices[0].message.content[:300])