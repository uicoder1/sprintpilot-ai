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

import app.config
from app.app_utils.mcp_client import MCPClientManager
from app.tools import (
    analyze_business_risks,
    create_executive_summary,
    create_project_roadmap,
    execute_business_planning_workflow,
    generate_business_plan,
    generate_documentation,
    generate_project_requirements,
    generate_user_stories,
)
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

mcp_manager = MCPClientManager()

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=app.config.config.model,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are SprintPilot AI, an Autonomous Business Operations Assistant designed to "
        "help startup founders, ecommerce businesses, and software teams plan, organize, "
        "and execute their projects.\n\n"
        "PERSISTENT MEMORY:\n"
        "You have access to persistent conversation memory. Always review previous conversation turns to locate "
        "any established context, including Business Name, Industry, target customer segments, budget, and project roadmaps.\n\n"
        "WORKFLOW ORCHESTRATION:\n"
        "When the user requests to plan, build, launch, or analyze a business, startup, or product (e.g. 'build an ecommerce storefront' "
        "or 'create a software consultancy startup'), you MUST execute the 'execute_business_planning_workflow' tool. "
        "This tool autonomously manages the sequential execution of: business planning, functional requirements compilation, "
        "user stories formatting, timeline/roadmap estimation, risk registry analysis, markdown documentation synthesis, and executive summaries.\n"
        "Do NOT call these tools step-by-step or ask the user for confirmation after each tool call.\n"
        "If any essential information (business name, industry, target audience, budget) is missing, the tool will notify you. "
        "In that case, ask the user only for those missing details. Once the details are collected, re-run 'execute_business_planning_workflow' "
        "to run the entire pipeline automatically and return the complete, unified Business Report.\n\n"
        "For manual execution or individual queries, you may invoke specific individual tools as needed."
    ),
    tools=[
        generate_business_plan,
        generate_project_requirements,
        generate_user_stories,
        create_project_roadmap,
        generate_documentation,
        analyze_business_risks,
        create_executive_summary,
        execute_business_planning_workflow,
    ] + mcp_manager.get_all_enabled_tools(),
)

app = App(
    root_agent=root_agent,
    name="app",
)
