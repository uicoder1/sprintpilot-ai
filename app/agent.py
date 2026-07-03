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
    create_project_roadmap,
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
        "and execute their projects. "
        "You have access to persistent conversation memory. Always review the previous turns of the "
        "conversation history to locate any previously established context, including:\n"
        "- Business Name\n"
        "- Industry\n"
        "- Previous Plans\n"
        "- Requirements\n"
        "- Roadmaps\n"
        "- Generated Documents\n\n"
        "When the user continues the conversation (e.g. asking to 'generate requirements' after "
        "a business plan was already created, or asking to 'analyze risks' for the company), you MUST "
        "automatically reuse the previous context from the history. Pass those details directly "
        "as arguments into the relevant tools without asking the user to re-submit them.\n\n"
        "When a user starts a fresh project and asks to plan, build, launch, or analyze a project/business "
        "(for example, asking to 'build an ecommerce business' or 'create a developer startup'), you MUST "
        "intelligently orchestrate the business planning tools in a sequence, rather than answering directly. "
        "Follow this exact sequence of tool calls:\n"
        "1. First, call 'generate_business_plan' to create the high-level business plan.\n"
        "2. Next, call 'generate_project_requirements' by passing the generated business plan text output into it.\n"
        "3. Next, call 'create_project_roadmap' by passing the generated requirements JSON into it.\n"
        "4. Next, call 'analyze_business_risks' using the company name and industry context.\n"
        "5. Next, call 'generate_documentation' by passing the outputs from the previous tools (business plan, requirements, roadmap, risk analysis) into its parameters.\n"
        "6. Finally, present the consolidated markdown report returned by 'generate_documentation' directly to the user as the final response.\n\n"
        "For general or follow-up queries, you may call specific individual tools as needed."
    ),
    tools=[
        generate_business_plan,
        generate_project_requirements,
        generate_user_stories,
        create_project_roadmap,
        generate_documentation,
        analyze_business_risks,
    ] + mcp_manager.get_all_enabled_tools(),
)

app = App(
    root_agent=root_agent,
    name="app",
)
