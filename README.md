![Cover Banner](assets/cover_page_banner.png)

# sprintpilot-ai

An autonomous business operations assistant powered by the Google Agent Development Kit (ADK) that helps startup founders, ecommerce businesses, and software teams plan, organize, and execute their projects.

## Prerequisites

Before running the project, ensure you have:
*   **Python 3.11+** installed.
*   **uv**: The high-performance Python package installer and manager.
*   **Gemini API Key**: Obtain a free API key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

## Quick Start

```bash
# Clone the repository
git clone <repo-url>
cd sprintpilot-ai

# Set up local configuration
cp .env.example .env   # edit .env and configure your GOOGLE_API_KEY / GEMINI_API_KEY

# Install dependencies
make install

# Launch the local playground
make playground        # opens the interactive developer UI at http://localhost:18081
```

---

## Architecture Diagram

The diagram below outlines the updated pipeline architecture of `sprintpilot-ai` and how requests flow through the application:

```mermaid
graph TD
    User([User Client]) -->|HTTP Requests| FastAPI[FastAPI App / Backend]
    
    subgraph FastAPI Application
        FastAPI -->|Internal Route Dispatch| Adapters[Reasoning Engine Adapter]
        Adapters -->|AdkApp Lifecycle| ADK[AdkApp]
        ADK -->|Generative Model| Model[Gemini LLM Client]
        ADK -->|Root Agent Context| Agent[RootAgent]
    end
    
    subgraph Business Operations Pipeline
        Agent -->|1. Create Outline| BizPlan[generate_business_plan]
        BizPlan -->|2. Derive PRD JSON| PRD[generate_project_requirements]
        PRD -->|3. Calculate Timeline JSON| Roadmap[create_project_roadmap]
        Roadmap -->|4. Assess Registry JSON| Risk[analyze_business_risks]
        Risk -->|5. Compile Markdown Doc| Doc[generate_documentation]
    end

    subgraph Persistent Memory
        Agent <-->|Session History| History[(Conversation Session Storage)]
    end

    subgraph Model Context Protocol (MCP)
        Agent -->|File Access| MCPFilesystem[mcp_read_file / mcp_write_file]
        Agent -->|Issue Tracker| MCPGithub[mcp_create_github_issue]
        Agent -->|Cloud Docs| MCPGoogle[mcp_upload_to_drive / mcp_create_google_doc]
        Agent -->|Scheduling| MCPCalendar[mcp_schedule_event]
    end
```

![Architecture Diagram](assets/architecture_diagram.png)

---

## Model Context Protocol (MCP) Integration

