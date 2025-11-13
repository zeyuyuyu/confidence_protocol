# LLM Confidence Protocol

## Project Overview

This is an experimental protocol system designed to reduce LLM "hallucination" phenomena and improve answer quality and reliability.

### Core Findings

Through experimental observations, we discovered:
1. **Challenge Effect**: When challenging LLMs with "Are you sure?", if the answer is wrong, LLMs often self-correct; if correct, LLMs maintain their answer
2. **Confidence Awareness**: Requiring LLMs to provide confidence assessments can significantly improve answer quality
3. **Self-Questioning**: Building self-questioning mechanisms into system prompts can reduce hallucinations

## Protocol Strategies

### Strategy 1: Basic Strategy
Direct answer to questions without any special prompts.

**Pros**: Fast, low token consumption  
**Cons**: May confidently give wrong answers, cannot identify uncertainty

### Strategy 2: Confidence Strategy
Require LLM to provide when answering:
- Answer content
- Confidence score (0-100%)
- Confidence reasoning

**Pros**: Helps identify uncertain answers  
**Cons**: Initial answer confidence may be inaccurate

### Strategy 3: Self-Reflection Strategy
Require LLM in system prompt to:
1. Give preliminary answer
2. Question their own answer
3. Re-verify
4. Give final answer and confidence

**Pros**: Higher first-answer quality  
**Cons**: Consumes more tokens

### Strategy 4: Multi-turn Verification Strategy
Simulate human challenging process:
1. Round 1: Get initial answer
2. Round 2: Challenge with "Are you sure?"
3. Round 3: Final confirmation

**Pros**: Best correction effect for wrong answers  
**Cons**: Requires multiple rounds, higher cost

### Strategy 5: Chain of Verification Strategy
Systematically:
1. Give baseline answer
2. Generate 2-3 verification questions
3. Answer verification questions
4. Cross-check consistency
5. Give final answer

**Pros**: Structured verification, suitable for complex questions  
**Cons**: Highest token consumption

## Experimental Results Comparison

### Test Case: Calculation Problem
Question: "If a product originally costs $100, first gets 20% off, then another 10% off, what's the final price?"

| Strategy | Answer | Confidence | Tokens Used | Result |
|----------|--------|------------|-------------|--------|
| Basic | $72 | Not provided | 130 | ✅ Correct |
| Confidence | $72 | 95% | 213 | ✅ Correct |
| Self-Reflection | $72 | 100% | 315 | ✅ Correct |
| Multi-turn | $72 | High | 406 | ✅ Correct |
| Chain of Verification | $72 | 100% | 384 | ✅ Correct |

### Test Case: Logic Problem
Question: "Three switches in room A control three lights in room B, how to determine the mapping?"

| Strategy | Correctness | Confidence | Notes |
|----------|-------------|------------|-------|
| Basic | ✅ | Not provided | Gave correct temperature method |
| Multi-turn (first challenge) | ✅ | Not explicit | Confirmed answer correctness |
| Self-Reflection | ✅ | 95% | Identified possible edge cases |

## Usage

### Quick Start

#### 1. Set up your OpenAI API key

You can set your API key in one of two ways:

**Option A: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

**Option B: Pass directly in code**
```python
protocol = ConfidenceProtocol(api_key="your-api-key")
```

#### 2. Use the protocol

```python
from confidence_protocol import ConfidenceProtocol

# Initialize protocol (will use OPENAI_API_KEY environment variable if set)
protocol = ConfidenceProtocol(
    api_key="your-api-key",  # Or use os.environ.get("OPENAI_API_KEY")
    model="gpt-4o-mini",
    confidence_threshold=80.0  # Trigger verification below 80%
)

# Ask question
answer = protocol.ask("Your question", auto_verify=True)

print(f"Answer: {answer.content}")
print(f"Confidence: {answer.confidence}%")
print(f"Strategy: {answer.strategy_used}")
```

### Advanced Usage

```python
# Use chain of verification strategy (suitable for complex questions)
answer = protocol.ask_with_chain_of_verification("Complex question")

# Batch questions
questions = ["Question 1", "Question 2", "Question 3"]
answers = protocol.batch_ask(questions, use_verification=True)

# Check confidence level
level = protocol.get_confidence_level(answer.confidence)
if level == ConfidenceLevel.LOW:
    print("⚠️  Manual review recommended")
```

