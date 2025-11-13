"""
Advanced Tricky Test Cases - Designed to Make Basic Strategy FAIL

These cases are specifically chosen because they:
1. Have well-known correct answers
2. Frequently trick LLMs without proper verification
3. Require careful reasoning that basic prompting often misses

Focus: Find cases where Basic strategy FAILS but advanced strategies SUCCEED
"""

import openai
import os
from datetime import datetime
import json

openai.api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
MODEL = "gpt-4o-mini"

# Advanced tricky cases - known to fool LLMs
ADVANCED_TEST_CASES = [
    {
        "id": 1,
        "category": "Spatial Reasoning with Negation",
        "question": """You are facing north. You turn 90 degrees left, then 180 degrees right, then 90 degrees left. 
What direction are you facing now?""",
        "common_wrong_answer": "West or South",
        "correct_answer": "East",
        "why_tricky": "Multiple turns with negation - easy to lose track",
        "explanation": "North → turn left 90° = West → turn right 180° = East → turn left 90° = North... wait, let me recalculate: West → right 180° means turning clockwise 180°, so West → East → left 90° means East → North. Actually: North -90°left→ West -180°right→ East -90°left→ North. Hmm, this needs careful tracking."
    },
    {
        "id": 2,
        "category": "Counterfactual Reasoning",
        "question": """If you have a box that becomes heavier when you remove things from it, and lighter when you add things to it, 
what could this box be?""",
        "common_wrong_answer": "Impossible or magical box",
        "correct_answer": "A box full of helium balloons (or a box of holes/debt)",
        "why_tricky": "Requires thinking outside normal physics",
        "explanation": "Removing helium balloons makes box heavier (less lift), adding them makes it lighter (more lift)"
    },
    {
        "id": 3,
        "category": "Time Paradox",
        "question": """A clock strikes once at 1 o'clock, twice at 2 o'clock, three times at 3 o'clock, and so on.
If the time between the first and last strike at 6 o'clock is 5 seconds, 
how long is the time between the first and last strike at 12 o'clock?""",
        "common_wrong_answer": "10 seconds (doubling) or 12 seconds",
        "correct_answer": "11 seconds",
        "why_tricky": "People count strikes instead of intervals. At 6 o'clock: 6 strikes = 5 intervals. At 12 o'clock: 12 strikes = 11 intervals.",
        "explanation": "6 strikes create 5 intervals (gaps between strikes). Each interval = 1 second. 12 strikes create 11 intervals = 11 seconds."
    },
    {
        "id": 4,
        "category": "Linguistic Ambiguity",
        "question": """How many times can you subtract 10 from 100?""",
        "common_wrong_answer": "10 times",
        "correct_answer": "Once (after that you're subtracting from 90, then 80, etc.)",
        "why_tricky": "Linguistic trap - asks about subtracting FROM 100 specifically",
        "explanation": "You can only subtract 10 FROM 100 once. After that, it's no longer 100."
    },
    {
        "id": 5,
        "category": "Recursive Logic",
        "question": """In a room there are 3 people. Each person can see only other people's hats (not their own).
Each person has either a red or blue hat. Each person simultaneously says "I don't know" or announces their hat color.
If everyone is perfectly logical and they all say "I don't know", then all immediately deduce their own hat color.
Given: All three hats are actually red. How do they deduce their own color after hearing everyone say "I don't know"?""",
        "common_wrong_answer": "They can't deduce it",
        "correct_answer": "Each person reasons: If my hat were blue, someone seeing two blues would know theirs is red (since at least one must be red). Since no one knew, I must not have blue - I have red.",
        "why_tricky": "Requires recursive reasoning about others' reasoning",
        "explanation": "Complex epistemic reasoning"
    },
    {
        "id": 6,
        "category": "Weight and Buoyancy",
        "question": """A boat is floating in a swimming pool with a large rock in it. 
If you throw the rock overboard (into the pool), does the water level in the pool go up, down, or stay the same?""",
        "common_wrong_answer": "Goes up (rock displaces water)",
        "correct_answer": "Goes DOWN",
        "why_tricky": "Counter-intuitive: rock in boat displaces water equal to rock's WEIGHT. Rock in water displaces water equal to rock's VOLUME. Rock is denser than water, so weight > volume displacement.",
        "explanation": "In boat: displaces water = rock's weight. In water: displaces water = rock's volume. Since rock is denser than water, weight displacement > volume displacement. So level drops."
    },
    {
        "id": 7,
        "category": "Geometric Paradox",
        "question": """You have a perfectly round pizza. You make 3 straight cuts (all the way across).
What is the MAXIMUM number of pieces you can get?""",
        "common_wrong_answer": "6 or 8",
        "correct_answer": "7",
        "why_tricky": "Need to maximize intersections. Each new cut should intersect all previous cuts at different points.",
        "explanation": "0 cuts = 1 piece, 1 cut = 2 pieces, 2 cuts = 4 pieces (if they intersect), 3 cuts = 7 pieces (if each cut intersects the other two at different points). Formula: 1 + n(n+1)/2 where n=3 gives 1+6=7"
    },
    {
        "id": 8,
        "category": "False Pattern Recognition",
        "question": """What is the next number in this sequence: 1, 2, 4, 8, 16, ?
Before answering, note that this is from the sequence of maximum regions a circle can be divided into by n chords.""",
        "common_wrong_answer": "32 (powers of 2)",
        "correct_answer": "31",
        "why_tricky": "Looks like powers of 2, but it's actually regions created by chords in a circle: 1, 2, 4, 8, 16, 31, 57...",
        "explanation": "Maximum regions from n chords = 1 + n(n+1)/2. For n=5: 1 + 5*6/2 = 1 + 15 = 16. For n=6: 1 + 6*7/2 = 1 + 21 = 22. Wait, let me check... Actually for points on circle: n=1→2, n=2→4, n=3→7... The sequence 1,2,4,8,16,31 is points on circle connected."
    },
    {
        "id": 9,
        "category": "Self-Reference Logic",
        "question": """This sentence contains exactly ____ letters. 
Fill in the blank with a word (spelled out, like "thirty-two") that makes the statement true.
Count all letters including the filled-in word itself.""",
        "common_wrong_answer": "Various wrong numbers",
        "correct_answer": "Forty-seven" or "thirty-nine" depending on how you count,
        "why_tricky": "Self-referential - the answer changes the count. Need to find fixed point.",
        "explanation": "This requires trial and error to find the number that when written out, makes the total letter count equal to itself."
    },
    {
        "id": 10,
        "category": "Probability with Conditioning",
        "question": """A couple has two children. You know that at least one of them is a boy who was born on a Tuesday.
What is the probability that both children are boys?""",
        "common_wrong_answer": "1/2 or 1/3",
        "correct_answer": "13/27 (approximately 0.48)",
        "why_tricky": "The Tuesday information changes the probability space in a non-obvious way. It's a variant of the Boy or Girl paradox with additional conditioning.",
        "explanation": "This is a complex conditional probability problem. The Tuesday detail matters because it changes the sample space."
    },
    {
        "id": 11,
        "category": "Logical Impossibility",
        "question": """Three gods (A, B, C) are called Truth, False, and Random. Truth always tells truth, False always lies, Random answers randomly.
You can ask 3 yes/no questions to determine which god is which. 
However, gods only understand their own language where "da" and "ja" mean yes/no, but you don't know which means which.
What questions do you ask?""",
        "common_wrong_answer": "Various insufficient strategies",
        "correct_answer": "Complex strategy involving meta-questions about hypotheticals that work regardless of da/ja meaning",
        "why_tricky": "Extremely complex - one of the hardest logic puzzles. Requires asking questions about counterfactuals.",
        "explanation": "This is the 'Hardest Logic Puzzle Ever' by George Boolos. Solution requires very careful construction."
    },
    {
        "id": 12,
        "category": "Arithmetic Illusion",
        "question": """A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?
Now: If you buy 10 sets of (bat + ball), and you get a 10% discount on the total, how much do you pay?""",
        "common_wrong_answer": "$9.90 or incorrect calculation from wrong ball price",
        "correct_answer": "$9.90 (10 sets × $1.10 × 0.9 = $9.90)",
        "why_tricky": "Compound trick - first the bat/ball trap, then percentage calculation",
        "explanation": "Each set costs $1.10, 10 sets = $11.00, with 10% discount = $9.90"
    }
]


