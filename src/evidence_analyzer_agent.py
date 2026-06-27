import os
import json
from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types

class EvidenceAnalyzerResponse(BaseModel):
    scam_indicators: List[str]
    explanation: str

class EvidenceAnalyzerAgent:
    def __init__(self):
        # Initialize Gemini Client
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        
        # System instructions to guide the model's behavior and output schema
        self.system_instruction = """
You are the Evidence Analyzer Agent for ScamShield AI.
Your job is to analyze a text message and the initial threat assessment (risk_score, risk_level) to identify specific scam indicators and provide a concise explanation.

Rules for scam_indicators:
1. Prefer these predefined indicators:
   - urgency
   - prize claim
   - suspicious URL
   - payment request
   - credential request
   - impersonation
   - unrealistic job offer
2. You may add a new, concise indicator only if strictly needed.
3. For LOW risk messages, scam_indicators should usually be an empty list []. If there is a minor concern (e.g., "minor suspicious link"), you can include it, but the explanation MUST clearly state that the overall risk is low.

Rules for explanation:
1. Provide a short, clear, and user-friendly explanation of why the message is suspicious or safe.
2. Keep it concise.

You must always output a valid JSON object strictly adhering to the schema.
"""

    def analyze_evidence(self, message: str, threat_assessment: dict) -> dict:
        """
        Analyzes the evidence of a message using Gemini and returns a structured dictionary.
        
        Args:
            message (str): The text message to analyze.
            threat_assessment (dict): The output from the ThreatDetectionAgent containing 'risk_score' and 'risk_level'.
            
        Returns:
            dict: A dictionary containing 'scam_indicators' (list of str) and 'explanation' (str).
            
        Raises:
            ValueError: If Gemini returns invalid JSON or missing fields.
        """
        # Combine the inputs into a single prompt for the model
        prompt = f"""
Message Content:
{message}

Threat Assessment:
Risk Score: {threat_assessment.get('risk_score')}
Risk Level: {threat_assessment.get('risk_level')}
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                response_mime_type="application/json",
                response_schema=EvidenceAnalyzerResponse,
                temperature=0.1
            ),
        )
        
        # Parse JSON response safely
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Gemini returned invalid JSON. Response text: {response.text}") from e
            
        # Validate schema presence
        if "scam_indicators" not in data or not isinstance(data["scam_indicators"], list):
            raise ValueError(f"Missing or invalid 'scam_indicators' in response: {data}")
            
        if "explanation" not in data or not isinstance(data["explanation"], str):
            raise ValueError(f"Missing or invalid 'explanation' in response: {data}")
            
        # Validate all indicators are strings
        if not all(isinstance(ind, str) for ind in data["scam_indicators"]):
            raise ValueError(f"All items in 'scam_indicators' must be strings: {data['scam_indicators']}")
            
        # Clean indicators: strip whitespace and remove empty strings
        cleaned_indicators = [ind.strip() for ind in data["scam_indicators"] if ind.strip()]
        data["scam_indicators"] = cleaned_indicators
        
        # Clean and validate explanation
        cleaned_explanation = data["explanation"].strip()
        if not cleaned_explanation:
            raise ValueError("The 'explanation' field cannot be empty.")
        data["explanation"] = cleaned_explanation
        
        # Enforce LOW risk indicator limit
        if threat_assessment.get("risk_level") == "LOW" and len(cleaned_indicators) > 1:
            data["scam_indicators"] = [cleaned_indicators[0]]
            
        return data

if __name__ == "__main__":
    # Quick test if run directly
    import dotenv
    dotenv.load_dotenv()
    agent = EvidenceAnalyzerAgent()
    try:
        sample_msg = "Hey, your bank account has been locked. Click here to verify your identity."
        sample_assessment = {"risk_score": 95, "risk_level": "HIGH"}
        result = agent.analyze_evidence(sample_msg, sample_assessment)
        print("Success! Parsed result:", result)
    except Exception as e:
        print("Error during analysis:", e)
