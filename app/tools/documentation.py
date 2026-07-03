import json
import logging

from google import genai

import app.config

logger = logging.getLogger(__name__)

def generate_documentation(
    business_plan: str = "",
    project_requirements: str = "",
    project_roadmap: str = "",
    risk_analysis: str = ""
) -> str:
    """Generates consolidated markdown documentation including README, SRS, Architecture Overview, Meeting Notes, Executive Summary, and API docs.

    Args:
        business_plan: Structured business plan details.
        project_requirements: Functional and non-functional requirements JSON.
        project_roadmap: Phased timelines, epics, and deliverables JSON.
        risk_analysis: Risk registry and mitigation strategies JSON.

    Returns:
        A structured markdown string compiling all documentation sections.
    """
    logger.info("Generating consolidated markdown documentation using Gemini synthesis model.")
    client = genai.Client()  # Uses AI Studio (GEMINI_API_KEY) or Vertex (ADC) automatically

    prompt = (
        "You are an expert technical writer and operations architect. "
        "Your task is to synthesize the provided inputs into a single, cohesive, "
        "comprehensive markdown document containing the following exact sections:\n"
        "1. Executive Summary\n"
        "2. README (quick start, prerequisites)\n"
        "3. Software Requirement Specification (SRS)\n"
        "4. Architecture Overview\n"
        "5. API Documentation\n"
        "6. Meeting Notes (scaffolded meeting summary)\n\n"
        "Inputs:\n"
        f"- Business Plan: {business_plan}\n"
        f"- Project Requirements: {project_requirements}\n"
        f"- Project Roadmap: {project_roadmap}\n"
        f"- Risk Analysis: {risk_analysis}\n"
    )

    try:
        response = client.models.generate_content(
            model=app.config.config.model,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        logger.warning(f"Gemini documentation synthesis failed (likely quota limit). Using markdown synthesis fallback. Error: {e}")
        # Fallback to manual assembly of structured markdown
        try:
            req_dict = json.loads(project_requirements)
            req_md = "\n".join([f"- **Functional:** {item}" for item in req_dict.get("functional_requirements", [])])
        except Exception:
            req_md = project_requirements

        try:
            roadmap_dict = json.loads(project_roadmap)
            timeline_summary = roadmap_dict.get("timeline", "4-week development window")
        except Exception:
            timeline_summary = project_roadmap

        fallback_md = f"""# Consolidated Project Documentation

## 1. Executive Summary
This document consolidates the plan and design parameters for the target project.
The business objective centers around deploying operations pipelines on top of the ADK framework.

## 2. README
### Prerequisites
- Python 3.11+
- uv package manager
- Gemini API Key

### Quick Start
```bash
make install
make playground
```

## 3. Software Requirement Specification (SRS)
### Requirements Summary
{req_md}

## 4. Architecture Overview
The system relies on a ReAct loop orchestrating custom operations tools, backed by FastAPI routes and OTel telemetry monitoring.

## 5. API Documentation
- `POST /run_sse`: Executes ReAct queries and returns a stream of events.
- `POST /a2a/app/`: Standard JSON-RPC chat endpoint.

## 6. Meeting Notes
- **Subject:** Project Kickoff & Tool Scaffolding
- **Timeline:** Target schedule aligns with {timeline_summary}.
- **Next Steps:** Proceed with infrastructure deployment.
"""
        return fallback_md
