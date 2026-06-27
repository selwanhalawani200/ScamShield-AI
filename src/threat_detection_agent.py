import os
import json
from pydantic import BaseModel
from google import genai
from google.genai import types

class ThreatDetectionResponse(BaseModel):
    risk_score: int
    risk_level: str

class ThreatDetectionAgent:
    def __init__(self):
        # The genai.Client() automatically picks up GEMINI_API_KEY from environment
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        
        # System instructions to guide the model's behavior and output schema
        self.system_instruction = """
You are the Threat Detection Agent for ScamShield AI.
Your job is to analyze incoming text messages and determine if they contain a scam, threat, or malicious intent.
Analyze the provided message text and assign:
1. A risk_score from 0 to 100 (0 = completely safe, 100 = definitely a scam/threat).
2. A risk_level (must be exactly one of: "LOW", "MEDIUM", "HIGH").
   - LOW: 0-33
   - MEDIUM: 34-66
   - HIGH: 67-100

You must always output a valid JSON object strictly adhering to the schema.
"""

    def analyze_message(self, message: str) -> dict:
        """
        Analyzes a message using Gemini and returns a structured dictionary.
        
        Args:
            message (str): The text message to analyze.
            
        Returns:
            dict: A dictionary containing 'risk_score' and 'risk_level'.
            
        Raises:
            ValueError: If Gemini returns invalid JSON, missing fields, 
                        out-of-bounds values, or mismatched score/level.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                response_mime_type="application/json",
                response_schema=ThreatDetectionResponse,
                temperature=0.1
            ),
        )
        
        # Parse JSON response safely
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Gemini returned invalid JSON. Response text: {response.text}") from e
            
        # Validate risk_score presence and type
        if "risk_score" not in data or not isinstance(data["risk_score"], int):
            raise ValueError(f"Missing or invalid 'risk_score' in response: {data}")
            
        score = data["risk_score"]
        
        # Validate risk_score range
        if score < 0 or score > 100:
            raise ValueError(f"'risk_score' must be between 0 and 100. Got: {score}")
            
        # Validate risk_level presence and type
        if "risk_level" not in data or not isinstance(data["risk_level"], str):
            raise ValueError(f"Missing or invalid 'risk_level' in response: {data}")
            
        level = data["risk_level"]
        valid_levels = ["LOW", "MEDIUM", "HIGH"]
        
        # Validate risk_level valid choices
        if level not in valid_levels:
            raise ValueError(f"'risk_level' must be one of {valid_levels}. Got: '{level}'")
            
        # Validate risk_level matches score range
        expected_level = "LOW"
        if 34 <= score <= 66:
            expected_level = "MEDIUM"
        elif 67 <= score <= 100:
            expected_level = "HIGH"
            
        if level != expected_level:
            raise ValueError(
                f"Mismatch: 'risk_level' is '{level}', but 'risk_score' is {score} "
                f"(expected '{expected_level}')."
            )
            
        return data

if __name__ == "__main__":
    # Quick test if run directly
    import dotenv
    dotenv.load_dotenv()
    agent = ThreatDetectionAgent()
    try:
        result = agent.analyze_message("Hey, your bank account has been locked. Click here to verify your identity.")
        print("Success! Parsed result:", result)
    except Exception as e:
        print("Error during analysis:", e)