## Core System Prompt

```python
base_prompt = """You are a rigorous and honest AI assistant. When answering questions, please follow these guidelines:

1. **Self-questioning**: Question your first reaction before giving an answer
2. **Honest assessment**: Clearly state uncertainties rather than making things up
3. **Confidence assessment**: Evaluate your certainty about the answer (0-100%)

Please answer in the following format:
[Thinking]: (Briefly explain your reasoning process, including any uncertainties)
[Answer]: (Your answer)
[Confidence]: (A number from 0-100)
[Confidence Reason]: (Why this confidence level)
"""
```

## Best Practice Recommendations

### 1. Choose Strategy by Scenario

| Scenario | Recommended Strategy | Reason |
|----------|---------------------|---------|
| Simple queries | Basic strategy | Fast and low cost |
| General questions | Confidence strategy | Balance quality and cost |
| Critical decisions | Self-reflection or multi-turn | Quality first |
| Complex logic | Chain of verification | Needs systematic verification |

### 2. Confidence Threshold Settings

- **High-risk scenarios**: Set threshold to 90%, only accept high-confidence answers
- **General scenarios**: Set threshold to 80%, trigger verification for medium-low confidence
- **Exploratory scenarios**: Set threshold to 60%, accept more uncertainty

### 3. Auto-Verification Strategy

```python
def smart_ask(question, importance="normal"):
    if importance == "critical":
        # Critical questions: Use chain of verification directly
        return protocol.ask_with_chain_of_verification(question)
    elif importance == "high":
        # Important questions: Use auto-verification
        return protocol.ask(question, auto_verify=True)
    else:
        # General questions: Basic strategy
        return protocol.ask(question, auto_verify=False)
```

### 4. Cost Optimization

- **Priority sorting**: Use basic strategy for quick filtering first, only use high-cost strategies for important questions
- **Cache answers**: Cache high-confidence answers for repeated questions
- **Batch processing**: Use batch_ask() to improve efficiency

## Experimental Files Description

| File | Description |
|------|-------------|
| `confidence_protocol.py` | Core protocol implementation (recommended) |
| `demo_experiment.py` | Comparison demonstration of 5 strategies |
| `test_hallucination.py` | Tests for hallucination-prone questions |
| `llm_confidence_experiment.py` | Complete experimental framework (interactive) |

## Running Experiments

```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install openai

# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key-here"

# Run demonstration
python3 demo_experiment.py

# Test hallucination questions
python3 test_hallucination.py

# Use protocol
python3 confidence_protocol.py
```

## Key Insights

### 1. The Magic of Challenging
Through multiple experiments, we verified that "challenging" can indeed improve LLM accuracy. This might be because:
- Triggers deeper reasoning
- Activates self-checking mechanisms
- Re-evaluates initial assumptions

### 2. The Value of Confidence
Requiring LLMs to provide confidence has multiple benefits:
- Helps identify uncertain answers
- Reduces overconfidence risks
- Provides trigger points for human intervention

### 3. The Effect of Self-Questioning
Building self-questioning mechanisms into system prompts can:
- Improve first-answer quality
- Reduce obvious errors
- Enhance consideration of edge cases

### 4. Cost vs Quality Tradeoff
- Basic strategy: ~130 tokens
- Confidence strategy: ~210 tokens (+62%)
- Self-reflection: ~315 tokens (+142%)
- Multi-turn verification: ~400 tokens (+208%)
- Chain of verification: ~384 tokens (+195%)

For critical questions, spending 2-3x more tokens to get higher quality answers is worthwhile.

## Future Improvement Directions

1. **Adaptive thresholds**: Dynamically adjust confidence thresholds based on question type and historical accuracy
2. **Integrate external verification**: Combine search engines and knowledge bases for fact-checking
3. **Multi-model voting**: Use multiple models to answer the same question, judge reliability through consistency
4. **Confidence calibration**: Train a model to more accurately assess LLM confidence
5. **Incremental verification**: Intelligently select verification strategies based on initial answer confidence

## Contributing

Welcome suggestions for improvements and new verification strategies!

## License

MIT License

## Acknowledgments

This project is based on observations and experiments of LLM behavior, aiming to explore practical methods for improving LLM reliability.
