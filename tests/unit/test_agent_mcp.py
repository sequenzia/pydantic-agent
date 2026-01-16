"""Tests for Agent with MCP toolsets integration."""

from __future__ import annotations

from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.test import TestModel

from mamba_agents import Agent
from mamba_agents.mcp import MCPClientManager, MCPServerConfig


class TestAgentToolsetsParameter:
    """Tests for Agent toolsets parameter."""

    def test_agent_accepts_toolsets(self, test_model: TestModel) -> None:
        """Test that Agent accepts toolsets parameter."""
        # Create a simple MCP server (not connected, just instantiated)
        server = MCPServerStdio("echo", args=["hello"])

        # Agent should accept toolsets without error
        agent = Agent(
            test_model,
            toolsets=[server],
            system_prompt="Test agent",
        )
        assert agent is not None

    def test_agent_accepts_both_tools_and_toolsets(self, test_model: TestModel) -> None:
        """Test that Agent can have both tools and toolsets."""

        def my_tool(x: int) -> int:
            return x * 2

        server = MCPServerStdio("echo", args=["hello"])

        agent = Agent(
            test_model,
            tools=[my_tool],
            toolsets=[server],
            system_prompt="Test agent",
        )
        assert agent is not None

    def test_agent_with_mcp_client_manager(self, test_model: TestModel) -> None:
        """Test Agent with MCPClientManager.as_toolsets()."""
        configs = [
            MCPServerConfig(
                name="test-server",
                transport="stdio",
                command="echo",
                args=["hello"],
                tool_prefix="test",
            ),
        ]
        manager = MCPClientManager(configs)
        toolsets = manager.as_toolsets()

        agent = Agent(
            test_model,
            toolsets=toolsets,
            system_prompt="Test agent with MCP",
        )
        assert agent is not None

    def test_agent_from_settings_accepts_toolsets(self, test_model: TestModel) -> None:
        """Test that Agent.from_settings accepts toolsets parameter."""
        from mamba_agents.config.settings import AgentSettings

        settings = AgentSettings()
        server = MCPServerStdio("echo", args=["hello"])

        # Need to use override to inject test model
        agent = Agent.from_settings(
            settings,
            toolsets=[server],
            system_prompt="Test agent",
        )
        assert agent is not None


class TestMCPClientManagerIntegration:
    """Integration tests for MCPClientManager with Agent."""

    def test_multiple_servers_with_prefixes(self, test_model: TestModel) -> None:
        """Test multiple MCP servers with different prefixes."""
        configs = [
            MCPServerConfig(
                name="server1",
                transport="stdio",
                command="cmd1",
                tool_prefix="s1",
            ),
            MCPServerConfig(
                name="server2",
                transport="stdio",
                command="cmd2",
                tool_prefix="s2",
            ),
        ]
        manager = MCPClientManager(configs)
        toolsets = manager.as_toolsets()

        assert len(toolsets) == 2

        agent = Agent(
            test_model,
            toolsets=toolsets,
            system_prompt="Multi-server agent",
        )
        assert agent is not None

    def test_sse_server_with_auth(self, test_model: TestModel) -> None:
        """Test SSE server configuration with authentication."""
        from mamba_agents.mcp import MCPAuthConfig

        configs = [
            MCPServerConfig(
                name="secure-server",
                transport="sse",
                url="http://localhost:8080/sse",
                auth=MCPAuthConfig(key="test-api-key"),
            ),
        ]
        manager = MCPClientManager(configs)
        toolsets = manager.as_toolsets()

        assert len(toolsets) == 1

        agent = Agent(
            test_model,
            toolsets=toolsets,
            system_prompt="Secure agent",
        )
        assert agent is not None
