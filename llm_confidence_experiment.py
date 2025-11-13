"""
LLM Confidence and Accuracy Improvement Experiment
Test different prompt strategies to reduce hallucinations and improve answer quality
"""

import openai
import json
import os
from typing import Dict, List, Tuple
from datetime import datetime

# Set API key
openai.api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")

# Model to use
MODEL = "gpt-4o-mini"

class ConfidenceProtocol:
    """Implement different confidence and accuracy improvement protocols"""
    
    @staticmethod
    def strategy_baseline(question: str) -> Dict:
        """Strategy 1: Basic Strategy - Direct answer"""
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Please answer the user's question."},
            {"role": "user", "content": question}
        ]
        
        response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7
        )
        
        return {
            "strategy": "Basic Strategy",
            "answer": response.choices[0].message.content,
            "total_tokens": response.usage.total_tokens
        }
    
    @staticmethod
    def strategy_with_confidence(question: str) -> Dict:
        """Strategy 2: Answer with confidence"""
        system_prompt = """You are a helpful AI assistant. When answering questions, you need to:
1. Give your answer
2. Assess your confidence in this answer (0-100%)
3. Briefly explain your confidence source (based on certain knowledge, reasoning, or uncertain information)

Please answer in the following format:
[Answer]: (Your answer)
[Confidence]: (0-100%)
[Confidence Explanation]: (Why this confidence level)
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
            "strategy": "Confidence Strategy",
            "answer": response.choices[0].message.content,
            "total_tokens": response.usage.total_tokens
        }
    
    @staticmethod
    def strategy_self_reflection(question: str) -> Dict:
        """Strategy 3: Self-reflection strategy - Internal questioning before answering"""
        system_prompt = """You are a rigorous AI assistant. When answering questions, follow this thinking process:

