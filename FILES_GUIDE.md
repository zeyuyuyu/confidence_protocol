# File Usage Guide

## 📋 Quick Navigation

### 🚀 Want to start quickly?
→ Run `python3 interactive_test.py`

### 📖 Want to understand the principles?
→ Read `README.md` and `PROJECT_SUMMARY.md`

### 💻 Want to use in code?
→ Import `confidence_protocol.py`

### 🔬 Want to see experimental results?
→ Run `demo_experiment.py` or `test_hallucination.py`

---

## 📁 Detailed File Descriptions

### Core Files (Must Read)

#### 1. `confidence_protocol.py` ⭐⭐⭐⭐⭐
**Purpose**: Core protocol implementation, production-ready

**Contains**:
- `ConfidenceProtocol` class: Main protocol implementation
- `Answer` dataclass: Answer structure
- `ConfidenceLevel` enum: Confidence levels
- Implementation of 5 verification strategies

**How to use**:
```python
from confidence_protocol import ConfidenceProtocol

protocol = ConfidenceProtocol(api_key="your-key")
answer = protocol.ask("Your question", auto_verify=True)
print(answer.content, answer.confidence)
```

**Suitable for**:
- Integration into production environment
- Import as library
- Scenarios requiring stable API

---

#### 2. `interactive_test.py` ⭐⭐⭐⭐⭐
**Purpose**: Interactive test tool, user-friendly

**Features**:
- Interactive Q&A interface
- Strategy selection
- Strategy comparison
- Detailed result display

**How to use**:
```bash
# Interactive mode
python3 interactive_test.py

# Quick test mode
python3 interactive_test.py quick
```

**Suitable for**:
- First time using this protocol
- Want to quickly test effects
- Need to compare different strategies
- Demonstrate to others

---

### Documentation Files

#### 3. `README.md` ⭐⭐⭐⭐⭐
**Purpose**: Complete project documentation

**Contains**:
- Project overview and core findings
- Detailed description of all strategies
- Experimental results comparison
- Usage methods and code examples
- Best practice recommendations
- Cost analysis

**Suitable for**:
- Want to fully understand the project
- Need to check API documentation
- Looking for usage examples
- Understanding design philosophy

---

#### 4. `PROJECT_SUMMARY.md` ⭐⭐⭐⭐
**Purpose**: Project summary and guide

**Contains**:
- Project background and motivation
- Core innovation points
- Experimental results analysis
- Core insights
- Future expansion directions
- Best practices

**Suitable for**:
- Want to quickly understand project value
- Need to introduce project to others
- Looking for practical application guidance
- Planning subsequent development

---

#### 5. `FILES_GUIDE.md` ⭐⭐⭐
**Purpose**: This file, file navigation guide

---

### Experimental Files

#### 6. `demo_experiment.py` ⭐⭐⭐⭐
**Purpose**: Complete comparison demonstration of 5 strategies

**Features**:
- Test all strategies using the same question
- Show each strategy's output
- Compare token consumption
- Assess quality differences

**How to use**:
```bash
python3 demo_experiment.py
```

**Suitable for**:
- Want to see strategy comparison
- Assess which strategy is most suitable
- Understand token costs
- Learn effects of different strategies

**Expected output**:
```
====================================================================================================
[Strategy 1: Basic Strategy] - Direct answer, no special prompts
====================================================================================================
Answer: ...
Tokens used: 130

====================================================================================================
[Strategy 2: Confidence Strategy] - Require LLM to provide confidence assessment
====================================================================================================
Answer: ...
Confidence: 95%
Tokens used: 213

... (other strategies continue)
```

---

#### 7. `test_hallucination.py` ⭐⭐⭐⭐
**Purpose**: Test questions prone to hallucination

**Features**:
- Use error-prone questions for testing
- Show difference between basic strategy vs verification strategy
- Verify effect of challenging mechanism
- Include multiple trap questions

**How to use**:
```bash
python3 test_hallucination.py
```

**Suitable for**:
- Verify if challenging mechanism is effective
- Test complex logic problems
- Assess protocol's resistance to hallucinations
- Find protocol limitations

**Test questions**:
1. Three switches and three lights problem (logic trap)
2. Pirate gem division problem (game theory)

---

#### 8. `llm_confidence_experiment.py` ⭐⭐⭐
**Purpose**: Complete experimental framework (interactive)

**Features**:
- Implementation of all strategies
- Multiple preset test questions
- Interactive Q&A
- Save results as JSON

**How to use**:
```bash
python3 llm_confidence_experiment.py
```

Then:
- Choose 1: Run all preset questions
- Choose 2: Input custom question

**Suitable for**:
- Systematic experimental research
- Need to save experimental results
- Batch test multiple questions
- Deep research on protocol effects

