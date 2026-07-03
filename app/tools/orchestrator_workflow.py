import json
import logging

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

import app.config

# Import individual step tools
from app.tools.business_plan import generate_business_plan
from app.tools.business_risks import analyze_business_risks
from app.tools.documentation import generate_documentation
from app.tools.executive_summary import create_executive_summary
from app.tools.project_requirements import generate_project_requirements
from app.tools.project_roadmap import create_project_roadmap
from app.tools.user_stories import generate_user_stories

logger = logging.getLogger(__name__)

class BusinessParameters(BaseModel):
    company_name: str = Field(default="", description="Name of the company/startup, empty if not found")
    industry: str = Field(default="", description="Industry segment, empty if not found")
    target_audience: str = Field(default="", description="Target customer segment, empty if not found")
    budget: str = Field(default="", description="Estimated budget or funding level, empty if not found")


def execute_business_planning_workflow(business_idea: str, company_name: str = "", industry: str = "", target_audience: str = "", budget: str = "") -> str:
    """Executes the full sequential business planning and documentation workflow automatically.

    Args:
        business_idea: The raw description of the business idea.
        company_name: Optional name of the company.
        industry: Optional industry domain.
        target_audience: Optional target customer segment.
        budget: Optional budget or funding level.

    Returns:
        A unified, comprehensive structured markdown Business Report or a prompt requesting missing information.
    """
    logger.info("Initializing business planning orchestration workflow.")
    client = genai.Client()

    # Extract parameters using Gemini if not already provided
    parsed = None
    if not (company_name and industry and target_audience and budget):
        logger.info("Some parameters are missing. Attempting to parse details from raw business idea.")
        prompt = (
            "You are an expert operations parser. Extract the company name, industry, target audience, "
            "and budget from the following business idea. If any are not found, leave them as empty strings.\n\n"
            f"Business Idea: {business_idea}"
        )
        try:
            response = client.models.generate_content(
                model=app.config.config.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                    response_schema=BusinessParameters,
                )
            )
            parsed = json.loads(response.text)
            logger.info(f"Gemini parsed parameters: {parsed}")
        except Exception as e:
            logger.warning(f"Failed to parse parameters via Gemini: {e}")

    # Merge parsed parameters with arguments
    if parsed:
        if not company_name:
            company_name = parsed.get("company_name", "")
        if not industry:
            industry = parsed.get("industry", "")
        if not target_audience:
            target_audience = parsed.get("target_audience", "")
        if not budget:
            budget = parsed.get("budget", "")

    # Check for missing information
    missing_fields = []
    if not company_name:
        missing_fields.append("business name")
    if not industry:
        missing_fields.append("industry")
    if not target_audience:
        missing_fields.append("target audience")
    if not budget:
        missing_fields.append("budget")

    if missing_fields:
        fields_str = ", ".join(missing_fields)
        logger.info(f"Cannot run workflow. Missing parameters: {fields_str}")
        return f"To generate your complete Business Report, please provide the following missing details: {fields_str}."

    # Execute workflow steps sequentially
    logger.info(f"All parameters present. Executing sequential workflow for '{company_name}'...")

    # Step 1: generate_business_plan()
    logger.info("\n🟢 Business Planner      Working...\n⏳ Requirements Agent    Waiting...\n⏳ User Stories Agent    Waiting...\n⏳ Roadmap Agent         Waiting...\n⏳ Risk Agent            Waiting...\n⏳ Documentation Agent   Waiting...\n⏳ Executive Agent       Waiting...\n")
    biz_plan = generate_business_plan(company_name, industry, target_audience)

    # Step 2: generate_project_requirements()
    logger.info("\n🟢 Business Planner      ✓\n🟡 Requirements Agent    Working...\n⏳ User Stories Agent    Waiting...\n⏳ Roadmap Agent         Waiting...\n⏳ Risk Agent            Waiting...\n⏳ Documentation Agent   Waiting...\n⏳ Executive Agent       Waiting...\n")
    proj_reqs = generate_project_requirements(biz_plan)

    # Step 3: generate_user_stories()
    logger.info("\n🟢 Business Planner      ✓\n🟢 Requirements Agent    ✓\n🟡 User Stories Agent    Working...\n⏳ Roadmap Agent         Waiting...\n⏳ Risk Agent            Waiting...\n⏳ Documentation Agent   Waiting...\n⏳ Executive Agent       Waiting...\n")
    feature_name = f"{company_name} Platform Portal"
    user_stories = generate_user_stories(feature_name, f"Support {industry} core operations and client interactions")

    # Step 4: create_project_roadmap()
    logger.info("\n🟢 Business Planner      ✓\n🟢 Requirements Agent    ✓\n🟢 User Stories Agent    ✓\n🟡 Roadmap Agent         Working...\n⏳ Risk Agent            Waiting...\n⏳ Documentation Agent   Waiting...\n⏳ Executive Agent       Waiting...\n")
    roadmap = create_project_roadmap(proj_reqs)

    # Step 5: analyze_business_risks()
    logger.info("\n🟢 Business Planner      ✓\n🟢 Requirements Agent    ✓\n🟢 User Stories Agent    ✓\n🟢 Roadmap Agent         ✓\n🟡 Risk Agent            Working...\n⏳ Documentation Agent   Waiting...\n⏳ Executive Agent       Waiting...\n")
    risks = analyze_business_risks(company_name, industry)

    # Step 6: generate_documentation()
    logger.info("\n🟢 Business Planner      ✓\n🟢 Requirements Agent    ✓\n🟢 User Stories Agent    ✓\n🟢 Roadmap Agent         ✓\n🟢 Risk Agent            ✓\n🟡 Documentation Agent   Working...\n⏳ Executive Agent       Waiting...\n")
    documentation = generate_documentation(biz_plan, proj_reqs, roadmap, risks)

    # Step 7: create_executive_summary()
    logger.info("\n🟢 Business Planner      ✓\n🟢 Requirements Agent    ✓\n🟢 User Stories Agent    ✓\n🟢 Roadmap Agent         ✓\n🟢 Risk Agent            ✓\n🟢 Documentation Agent   ✓\n🟡 Executive Agent       Working...\n")
    exec_summary = create_executive_summary(biz_plan, proj_reqs, roadmap)

    logger.info("\n🟢 Business Planner      ✓\n🟢 Requirements Agent    ✓\n🟢 User Stories Agent    ✓\n🟢 Roadmap Agent         ✓\n🟢 Risk Agent            ✓\n🟢 Documentation Agent   ✓\n🟢 Executive Agent       ✓\n")

    # Compile final structured Business Report
    logger.info("Consolidating all generated resources into the final Business Report.")
    report = f"""# SPRINT PILOT OPERATIONS REPORT: {company_name.upper()}
**Industry Sector:** {industry}
**Target Audience:** {target_audience}
**Initial Budget/Funding:** {budget}

---

{exec_summary}

---

{biz_plan}

---

## Software Requirement Specification (SRS)
{user_stories}

---

## Project Roadmap & Timeline
{roadmap}

---

## Strategic Risk Analysis
{risks}

---

{documentation}
"""
    return report
