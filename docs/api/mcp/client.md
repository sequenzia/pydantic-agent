# MCPClientManager

Manage MCP server connections.

## Quick Example

```python
from mamba_agents.mcp import MCPClientManager, MCPServerConfig

manager = MCPClientManager()

# Add server
manager.add_server(MCPServerConfig(
    name="server1",
    transport="stdio",
    command="my-server",
))

# Get toolsets for agent
toolsets = manager.as_toolsets()
```

## With Agent

```python
from mamba_agents import Agent
from mamba_agents.mcp import MCPClientManager, MCPServerConfig

configs = [
    MCPServerConfig(
        name="filesystem",
        transport="stdio",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/project"],
    ),
]

manager = MCPClientManager(configs)
agent = Agent("gpt-4o", toolsets=manager.as_toolsets())
result = await agent.run("List project files")
```

## API Reference

::: mamba_agents.mcp.client.MCPClientManager
    options:
      show_root_heading: true
      show_source: true
