# MCP Module

Model Context Protocol integration.

## Classes

| Class | Description |
|-------|-------------|
| [MCPClientManager](client.md) | Manage MCP server connections |
| [MCPServerConfig](config.md) | Server configuration |

## Quick Example

```python
from mamba_agents import Agent
from mamba_agents.mcp import MCPClientManager, MCPServerConfig

configs = [
    MCPServerConfig(
        name="filesystem",
        transport="stdio",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/path"],
    ),
]

manager = MCPClientManager(configs)
agent = Agent("gpt-4o", toolsets=manager.as_toolsets())
result = await agent.run("List files")
```

## Imports

```python
from mamba_agents.mcp import MCPClientManager, MCPServerConfig, MCPAuthConfig
```
