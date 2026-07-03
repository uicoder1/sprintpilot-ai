import logging
import os
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

class MCPClientManager:
    """Manages the connection configuration and tools registration for Model Context Protocol (MCP) servers.

    Supports:
    - Filesystem (Local workspace file reading/writing)
    - GitHub (Repo commits, issues, PRs)
    - Google Drive (File storage and retrieval)
    - Google Docs (Document editing and creation)
    - Google Calendar (Scheduling events and checkpoints)
    """

    def __init__(self):
        # Read server configurations from environment variables
        self.configs = {
            "filesystem": {
                "enabled": os.getenv("MCP_FILESYSTEM_ENABLED", "false").lower() == "true",
                "workspace": os.getenv("MCP_FILESYSTEM_WORKSPACE", "."),
            },
            "github": {
                "enabled": os.getenv("MCP_GITHUB_ENABLED", "false").lower() == "true",
                "token": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", ""),
                "repo": os.getenv("GITHUB_REPOSITORY", ""),
            },
            "google_drive": {
                "enabled": os.getenv("MCP_GDRIVE_ENABLED", "false").lower() == "true",
                "credentials_json": os.getenv("GDRIVE_CREDENTIALS_JSON", ""),
            },
            "google_docs": {
                "enabled": os.getenv("MCP_GDOCS_ENABLED", "false").lower() == "true",
                "credentials_json": os.getenv("GDOCS_CREDENTIALS_JSON", ""),
            },
            "calendar": {
                "enabled": os.getenv("MCP_GCALENDAR_ENABLED", "false").lower() == "true",
                "credentials_json": os.getenv("GCALENDAR_CREDENTIALS_JSON", ""),
            }
        }
        self.active_connections = {}

    def get_filesystem_tools(self) -> list[Callable[..., Any]]:
        """Mocks or initializes tools for Filesystem MCP server."""
        if not self.configs["filesystem"]["enabled"]:
            return []

        workspace_dir = self.configs["filesystem"]["workspace"]
        logger.info(f"Configuring Filesystem MCP toolset rooted at: {workspace_dir}")

        def mcp_read_file(file_path: str) -> str:
            """MCP Filesystem Tool: Reads a file from the configured workspace.

            Args:
                file_path: Relative path to the file inside the workspace.
            """
            target = os.path.abspath(os.path.join(workspace_dir, file_path))
            if not target.startswith(os.path.abspath(workspace_dir)):
                return "Error: Security violation - Path is outside workspace bounds."
            try:
                with open(target, encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file: {e}"

        def mcp_write_file(file_path: str, content: str) -> str:
            """MCP Filesystem Tool: Writes content to a file in the configured workspace.

            Args:
                file_path: Relative path to the target file.
                content: Text content to write.
            """
            target = os.path.abspath(os.path.join(workspace_dir, file_path))
            if not target.startswith(os.path.abspath(workspace_dir)):
                return "Error: Security violation - Path is outside workspace bounds."
            try:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, "w", encoding="utf-8") as f:
                    f.write(content)
                return f"Successfully wrote to {file_path}."
            except Exception as e:
                return f"Error writing file: {e}"

        return [mcp_read_file, mcp_write_file]

    def get_github_tools(self) -> list[Callable[..., Any]]:
        """Mocks or initializes tools for GitHub MCP server."""
        if not self.configs["github"]["enabled"]:
            return []

        repo = self.configs["github"]["repo"]
        token = self.configs["github"]["token"]
        logger.info(f"Configuring GitHub MCP toolset targeting repo: {repo}")

        def mcp_create_github_issue(title: str, body: str) -> str:
            """MCP GitHub Tool: Creates a new issue in the target repository.

            Args:
                title: Title of the issue.
                body: Detailed description body.
            """
            if not token:
                return "Error: GitHub Personal Access Token (GITHUB_PERSONAL_ACCESS_TOKEN) is not configured."
            # Simulated API action
            return f"Simulated: Created GitHub Issue in {repo} - Title: '{title}'"

        return [mcp_create_github_issue]

    def get_google_drive_tools(self) -> list[Callable[..., Any]]:
        """Mocks or initializes tools for Google Drive MCP server."""
        if not self.configs["google_drive"]["enabled"]:
            return []

        logger.info("Configuring Google Drive MCP toolset")

        def mcp_upload_to_drive(file_name: str, folder_id: str = "") -> str:
            """MCP Google Drive Tool: Uploads a file to Google Drive.

            Args:
                file_name: Target name of the file in Drive.
                folder_id: Optional ID of the parent folder.
            """
            if not self.configs["google_drive"]["credentials_json"]:
                return "Error: Google Drive credentials not configured."
            return f"Simulated: Uploaded '{file_name}' to Google Drive folder '{folder_id}'."

        return [mcp_upload_to_drive]

    def get_google_docs_tools(self) -> list[Callable[..., Any]]:
        """Mocks or initializes tools for Google Docs MCP server."""
        if not self.configs["google_docs"]["enabled"]:
            return []

        logger.info("Configuring Google Docs MCP toolset")

        def mcp_create_google_doc(doc_title: str, text_content: str) -> str:
            """MCP Google Docs Tool: Creates a new document in Google Docs.

            Args:
                doc_title: Title of the new Google Doc.
                text_content: Document content.
            """
            if not self.configs["google_docs"]["credentials_json"]:
                return "Error: Google Docs credentials not configured."
            return f"Simulated: Created Google Doc '{doc_title}'."

        return [mcp_create_google_doc]

    def get_calendar_tools(self) -> list[Callable[..., Any]]:
        """Mocks or initializes tools for Google Calendar MCP server."""
        if not self.configs["calendar"]["enabled"]:
            return []

        logger.info("Configuring Google Calendar MCP toolset")

        def mcp_schedule_event(summary: str, start_time: str, end_time: str) -> str:
            """MCP Google Calendar Tool: Schedules a new event in the Google Calendar.

            Args:
                summary: Event title / summary.
                start_time: ISO-8601 formatted start time (e.g. '2026-07-03T18:00:00Z').
                end_time: ISO-8601 formatted end time.
            """
            if not self.configs["calendar"]["credentials_json"]:
                return "Error: Google Calendar credentials not configured."
            return f"Simulated: Scheduled event '{summary}' from {start_time} to {end_time}."

        return [mcp_schedule_event]

    def get_all_enabled_tools(self) -> list[Callable[..., Any]]:
        """Consolidates and returns all active MCP server tools."""
        tools = []
        tools.extend(self.get_filesystem_tools())
        tools.extend(self.get_github_tools())
        tools.extend(self.get_google_drive_tools())
        tools.extend(self.get_google_docs_tools())
        tools.extend(self.get_calendar_tools())
        return tools
