# ToolRegistry

Registry for organizing and managing tools.

## Quick Example

```python
from mamba_agents.tools import ToolRegistry
from mamba_agents.tools import read_file, write_file

registry = ToolRegistry()

# Register tools
registry.register(read_file)
registry.register(write_file)

# Get all tools
all_tools = registry.get_all()

# Use with agent
from mamba_agents import Agent
agent = Agent("gpt-4o", tools=all_tools)
```

## API Reference

::: mamba_agents.tools.registry.ToolRegistry
    options:
      show_root_heading: true
      show_source: true
