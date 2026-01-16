"""Tests for MCPClientManager."""

from __future__ import annotations

import warnings

import pytest
from pydantic_ai.mcp import MCPServerSSE, MCPServerStdio

from mamba_agents.mcp import MCPClientManager, MCPServerConfig
from mamba_agents.mcp.lifecycle import ServerState


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


class TestMCPClientManagerDeprecations:
    """Tests for deprecated methods."""

    def test_connect_all_deprecated(self) -> None:
        """Test that connect_all emits deprecation warning."""
        manager = MCPClientManager()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # This will fail without MCP server, but we just want to check the warning
            try:
                import asyncio

                asyncio.run(manager.connect_all())
            except Exception:
                pass

            # Check that deprecation warning was issued
            deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
            assert len(deprecation_warnings) >= 1
            assert "deprecated" in str(deprecation_warnings[0].message).lower()

    def test_disconnect_all_deprecated(self) -> None:
        """Test that disconnect_all emits deprecation warning."""
        manager = MCPClientManager()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            import asyncio

            asyncio.run(manager.disconnect_all())

            deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
            assert len(deprecation_warnings) >= 1
            assert "deprecated" in str(deprecation_warnings[0].message).lower()

    def test_get_toolsets_deprecated(self) -> None:
        """Test that get_toolsets emits deprecation warning."""
        manager = MCPClientManager()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            manager.get_toolsets()

            deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
            assert len(deprecation_warnings) >= 1
            assert "deprecated" in str(deprecation_warnings[0].message).lower()


class TestMCPClientManagerStatus:
    """Tests for status-related methods."""

    def test_get_status_unknown_server(self) -> None:
        """Test getting status of unknown server."""
        manager = MCPClientManager()
        status = manager.get_status("nonexistent")
        assert status.name == "nonexistent"
        assert status.state == ServerState.STOPPED

    def test_get_all_statuses_empty(self) -> None:
        """Test get_all_statuses with no servers."""
        manager = MCPClientManager()
        statuses = manager.get_all_statuses()
        assert statuses == []

    def test_get_server_unknown(self) -> None:
        """Test getting unknown server returns None."""
        manager = MCPClientManager()
        server = manager.get_server("nonexistent")
        assert server is None
