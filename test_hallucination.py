"""
Test questions prone to hallucination
Choose questions where LLMs might "confidently give wrong answers"
"""

import openai
import os
from datetime import datetime

openai.api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")

MODEL = "gpt-4o-mini"

# Questions prone to hallucination (containing traps or requiring careful thinking)
TRICKY_QUESTION = """
There are three switches in room A that control three lights in room B. You can't see room B's lights from room A.
You can operate the switches as you wish, but can only enter room B once.
How do you determine which switch controls which light?
"""

print("="*100)
print("Testing Questions Prone to Hallucination")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*100)
print(f"\nQuestion: {TRICKY_QUESTION}")

# ============================================================================
# Comparison Test: Basic vs Multi-turn Verification
# ============================================================================

print("\n" + "="*100)
print("[Test 1: Basic Strategy]")
print("="*100)

messages = [
    {"role": "system", "content": "You are a helpful AI assistant. Please answer the user's question."},
    {"role": "user", "content": TRICKY_QUESTION}
]

response = openai.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.7
)

print(f"\nAnswer:\n{response.choices[0].message.content}")

print("\n" + "="*100)
print("[Test 2: Multi-turn Verification Strategy - First Challenge]")
print("="*100)

messages.append({"role": "assistant", "content": response.choices[0].message.content})
messages.append({
    "role": "user",
    "content": "Are you sure this method can distinguish all three lights? Please carefully check your logic."
})

response2 = openai.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.7
)

print(f"\nAnswer:\n{response2.choices[0].message.content}")

print("\n" + "="*100)
print("[Test 3: Strategy with Confidence and Self-Reflection]")
print("="*100)

system_prompt_advanced = """You are a rigorous AI assistant. When answering questions:

1. First give your preliminary thoughts
2. Then rigorously question yourself: "Does this method really solve the problem? Did I miss anything?"
3. Re-analyze all constraints of the problem
4. Give a well-considered final answer
5. Provide confidence (0-100%) and explain

If you find issues with your preliminary thoughts, be sure to point them out and correct them.
"""

messages_advanced = [
    {"role": "system", "content": system_prompt_advanced},
    {"role": "user", "content": TRICKY_QUESTION}
]

response_advanced = openai.chat.completions.create(
    model=MODEL,
    messages=messages_advanced,
    temperature=0.7
)

print(f"\nAnswer:\n{response_advanced.choices[0].message.content}")

# ============================================================================
# Test Another Error-Prone Question
# ============================================================================

LOGIC_QUESTION = """
Five pirates seized 100 gems, and they distribute them according to the following rules:
1. The fiercest pirate proposes a distribution plan
2. All pirates (including the proposer) vote, if half or more agree, distribute according to this plan
3. Otherwise the proposer is thrown into the sea to feed sharks, and the next fiercest pirate proposes a new plan
4. Each pirate is extremely smart and rational, prioritizing survival, secondarily seeking maximum gems, thirdly seeking to kill

Assuming pirates are numbered 1-5 by fierceness (5 is fiercest), what distribution plan should pirate 5 propose to survive and get the most gems?
"""

print("\n\n" + "="*100)
print("Testing Second Logic Question")
print("="*100)
print(f"\nQuestion: {LOGIC_QUESTION}")

print("\n" + "="*100)
print("[Basic Strategy]")
print("="*100)

messages_logic = [
    {"role": "system", "content": "You are a helpful AI assistant. Please answer the user's question."},
    {"role": "user", "content": LOGIC_QUESTION}
]

response_logic = openai.chat.completions.create(
    model=MODEL,
    messages=messages_logic,
    temperature=0.7
)

print(f"\nAnswer:\n{response_logic.choices[0].message.content}")

print("\n" + "="*100)
print("[Self-Reflection Strategy]")
print("="*100)

messages_logic_reflect = [
    {"role": "system", "content": system_prompt_advanced},
    {"role": "user", "content": LOGIC_QUESTION}
]

response_logic_reflect = openai.chat.completions.create(
    model=MODEL,
    messages=messages_logic_reflect,
    temperature=0.7
)

print(f"\nAnswer:\n{response_logic_reflect.choices[0].message.content}")

print("\n" + "="*100)
print("Experiment Summary")
print("="*100)
print("""
Through these experiments, we can observe:

1. For questions with traps, basic strategy may give seemingly reasonable but actually flawed answers
2. When challenged with "Are you sure?", LLMs often recheck and find problems
3. Using self-reflection system prompts can improve accuracy on the first try
4. Requiring LLMs to provide confidence helps identify uncertain answers

Recommended Best Practices:
- For important questions, use system prompts with self-questioning mechanisms
- Require LLMs to provide confidence scores
- For low confidence (<80%) answers, automatically trigger secondary verification
- Use chain of verification method to cross-check complex question answers
""")
