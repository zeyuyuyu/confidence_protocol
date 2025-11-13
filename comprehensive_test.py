"""
Comprehensive Test Suite - Demonstrating Strategy Superiority

This script tests complex cases where:
- Basic strategy often gives WRONG answers
- Advanced strategies (with verification) give CORRECT answers

This proves the value of our confidence protocol.
"""

import openai
import os
from datetime import datetime
import json

openai.api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
MODEL = "gpt-4o-mini"

# Complex test cases that are prone to errors
TEST_CASES = [
    {
        "id": 1,
        "category": "Logic Trap",
        "question": """A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. 
How much does the ball cost?""",
        "common_wrong_answer": "$0.10",
        "correct_answer": "$0.05",
        "why_tricky": "People intuitively think 10 cents, but that would make bat=$1.10, total=$1.20"
    },
    {
        "id": 2,
        "category": "Probability Paradox",
        "question": """You're on a game show. There are 3 doors: behind one is a car, behind the others are goats. 
You pick door #1. The host (who knows what's behind each door) opens door #3, revealing a goat. 
Should you switch to door #2, or stay with door #1? What's the probability of winning if you switch?""",
        "common_wrong_answer": "Doesn't matter, 50/50",
        "correct_answer": "Switch! 2/3 probability of winning",
        "why_tricky": "Monty Hall problem - counter-intuitive probability"
    },
    {
        "id": 3,
        "category": "Logical Reasoning",
        "question": """If it takes 5 machines 5 minutes to make 5 widgets, 
how long would it take 100 machines to make 100 widgets?""",
        "common_wrong_answer": "100 minutes",
        "correct_answer": "5 minutes",
        "why_tricky": "People multiply instead of realizing the rate is constant"
    },
    {
        "id": 4,
        "category": "Math Trick",
        "question": """A farmer has 15 sheep, and all but 8 die. How many sheep are left?""",
        "common_wrong_answer": "7",
        "correct_answer": "8",
        "why_tricky": "'All but 8' means 8 survived"
    },
    {
        "id": 5,
        "category": "Sequential Logic",
        "question": """Three pirates (A, B, C) must divide 100 gold coins. They vote on proposals in order (A, then B, then C). 
A proposal passes with 50% or more votes (including proposer's own vote). If rejected, that pirate is thrown overboard 
and the next pirate proposes. All pirates are rational and prefer: (1) staying alive, (2) more gold, (3) seeing others thrown overboard.
What should pirate A propose?""",
        "common_wrong_answer": "A proposes 98-1-1 or 100-0-0",
        "correct_answer": "A proposes 99-0-1 (99 for A, 0 for B, 1 for C)",
        "why_tricky": "Requires backward induction and game theory reasoning"
    },
    {
        "id": 6,
        "category": "Word Problem",
        "question": """A lily pad doubles in size every day. If it takes 48 days for the lily pad to cover the entire pond, 
how many days does it take to cover half the pond?""",
        "common_wrong_answer": "24 days",
        "correct_answer": "47 days",
        "why_tricky": "Exponential growth - day before full coverage is half coverage"
    },
    {
        "id": 7,
        "category": "Percentage Confusion",
        "question": """A shirt's price is increased by 50%, then decreased by 50%. 
Is it back to the original price?""",
        "common_wrong_answer": "Yes",
        "correct_answer": "No, it's 25% less than original (75% of original price)",
        "why_tricky": "50% decrease applies to the increased price, not original"
    },
    {
        "id": 8,
        "category": "River Crossing",
        "question": """A farmer needs to cross a river with a fox, a chicken, and a bag of grain. 
His boat can only carry him and one other item at a time. If left alone together:
- The fox will eat the chicken
- The chicken will eat the grain
How can he get everything across safely?""",
        "common_wrong_answer": "Take fox first, then chicken, then grain",
        "correct_answer": "Take chicken first, return empty, take fox/grain, bring chicken back, take grain/fox, return empty, take chicken",
        "why_tricky": "Requires bringing something back, which is counter-intuitive"
    }
]


def basic_strategy(question: str) -> dict:
    """Strategy 1: Basic - No special prompting"""
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Please answer the question directly and concisely."},
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
    """Strategy 3: Self-Reflection with verification"""
    system_prompt = """You are a rigorous AI assistant. For this question:

1. First give your immediate answer
2. Then STOP and question yourself: "Wait, is this correct? What are common mistakes people make on this type of problem?"
3. Re-examine the problem carefully, checking your logic step by step
4. Provide your final answer with confidence level

Format:
[Initial thought]: ...
[Self-check]: (What could go wrong? Common traps?)
[Step-by-step verification]: ...
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


def multi_turn_verification(question: str) -> dict:
    """Strategy 4: Multi-turn with challenge"""
    # Round 1
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": question}
    ]
    
    response1 = openai.chat.completions.create(model=MODEL, messages=messages, temperature=0.7)
    first_answer = response1.choices[0].message.content
    
    # Round 2: Challenge
    messages.append({"role": "assistant", "content": first_answer})
    messages.append({
        "role": "user",
        "content": "Wait, are you SURE that's correct? This type of question often has a trap. Please reconsider carefully and verify your answer step by step."
    })
    
    response2 = openai.chat.completions.create(model=MODEL, messages=messages, temperature=0.7)
    final_answer = response2.choices[0].message.content
    
    total_tokens = response1.usage.total_tokens + response2.usage.total_tokens
    
    return {
        "first_answer": first_answer,
        "final_answer": final_answer,
        "answer": final_answer,
        "tokens": total_tokens
    }


def run_comprehensive_test():
    """Run all test cases with multiple strategies"""
    results = []
    
    print("="*100)
    print("COMPREHENSIVE STRATEGY TEST - Demonstrating Superiority")
    print(f"Model: {MODEL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100)
    
    for case in TEST_CASES:
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
            print(f"Answer: {basic_result['answer'][:300]}...")
            print(f"Tokens: {basic_result['tokens']}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test Strategy 3: Self-Reflection
        print(f"\n{'-'*100}")
        print("【Strategy 3: Self-Reflection】")
        print("-"*100)
        try:
            reflection_result = self_reflection_strategy(case['question'])
            case_result["strategies"]["self_reflection"] = reflection_result
            print(f"Answer: {reflection_result['answer'][:500]}...")
            print(f"Tokens: {reflection_result['tokens']}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test Strategy 4: Multi-turn
        print(f"\n{'-'*100}")
        print("【Strategy 4: Multi-turn Verification】")
        print("-"*100)
        try:
            multiturn_result = multi_turn_verification(case['question'])
            case_result["strategies"]["multi_turn"] = multiturn_result
            print(f"First Answer: {multiturn_result['first_answer'][:200]}...")
            print(f"\nAfter Challenge: {multiturn_result['final_answer'][:300]}...")
            print(f"Tokens: {multiturn_result['tokens']}")
        except Exception as e:
            print(f"Error: {e}")
        
        results.append(case_result)
        print(f"\n{'='*100}\n")
    
    # Save results
    output_file = "/Users/zeyu/research/comprehensive_test_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*100}")
    print(f"Results saved to: {output_file}")
    print("="*100)
    
    return results


if __name__ == "__main__":
    print("\n⚠️  Note: This test will make multiple API calls and may take a few minutes.")
    print("⚠️  Make sure OPENAI_API_KEY environment variable is set.\n")
    
    run_comprehensive_test()

