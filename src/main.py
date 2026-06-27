import os
import sys
import time
from dotenv import load_dotenv
from threat_detection_agent import ThreatDetectionAgent
from evidence_analyzer_agent import EvidenceAnalyzerAgent
from privacy_agent import PrivacyAgent
from safety_advisor_agent import SafetyAdvisorAgent
from link_inspector_agent import LinkInspectorAgent

def analyze_with_retry(func, *args, max_retries=2, **kwargs):
    """Attempts to execute an API call, retrying on temporary API errors."""
    for attempt in range(max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_str = str(e).upper()
            is_temporary_error = any(
                err in error_str for err in ["429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE"]
            )
            
            if is_temporary_error and attempt < max_retries:
                print(f"API Error ({e}). Retrying in 35 seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(35)
            else:
                raise e

def process_file(
    privacy_agent: PrivacyAgent,
    threat_agent: ThreatDetectionAgent,
    evidence_agent: EvidenceAnalyzerAgent,
    link_agent: LinkInspectorAgent,
    safety_agent: SafetyAdvisorAgent,
    file_path: str
):
    
    """Processes messages from a file and prints the output with evaluation."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    print(f"\n--- Processing messages from {file_path} ---")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        
    # Split by double newlines to separate records
    records = content.split('\n\n')
    
    total = 0
    successful = 0
    failed = 0
    correct = 0
    
    for i, record in enumerate(records, 1):
        lines = record.strip().split('\n', 1)
        if len(lines) < 2:
            continue
            
        expected_label = lines[0].strip()
        message = lines[1].strip()
        
        print(f"\nExample {i}:")
        print(f"Expected Label: {expected_label}")
        
        
        sanitized_message = privacy_agent.sanitize_message(message)
        print(f"Sanitized Message: {sanitized_message}")
        
        total += 1
        
        try:
            result = analyze_with_retry(threat_agent.analyze_message, sanitized_message)
            risk_level = result.get("risk_level")
            print("Threat Assessment:")
            print(result)
            print(f"Predicted Risk Level: {risk_level}")
            
            # Evidence Analysis
            evidence = analyze_with_retry(
               evidence_agent.analyze_evidence,
               sanitized_message,
               result
            )
            print("Evidence Analysis:")
            print(evidence)
            
            link_result = link_agent.inspect_links(sanitized_message)

            print("Link Analysis:")
            print(link_result)

            advice = analyze_with_retry(
               safety_agent.generate_advice,
               sanitized_message,
               result,
               evidence
            )

            print("Safety Recommendation:")
            print(advice)

            successful += 1
            
            # Evaluation
            is_correct = False
            if expected_label == "[SCAM]" and risk_level in ["MEDIUM", "HIGH"]:
                is_correct = True
            elif expected_label == "[SAFE]" and risk_level == "LOW":
                is_correct = True
                
            if is_correct:
                print("Evaluation: CORRECT")
                correct += 1
            else:
                print("Evaluation: REVIEW")
                
        except Exception as e:
            print(f"Error analyzing message: {e}")
            print("Evaluation: FAILED API CALL")
            failed += 1
            
    print("\n--- Summary ---")
    print(f"Total Examples: {total}")
    print(f"Successful Predictions: {successful}")
    print(f"Failed API Calls: {failed}")
    print(f"Correct Predictions: {correct}")
    if successful > 0:
        accuracy = (correct / successful) * 100
        print(f"Accuracy: {accuracy:.2f}%")
    else:
        print("Accuracy: N/A")

def interactive_mode(
    privacy_agent: PrivacyAgent,
    threat_agent: ThreatDetectionAgent,
    evidence_agent: EvidenceAnalyzerAgent,
    link_agent: LinkInspectorAgent,
    safety_agent: SafetyAdvisorAgent
):
    
    """Runs an interactive loop for manual input."""
    print("\n--- Interactive Mode ---")
    print("Enter your message to analyze (or type 'quit' to exit):")
    while True:
        try:
            msg = input("> ")
            if msg.lower() in ['quit', 'exit']:
                break
            if not msg.strip():
                continue
                
            sanitized_msg = privacy_agent.sanitize_message(msg)
            print(f"\nSanitized Message: {sanitized_msg}")
            
            result = analyze_with_retry(threat_agent.analyze_message, sanitized_msg)
            print("\nThreat Assessment:")
            print(result)
            
            evidence = analyze_with_retry(evidence_agent.analyze_evidence, sanitized_msg, result)
            print("\nEvidence Analysis:")
            print(evidence)
            
            link_result = link_agent.inspect_links(sanitized_msg)

            print("\nLink Analysis:")
            print(link_result)
            
            advice = analyze_with_retry(
                safety_agent.generate_advice,
                sanitized_msg,
                result,
                evidence
            )

            print("\nSafety Recommendation:")
            print(advice)
        except KeyboardInterrupt:
            print("\nExiting interactive mode.")
            break
        except Exception as e:
            print(f"Error analyzing message: {e}")

def main():
    # Load environment variables (like GEMINI_API_KEY)
    load_dotenv()
    
    if not os.environ.get("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY not found in environment or .env file.")
        print("Please set it before running the script.")
        sys.exit(1)
        
    try:
        privacy_agent = PrivacyAgent()
        threat_agent = ThreatDetectionAgent()
        evidence_agent = EvidenceAnalyzerAgent()
        safety_agent = SafetyAdvisorAgent()
        link_agent = LinkInspectorAgent()
    except Exception as e:
        print(f"Failed to initialize Agents: {e}")
        sys.exit(1)

    print("ScamShield AI - Multi-Agent Scam Analysis MVP")
    print("1. Interactive Mode (Terminal Input)")
    print("2. File Mode (Process sample_messages.txt)")
    print("3. Exit")
    
    choice = input("Select an option (1-3): ")
    
    if choice == '1':
        interactive_mode(privacy_agent, threat_agent, evidence_agent,link_agent, safety_agent)
    elif choice == '2':
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_messages.txt")
        process_file(privacy_agent, threat_agent, evidence_agent,link_agent, safety_agent, file_path)
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()
