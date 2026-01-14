# Context Module

Context window management and compaction.

## Classes

| Class | Description |
|-------|-------------|
| [ContextManager](manager.md) | Manages conversation context |
| [CompactionConfig](config.md) | Compaction configuration |
| [Compaction Strategies](strategies.md) | 5 compaction strategies |

## Quick Example

```python
from mamba_agents.context import ContextManager, CompactionConfig

config = CompactionConfig(
    strategy="hybrid",
    trigger_threshold_tokens=100000,
    target_tokens=80000,
)

manager = ContextManager(config=config)
manager.add_messages([{"role": "user", "content": "Hello"}])

if manager.should_compact():
    result = await manager.compact()
```

## Imports

```python
from mamba_agents import CompactionConfig, ContextState
from mamba_agents.context import ContextManager, CompactionConfig
```
