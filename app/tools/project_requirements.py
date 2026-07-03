import json
import logging

logger = logging.getLogger(__name__)

def generate_project_requirements(business_plan: str) -> str:
    """Generates structured project requirements from a business plan.

    Args:
        business_plan: The text or content of the business plan.

    Returns:
        A JSON string containing functional requirements, non-functional requirements,
        user personas, user stories, acceptance criteria, and nice to have features.
    """
    logger.info("Extracting and compiling requirements from business plan.")

    # Simple extraction of company name or industry from input to customize output
    company_name = "Target Startup"
    industry = "SaaS"

    try:
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
    except Exception as e:
        logger.error(f"Error compiling requirements: {e}")
        return json.dumps({"error": str(e)}, indent=2)
