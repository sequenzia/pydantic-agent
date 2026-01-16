# MCP Integration

Mamba Agents supports the Model Context Protocol (MCP) for connecting to external tool servers.

## Overview

MCP allows your agent to use tools provided by external servers:

- **Stdio transport** - Run MCP servers as subprocesses
- **SSE transport** - Connect to HTTP-based MCP servers
- **Authentication** - API key support for secure servers
- **Tool prefixing** - Avoid name conflicts between servers

## Quick Start

```python
from mamba_agents import Agent
from mamba_agents.mcp import MCPServerConfig, MCPClientManager

# Configure MCP servers
configs = [
    MCPServerConfig(
        name="filesystem",
        transport="stdio",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/project"],
        tool_prefix="fs",  # Tools become: fs_read, fs_write, etc.
    ),
]

# Create manager and get toolsets
manager = MCPClientManager(configs)

# Pass toolsets to Agent (pydantic-ai handles server lifecycle)
agent = Agent("gpt-4o", toolsets=manager.as_toolsets())

# Use the agent - MCP servers connect automatically
result = await agent.run("List files in the project")
```

## Transport Types

### Stdio Transport

Run MCP servers as subprocesses:

```python
MCPServerConfig(
    name="filesystem",
    transport="stdio",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/path"],
)

# Or with a local command
MCPServerConfig(
    name="custom",
    transport="stdio",
    command="python",
    args=["-m", "my_mcp_server"],
)
```

### SSE Transport

Connect to HTTP-based servers:

```python
MCPServerConfig(
    name="web-tools",
    transport="sse",
    url="http://localhost:8080/sse",
)
```

## Authentication

### API Key Authentication

```python
from mamba_agents.mcp import MCPServerConfig, MCPAuthConfig

MCPServerConfig(
    name="secure-server",
    transport="sse",
    url="https://api.example.com/mcp",
    auth=MCPAuthConfig(
        type="api_key",
        key="my-api-key",  # Direct key
        header="Authorization",  # Header name (default)
    ),
)
```

### Using Environment Variables

```python
MCPAuthConfig(
    type="api_key",
    key_env="MY_API_KEY",  # Read from env var
)

# Or with ${} syntax
MCPAuthConfig(
    type="api_key",
    key="${MY_API_KEY}",  # Expanded at runtime
)
```

## MCPClientManager

### Recommended Usage

```python
from mamba_agents import Agent
from mamba_agents.mcp import MCPClientManager, MCPServerConfig

# Configure servers
configs = [
    MCPServerConfig(
        name="filesystem",
        transport="stdio",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/project"],
    ),
]

# Create manager
manager = MCPClientManager(configs)

# Get toolsets and pass to Agent
agent = Agent("gpt-4o", toolsets=manager.as_toolsets())

# pydantic-ai handles MCP server lifecycle automatically
result = await agent.run("Use the MCP tools")
```

### Adding Servers Dynamically

```python
manager = MCPClientManager()

# Add servers one by one
manager.add_server(MCPServerConfig(
    name="server1",
    transport="stdio",
    command="my-server",
))

manager.add_server(MCPServerConfig(
    name="server2",
    transport="sse",
    url="http://localhost:8080/sse",
))

# Get all toolsets
toolsets = manager.as_toolsets()
agent = Agent("gpt-4o", toolsets=toolsets)
```

### Server Status

```python
from mamba_agents.mcp.lifecycle import ServerState

# Check individual server status
status = manager.get_status("filesystem")
print(f"State: {status.state}")  # ServerState.STOPPED, RUNNING, ERROR, etc.
print(f"Error: {status.error}")  # Error message if state is ERROR

# Check all servers
for status in manager.get_all_statuses():
    print(f"{status.name}: {status.state.value}")
```

## Tool Prefixing

Avoid name conflicts with tool prefixes:

