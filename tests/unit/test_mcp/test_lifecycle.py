"""Tests for MCP server lifecycle management."""

from __future__ import annotations

import pytest

from mamba_agents.mcp.config import MCPServerConfig
from mamba_agents.mcp.lifecycle import ServerLifecycleManager, ServerState, ServerStatus


class TestServerState:
    """Tests for ServerState enum."""

    def test_all_states_exist(self) -> None:
        """Test that all expected states exist."""
        assert ServerState.STOPPED.value == "stopped"
        assert ServerState.STARTING.value == "starting"
        assert ServerState.RUNNING.value == "running"
        assert ServerState.ERROR.value == "error"
        assert ServerState.STOPPING.value == "stopping"


class TestServerStatus:
    """Tests for ServerStatus dataclass."""

    def test_basic_status(self) -> None:
        """Test creating basic status."""
        status = ServerStatus(name="test", state=ServerState.RUNNING)
        assert status.name == "test"
        assert status.state == ServerState.RUNNING
        assert status.error is None
        assert status.tools == []

    def test_status_with_error(self) -> None:
        """Test creating status with error."""
        status = ServerStatus(
            name="broken",
            state=ServerState.ERROR,
            error="Connection failed",
        )
        assert status.error == "Connection failed"

    def test_status_with_tools(self) -> None:
        """Test creating status with tools."""
        status = ServerStatus(
            name="server",
            state=ServerState.RUNNING,
            tools=["read_file", "write_file"],
        )
        assert status.tools == ["read_file", "write_file"]


class TestServerLifecycleManager:
    """Tests for ServerLifecycleManager."""

    def test_init(self) -> None:
        """Test initialization."""
        manager = ServerLifecycleManager()
        assert manager.get_all_servers() == []
        assert manager.get_all_statuses() == []

    def test_get_status_unknown_server(self) -> None:
        """Test getting status of unknown server."""
        manager = ServerLifecycleManager()
        status = manager.get_status("unknown")
        assert status.name == "unknown"
        assert status.state == ServerState.STOPPED

    def test_get_server_unknown(self) -> None:
        """Test getting unknown server returns None."""
        manager = ServerLifecycleManager()
        server = manager.get_server("unknown")
        assert server is None

    def test_invalid_transport_rejected_by_pydantic(self) -> None:
        """Test that invalid transport is rejected by pydantic validation."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError, match="Input should be 'stdio' or 'sse'"):
            MCPServerConfig(
                name="test",
                transport="invalid",  # type: ignore[arg-type]
                command="cmd",
            )

    @pytest.mark.asyncio
    async def test_start_server_stdio_missing_command(self) -> None:
        """Test that stdio without command raises ValueError."""
        manager = ServerLifecycleManager()
        config = MCPServerConfig(name="test", transport="stdio")
        with pytest.raises(ValueError, match="Command required for stdio transport"):
            await manager.start_server(config)

    @pytest.mark.asyncio
    async def test_start_server_sse_missing_url(self) -> None:
        """Test that SSE without URL raises ValueError."""
        manager = ServerLifecycleManager()
        config = MCPServerConfig(name="test", transport="sse")
        with pytest.raises(ValueError, match="URL required for SSE transport"):
            await manager.start_server(config)

    @pytest.mark.asyncio
    async def test_stop_unknown_server(self) -> None:
        """Test stopping unknown server does nothing."""
        manager = ServerLifecycleManager()
        # Should not raise
        await manager.stop_server("unknown")

    @pytest.mark.asyncio
    async def test_stop_all_empty(self) -> None:
        """Test stop_all with no servers does nothing."""
        manager = ServerLifecycleManager()
        # Should not raise
        await manager.stop_all()
