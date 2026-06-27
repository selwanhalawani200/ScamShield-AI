from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from src.privacy_agent import PrivacyAgent
from src.threat_detection_agent import ThreatDetectionAgent
from src.evidence_analyzer_agent import EvidenceAnalyzerAgent
from src.safety_advisor_agent import SafetyAdvisorAgent
from src.link_inspector_agent import LinkInspectorAgent

load_dotenv()

app = FastAPI(title="ScamShield AI API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

privacy_agent = PrivacyAgent()
threat_agent = ThreatDetectionAgent()
evidence_agent = EvidenceAnalyzerAgent()
safety_agent = SafetyAdvisorAgent()
link_agent = LinkInspectorAgent()


@app.get("/")
def home():
    return {"message": "ScamShield AI API Running"}


@app.post("/analyze")
def analyze(payload: dict):

    message = payload.get("message", "")

    sanitized_message = privacy_agent.sanitize_message(message)

    threat_result = threat_agent.analyze_message(
        sanitized_message
    )

    evidence_result = evidence_agent.analyze_evidence(
        sanitized_message,
        threat_result
    )

    link_result = link_agent.inspect_links(
        sanitized_message
    )

    advice_result = safety_agent.generate_advice(
        sanitized_message,
        threat_result,
        evidence_result
    )

    return {
        "original_message": message,
        "sanitized_message": sanitized_message,
        "threat_assessment": threat_result,
        "evidence_analysis": evidence_result,
        "link_analysis": link_result,
        "safety_recommendation": advice_result
    }