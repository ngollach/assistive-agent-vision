from agents.mcp_policy import MCPPermission, MCPPolicy, MCPToolRequest


def test_mcp_policy_allows_known_read_only_tool():
    policy = MCPPolicy()

    request = MCPToolRequest(
        tool_name="google_drive_read",
        permission=MCPPermission.READ,
        description="Read a document summary.",
    )

    assert policy.evaluate(request) is True


def test_mcp_policy_blocks_unknown_read_tool():
    policy = MCPPolicy()

    request = MCPToolRequest(
        tool_name="unknown_read_tool",
        permission=MCPPermission.READ,
        description="Unknown read tool.",
    )

    assert policy.evaluate(request) is False


def test_mcp_policy_blocks_write_tool_without_confirmation():
    policy = MCPPolicy()

    request = MCPToolRequest(
        tool_name="google_docs_write",
        permission=MCPPermission.WRITE,
        description="Write a summary to Google Docs.",
    )

    assert policy.evaluate(request) is False


def test_mcp_policy_blocks_export_tool_without_confirmation():
    policy = MCPPolicy()

    request = MCPToolRequest(
        tool_name="google_drive_write",
        permission=MCPPermission.EXPORT,
        description="Export user data.",
    )

    assert policy.evaluate(request) is False