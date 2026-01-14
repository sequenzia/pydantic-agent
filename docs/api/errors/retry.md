# Retry Utilities

Retry decorators and utilities.

## Quick Example

```python
from mamba_agents.errors import create_retry_decorator

@create_retry_decorator(max_attempts=3, base_wait=1.0)
async def call_api():
    response = await httpx.get(url)
    return response.json()
```

## Retry Levels

| Level | Max Retries | Base Wait | Description |
|-------|-------------|-----------|-------------|
| 1 | 2 | 1.0s | Conservative |
| 2 | 3 | 1.0s | Balanced (default) |
| 3 | 5 | 0.5s | Aggressive |

## Configuration

```python
from mamba_agents.config import ErrorRecoveryConfig

config = ErrorRecoveryConfig(
    retry_level=2,
    max_retries=3,
    base_wait=1.0,
    max_wait=30.0,
    exponential_base=2.0,
    jitter=True,
)
```

## API Reference

::: mamba_agents.errors.retry.create_retry_decorator
    options:
      show_root_heading: true
      show_source: true
