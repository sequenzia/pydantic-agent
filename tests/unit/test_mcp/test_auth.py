"""Tests for MCP authentication handling."""

from __future__ import annotations

import pytest

from mamba_agents.mcp.auth import build_auth_headers, resolve_auth_key
from mamba_agents.mcp.config import MCPAuthConfig


class TestResolveAuthKey:
    """Tests for resolve_auth_key function."""

    def test_direct_key(self) -> None:
        """Test resolving a direct key value."""
        auth = MCPAuthConfig(key="my-api-key")
        result = resolve_auth_key(auth)
        assert result == "my-api-key"

    def test_key_env_variable(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test resolving key from environment variable via key_env."""
        monkeypatch.setenv("MY_TEST_KEY", "env-api-key")
        auth = MCPAuthConfig(key_env="MY_TEST_KEY")
        result = resolve_auth_key(auth)
        assert result == "env-api-key"

    def test_key_env_variable_not_found(self) -> None:
        """Test error when key_env variable not found."""
        auth = MCPAuthConfig(key_env="NONEXISTENT_VAR_123")
        with pytest.raises(ValueError, match="Environment variable NONEXISTENT_VAR_123 not found"):
            resolve_auth_key(auth)

    def test_key_with_env_var_syntax(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test resolving key with ${VAR_NAME} syntax."""
        monkeypatch.setenv("MY_SECRET", "secret-value")
        auth = MCPAuthConfig(key="${MY_SECRET}")
        result = resolve_auth_key(auth)
        assert result == "secret-value"

    def test_key_with_env_var_syntax_not_found(self) -> None:
        """Test error when ${VAR_NAME} variable not found."""
        auth = MCPAuthConfig(key="${MISSING_VAR_456}")
        with pytest.raises(ValueError, match="Environment variable MISSING_VAR_456 not found"):
            resolve_auth_key(auth)

    def test_no_key_configured(self) -> None:
        """Test that None is returned when no key is configured."""
        auth = MCPAuthConfig()
        result = resolve_auth_key(auth)
        assert result is None

    def test_key_env_takes_precedence(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that key_env takes precedence over key."""
        monkeypatch.setenv("PRIORITY_KEY", "from-env")
        auth = MCPAuthConfig(key_env="PRIORITY_KEY", key="direct-value")
        result = resolve_auth_key(auth)
        assert result == "from-env"


class TestBuildAuthHeaders:
    """Tests for build_auth_headers function."""

    def test_authorization_header_with_bearer_prefix(self) -> None:
        """Test that Bearer prefix is added for Authorization header."""
        auth = MCPAuthConfig(key="my-token")
        headers = build_auth_headers(auth)
        assert headers == {"Authorization": "Bearer my-token"}

    def test_authorization_header_already_has_bearer(self) -> None:
        """Test that Bearer prefix is not duplicated."""
        auth = MCPAuthConfig(key="Bearer existing-token")
        headers = build_auth_headers(auth)
        assert headers == {"Authorization": "Bearer existing-token"}

    def test_custom_header_no_bearer(self) -> None:
        """Test that custom headers don't get Bearer prefix."""
        auth = MCPAuthConfig(key="my-key", header="X-API-Key")
        headers = build_auth_headers(auth)
        assert headers == {"X-API-Key": "my-key"}

    def test_no_key_returns_empty(self) -> None:
        """Test that empty dict is returned when no key."""
        auth = MCPAuthConfig()
        headers = build_auth_headers(auth)
        assert headers == {}

    def test_case_insensitive_authorization_header(self) -> None:
        """Test that authorization header check is case insensitive."""
        auth = MCPAuthConfig(key="my-token", header="AUTHORIZATION")
        headers = build_auth_headers(auth)
        assert headers == {"AUTHORIZATION": "Bearer my-token"}
