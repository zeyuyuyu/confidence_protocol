"""
LLM Confidence Protocol
A practical system to reduce LLM hallucinations and improve answer quality and reliability
through multiple strategies.

Author: Based on observations and experiments of LLM behavior
Date: 2025-11-12
"""

import openai
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

@dataclass
class Answer:
    """Answer structure"""
    content: str
    confidence: float  # 0-100
    reasoning: Optional[str] = None
    strategy_used: Optional[str] = None
    token_usage: int = 0


class ConfidenceLevel(Enum):
    """Confidence level"""
    HIGH = "high"  # >= 80%
    MEDIUM = "medium"  # 50-79%
    LOW = "low"  # < 50%


class ConfidenceProtocol:
    """
    Main Confidence Protocol Class
    
    Core principles:
    1. Require LLM to provide confidence assessment
    2. Built-in self-questioning mechanism
    3. Automatically trigger verification based on confidence
    4. Provide multiple verification strategies
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", 
                 confidence_threshold: float = 80.0):
        """
        Initialize protocol
        
        Args:
            api_key: OpenAI API key
            model: Model to use
            confidence_threshold: Confidence threshold below which additional verification is triggered
        """
        openai.api_key = api_key
        self.model = model
        self.confidence_threshold = confidence_threshold
        
        # Core System Prompt
        self.base_prompt = """You are a rigorous and honest AI assistant. When answering questions, please follow these guidelines:

1. **Self-questioning**: Question your first reaction before giving an answer
2. **Honest assessment**: Clearly state uncertainties rather than making things up
3. **Confidence assessment**: Evaluate your certainty about the answer (0-100%)

Please answer in the following format:
[Thinking]: (Briefly explain your reasoning process, including any uncertainties)
[Answer]: (Your answer)
[Confidence]: (A number from 0-100)
[Confidence Reason]: (Why this confidence level)
"""
    
    def ask(self, question: str, auto_verify: bool = True) -> Answer:
        """
        Ask a question and get an answer
        
        Args:
            question: User question
            auto_verify: Whether to automatically trigger verification based on confidence
            
        Returns:
            Answer object
        """
        # First answer
        answer = self._get_initial_answer(question)
        
        # If confidence is low and auto-verify is enabled, perform verification
        if auto_verify and answer.confidence < self.confidence_threshold:
            print(f"\n⚠️  Low confidence ({answer.confidence}%), triggering automatic verification...")
            verified_answer = self._verify_answer(question, answer)
            return verified_answer
        
        return answer
    
    def _get_initial_answer(self, question: str) -> Answer:
        """Get initial answer"""
        messages = [
            {"role": "system", "content": self.base_prompt},
            {"role": "user", "content": question}
        ]
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        confidence = self._extract_confidence(content)
        
        return Answer(
            content=content,
            confidence=confidence,
            strategy_used="initial",
            token_usage=response.usage.total_tokens
        )
    
    def _verify_answer(self, question: str, initial_answer: Answer) -> Answer:
        """Verify answer - using multi-turn dialogue"""
        messages = [
            {"role": "system", "content": self.base_prompt},
            {"role": "user", "content": question},
            {"role": "assistant", "content": initial_answer.content}
        ]
        
        # First verification round: challenge
        messages.append({
            "role": "user",
            "content": "Are you sure? Please think carefully again and check for any omissions or errors. If you find issues, please correct them. If you're confident it's correct, please restate your answer and confidence."
        })
        
        response1 = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        
        content1 = response1.choices[0].message.content
        confidence1 = self._extract_confidence(content1)
        
        # Second verification round: final confirmation
        messages.append({"role": "assistant", "content": content1})
        messages.append({
            "role": "user",
            "content": "Final confirmation: Please provide your final answer and confidence level."
        })
        
        response2 = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        
        final_content = response2.choices[0].message.content
        final_confidence = self._extract_confidence(final_content)
        
        total_tokens = (initial_answer.token_usage + 
                       response1.usage.total_tokens + 
                       response2.usage.total_tokens)
        
        return Answer(
            content=final_content,
            confidence=final_confidence,
            reasoning=f"After 2 rounds of verification. Initial confidence: {initial_answer.confidence}% -> Round 1: {confidence1}% -> Final: {final_confidence}%",
            strategy_used="multi_turn_verification",
            token_usage=total_tokens
        )
    
    def ask_with_chain_of_verification(self, question: str) -> Answer:
        """Use chain of verification strategy"""
        system_prompt = """You are a rigorous AI assistant. Answer questions using the "Chain of Verification" method:

