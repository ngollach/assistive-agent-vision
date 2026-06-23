from enum import Enum

from pydantic import BaseModel


class MCPPermission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXPORT = "export"


class MCPToolRequest(BaseModel):
    tool_name: str
    permission: MCPPermission
    description: str
    requires_user_confirmation: bool = True


class MCPPolicy:
    """Simple MCP safety policy for future external tool integrations."""

    READ_ONLY_TOOLS = {
        "filesystem_read",
        "google_drive_read",
        "google_docs_read",
    }

    WRITE_TOOLS = {
        "google_drive_write",
        "google_docs_write",
        "google_sheets_write",
    }

    def evaluate(self, request: MCPToolRequest) -> bool:
        """Return True if tool call is allowed without extra confirmation."""

        if request.permission == MCPPermission.READ:
            return request.tool_name in self.READ_ONLY_TOOLS

        if request.permission in {MCPPermission.WRITE, MCPPermission.EXPORT}:
            return False

        return False