The project includes an extensible Model Context Protocol client manager located at [app/app_utils/mcp_client.py](file:///c:/Users/Anshu%20Gupta/Desktop/adk-workspace/sprintpilot-ai/app/app_utils/mcp_client.py) supporting:
*   **Filesystem:** Reads and writes workspace files (`MCP_FILESYSTEM_ENABLED`).
*   **GitHub:** Integrates with issue trackers (`MCP_GITHUB_ENABLED`).
*   **Google Drive & Google Docs:** Uploads documents and spreadsheets (`MCP_GDRIVE_ENABLED` & `MCP_GDOCS_ENABLED`).
*   **Google Calendar:** Schedules project timeline events (`MCP_GCALENDAR_ENABLED`).

All services are configured dynamically using environment variables, avoiding any hardcoded secrets.

---

## How to Run

You can run the project in two different modes:
*   **Playground Mode:** Run `make playground` to start the local developer playground server. Access the interactive user interface in your browser at [http://localhost:18081/dev-ui/?app=app](http://localhost:18081/dev-ui/?app=app).
*   **Web Server Mode:** Run `make run` to spin up the local FastAPI web server at [http://localhost:8000](http://localhost:8000).

---

## Sample Test Cases

Here are 3 specific test cases you can execute in the local playground:

### 1. End-to-End Business Operations Orchestration
*   **Input:** `"I want to build a software development agency startup named DevSprint in the SaaS industry."`
*   **Expected Behavior:** `RootAgent` identifies this as a fresh startup planning request. It triggers the planning sequence: `generate_business_plan` -> `generate_project_requirements` -> `create_project_roadmap` -> `analyze_business_risks` -> `generate_documentation` and outputs a single consolidated operations report.
*   **Check:** The user sees a markdown report containing Executive Summary, README, SRS, Architecture, API details, and Meeting Notes. In the logs, all 5 tool runs appear in order.

### 2. Context-Aware Requirements Generation (Memory Validation)
*   **Input:** (Direct follow-up to case 1 in same session) `"Now draft user stories for the platform onboarding flow."`
*   **Expected Behavior:** `RootAgent` scans the session conversation history to extract `company_name="DevSprint"` and the SaaS industry requirements. It invokes `generate_user_stories(feature_name="platform onboarding flow", goal="SaaS user onboarding")`.
*   **Check:** The user receives a detailed user stories document without having to re-provide company details or goals.

### 3. Extensible MCP Filesystem Check
*   **Input:** `"Save the generated requirements doc to workspace file requirements.md."`
*   **Expected Behavior:** `RootAgent` triggers the active MCP Filesystem tool `mcp_write_file` with the path `requirements.md` and the document text as content.
*   **Check:** The workspace local filesystem has a new file `requirements.md` created with correct contents.

---

## Troubleshooting

### 1. NameError: name `_default_instrumentor_builder` is not defined
*   **Cause:** The telemetry module is missing the import statement for the internal telemetry builder.
*   **Fix:** Ensure that `_default_instrumentor_builder` is imported from `vertexai.agent_engines.templates.adk` inside the `try` block in [telemetry.py](file:///c:/Users/Anshu%20Gupta/Desktop/adk-workspace/sprintpilot-ai/app/app_utils/telemetry.py#L71).

### 2. ValueError: Cannot encode value: `<fastapi.responses.StreamingResponse object>`
*   **Cause:** Using namespaces like `responses.StreamingResponse` in route type hints causes FastAPI to construct a validation model for it instead of recognizing it as a direct Response subclass.
*   **Fix:** Explicitly import `StreamingResponse` and `JSONResponse` from `fastapi.responses` in [reasoning_engine_adapter.py](file:///c:/Users/Anshu%20Gupta/Desktop/adk-workspace/sprintpilot-ai/app/app_utils/reasoning_engine_adapter.py#L28) and use them directly in type annotations.

### 3. RESOURCE_EXHAUSTED / 429 Too Many Requests
*   **Cause:** Rate limits or quotas for `generativelanguage.googleapis.com` have been exceeded on the free Gemini API tier.
*   **Fix:** Wait approximately 30-60 seconds for the current window to reset, or check billing settings/upgrade your plan in Google AI Studio.

---

## Assets

### Cover Page Banner
![Cover Page Banner](assets/cover_page_banner.png)

### Architecture Workflow Diagram
![Architecture Workflow Diagram](assets/architecture_diagram.png)

---

## Demo Script

A spoken presentation script with visual cues is available at [DEMO_SCRIPT.txt](file:///c:/Users/Anshu%20Gupta/Desktop/adk-workspace/sprintpilot-ai/DEMO_SCRIPT.txt) to guide you through a 3–4 minute walkthrough of the running project.

---

## Push to GitHub

1. Create a new repo at https://github.com/new
   - Name: sprintpilot-ai
   - Visibility: Public or Private
   - Do NOT initialize with README (you already have one)

2. In your terminal, navigate into your project folder:
   cd sprintpilot-ai
   git init
   git add .
   git commit -m "Initial commit: sprintpilot-ai ADK agent"
   git branch -M main
   git remote add origin https://github.com/uicoder1/sprintpilot-ai.git
   git push -u origin main

3. Verify .gitignore includes:
   .env          ← your API key — must NEVER be pushed
   .venv/
   __pycache__/
   *.pyc
   .adk/

⚠ NEVER push .env to GitHub. Your API key will be exposed publicly.
