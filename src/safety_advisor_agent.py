import os
import json
from pydantic import BaseModel
from google import genai
from google.genai import types


class SafetyAdvisorResponse(BaseModel):
    recommendation: str


class SafetyAdvisorAgent:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")

        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"

        self.system_instruction = """
You are the Safety Advisor Agent for ScamShield AI.

Your task is to provide a short, practical recommendation to the user.

Rules:
1. If risk level is HIGH:
   - Advise the user not to interact with the message.
   - Suggest blocking the sender.
   - Suggest reporting the scam if appropriate.

2. If risk level is MEDIUM:
   - Advise caution.
   - Suggest verifying information independently.

3. If risk level is LOW:
   - Explain that the message appears safe.
   - No action is usually required.

Keep recommendations short and user-friendly.

You must always return valid JSON.
"""

    def generate_advice(
        self,
        message: str,
        threat_assessment: dict,
        evidence_analysis: dict
    ) -> dict:

        prompt = f"""
Message:
{message}

Threat Assessment:
{threat_assessment}

Evidence Analysis:
{evidence_analysis}
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                response_mime_type="application/json",
                response_schema=SafetyAdvisorResponse,
                temperature=0.1
            ),
        )

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Gemini returned invalid JSON. Response text: {response.text}"
            ) from e

        if "recommendation" not in data:
            raise ValueError(
                f"Missing recommendation field in response: {data}"
            )

        if not isinstance(data["recommendation"], str):
            raise ValueError(
                f"Recommendation must be a string: {data}"
            )

        data["recommendation"] = data["recommendation"].strip()

        if not data["recommendation"]:
            raise ValueError("Recommendation cannot be empty.")

        return data
    
if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv()

    agent = SafetyAdvisorAgent()

    threat = {
        "risk_score": 95,
        "risk_level": "HIGH"
    }

    evidence = {
        "scam_indicators": ["prize claim"],
        "explanation": "Suspicious prize message."
    }

    result = agent.generate_advice(
        "You won a free iPhone!",
        threat,
        evidence
    )

    print(result)