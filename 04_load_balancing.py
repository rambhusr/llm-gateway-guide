# Hit rate limits on one API key Provider? Add more keys to the same alias — the router load-balances automatically.
# Strategy-1: least-busy The router tracks how many requests are currently in flight to each deployment and sends the new request to whichever one is least busy.
# Strategy-2: latency-based-routing The router measures the response time of each deployment over recent calls and sends new requests to whichever has been fastest.
# Strategy-3: simple-shuffle. The router sends request randomly
# Strategy-4: cost-based-routing. Pick the deployment that costs the least per token right now

import os
from dotenv import load_dotenv
load_dotenv()
from litellm import Router
from collections import Counter

model_list = [
    {"model_name": "chat",
     "litellm_params": {"model": "gemini/gemini-2.5-flash",
                        "api_key": os.getenv("GEMINI_API_KEY")},
     "model_info": {"id": "🔵 GeminiAI"}},
    {"model_name": "chat",
     "litellm_params": {"model": "groq/allam-2-7b",
                        "api_key": os.getenv("GROQ_API_KEY")},
     "model_info": {"id": "🟢 Groq"}},
]

router = Router(
    model_list=model_list,
    routing_strategy="least-busy"   # 👈 the magic
)

hits = Counter()
for i in range(8):
    r = router.completion(
        model="chat",
        messages=[{"role": "user", "content": f"Say 'OK' #{i}"}],
        max_tokens=5
    )
    hits[r._hidden_params.get("model_id", "?")] += 1
    print(f"Request {i+1} → {r._hidden_params.get('model_id', '?')}")

print("\n🎯 Distribution:")
for k, v in hits.most_common():
    print(f"   {k}: {'█' * v} ({v})")