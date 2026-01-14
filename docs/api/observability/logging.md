# Logging

Structured logging utilities.

## Quick Example

```python
from mamba_agents.observability import setup_logging
from mamba_agents.config import LoggingConfig

config = LoggingConfig(
    level="INFO",
    format="json",
    redact_sensitive=True,
)

logger = setup_logging(config)
logger.info("Agent started", model="gpt-4o")
```

## Formats

### Text Format

```
2024-01-15 10:30:00 INFO [agent] Starting agent run
```

### JSON Format

```json
{"timestamp": "2024-01-15T10:30:00", "level": "INFO", "message": "Starting agent run"}
```

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `level` | str | `"INFO"` | Log level |
| `format` | str | `"text"` | Output format |
| `redact_sensitive` | bool | True | Redact secrets |

## API Reference

::: mamba_agents.observability.logging.setup_logging
    options:
      show_root_heading: true

::: mamba_agents.observability.logging.AgentLogger
    options:
      show_root_heading: true