**Output**:
- Console shows detailed results
- Save JSON file: `experiment_results.json`

---

### Configuration Files

#### 9. `requirements.txt` ⭐⭐⭐⭐⭐
**Purpose**: Python dependency list

**Content**:
```
openai>=1.0.0
```

**How to use**:
```bash
pip install -r requirements.txt
```

---

## 🎯 Usage Scenario Recommendations

### Scenario 1: First Contact with This Project
**Recommended Path**:
1. Read `PROJECT_SUMMARY.md` (5 minutes)
2. Run `python3 interactive_test.py quick` (3 minutes)
3. Try interactive mode `python3 interactive_test.py` (10 minutes)
4. Read `README.md` for details (15 minutes)

### Scenario 2: Want to Use in Project
**Recommended Path**:
1. Read "Usage" section in `README.md`
2. Check example code in `confidence_protocol.py`
3. Run `demo_experiment.py` to understand each strategy
4. Choose appropriate strategy to integrate based on needs

### Scenario 3: Research and Experimentation
**Recommended Path**:
1. Read "Core Insights" section in `PROJECT_SUMMARY.md`
2. Run `test_hallucination.py` to see effects
3. Run `llm_confidence_experiment.py` for custom testing
4. Modify `confidence_protocol.py` to add new strategies
5. Record results, improve experiments

### Scenario 4: Demonstrate to Others
**Recommended Path**:
1. Prepare: Read `PROJECT_SUMMARY.md`
2. Demonstrate: Run `interactive_test.py`, select strategy comparison
3. Explain: Use `README.md` to explain principles
4. Q&A: Reference results from experimental files

---

## 🔧 Modifications and Extensions

### Want to add new strategy?
→ Modify `confidence_protocol.py`, add new method to `ConfidenceProtocol` class

### Want to change default parameters?
→ Modify `__init__` method in `confidence_protocol.py`

### Want to use different model?
→ Specify at initialization: `ConfidenceProtocol(api_key="...", model="gpt-4")`

### Want to add new test questions?
→ Modify `TEST_QUESTIONS` list in `llm_confidence_experiment.py`

### Want to adjust confidence threshold?
→ Set at initialization: `ConfidenceProtocol(api_key="...", confidence_threshold=90.0)`

---

## 📊 File Size and Complexity

| File | Lines | Complexity | Reading Time |
|------|-------|------------|--------------|
| `confidence_protocol.py` | ~300 | Medium | 20 minutes |
| `interactive_test.py` | ~200 | Low | 10 minutes |
| `demo_experiment.py` | ~150 | Low | 10 minutes |
| `test_hallucination.py` | ~200 | Low | 10 minutes |
| `llm_confidence_experiment.py` | ~320 | Medium | 25 minutes |
| `README.md` | ~400 | Low | 15 minutes |
| `PROJECT_SUMMARY.md` | ~500 | Low | 20 minutes |

---

## ⚡ Quick Command Reference

```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Interactive test (recommended for beginners)
python3 interactive_test.py

# Quick test
python3 interactive_test.py quick

# Strategy comparison demonstration
python3 demo_experiment.py

# Hallucination test
python3 test_hallucination.py

# Complete experimental framework
python3 llm_confidence_experiment.py
```

---

## 🆘 Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'openai'`
**Solution**:
```bash
source venv/bin/activate
pip install openai
```

### Problem: API key error
**Solution**: Update API key in the Python file being used

### Problem: Want to use your own API key
**Solution**:
```python
# Method 1: Modify in code
protocol = ConfidenceProtocol(api_key="your-key")

# Method 2: Use environment variable
import os
os.environ["OPENAI_API_KEY"] = "your-key"
```

---

## 📈 Advanced Usage

### Integrate into Web Application
```python
from flask import Flask, request, jsonify
from confidence_protocol import ConfidenceProtocol

app = Flask(__name__)
protocol = ConfidenceProtocol(api_key="your-key")

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json['question']
    answer = protocol.ask(question, auto_verify=True)
    return jsonify({
        'answer': answer.content,
        'confidence': answer.confidence,
        'reliable': answer.confidence >= 80
    })
```

### Batch Processing
```python
questions = [...]  # Many questions
answers = protocol.batch_ask(questions, use_verification=True)

# Filter low-confidence answers
low_confidence = [a for a in answers if a.confidence < 80]
```

### Custom Verification Logic
```python
def custom_verify(question, answer):
    if answer.confidence < 70:
        # Use chain of verification
        return protocol.ask_with_chain_of_verification(question)
    elif answer.confidence < 85:
        # Use multi-turn verification
        return protocol.ask(question, auto_verify=True)
    else:
        # Accept answer
        return answer
```

---

**Last Updated**: 2025-11-12  
**Maintainer**: AI Assistant  
**Status**: ✅ Complete and usable
