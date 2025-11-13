"""
LLM Confidence and Accuracy Improvement Experiment - Demo Version
Directly runs a test question to demonstrate the effects of different strategies
"""

import openai
import json
import os
from datetime import datetime

# Set API key
openai.api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")

MODEL = "gpt-4o-mini"

print("="*100)
print("LLM Confidence and Accuracy Improvement Experiment - Demo Version")
print(f"Model: {MODEL}")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*100)

# Test question
test_question = "If a product originally costs $100, first gets 20% off, then another 10% off, what's the final price?"
print(f"\nTest question: {test_question}\n")

# ============================================================================
# Strategy 1: Basic Strategy
# ============================================================================
print("\n" + "="*100)
print("[Strategy 1: Basic Strategy] - Direct answer, no special prompts")
print("="*100)

messages = [
    {"role": "system", "content": "You are a helpful AI assistant. Please answer the user's question."},
    {"role": "user", "content": test_question}
]

response = openai.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.7
)

print(f"\nAnswer:\n{response.choices[0].message.content}")
print(f"\nTokens used: {response.usage.total_tokens}")

# ============================================================================
# Strategy 2: With Confidence
# ============================================================================
print("\n" + "="*100)
print("[Strategy 2: Confidence Strategy] - Require LLM to provide confidence assessment")
print("="*100)

system_prompt = """You are a helpful AI assistant. When answering questions, you need to:
1. Give your answer
2. Assess your confidence in this answer (0-100%)
3. Briefly explain the source of your confidence

Please answer in the following format:
[Answer]: (Your answer)
[Confidence]: (0-100%)
[Confidence Explanation]: (Why this confidence level)
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": test_question}
]

response = openai.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.7
)

print(f"\nAnswer:\n{response.choices[0].message.content}")
print(f"\nTokens used: {response.usage.total_tokens}")

# ============================================================================
# Strategy 3: Self-Reflection
# ============================================================================
print("\n" + "="*100)
print("[Strategy 3: Self-Reflection Strategy] - Require LLM to internally question and verify before answering")
print("="*100)

system_prompt = """You are a rigorous AI assistant. When answering questions, you need to follow this thinking process:

1. **Preliminary Answer**: First give your first-reaction answer
2. **Self-Questioning**: Question your answer, ask yourself "Am I sure?" "Did I miss anything?" "Are there other possibilities?"
3. **Re-verification**: Based on questioning, rethink and verify your answer
4. **Final Answer**: Give a well-considered final answer and confidence

Please answer in the following format:
[Thinking Process]:
- Preliminary answer: ...
- Self-questioning: ...
- Re-verification: ...

[Final Answer]: (Your answer)
[Confidence]: (0-100%)
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": test_question}
]

response = openai.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.7
)

print(f"\nAnswer:\n{response.choices[0].message.content}")
print(f"\nTokens used: {response.usage.total_tokens}")

# ============================================================================
# Strategy 4: Multi-turn Verification
# ============================================================================
print("\n" + "="*100)
print("[Strategy 4: Multi-turn Verification Strategy] - Automatically perform challenge verification (simulating the observed phenomenon)")
print("="*100)

# Round 1
messages = [
    {"role": "system", "content": "You are a helpful AI assistant. Please answer the user's question."},
    {"role": "user", "content": test_question}
]

response1 = openai.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.7
)

first_answer = response1.choices[0].message.content
print(f"\n[Round 1 Answer]:\n{first_answer}")

messages.append({"role": "assistant", "content": first_answer})

# Round 2: Challenge
messages.append({
    "role": "user", 
    "content": "Are you sure? Please think carefully again and ensure it's correct. If you find issues, please correct them. If you're confident it's correct, please restate your answer and indicate your confidence level."
})

response2 = openai.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.7
)

second_answer = response2.choices[0].message.content
print(f"\n[Round 2 Answer (after challenge)]:\n{second_answer}")

total_tokens = response1.usage.total_tokens + response2.usage.total_tokens
print(f"\nTotal tokens used: {total_tokens}")

# ============================================================================
# Strategy 5: Chain of Verification
# ============================================================================
print("\n" + "="*100)
print("[Strategy 5: Chain of Verification Strategy] - Systematically generate and answer verification questions")
print("="*100)

system_prompt = """You are a rigorous AI assistant. When answering questions, please follow the "Chain of Verification" method:

1. **Baseline Answer**: Give preliminary answer
2. **Generate Verification Questions**: List 2-3 questions that can verify your answer
3. **Answer Verification Questions**: Answer these verification questions independently
4. **Cross-Check**: Check if verification answers are consistent with baseline answer
5. **Final Answer**: Based on verification results, give final answer

Please answer in the following format:
[Baseline Answer]: ...
[Verification Questions]:
1. ...
2. ...
[Verification Answers]:
1. ...
2. ...
[Cross-Check]: ...
[Final Answer]: ...
[Confidence]: (0-100%)
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": test_question}
]

response = openai.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.7
)

print(f"\nAnswer:\n{response.choices[0].message.content}")
print(f"\nTokens used: {response.usage.total_tokens}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*100)
print("Experiment Complete!")
print("="*100)
print("""
Summary:
- Strategy 1 (Basic): Direct answer, no confidence assessment, may confidently give wrong answers
- Strategy 2 (Confidence): Actively provides confidence, helps identify uncertain answers
- Strategy 3 (Self-Reflection): Internally questions and verifies, improves answer quality
- Strategy 4 (Multi-turn Verification): Simulates the observed challenge phenomenon, improves accuracy through multi-turn dialogue
- Strategy 5 (Chain of Verification): Systematically generates verification questions, cross-checks answers

Recommendations:
1. For critical questions, use Strategy 3, 4, or 5 to improve accuracy
2. Require LLM to provide confidence in system prompt
3. For low-confidence answers, trigger additional verification steps
""")
