# LiteLLM supports custom callbacks

import litellm
from litellm import completion
import os
from dotenv import load_dotenv
load_dotenv()

# A simple in-memory log store
call_logs = []

def log_success(kwargs, completion_response, start_time, end_time):
    """Called automatically after every successful LLM call."""
    call_logs.append({
        "model": kwargs.get("model"),
        "prompt": kwargs["messages"][-1]["content"][:60],
        "input_tokens": completion_response.usage.prompt_tokens,
        "output_tokens": completion_response.usage.completion_tokens,
        "latency_sec": round((end_time - start_time).total_seconds(), 2),
        "cost_usd": kwargs.get("response_cost", 0),
        "user": kwargs.get("user", "anonymous")
    })

def log_failure(kwargs, completion_response, start_time, end_time):
    print("❌ Call failed:", kwargs.get("exception"))

# Register the callbacks
litellm.success_callback = [log_success]
litellm.failure_callback = [log_failure]

# Make a few tagged calls
for q, user in [
    ("What is RAG?", "Ram"),
    ("Explain transformers.", "Bhuvanesh"),
    ("What is fine-tuning?", "Ram"),
]:
    completion(
        model="gemini/gemini-2.5-flash",
        messages=[{"role": "user", "content": q}],
        user=user  # tag the call for attribution
    )

# Review the audit log
import json
print(json.dumps(call_logs, indent=2, default=str))