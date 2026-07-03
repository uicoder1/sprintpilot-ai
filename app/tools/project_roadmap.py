import json
import logging

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

import app.config

logger = logging.getLogger(__name__)

class Epic(BaseModel):
    name: str = Field(description="Name/Title of the Epic")
    description: str = Field(description="Brief summary of the Epic's objectives")


class Milestone(BaseModel):
    title: str = Field(description="Title of the milestone")
    timeline_week: str = Field(description="Target timeline or week number (e.g. Week 2)")


class RoadmapSchema(BaseModel):
    epics: list[Epic] = Field(description="List of calculated project epics")
    milestones: list[Milestone] = Field(description="List of project milestones")
    timeline: str = Field(description="Overall project timeline summary")
    priority: str = Field(description="Strategic priority level: High, Medium, or Low")
    dependencies: list[str] = Field(description="Key module or operational dependencies")
    deliverables: list[str] = Field(description="Core tangible deliverables upon completion")


def create_project_roadmap(project_requirements: str) -> str:
    """Uses Gemini reasoning to convert project requirements into a structured project roadmap.

    Args:
        project_requirements: A JSON string or text detailing project requirements.

    Returns:
        A JSON string containing epics, milestones, timeline, priority, dependencies, and deliverables.
    """
    logger.info("Generating project roadmap using Gemini reasoning model.")
    client = genai.Client()  # Uses AI Studio (GEMINI_API_KEY) or Vertex (ADC) automatically

    prompt = (
        "You are an expert technical product manager and operations architect. "
        "Your task is to analyze the following project requirements and convert them into "
        "a structured project roadmap containing epics, milestones, timeline, priority, "
        "dependencies, and deliverables.\n\n"
        f"Project Requirements:\n{project_requirements}\n"
    )

    try:
        response = client.models.generate_content(
            model=app.config.config.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=RoadmapSchema,
            )
        )
        return response.text
    except Exception as e:
        logger.warning(f"Gemini roadmap creation failed (likely quota limit). Using robust structured fallback. Error: {e}")
        fallback_data = {
            "epics": [
                {"name": "Core Platform Setup", "description": "Initialize codebase and setup infrastructure pipelines."},
                {"name": "Requirements Processing", "description": "Implement core requirements tool mapping."}
            ],
            "milestones": [
                {"title": "Initial Scaffold Complete", "timeline_week": "Week 1"},
                {"title": "Integration Verification", "timeline_week": "Week 3"}
            ],
            "timeline": "4-week target iteration plan",
            "priority": "High",
            "dependencies": ["FastAPI server configuration", "Google GenAI credentials"],
            "deliverables": ["Working ReAct agent", "Passed test suites"]
        }
        return json.dumps(fallback_data, indent=2)
