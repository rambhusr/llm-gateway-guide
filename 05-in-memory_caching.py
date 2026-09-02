import litellm
import time
from litellm import completion
from litellm.caching import Cache
import os
from dotenv import load_dotenv
load_dotenv()

# 🧹 Reset any callbacks/strategies left over from earlier cells
litellm.callbacks = []
litellm.success_callback = []
litellm.failure_callback = []
litellm._async_success_callback = []
litellm._async_failure_callback = []

# Also clear any router-strategy state
litellm.cache = None

print("✅ LiteLLM state reset — ready for clean caching demo")

# Enable in-memory caching (you can also use Redis in production)
litellm.cache = Cache(type="local")

prompt = "What does LLM stand for? Answer in one line."

# First call — actually hits OpenAI
start = time.time()
r1 = completion(
    model="gemini/gemini-2.5-flash",
    messages=[{"role": "user", "content": prompt}],
    caching=True
)
t1 = time.time() - start
print(f"❄️  First call (API):   {t1:.2f}s — {r1.choices[0].message.content}")

# Second call — served from cache, near-instant
start = time.time()
r2 = completion(
    model="gemini/gemini-2.5-flash",
    messages=[{"role": "user", "content": prompt}],
    caching=True
)
t2 = time.time() - start
print(f"⚡ Second call (cache): {t2:.4f}s — {r2.choices[0].message.content}")

print(f"\n🚀 Speedup: {t1/t2:.1f}x faster, and ZERO cost on the second call!")