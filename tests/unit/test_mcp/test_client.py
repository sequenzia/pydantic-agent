"""Tests for MCPClientManager."""

from __future__ import annotations

import pytest
from pydantic_ai.mcp import MCPServerSSE, MCPServerStdio

from mamba_agents.mcp import MCPClientManager, MCPServerConfig


class TestMCPClientManager:
    """Tests for MCPClientManager."""

    def test_init_empty(self) -> None:
        """Test initialization with no configs."""
        manager = MCPClientManager()
        assert manager.configs == []

    def test_init_with_configs(self) -> None:
        """Test initialization with configs."""
        configs = [
            MCPServerConfig(name="server1", transport="stdio", command="cmd1"),
            MCPServerConfig(name="server2", transport="stdio", command="cmd2"),
        ]
        manager = MCPClientManager(configs)
        assert len(manager.configs) == 2
        assert manager.configs[0].name == "server1"

    def test_add_server(self) -> None:
        """Test adding a server configuration."""
        manager = MCPClientManager()
        config = MCPServerConfig(name="new-server", transport="stdio", command="cmd")
        manager.add_server(config)
        assert len(manager.configs) == 1
        assert manager.configs[0].name == "new-server"

    def test_configs_returns_copy(self) -> None:
        """Test that configs property returns a copy."""
        configs = [MCPServerConfig(name="server1", command="cmd")]
        manager = MCPClientManager(configs)

        # Modifying returned list shouldn't affect internal state
        returned_configs = manager.configs
        returned_configs.append(MCPServerConfig(name="server2", command="cmd2"))

        assert len(manager.configs) == 1


class TestMCPClientManagerAsToolsets:
    """Tests for as_toolsets() method."""

    def test_as_toolsets_creates_stdio_server(self) -> None:
        """Test that as_toolsets creates MCPServerStdio for stdio transport."""
        configs = [
            MCPServerConfig(
                name="fs",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", "/path"],
            ),
        ]
        manager = MCPClientManager(configs)
        toolsets = manager.as_toolsets()

        assert len(toolsets) == 1
        assert isinstance(toolsets[0], MCPServerStdio)

    def test_as_toolsets_creates_sse_server(self) -> None:
        """Test that as_toolsets creates MCPServerSSE for SSE transport."""
        configs = [
            MCPServerConfig(
                name="web",
                transport="sse",
                url="http://localhost:8080/sse",
            ),
        ]
        manager = MCPClientManager(configs)
        toolsets = manager.as_toolsets()

        assert len(toolsets) == 1
        assert isinstance(toolsets[0], MCPServerSSE)

    def test_as_toolsets_with_tool_prefix(self) -> None:
        """Test that tool_prefix is applied to servers."""
        configs = [
            MCPServerConfig(
                name="fs",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", "/path"],
                tool_prefix="fs",
            ),
        ]
        manager = MCPClientManager(configs)
        toolsets = manager.as_toolsets()

        assert len(toolsets) == 1
        # The tool_prefix is stored internally by pydantic-ai

    def test_as_toolsets_multiple_servers(self) -> None:
        """Test creating multiple servers."""
        configs = [
            MCPServerConfig(name="server1", transport="stdio", command="cmd1"),
            MCPServerConfig(name="server2", transport="sse", url="http://localhost/sse"),
        ]
        manager = MCPClientManager(configs)
        toolsets = manager.as_toolsets()

        assert len(toolsets) == 2
        assert isinstance(toolsets[0], MCPServerStdio)
        assert isinstance(toolsets[1], MCPServerSSE)

    def test_as_toolsets_empty_configs(self) -> None:
        """Test as_toolsets with no configs returns empty list."""
        manager = MCPClientManager()
        toolsets = manager.as_toolsets()
        assert toolsets == []

    def test_as_toolsets_stdio_missing_command(self) -> None:
        """Test that ValueError is raised when stdio config missing command."""
        configs = [MCPServerConfig(name="broken", transport="stdio")]
        manager = MCPClientManager(configs)

        with pytest.raises(ValueError, match="Command required for stdio transport"):
            manager.as_toolsets()

    def test_as_toolsets_sse_missing_url(self) -> None:
        """Test that ValueError is raised when SSE config missing URL."""
        configs = [MCPServerConfig(name="broken", transport="sse")]
        manager = MCPClientManager(configs)

        with pytest.raises(ValueError, match="URL required for SSE transport"):
            manager.as_toolsets()
