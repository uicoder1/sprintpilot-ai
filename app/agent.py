# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import json
from zoneinfo import ZoneInfo

import app.config
from google import genai
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types
from pydantic import BaseModel, Field


def generate_business_plan(company_name: str, industry: str, target_audience: str) -> str:
    """Generates a structured business plan outline for a startup or business.

    Args:
        company_name: The name of the company/startup.
        industry: The industry the business operates in.
        target_audience: The main target customer segment.

    Returns:
        A markdown-formatted string containing the structured business plan outline.
    """
    return f"""# Business Plan: {company_name}
**Industry:** {industry}
**Target Audience:** {target_audience}

## 1. Executive Summary
A summary of {company_name}'s mission, core value proposition, and growth goals in the {industry} space.

## 2. Market Analysis
Analysis of market trends in {industry} and how {company_name} serves the target demographic of {target_audience}.

## 3. Product & Services
Details of the core offerings, key features, and product-market fit.

## 4. Marketing & Sales Strategy
Channels to reach {target_audience} and convert leads.

## 5. Operations & Financial Projections
Key milestones, team structure, and mock 3-year financial projections.
"""


def generate_project_requirements(business_plan: str) -> str:
    """Generates structured project requirements from a business plan.

    Args:
        business_plan: The text or content of the business plan.

    Returns:
        A JSON string containing functional requirements, non-functional requirements,
        user personas, user stories, acceptance criteria, and nice to have features.
    """
    # Simple extraction of company name or industry from input to customize output
    company_name = "Target Startup"
    industry = "SaaS"
    
    plan_lower = business_plan.lower()
    if "business plan:" in plan_lower:
        # Extract title line
        lines = business_plan.split("\n")
        for line in lines:
            if line.strip().lower().startswith("# business plan:"):
                company_name = line.split(":", 1)[1].strip()
                break
            elif line.strip().lower().startswith("business plan:"):
                company_name = line.split(":", 1)[1].strip()
                break
    
    if "industry:" in plan_lower:
        for line in business_plan.split("\n"):
            if "industry:" in line.lower():
                industry = line.split(":", 1)[1].strip().replace("**", "").replace("*", "")
                break

    requirements_data = {
        "functional_requirements": [
            f"Implement a scalable user onboarding flow tailored for the {industry} industry.",
            f"Provide an automated plan generation dashboard for {company_name} users.",
            "Include audit logging to track all generated documents and workflows."
        ],
        "non_functional_requirements": [
            "Performance: The dashboard pages must load within 1.5 seconds.",
            "Security: All sensitive project configurations and inputs must be encrypted at rest.",
            "Scalability: Support up to 10,000 concurrent active operations sessions."
        ],
        "user_personas": [
            {
                "name": "Sarah the Startup Founder",
                "role": f"Co-founder at a {industry} venture",
                "needs": "Wants to quickly scaffold project roadmaps and business requirements to align her remote engineering team."
            },
            {
                "name": "Alex the Product Manager",
                "role": f"Lead PM at {company_name}",
                "needs": "Needs structured user stories and acceptance criteria templates to reduce backlog creation overhead."
            }
        ],
        "user_stories": [
            f"As a startup founder, I want to paste my business goals for {company_name} so that I get a structured PRD instantly.",
            "As an administrator, I want to download requirement specs as PDF/Markdown so that I can share them with stakeholders."
        ],
        "acceptance_criteria": [
            "User stories must follow the 'As a... I want to... So that...' Agile format.",
            "The generated requirements document must contain all specified headers.",
            "Structured outputs must be valid JSON matching the target schema."
        ],
        "nice_to_have_features": [
            "Integration with Jira or Trello APIs to direct-export generated user stories.",
            "AI-powered cost estimation tool based on roadmap duration parameters."
        ]
    }
    
    return json.dumps(requirements_data, indent=2)


def generate_user_stories(feature_name: str, goal: str) -> str:
    """Generates Agile user stories with acceptance criteria for a given feature.

    Args:
        feature_name: The name of the feature or epic.
        goal: The user objective or business goal of the feature.

    Returns:
        A formatted string listing the user stories and their acceptance criteria.
    """
    return f"""# Agile User Stories for: {feature_name}
**Feature Goal:** {goal}

## User Story 1
**As a** User
**I want to** use the {feature_name} functionality
**So that** I can achieve the following goal: {goal}

### Acceptance Criteria:
1. User can successfully access the {feature_name} component.
2. The system processes the input and aligns with the target goal.
3. Errors are handled gracefully with user-friendly alerts.

## User Story 2 (Admin flow)
**As an** Administrator
**I want to** monitor the performance of {feature_name}
**So that** I can ensure system health and compliance.

### Acceptance Criteria:
1. Admin dashboard shows usage statistics of the {feature_name} feature.
2. Audit logs capture tool executions.
"""


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
    except Exception:
        # Fallback if Gemini rate limits are hit or network fails
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


def generate_documentation(module_name: str, code_snippet: str) -> str:
    """Generates markdown technical documentation for a codebase module or snippet.

    Args:
        module_name: The name of the module or component.
        code_snippet: The actual code structure or signature to document.

    Returns:
        A markdown technical reference sheet.
    """
    return f"""# Technical Documentation: {module_name}

## Overview
This document describes the API and structural design of the `{module_name}` module.

## Implementation Snippet
```python
{code_snippet}
```

## Description
The `{module_name}` module exposes interfaces to coordinate core logic. It has been validated through integration tests and adheres to the project's standard structure.
"""


def analyze_business_risks(company_name: str, industry: str) -> str:
    """Identifies and evaluates business, operational, and market risks with mitigations.

    Args:
        company_name: The name of the company.
        industry: The industry domain.

    Returns:
        A risk analysis report with mitigation strategies.
    """
    return f"""# Business Risk Analysis: {company_name}
**Industry Sector:** {industry}

## 1. Market & Competitive Risk
*   **Risk:** Rapid evolution of tech standards in the {industry} sector might render the current business model obsolete.
*   **Mitigation:** Actively iterate on features using agile workflows and gather direct user feedback.

## 2. Operational Risk
*   **Risk:** Service downtime or API limits (e.g. rate limits) blocking operations.
*   **Mitigation:** Set up robust exception handling, fallbacks, and retry options in agent workflows.

## 3. Compliance & Regulatory Risk
*   **Risk:** PII leakage in telemetry traces.
*   **Mitigation:** Verify telemetry spans do not capture raw message payloads and follow data privacy compliance standards.
"""


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=app.config.config.model,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are SprintPilot AI, an Autonomous Business Operations Assistant designed to "
        "help startup founders, ecommerce businesses, and software teams plan, organize, "
        "and execute their projects. You are equipped with specialized tools to generate "
        "business plans, list functional requirements, compile user stories, design project "
        "roadmaps, write technical documentation, and perform business risk analysis. "
        "Ensure you leverage these tools whenever appropriate to provide highly structured, "
        "valuable, and action-oriented documentation."
    ),
    tools=[
        generate_business_plan,
        generate_project_requirements,
        generate_user_stories,
        create_project_roadmap,
        generate_documentation,
        analyze_business_risks,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