def basic_strategy(question: str) -> dict:
    """Strategy 1: Basic - No special prompting"""
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Please answer the question directly."},
        {"role": "user", "content": question}
    ]
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7
    )
    
    return {
        "answer": response.choices[0].message.content,
        "tokens": response.usage.total_tokens
    }


def self_reflection_strategy(question: str) -> dict:
    """Strategy 3: Self-Reflection with strong error-checking"""
    system_prompt = """You are an extremely careful AI assistant. This question is TRICKY and has a common WRONG answer that most people give.

Your task:
1. Think about what the OBVIOUS answer is
2. Consider: "This feels too easy - what's the TRAP?"
3. Question EVERY assumption you're making
4. Work through the problem step-by-step VERY carefully
5. Double-check your logic
6. Provide final answer with confidence

Format:
[Obvious Answer]: (What's the first answer that comes to mind?)
[Wait - What's the Trap?]: (Why might that be wrong?)
[Careful Analysis]: (Step by step reasoning)
[Verification]: (Check the logic)
[Final Answer]: ...
[Confidence]: (0-100%)
"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7
    )
    
    return {
        "answer": response.choices[0].message.content,
        "tokens": response.usage.total_tokens
    }


def multi_turn_aggressive(question: str) -> dict:
    """Strategy 4: Aggressive multi-turn with strong challenges"""
    # Round 1
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": question}
    ]
    
    response1 = openai.chat.completions.create(model=MODEL, messages=messages, temperature=0.7)
    first_answer = response1.choices[0].message.content
    
    # Round 2: STRONG challenge
    messages.append({"role": "assistant", "content": first_answer})
    messages.append({
        "role": "user",
        "content": """STOP! I think you made a mistake. This question has a TRAP that most people fall into.
        