```python
MCPServerConfig(
    name="server1",
    transport="stdio",
    command="server1",
    tool_prefix="s1",  # Tools become: s1_read, s1_write, etc.
)

MCPServerConfig(
    name="server2",
    transport="stdio",
    command="server2",
    tool_prefix="s2",  # Tools become: s2_read, s2_write, etc.
)
```

## Common MCP Servers

### Filesystem Server

```python
MCPServerConfig(
    name="filesystem",
    transport="stdio",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
    tool_prefix="fs",
)
```

### GitHub Server

```python
MCPServerConfig(
    name="github",
    transport="stdio",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    auth=MCPAuthConfig(
        type="api_key",
        key_env="GITHUB_TOKEN",
    ),
    tool_prefix="gh",
)
```

### Brave Search Server

```python
MCPServerConfig(
    name="search",
    transport="stdio",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-brave-search"],
    auth=MCPAuthConfig(
        type="api_key",
        key_env="BRAVE_API_KEY",
    ),
    tool_prefix="search",
)
```

## Configuration Reference

### MCPServerConfig

| Option | Type | Description |
|--------|------|-------------|
| `name` | str | Unique server identifier |
| `transport` | str | `"stdio"` or `"sse"` |
| `command` | str | Command to run (stdio only) |
| `args` | list | Command arguments (stdio only) |
| `url` | str | Server URL (SSE only) |
| `auth` | MCPAuthConfig | Authentication config |
| `tool_prefix` | str | Prefix for tool names |

### MCPAuthConfig

| Option | Type | Description |
|--------|------|-------------|
| `type` | str | Auth type (`"api_key"`) |
| `key` | str | Direct API key |
| `key_env` | str | Environment variable name |
| `header` | str | HTTP header (default: `"Authorization"`) |

## Error Handling

```python
from mamba_agents import Agent
from mamba_agents.mcp import MCPClientManager, MCPServerConfig

configs = [
    MCPServerConfig(
        name="my-server",
        transport="stdio",
        command="my-mcp-server",
    ),
]

try:
    manager = MCPClientManager(configs)
    toolsets = manager.as_toolsets()
    agent = Agent("gpt-4o", toolsets=toolsets)
    result = await agent.run("Use the tools")
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Runtime error: {e}")
```

## Best Practices

### 1. Use `as_toolsets()` (Recommended)

```python
# Good - pydantic-ai handles lifecycle
manager = MCPClientManager(configs)
agent = Agent("gpt-4o", toolsets=manager.as_toolsets())
result = await agent.run("Use tools")
```

### 2. Use Tool Prefixes

```python
# Prevent name conflicts between servers
server1 = MCPServerConfig(name="s1", tool_prefix="s1", ...)
server2 = MCPServerConfig(name="s2", tool_prefix="s2", ...)
```

### 3. Use Environment Variables for Secrets

```python
# Don't hardcode API keys
auth = MCPAuthConfig(key_env="MY_API_KEY")  # Good
auth = MCPAuthConfig(key="sk-...")  # Avoid in production
```

### 4. Validate Configurations Early

```python
# Check for configuration errors before runtime
manager = MCPClientManager(configs)
try:
    toolsets = manager.as_toolsets()
except ValueError as e:
    print(f"Invalid config: {e}")
```

## Migration from Deprecated API

If you're using the deprecated async context manager pattern:

```python
# Old (deprecated)
async with MCPClientManager(configs) as manager:
    toolsets = manager.get_toolsets()
    agent = Agent("gpt-4o", tools=toolsets)  # Wrong parameter!
    ...

# New (recommended)
manager = MCPClientManager(configs)
agent = Agent("gpt-4o", toolsets=manager.as_toolsets())  # Correct!
result = await agent.run("Use the tools")
```

## Next Steps

- [Model Backends](model-backends.md) - Connect to local models
- [MCPClientManager API](../api/mcp/client.md) - Full reference
- [MCPServerConfig API](../api/mcp/config.md) - Configuration reference
