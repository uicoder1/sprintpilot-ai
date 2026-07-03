import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()
if "GOOGLE_API_KEY" in os.environ and "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")  # Gemini API key only
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "test-project")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")

try:
    import google.auth
    google.auth.default()
except Exception:
    try:
        import google.auth
        from google.auth.credentials import AnonymousCredentials
        def mock_default(*args, **kwargs):
            return AnonymousCredentials(), os.environ.get("GOOGLE_CLOUD_PROJECT", "test-project")
        google.auth.default = mock_default
    except Exception:
        pass

try:
    import vertexai
    vertexai.init(
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ["GOOGLE_CLOUD_LOCATION"],
    )
except Exception:
    pass

@dataclass
class AgentConfig:
    # Reads model from environment GEMINI_MODEL. Default gemini-2.5-flash (the 1.5 family is retired and returns 404). Use gemini-2.5-flash-lite for tighter free-tier quota.
    model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    mcp_server_port: int = 8090
    max_iterations: int = 3
    pii_redaction_enabled: bool = True
    injection_detection_enabled: bool = True

config = AgentConfig()
