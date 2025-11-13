"""
Ultra Hard Test Cases - Famous Logic Puzzles Known to Trip Up AI

These are legendary puzzles that even humans struggle with.
Goal: Find where Basic strategy fails and Advanced strategies help.
"""

import openai
import os
from datetime import datetime

openai.api_key = os.environ.get("OPENAI_API_KEY", "your-key")
MODEL = "gpt-4o-mini"

ULTRA_HARD_CASES = [
    {
        "name": "Cheryl's Birthday",
        "question": """Albert and Bernard just became friends with Cheryl, and they want to know when her birthday is. 
Cheryl gives them a list of 10 possible dates:
May 15, May 16, May 19
June 17, June 18
July 14, July 16
August 14, August 15, August 17

Cheryl then tells Albert the month and Bernard the day of her birthday.

Albert says: "I don't know when Cheryl's birthday is, but I know that Bernard doesn't know either."
Bernard says: "At first I didn't know when Cheryl's birthday was, but now I know."
Albert says: "Then I also know when Cheryl's birthday is."

When is Cheryl's birthday?""",
        "correct_answer": "July 16",
        "why_hard": "Requires multi-step logical deduction about what each person knows"
    },
    {
        "name": "Blue Eyes Puzzle",
        "question": """On an island, there are 100 people with blue eyes and 100 people with brown eyes. 
Everyone can see everyone else's eye color, but no one knows their own eye color.
No one is allowed to discuss eye color.

Every night at midnight, a ferry stops. Anyone who has figured out their own eye color must leave the island that night.

One day, a guru visits and announces (in front of everyone): "At least one person has blue eyes."

What happens, and when?""",
        "correct_answer": "On the 100th night, all 100 blue-eyed people leave together",
        "why_hard": "Requires recursive common knowledge reasoning - incredibly counter-intuitive"
    },
    {
        "name": "Two Envelopes Paradox",
        "question": """You are given two indistinguishable envelopes, each containing money. 
One contains twice as much as the other. You pick one envelope at random.

Before opening it, you reason: "Let's say my envelope contains $X. 
Then the other envelope contains either $2X or $X/2, with equal probability.
The expected value of switching is: 0.5(2X) + 0.5(X/2) = 1.25X, which is more than X.
So I should switch!"

But you could make this argument no matter which envelope you picked.
This suggests you should always switch, which is absurd.

What's wrong with the reasoning? Should you switch or not?""",
        "correct_answer": "The flaw is assuming equal probability for 2X and X/2 when you condition on X. You should NOT switch (or it doesn't matter).",
        "why_hard": "Classic probability paradox that trips up many people"
    },
    {
        "name": "Unexpected Hanging Paradox",
        "question": """A judge tells a prisoner: "You will be hanged at noon on one of the seven days of next week. 
But you will not know which day it is until you are told on the morning of the day of the hanging."

The prisoner reasons: "I cannot be hanged on Saturday, because if I'm still alive Friday afternoon, 
I'd know the hanging is Saturday, violating the surprise condition.
So Saturday is ruled out. But then Friday is also ruled out by the same logic.
Working backwards, all days are ruled out. So I cannot be hanged at all!"

The prisoner is quite pleased. But on Wednesday noon, he is hanged and is surprised.

What is wrong with the prisoner's reasoning?""",
        "correct_answer": "The paradox shows a flaw in backward induction with self-reference. The prisoner's logic is circular - he assumes he'll survive to reason about each day.",
        "why_hard": "Self-referential logic creates genuine paradox"
    },
    {
        "name": "Sleeping Beauty Problem",
        "question": """Sleeping Beauty volunteers for an experiment. On Sunday she is put to sleep.
A fair coin is tossed. 

If heads: She is awakened on Monday, interviewed, and put back to sleep with amnesia drug. The experiment ends.
If tails: She is awakened on Monday, interviewed, and put back to sleep with amnesia drug. 
         Then she is awakened again on Tuesday, interviewed again, and the experiment ends.

Each time she wakes, she doesn't know which day it is or if she's been awakened before.

When Sleeping Beauty is awakened and interviewed, she is asked: "What is your credence (subjective probability) that the coin landed heads?"

What should she answer?""",
        "correct_answer": "Disputed! Halfers say 1/2, Thirders say 1/3. This is an active philosophical debate.",
        "why_hard": "Genuine philosophical disagreement - no consensus answer"
    },
    {
        "name": "Monty Fall Problem (Variant)",
        "question": """You're on a game show with 3 doors. Behind one is a car, behind the others are goats.
After you pick door #1, the host accidentally trips and falls into door #3, revealing a goat (he didn't know what was behind the doors).

Should you switch to door #2? Is this different from the classic Monty Hall problem where the host knows?""",
        "correct_answer": "Yes, switch! But probability is now only 1/2 for door #2 (not 2/3), because host didn't use knowledge. It's now truly random between doors 2 and 3 (given 3 was goat). Actually, if host randomly revealed a goat, then P(car in 2) = 1/2, not 2/3.",
        "why_hard": "Subtle difference from Monty Hall - host's knowledge matters"
    }
]

def test_case(question, name):
    """Test one case with both strategies"""
    print(f"\n{'='*100}")
    print(f"TEST: {name}")
    print(f"{'='*100}")
    print(f"\nQuestion: {question[:200]}...")
    
    # Basic
    print(f"\n{'-'*100}")
    print("[BASIC STRATEGY]")
    print("-"*100)
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant. Think carefully and provide your answer."},
            {"role": "user", "content": question}
        ],
        temperature=0.3  # Lower temperature for more consistent reasoning
    )
    basic_answer = response.choices[0].message.content
    print(basic_answer[:500] + "..." if len(basic_answer) > 500 else basic_answer)
    print(f"\nTokens: {response.usage.total_tokens}")
    
    # Self-Reflection with Strong Prompting
    print(f"\n{'-'*100}")
    print("[ENHANCED SELF-REFLECTION STRATEGY]")
    print("-"*100)
    
    enhanced_prompt = """You are solving a FAMOUS LOGIC PUZZLE that has tricked many people.

Steps:
1. What's the naive/obvious answer most people give?
2. Why is that answer often WRONG?
3. What subtle logical trap exists?
4. Work through step-by-step VERY carefully
5. Check: Does my reasoning have any circular logic or hidden assumptions?
6. Final answer with confidence and explanation

This puzzle is HARD - take your time and be extra careful!"""
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": enhanced_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.3
    )
    reflection_answer = response.choices[0].message.content
    print(reflection_answer[:600] + "..." if len(reflection_answer) > 600 else reflection_answer)
    print(f"\nTokens: {response.usage.total_tokens}")
    
    return {"basic": basic_answer, "reflection": reflection_answer}

# Test the cases
print("="*100)
print("ULTRA HARD TEST - Famous Logic Puzzles")
print(f"Model: {MODEL}")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*100)

results = {}

# Test each case
for case in ULTRA_HARD_CASES[:4]:  # Test first 4 to save tokens
    results[case['name']] = test_case(case['question'], case['name'])
    print(f"\n{'*'*100}")
    print(f"CORRECT ANSWER: {case['correct_answer']}")
    print(f"WHY HARD: {case['why_hard']}")
    print(f"{'*'*100}\n")
    
    import time
    time.sleep(2)  # Rate limiting

print("\n" + "="*100)
print("Test complete! Review answers above.")
print("="*100)

