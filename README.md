# ScamShield AI

### AI-Powered Multi-Agent Scam Detection and Prevention System

**Track:** Agents for Good | Kaggle AI Agents Capstone Project

---

## Problem Statement

Online scams, phishing attacks, and social engineering campaigns continue to grow in sophistication, causing financial losses, identity theft, and privacy breaches for millions of users worldwide.

Many existing solutions focus only on detection and provide limited explanations, leaving users uncertain about why a message is dangerous and what actions they should take.

ScamShield AI addresses this challenge by combining multiple specialized AI agents that work together to identify threats, explain risks, protect sensitive information, and provide actionable safety recommendations.

---

## Solution Overview

ScamShield AI is a privacy-aware multi-agent system designed to analyze messages, emails, and URLs for scam and phishing indicators.

Instead of relying on a single model, the system orchestrates multiple specialized agents, each responsible for a specific task within the analysis pipeline.

The result is a transparent, explainable, and user-focused scam detection experience.

---

## Multi-Agent Architecture

The system consists of five specialized agents:

### 1. Privacy Agent

* Detects and masks sensitive personal information before AI processing.
* Protects:

  * Email addresses
  * Phone numbers
  * Credit card numbers
  * IBANs

### 2. Threat Detection Agent

* Evaluates message content.
* Produces:

  * Risk Score (0–100)
  * Risk Level (LOW / MEDIUM / HIGH)

### 3. Evidence Analyzer Agent

* Identifies scam indicators.
* Explains why a message may be malicious.
* Generates structured evidence-based reasoning.

### 4. Link Inspector Agent

* Extracts URLs from messages.
* Flags potentially suspicious links and phishing domains.

### 5. Safety Advisor Agent

* Generates clear user guidance.
* Recommends appropriate next actions based on detected risks.

---

## System Workflow

Raw Message
↓
Privacy Agent
↓
Threat Detection Agent
↓
Evidence Analyzer Agent
↓
Link Inspector Agent
↓
Safety Advisor Agent
↓
Final Scam Report

---

## Key Features

### Privacy-First Design

Sensitive information is sanitized before being sent to AI models.

### Multi-Agent Reasoning

Multiple specialized agents collaborate to produce more reliable results.

### Scam Indicator Detection

Detects phishing and scam patterns such as:

* Urgency tactics
* Credential requests
* Suspicious URLs
* Prize claims
* Impersonation attempts
* Payment requests
* Unrealistic job offers

### Explainable AI

Provides transparent explanations rather than simple labels.

### Risk Scoring

Generates:

* Numerical Risk Score (0–100)
* Risk Classification (LOW / MEDIUM / HIGH)

### Safety Recommendations

Produces practical guidance to help users avoid scams.

---

## Technologies Used

* Python
* Gemini 2.5 Flash
* Google GenAI SDK
* Pydantic
* Python Dotenv
* Regular Expressions (Regex)

---

## Security Features

* Local privacy sanitization
* Sensitive data masking
* Structured JSON validation
* API error handling and retry mechanisms
* Separation of agent responsibilities

---

## Project Goals

* Protect users from phishing and scam attempts.
* Improve digital safety awareness.
* Demonstrate practical AI agent orchestration.
* Showcase privacy-aware AI system design.

---

## Repository Structure

src/
├── main.py
├── privacy_agent.py
├── threat_detection_agent.py
├── evidence_analyzer_agent.py
├── link_inspector_agent.py
├── safety_advisor_agent.py

---

## Future Improvements

* Streamlit Web Interface
* Real-time URL reputation lookup
* Browser extension integration
* Multilingual scam detection
* Mobile application support

---

## Architecture Documentation

For a detailed architecture diagram and agent interaction flow, see:

architecture.md

---

Developed as part of Kaggle's AI Agents Capstone Project.

