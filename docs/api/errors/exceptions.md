# Exceptions

Custom exception classes.

## Exception Hierarchy

```
AgentError (base)
├── ConfigurationError
├── ModelBackendError
│   └── RateLimitError
├── ToolExecutionError
├── ContextOverflowError
├── MCPError
├── AuthenticationError
└── TimeoutError
```

## Quick Example

```python
from mamba_agents.errors import (
    AgentError,
    ModelBackendError,
    RateLimitError,
    AuthenticationError,
    ToolExecutionError,
    ContextOverflowError,
)

try:
    result = await agent.run(query)
except RateLimitError as e:
    print(f"Rate limited, retry after: {e.retry_after}s")
except AuthenticationError:
    print("Invalid API key")
except ModelBackendError as e:
    print(f"Model error: {e}")
except ToolExecutionError as e:
    print(f"Tool {e.tool_name} failed: {e}")
except ContextOverflowError as e:
    print(f"Context overflow: {e.current_tokens}/{e.max_tokens} tokens")
except AgentError as e:
    print(f"Agent error: {e}")
```

## API Reference

::: mamba_agents.errors.exceptions.AgentError
    options:
      show_root_heading: true

::: mamba_agents.errors.exceptions.ConfigurationError
    options:
      show_root_heading: true

::: mamba_agents.errors.exceptions.ModelBackendError
    options:
      show_root_heading: true

::: mamba_agents.errors.exceptions.RateLimitError
    options:
      show_root_heading: true

::: mamba_agents.errors.exceptions.AuthenticationError
    options:
      show_root_heading: true

::: mamba_agents.errors.exceptions.ToolExecutionError
    options:
      show_root_heading: true

::: mamba_agents.errors.exceptions.ContextOverflowError
    options:
      show_root_heading: true

::: mamba_agents.errors.exceptions.MCPError
    options:
      show_root_heading: true

::: mamba_agents.errors.exceptions.TimeoutError
    options:
      show_root_heading: true
