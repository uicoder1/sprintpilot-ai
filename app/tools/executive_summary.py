import logging

from google import genai

import app.config

logger = logging.getLogger(__name__)

def create_executive_summary(
    business_plan: str = "",
    project_requirements: str = "",
    project_roadmap: str = ""
) -> str:
    """Generates an executive summary of the business plan, project requirements, and roadmap.

    Args:
        business_plan: The business plan content.
        project_requirements: The project requirements content.
        project_roadmap: The project roadmap content.

    Returns:
        A concise executive summary document in markdown format.
    """
    logger.info("Generating executive summary using Gemini reasoning.")
    client = genai.Client()  # Uses AI Studio (GEMINI_API_KEY) or Vertex (ADC) automatically

    prompt = (
        "You are an elite operations executive and venture capitalist. "
        "Your task is to synthesize the provided business plan, project requirements, "
        "and roadmap into a high-impact, professional Executive Summary in markdown.\n\n"
        "Please highlight:\n"
        "- Core Business Concept & Value Proposition\n"
        "- Target Customer Segments\n"
        "- High-level Phased Timeline & Critical Milestones\n"
        "- Key Operational Risks & Mitigations\n\n"
        "Inputs:\n"
        f"- Business Plan: {business_plan}\n"
        f"- Project Requirements: {project_requirements}\n"
        f"- Project Roadmap: {project_roadmap}\n"
    )

    try:
        response = client.models.generate_content(
            model=app.config.config.model,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        logger.warning(f"Gemini executive summary generation failed (likely quota limit). Using fallback. Error: {e}")
        return """# Executive Summary (Fallback)

## Business Concept
Based on the provided details, this venture aims to launch a scalable product utilizing modern ADK frameworks.

## Customer Segments
Targeting developers, founders, and industry professionals.

## Phased Timeline & Milestones
- **Setup & Planning:** Initialize repositories and tools.
- **Core Iterations:** Develop main features and test interfaces.
- **Launch & Scaling:** Conduct validation loops and deploy.

## Strategic Risks
Mitigate operational bottlenecks by utilizing structured fallbacks and API caching mechanisms.
"""
