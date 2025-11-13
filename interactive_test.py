"""
Interactive Test Tool
Allows users to directly test the confidence protocol
"""

from confidence_protocol import ConfidenceProtocol, ConfidenceLevel
import sys
import os

API_KEY = os.environ.get("OPENAI_API_KEY", "your-api-key-here")

def print_banner():
    """Print banner"""
    print("\n" + "="*100)
    print("🤖 LLM Confidence Protocol - Interactive Test Tool")
    print("="*100)
    print("""
This tool helps you test different strategies to reduce LLM hallucinations and improve answer quality.

Available strategies:
1. Basic Strategy - Direct answer (fast but may be less accurate)
2. Auto Verification - Automatically trigger verification based on confidence (recommended)
3. Chain of Verification - Systematic verification (suitable for complex questions)
4. Comparison Test - Use multiple strategies simultaneously for comparison

Type 'quit' or 'exit' to exit the program
Type 'help' to view help
""")

def print_answer(answer, show_details=True):
    """Print answer"""
    print("\n" + "-"*100)
    print("📝 Answer:")
    print(answer.content)
    
    if show_details:
        print("\n" + "-"*100)
        print(f"📊 Confidence: {answer.confidence}%")
        print(f"🔧 Strategy: {answer.strategy_used}")
        print(f"💰 Tokens used: {answer.token_usage}")
        
        if answer.reasoning:
            print(f"💭 Verification process: {answer.reasoning}")
        
        # Confidence level
        if answer.confidence >= 80:
            print("🟢 Confidence level: HIGH (highly reliable)")
        elif answer.confidence >= 50:
            print("🟡 Confidence level: MEDIUM (moderately reliable, verification recommended)")
        else:
            print("🔴 Confidence level: LOW (low reliability, requires manual review)")

def compare_strategies(protocol, question):
    """Compare different strategies"""
    print("\n" + "="*100)
    print("🔬 Strategy Comparison Test")
    print("="*100)
    
    # Strategy 1: Basic
    print("\n[Strategy 1: Basic Strategy]")
    print("Quick answer, no additional verification...")
    answer1 = protocol.ask(question, auto_verify=False)
    print(f"Answer summary: {answer1.content[:200]}...")
    print(f"Confidence: {answer1.confidence}% | Tokens: {answer1.token_usage}")
    
    # Strategy 2: Auto verification
    print("\n[Strategy 2: Auto Verification Strategy]")
    print("Automatically trigger verification based on confidence...")
    answer2 = protocol.ask(question, auto_verify=True)
    print(f"Answer summary: {answer2.content[:200]}...")
    print(f"Confidence: {answer2.confidence}% | Tokens: {answer2.token_usage}")
    
    # Strategy 3: Chain of verification
    print("\n[Strategy 3: Chain of Verification Strategy]")
    print("Systematically generate verification questions and cross-check...")
    answer3 = protocol.ask_with_chain_of_verification(question)
    print(f"Answer summary: {answer3.content[:200]}...")
    print(f"Confidence: {answer3.confidence}% | Tokens: {answer3.token_usage}")
    
    # Summary comparison
    print("\n" + "="*100)
    print("📊 Comparison Summary")
    print("="*100)
    print(f"{'Strategy':<20} {'Confidence':<15} {'Tokens':<15} {'Cost Ratio':<10}")
    print("-"*100)
    base_tokens = answer1.token_usage
    print(f"{'Basic Strategy':<20} {answer1.confidence:>6.1f}%        {answer1.token_usage:>8}        {1.0:>6.1f}x")
    print(f"{'Auto Verification':<20} {answer2.confidence:>6.1f}%        {answer2.token_usage:>8}        {answer2.token_usage/base_tokens:>6.1f}x")
    print(f"{'Chain of Verification':<20} {answer3.confidence:>6.1f}%        {answer3.token_usage:>8}        {answer3.token_usage/base_tokens:>6.1f}x")

def interactive_mode():
    """Interactive mode"""
    # Initialize protocol
    protocol = ConfidenceProtocol(
        api_key=API_KEY,
        model="gpt-4o-mini",
        confidence_threshold=80.0
    )
    
    print_banner()
    
    while True:
        try:
            # Get user input
            print("\n" + "="*100)
            question = input("\n💬 Please enter your question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit']:
                print("\n👋 Goodbye!")
                break
            
            if question.lower() == 'help':
                print_banner()
                continue
            
            # Select strategy
            print("\nPlease select a strategy:")
            print("1. Basic Strategy (fast)")
            print("2. Auto Verification (recommended)")
            print("3. Chain of Verification (deep)")
            print("4. Comparison Test (comprehensive)")
            
            choice = input("\nChoice (1-4, default 2): ").strip() or "2"
            
            if choice == "1":
                print("\n⏳ Answering using basic strategy...")
                answer = protocol.ask(question, auto_verify=False)
                print_answer(answer)
                
            elif choice == "2":
                print("\n⏳ Answering using auto verification strategy...")
                answer = protocol.ask(question, auto_verify=True)
                print_answer(answer)
                
            elif choice == "3":
                print("\n⏳ Answering using chain of verification strategy...")
                answer = protocol.ask_with_chain_of_verification(question)
                print_answer(answer)
                
            elif choice == "4":
                compare_strategies(protocol, question)
                
            else:
                print("❌ Invalid choice, using default strategy (auto verification)")
                answer = protocol.ask(question, auto_verify=True)
                print_answer(answer)
            
            # Ask to continue
            print("\n" + "-"*100)
            continue_choice = input("\nContinue testing? (y/n, default y): ").strip().lower()
            if continue_choice in ['n', 'no']:
                print("\n👋 Goodbye!")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error occurred: {str(e)}")
            print("Please try again...")

def quick_test():
    """Quick test"""
    protocol = ConfidenceProtocol(
        api_key=API_KEY,
        model="gpt-4o-mini",
        confidence_threshold=80.0
    )
    
    print("\n" + "="*100)
    print("🚀 Quick Test Mode")
    print("="*100)
    
    test_questions = [
        "What is the approximate diameter of Earth in kilometers?",
        "Why is the sky blue?",
        "What is quantum entanglement?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*100}")
        print(f"Test {i}/{len(test_questions)}: {question}")
        print('='*100)
        
        answer = protocol.ask(question, auto_verify=True)
        print_answer(answer, show_details=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        interactive_mode()
