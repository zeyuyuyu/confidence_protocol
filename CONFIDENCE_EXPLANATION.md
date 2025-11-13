# How Confidence is Calculated

## Overview

The confidence score (0-100%) in this protocol is **NOT calculated by code** - instead, it's **self-reported by the LLM itself**. The system uses a "metacognitive" approach where we ask the LLM to evaluate its own certainty.

## The Mechanism

### 1. Request Phase: Ask LLM to Provide Confidence

In the system prompt, we explicitly instruct the LLM to assess its own confidence:

```python
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
```

**Key Point**: We're asking the LLM to do introspection and report its own confidence level.

### 2. Extraction Phase: Parse the Confidence from Response

Once the LLM responds, we extract the confidence number using regex patterns:

```python
def _extract_confidence(self, content: str) -> float:
    """Extract confidence from answer"""
    import re
    
    # Search for confidence patterns
    patterns = [
        r'\[Confidence\][：:]\s*(\d+\.?\d*)%?',      # [Confidence]: 95
        r'\[置信度\][：:]\s*(\d+\.?\d*)%?',           # Chinese format
        r'confidence[：:]\s*(\d+\.?\d*)%?',          # confidence: 85
        r'Confidence[：:]\s*(\d+\.?\d*)%?',          # Confidence: 90
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
```

### 3. Default Value

If the LLM doesn't provide a confidence score (or we can't parse it), we default to **60%** - a medium confidence level.

## Example Flow

### Example 1: High Confidence Answer

**User Question**: "What is 2 + 2?"

**LLM Response**:
```
[Thinking]: This is a basic arithmetic question with a definite answer.
[Answer]: 2 + 2 equals 4
[Confidence]: 100
[Confidence Reason]: This is a fundamental mathematical fact with no uncertainty.
```

**Extracted Confidence**: `100.0`

---

### Example 2: Medium Confidence Answer

**User Question**: "What is the current maximum number of qubits in quantum computers?"

**LLM Response**:
```
[Thinking]: Quantum computing is rapidly evolving. I know IBM had 127 qubits in 2023, 
but there might be newer developments I'm not aware of.
[Answer]: As of my knowledge cutoff, the maximum was around 127 qubits (IBM), 
but this field advances quickly.
[Confidence]: 70
[Confidence Reason]: The field evolves rapidly, and my information might be outdated.
```

**Extracted Confidence**: `70.0`

---

### Example 3: Low Confidence Answer

**User Question**: "What will be the price of Bitcoin on December 31, 2025?"

**LLM Response**:
```
[Thinking]: This is asking for a future prediction which is inherently uncertain. 
I cannot predict future prices accurately.
[Answer]: I cannot reliably predict future Bitcoin prices as they depend on many 
unpredictable factors.
[Confidence]: 20
[Confidence Reason]: Predicting future cryptocurrency prices is highly speculative 
and unreliable.
```

**Extracted Confidence**: `20.0`

## Why This Approach?

### Advantages

1. **Metacognition**: Makes the LLM "think about its thinking"
2. **Calibration Effect**: The act of assessing confidence often improves accuracy
3. **Transparency**: Users can see why the LLM has a certain confidence level
4. **Trigger for Verification**: Low confidence automatically triggers additional verification

### Limitations

1. **Not Probabilistically Calibrated**: The confidence is subjective, not based on statistical models
2. **Can Be Overconfident**: LLMs sometimes report high confidence even when wrong
3. **Depends on Prompt Quality**: How we ask affects what we get

## How Confidence is Used

### Confidence Levels

```python
class ConfidenceLevel(Enum):
    HIGH = "high"     # >= 80%
    MEDIUM = "medium" # 50-79%
    LOW = "low"       # < 50%
```

### Automatic Verification

```python
def ask(self, question: str, auto_verify: bool = True) -> Answer:
    # Get initial answer
    answer = self._get_initial_answer(question)
    
    # If confidence is low and auto-verify is enabled, perform verification
    if auto_verify and answer.confidence < self.confidence_threshold:
        print(f"⚠️  Low confidence ({answer.confidence}%), triggering verification...")
        verified_answer = self._verify_answer(question, answer)
        return verified_answer
    
    return answer
```

**Default Threshold**: 80%
- If confidence < 80%: Automatically trigger multi-turn verification
- If confidence >= 80%: Accept the answer

## Comparison with Other Approaches

### Traditional ML Confidence
```python
# Traditional approach - based on model probability
confidence = max(softmax_probabilities)
# e.g., 0.95 for the highest probability class
```

**This is NOT what we do.**

### Our Approach - LLM Self-Assessment
```python
# Our approach - LLM self-reports
confidence = LLM_says_its_confidence()
# e.g., "I am 85% confident because..."
```

**This IS what we do.**

## Research Basis

This approach is inspired by:

1. **Chain-of-Thought Prompting**: Breaking down reasoning improves performance
2. **Self-Consistency**: Multiple reasoning paths improve reliability
3. **Constitutional AI**: Self-critique mechanisms
4. **Metacognitive Prompting**: Having AI assess its own knowledge state

## Improving Confidence Calibration

Future improvements could include:

### 1. Confidence Calibration Model
Train a separate model to predict actual accuracy from stated confidence:

```python
actual_confidence = calibration_model(
    question=question,
    answer=answer.content,
    stated_confidence=answer.confidence
)
```

### 2. Historical Accuracy Tracking
Track how often each confidence level is actually correct:

```python
if stated_confidence >= 90 and actual_correct:
    # This LLM is well-calibrated at high confidence
    calibration_score["90+"] += 1
```

### 3. Multi-Model Consensus
Compare confidence across different models:

```python
confidence_scores = []
for model in ["gpt-4", "claude-3", "gpt-4o-mini"]:
    answer = ask_model(model, question)
    confidence_scores.append(answer.confidence)

final_confidence = min(confidence_scores)  # Conservative approach
```

## Code Location

The confidence extraction logic is in:
- **File**: `confidence_protocol.py`
- **Class**: `ConfidenceProtocol`
- **Method**: `_extract_confidence()` (lines 212-233)

The system prompt that requests confidence is in:
- **File**: `confidence_protocol.py`
- **Class**: `ConfidenceProtocol`
- **Attribute**: `self.base_prompt` (lines 58-70)

## Summary

**Confidence is NOT calculated by algorithms** - it's **self-reported by the LLM** through:

1. ✅ **Explicit instruction** in system prompt to assess confidence
2. ✅ **Regex extraction** to parse the number from LLM response
3. ✅ **Default value (60%)** if not found
4. ✅ **Automatic verification** if confidence is below threshold

This "introspective" approach makes the LLM more aware of its uncertainties, which often leads to more honest and accurate responses.