1. **Preliminary Answer**: First give your initial reaction answer
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
            {"role": "user", "content": question}
        ]
        
        response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7
        )
        
        return {
            "strategy": "Self-Reflection Strategy",
            "answer": response.choices[0].message.content,
            "total_tokens": response.usage.total_tokens
        }
    
    @staticmethod
    def strategy_multi_turn_verification(question: str) -> Dict:
        """Strategy 4: Multi-turn verification strategy - Automatic challenge verification"""
        # Round 1: Initial answer
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Please answer the user's question and assess your confidence (0-100%) at the end."},
            {"role": "user", "content": question}
        ]
        
        response1 = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7
        )
        
        first_answer = response1.choices[0].message.content
        messages.append({"role": "assistant", "content": first_answer})
        
        # Round 2: Challenge confirmation
        messages.append({
            "role": "user", 
            "content": "Are you sure? Please think carefully again and ensure it's correct. If you find issues, please correct them. If you're confident it's correct, please restate your answer."
        })
        
        response2 = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7
        )
        
        second_answer = response2.choices[0].message.content
        messages.append({"role": "assistant", "content": second_answer})
        
        # Round 3: Final confirmation
        messages.append({
            "role": "user",
            "content": "Final confirmation, please give your final answer and confidence (0-100%)."
        })
        
        response3 = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7
        )
        
        final_answer = response3.choices[0].message.content
        
        total_tokens = response1.usage.total_tokens + response2.usage.total_tokens + response3.usage.total_tokens
        
        return {
            "strategy": "Multi-turn Verification Strategy",
            "first_answer": first_answer,
            "second_answer": second_answer,
            "final_answer": final_answer,
            "answer": final_answer,
            "total_tokens": total_tokens,
            "conversation": messages
        }
    
    @staticmethod
    def strategy_chain_of_verification(question: str) -> Dict:
        """Strategy 5: Chain of verification strategy - Systematically generate verification questions"""
        system_prompt = """You are a rigorous AI assistant. When answering questions, please follow the "Chain of Verification" method:

1. **Baseline Answer**: Give preliminary answer
2. **Generate Verification Questions**: List 2-3 questions that can verify your answer
3. **Answer Verification Questions**: Answer these verification questions independently
4. **Cross-Check**: Check if verification answers are consistent with baseline answer
5. **Final Answer**: Based on verification results, give corrected final answer

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
            {"role": "user", "content": question}
        ]
        
        response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7
        )
        
        return {
            "strategy": "Chain of Verification Strategy",
            "answer": response.choices[0].message.content,
            "total_tokens": response.usage.total_tokens
        }


def run_experiment(question: str):
    """Run experiment with all strategies"""
    print(f"\n{'='*80}")
    print(f"Question: {question}")
    print(f"{'='*80}\n")
    
    strategies = [
        ConfidenceProtocol.strategy_baseline,
        ConfidenceProtocol.strategy_with_confidence,
        ConfidenceProtocol.strategy_self_reflection,
        ConfidenceProtocol.strategy_multi_turn_verification,
        ConfidenceProtocol.strategy_chain_of_verification
    ]
    
    results = []
    
    for strategy in strategies:
        print(f"\n{'-'*80}")
        strategy_name = strategy.__name__.replace('strategy_', '').replace('_', ' ').title()
        print(f"Testing: {strategy_name}")
        print(f"{'-'*80}")
        
        try:
            result = strategy(question)
            results.append(result)
            
            print(f"\nStrategy: {result['strategy']}")
            print(f"Tokens used: {result['total_tokens']}")
            print(f"\nAnswer:")
            print(result['answer'][:500] + "..." if len(result['answer']) > 500 else result['answer'])
            
            # If multi-turn verification strategy, show detailed conversation
            if result['strategy'] == "Multi-turn Verification Strategy":
                print(f"\n[Round 1 Answer]:")
                print(result['first_answer'][:300] + "..." if len(result['first_answer']) > 300 else result['first_answer'])
                print(f"\n[Round 2 Answer (after challenge)]:")
                print(result['second_answer'][:300] + "..." if len(result['second_answer']) > 300 else result['second_answer'])
            
        except Exception as e:
            print(f"Error: {str(e)}")
            results.append({"strategy": strategy.__doc__, "error": str(e)})
    
    return results


# Test question set - includes questions prone to hallucinations
TEST_QUESTIONS = [
    # Factual question (clear answer)
    "In what year was the Eiffel Tower built?",
    
    # Easily confused question
    "What's the difference between list.append() and list.extend() in Python?",
    
    # Calculation question
    "If a product originally costs $100, first gets 20% off, then 10% off, what's the final price?",
    
    # Question prone to hallucination
    "What is the current maximum number of qubits in quantum computers?",
    
    # Logical reasoning question
    "Three people A, B, C. A says B is lying, B says C is lying, C says both A and B are lying. If only one person is telling the truth, who is it?"
]


def main():
    """Main function"""
    print("="*80)
    print("LLM Confidence and Accuracy Improvement Experiment")
    print(f"Model: {MODEL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Can choose to run all test questions or single question
    print("\nChoose test mode:")
    print("1. Run all test questions")
    print("2. Input custom question")
    
    choice = input("\nPlease choose (1 or 2): ").strip()
    
    if choice == "1":
        all_results = []
        for question in TEST_QUESTIONS:
            results = run_experiment(question)
            all_results.append({
                "question": question,
                "results": results
            })
            print("\n" + "="*80 + "\n")
        
        # Save results
        with open("/Users/zeyu/research/experiment_results.json", "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"\nExperiment results saved to: /Users/zeyu/research/experiment_results.json")
        
    else:
        question = input("\nPlease enter your question: ").strip()
        results = run_experiment(question)
        
        # Save single result
        with open("/Users/zeyu/research/single_experiment_result.json", "w", encoding="utf-8") as f:
            json.dump({
                "question": question,
                "results": results,
                "timestamp": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        print(f"\nExperiment results saved to: /Users/zeyu/research/single_experiment_result.json")


if __name__ == "__main__":
    main()
