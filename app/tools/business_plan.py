import logging

logger = logging.getLogger(__name__)

def generate_business_plan(company_name: str, industry: str, target_audience: str) -> str:
    """Generates a structured business plan outline for a startup or business.

    Args:
        company_name: The name of the company/startup.
        industry: The industry the business operates in.
        target_audience: The main target customer segment.

    Returns:
        A markdown-formatted string containing the structured business plan outline.
    """
    logger.info(f"Generating business plan for {company_name} in the {industry} industry.")
    try:
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
    except Exception as e:
        logger.error(f"Error generating business plan: {e}")
        return f"# Business Plan: {company_name}\nError generating content: {e}"
