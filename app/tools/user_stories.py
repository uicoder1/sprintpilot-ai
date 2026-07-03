import logging

logger = logging.getLogger(__name__)

def generate_user_stories(feature_name: str, goal: str) -> str:
    """Generates Agile user stories with acceptance criteria for a given feature.

    Args:
        feature_name: The name of the feature or epic.
        goal: The user objective or business goal of the feature.

    Returns:
        A formatted string listing the user stories and their acceptance criteria.
    """
    logger.info(f"Generating Agile user stories for feature '{feature_name}' with goal '{goal}'.")
    try:
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
    except Exception as e:
        logger.error(f"Error generating user stories: {e}")
        return f"# Agile User Stories for: {feature_name}\nError generating content: {e}"
