# LiteLLM gives you two callback hooks that are all you need:
# litellm.input_callback — runs before the LLM call (inspect/modify the prompt)
# litellm.success_callback — runs after a successful LLM call (inspect/modify the response)
# Inside these hooks, you can do any Python you want — regex, keyword matching, or even another LLM call for classification. No external libraries needed.Let me show you the full guardrail stack with just LiteLLM.

import re
import litellm
from litellm import completion
import os
from dotenv import load_dotenv
load_dotenv()

# 🎯 PII patterns — simple, fast, no external dependencies
PII_PATTERNS = {
    "EMAIL":       r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "PHONE_IN":    r"(\+91[\-\s]?)?[6-9]\d{9}",                  # Indian mobile
    "PHONE_US":    r"(\+1[\-\s]?)?\(?\d{3}\)?[\-\s]?\d{3}[\-\s]?\d{4}",
    "SSN":         r"\b\d{3}-\d{2}-\d{4}\b",
    "AADHAAR":     r"\b\d{4}\s?\d{4}\s?\d{4}\b",                 # Indian Aadhaar
    "PAN":         r"\b[A-Z]{5}\d{4}[A-Z]\b",                    # Indian PAN
    "CREDIT_CARD": r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",
    "IP_ADDRESS":  r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
}


def redact_pii(text: str):
    """Replace PII in text with placeholders. Returns (clean_text, detected_list)."""
    detected = []
    clean = text
    for label, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, clean)
        if matches:
            detected.append({"type": label, "count": len(matches)})
            clean = re.sub(pattern, f"<{label}_REDACTED>", clean)
    return clean, detected


def pii_input_guardrail(kwargs):
    """LiteLLM pre-call hook: scrub PII from user messages."""
    messages = kwargs.get("messages", [])
    for msg in messages:
        if msg.get("role") == "user":
            clean, detected = redact_pii(msg["content"])
            if detected:
                print(f"🚨 PII REDACTED: {detected}")
                msg["content"] = clean


# Register the guardrail
litellm.input_callback = [pii_input_guardrail]


# 🧪 Test
user_msg = (
    "Hi, I'm Ram. My email is rambhuvanesh96@gmail.com, "
    "my Indian mobile is +91-9488123456, my PAN is ABCDE1234F, "
    "and my Aadhaar is 1234 5678 9012."
)

response = completion(
    model="gemini/gemini-2.5-flash",
    messages=[{"role": "user", "content": user_msg}],
    max_tokens=80
)

print("\n💬 LLM Response:")
print(response.choices[0].message.content)