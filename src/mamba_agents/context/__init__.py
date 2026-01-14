"""Context window management."""

from mamba_agents.context.compaction.base import CompactionResult, CompactionStrategy
from mamba_agents.context.compaction.hybrid import HybridStrategy
from mamba_agents.context.compaction.importance import ImportanceScoringStrategy
from mamba_agents.context.compaction.selective import SelectivePruningStrategy
from mamba_agents.context.compaction.sliding_window import SlidingWindowStrategy
from mamba_agents.context.compaction.summarize import SummarizeOlderStrategy
from mamba_agents.context.config import CompactionConfig
from mamba_agents.context.history import MessageHistory
from mamba_agents.context.manager import ContextManager, ContextState

__all__ = [
    "CompactionConfig",
    "CompactionResult",
    "CompactionStrategy",
    "ContextManager",
    "ContextState",
    "HybridStrategy",
    "ImportanceScoringStrategy",
    "MessageHistory",
    "SelectivePruningStrategy",
    "SlidingWindowStrategy",
    "SummarizeOlderStrategy",
]