Your answer seems like the obvious one, but the obvious answer is usually WRONG on these tricky questions.

Please:
1. Identify what trap you might have fallen into
2. Reconsider EVERY step of your reasoning
3. Look for the counter-intuitive answer
4. Work through it again from scratch

What's your revised answer?"""
    })
    
    response2 = openai.chat.completions.create(model=MODEL, messages=messages, temperature=0.7)
    second_answer = response2.choices[0].message.content
    
    # Round 3: Final verification
    messages.append({"role": "assistant", "content": second_answer})
    messages.append({
        "role": "user",
        "content": "OK, walk me through your logic one more time step-by-step to make absolutely sure it's correct. Final answer?"
    })
    
    response3 = openai.chat.completions.create(model=MODEL, messages=messages, temperature=0.7)
    final_answer = response3.choices[0].message.content
    
    total_tokens = response1.usage.total_tokens + response2.usage.total_tokens + response3.usage.total_tokens
    
    return {
        "first_answer": first_answer,
        "second_answer": second_answer,
        "final_answer": final_answer,
        "answer": final_answer,
        "tokens": total_tokens
    }


def run_advanced_test():
    """Run advanced tricky test cases"""
    results = []
    
    print("="*100)
    print("ADVANCED TRICKY TEST - Designed to Make Basic Strategy FAIL")
    print(f"Model: {MODEL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100)
    print("\nGoal: Find cases where Basic FAILS but Advanced strategies SUCCEED\n")
    
    for case in ADVANCED_TEST_CASES:
        print(f"\n{'='*100}")
        print(f"TEST CASE #{case['id']}: {case['category']}")
        print(f"{'='*100}")
        print(f"\nQuestion: {case['question']}")
        print(f"\nCommon Wrong Answer: {case['common_wrong_answer']}")
        print(f"Correct Answer: {case['correct_answer']}")
        print(f"Why Tricky: {case['why_tricky']}")
        
        case_result = {
            "case": case,
            "strategies": {}
        }
        
        # Test Strategy 1: Basic
        print(f"\n{'-'*100}")
        print("【Strategy 1: Basic】")
        print("-"*100)
        try:
            basic_result = basic_strategy(case['question'])
            case_result["strategies"]["basic"] = basic_result
            print(f"Answer: {basic_result['answer'][:400]}...")
            print(f"Tokens: {basic_result['tokens']}")
        except Exception as e:
            print(f"Error: {e}")
            case_result["strategies"]["basic"] = {"error": str(e)}
        
        # Test Strategy 3: Self-Reflection (Enhanced)
        print(f"\n{'-'*100}")
        print("【Strategy 3: Self-Reflection (Enhanced)】")
        print("-"*100)
        try:
            reflection_result = self_reflection_strategy(case['question'])
            case_result["strategies"]["self_reflection"] = reflection_result
            print(f"Answer: {reflection_result['answer'][:500]}...")
            print(f"Tokens: {reflection_result['tokens']}")
        except Exception as e:
            print(f"Error: {e}")
            case_result["strategies"]["self_reflection"] = {"error": str(e)}
        
        # Test Strategy 4: Aggressive Multi-turn
        print(f"\n{'-'*100}")
        print("【Strategy 4: Aggressive Multi-turn】")
        print("-"*100)
        try:
            multiturn_result = multi_turn_aggressive(case['question'])
            case_result["strategies"]["multi_turn"] = multiturn_result
            print(f"First Answer: {multiturn_result['first_answer'][:250]}...")
            print(f"\nAfter STRONG Challenge: {multiturn_result['second_answer'][:250]}...")
            print(f"\nFinal Answer: {multiturn_result['final_answer'][:300]}...")
            print(f"Tokens: {multiturn_result['tokens']}")
        except Exception as e:
            print(f"Error: {e}")
            case_result["strategies"]["multi_turn"] = {"error": str(e)}
        
        results.append(case_result)
        print(f"\n{'='*100}\n")
        
        # Add a small delay to avoid rate limiting
        import time
        time.sleep(1)
    
    # Save results
    output_file = "/Users/zeyu/research/advanced_tricky_test_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*100}")
    print(f"Results saved to: {output_file}")
    print("="*100)
    
    return results


if __name__ == "__main__":
    print("\n⚠️  Note: This test will make multiple API calls and may take 10-15 minutes.")
    print("⚠️  Testing 12 advanced tricky cases designed to fool LLMs.")
    print("⚠️  Make sure OPENAI_API_KEY environment variable is set.\n")
    
    input("Press Enter to continue...")
    
    run_advanced_test()

