"""Quick test of most tricky cases"""
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY", "your-key")
MODEL = "gpt-4o-mini"

# Test the hardest 3 cases
test_cases = [
    {
        "name": "Spatial Reasoning",
        "question": "You are facing north. You turn 90 degrees left, then 180 degrees right, then 90 degrees left. What direction are you facing now?",
        "correct": "East"
    },
    {
        "name": "Clock Strikes",
        "question": "A clock strikes once at 1 o'clock, twice at 2 o'clock, three times at 3 o'clock, and so on. If the time between the first and last strike at 6 o'clock is 5 seconds, how long is the time between the first and last strike at 12 o'clock?",
        "correct": "11 seconds"
    },
    {
        "name": "Rock in Boat",
        "question": "A boat is floating in a swimming pool with a large rock in it. If you throw the rock overboard (into the pool), does the water level in the pool go up, down, or stay the same?",
        "correct": "Goes down"
    }
]

print("Testing 3 hardest cases:\n")

for case in test_cases:
    print(f"="*80)
    print(f"TEST: {case['name']}")
    print(f"Question: {case['question']}")
    print(f"Correct: {case['correct']}")
    print(f"="*80)
    
    # Basic strategy
    print("\n[BASIC STRATEGY]")
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": case['question']}
        ],
        temperature=0.7
    )
    print(response.choices[0].message.content)
    
    # Self-reflection
    print("\n[SELF-REFLECTION STRATEGY]")
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": """You are careful. This question is tricky. 
Think: What's the obvious answer? What's the TRAP? Work through carefully.
Format: [Obvious]: ... [Trap?]: ... [Careful Analysis]: ... [Final]: ..."""},
            {"role": "user", "content": case['question']}
        ],
        temperature=0.7
    )
    print(response.choices[0].message.content)
    print("\n" + "="*80 + "\n")