1. Give preliminary answer
2. Generate 2-3 verification questions to check your answer
3. Answer these verification questions
4. Cross-check for consistency
5. Provide final answer and confidence

Format:
[Preliminary Answer]: ...
[Verification Questions]:
1. ...
2. ...
[Verification Answers]:
1. ...
2. ...
[Cross-Check]: ...
[Final Answer]: ...
[Confidence]: (0-100)
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        confidence = self._extract_confidence(content)
        
        return Answer(
            content=content,
            confidence=confidence,
            strategy_used="chain_of_verification",
            token_usage=response.usage.total_tokens
        )
    
    def _extract_confidence(self, content: str) -> float:
        """Extract confidence from answer"""
        import re
        
        # Search for confidence patterns
        patterns = [
            r'\[Confidence\][：:]\s*(\d+\.?\d*)%?',
            r'\[置信度\][：:]\s*(\d+\.?\d*)%?',
            r'confidence[：:]\s*(\d+\.?\d*)%?',
            r'Confidence[：:]\s*(\d+\.?\d*)%?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except:
                    pass
        
        # If not found, return medium confidence
        return 60.0
    
    def get_confidence_level(self, confidence: float) -> ConfidenceLevel:
        """Get confidence level"""
        if confidence >= 80:
            return ConfidenceLevel.HIGH
        elif confidence >= 50:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def batch_ask(self, questions: List[str], 
                  use_verification: bool = True) -> List[Answer]:
        """Batch ask questions"""
        answers = []
        for i, question in enumerate(questions, 1):
            print(f"\nProcessing question {i}/{len(questions)}: {question[:50]}...")
            answer = self.ask(question, auto_verify=use_verification)
            answers.append(answer)
        return answers


# Usage example
def example_usage():
    """Usage example"""
    
    import os
    API_KEY = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
    
    # Create protocol instance
    protocol = ConfidenceProtocol(
        api_key=API_KEY,
        model="gpt-4o-mini",
        confidence_threshold=80.0  # Trigger verification below 80%
    )
    
    print("="*100)
    print("LLM Confidence Protocol - Usage Example")
    print("="*100)
    
    # Test questions
    questions = [
        "What is the current maximum number of qubits in quantum computers?",
        "What's the difference between Python's list.append() and list.extend()?",
        "If a number is first multiplied by 2, then divided by 2, is the result still the original number?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*100}")
        print(f"Question {i}: {question}")
        print('='*100)
        
        # Ask using protocol
        answer = protocol.ask(question, auto_verify=True)
        
        print(f"\n{answer.content}")
        print(f"\n📊 Confidence: {answer.confidence}%")
        print(f"🔧 Strategy: {answer.strategy_used}")
        print(f"💰 Tokens used: {answer.token_usage}")
        
        if answer.reasoning:
            print(f"💭 Verification process: {answer.reasoning}")
        
        # Display confidence level
        level = protocol.get_confidence_level(answer.confidence)
        level_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}
        print(f"{level_emoji[level.value]} Confidence level: {level.value.upper()}")
    
    print("\n" + "="*100)
    print("Testing complete!")
    print("="*100)
    
    # Demonstrate chain of verification strategy
    print("\n\n" + "="*100)
    print("Demonstration: Chain of Verification Strategy")
    print("="*100)
    
    difficult_question = "Three pirates divide 100 gems. Voting requires half majority or proposer dies. How should the first pirate allocate?"
    print(f"\nQuestion: {difficult_question}")
    
    answer = protocol.ask_with_chain_of_verification(difficult_question)
    print(f"\n{answer.content}")
    print(f"\n📊 Confidence: {answer.confidence}%")
    print(f"💰 Tokens used: {answer.token_usage}")


if __name__ == "__main__":
    example_usage()
