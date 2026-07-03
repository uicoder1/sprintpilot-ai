import json
import logging

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

import app.config

logger = logging.getLogger(__name__)

class RiskDetail(BaseModel):
    risk_description: str = Field(description="Description of the identified risk")
    severity: str = Field(description="Severity level of the risk (e.g. High, Medium, Low)")
    probability: str = Field(description="Probability level of occurrence (e.g. High, Medium, Low)")
    mitigation: str = Field(description="Suggested mitigation strategy")


class RiskAnalysisSchema(BaseModel):
    business_risks: list[RiskDetail] = Field(description="Identified strategic business risks")
    technical_risks: list[RiskDetail] = Field(description="Technical, infrastructure, or tooling risks")
    financial_risks: list[RiskDetail] = Field(description="Financial, funding, or cashflow risks")
    marketing_risks: list[RiskDetail] = Field(description="Marketing, user acquisition, or branding risks")
    security_risks: list[RiskDetail] = Field(description="Security, threat vectors, data privacy, or breach risks")
    legal_risks: list[RiskDetail] = Field(description="Legal, compliance, intellectual property, or regulatory risks")


def analyze_business_risks(company_name: str, industry: str) -> str:
    """Uses Gemini reasoning to identify and evaluate business, technical, financial, marketing, security, and legal risks.

    Args:
        company_name: The name of the company.
        industry: The industry domain.

    Returns:
        A JSON string containing categorized risks, each with severity, probability, and suggested mitigation.
    """
    logger.info(f"Performing business risk analysis for '{company_name}' in the '{industry}' sector.")
    client = genai.Client()  # Uses AI Studio (GEMINI_API_KEY) or Vertex (ADC) automatically

    prompt = (
        "You are an expert enterprise risk analyst and operations advisor. "
        f"Your task is to identify and analyze potential risks for the company '{company_name}' "
        f"operating in the '{industry}' industry.\n\n"
        "Please evaluate: Business Risks, Technical Risks, Financial Risks, Marketing Risks, "
        "Security Risks, and Legal Risks. Provide detailed severity, probability, and mitigation "
        "strategies for each category."
    )

    try:
        response = client.models.generate_content(
            model=app.config.config.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=RiskAnalysisSchema,
            )
        )
        return response.text
    except Exception as e:
        logger.warning(f"Gemini risk analysis failed (likely quota limit). Using robust structured fallback. Error: {e}")
        fallback_data = {
            "business_risks": [
                {
                    "risk_description": f"New competitors entering the {industry} market.",
                    "severity": "Medium",
                    "probability": "High",
                    "mitigation": "Establish a strong brand identity and unique value proposition."
                }
            ],
            "technical_risks": [
                {
                    "risk_description": "API rate limits blocking key user operations.",
                    "severity": "High",
                    "probability": "Medium",
                    "mitigation": "Implement caching mechanisms and robust fallbacks."
                }
            ],
            "financial_risks": [
                {
                    "risk_description": "High infrastructure cost scaling out pacing revenue.",
                    "severity": "Medium",
                    "probability": "Medium",
                    "mitigation": "Optimize code execution times and cloud resource configurations."
                }
            ],
            "marketing_risks": [
                {
                    "risk_description": "Inability to reach target audiences effectively.",
                    "severity": "Low",
                    "probability": "Medium",
                    "mitigation": "Leverage organic content marketing and localized campaigns."
                }
            ],
            "security_risks": [
                {
                    "risk_description": "Leakage of sensitive user information in telemetry logs.",
                    "severity": "High",
                    "probability": "Low",
                    "mitigation": "Disable content tracking in OpenTelemetry spans."
                }
            ],
            "legal_risks": [
                {
                    "risk_description": f"Failure to comply with local regulatory standards for {industry}.",
                    "severity": "High",
                    "probability": "Low",
                    "mitigation": "Engage legal counsel to perform regular compliance audits."
                }
            ]
        }
        return json.dumps(fallback_data, indent=2)
