"""ReAct (Reasoning and Acting) workflow implementation.

This module provides the ReActWorkflow class that implements the ReAct paradigm
for agentic task execution. ReAct interleaves reasoning traces (Thoughts) with
task-specific actions, enabling dynamic reasoning and plan adjustment.

Example:
    >>> from mamba_agents import Agent
    >>> from mamba_agents.workflows.react import ReActWorkflow, ReActConfig
    >>>
    >>> agent = Agent("gpt-4o", tools=[read_file, run_bash])
    >>> workflow = ReActWorkflow(
    ...     agent=agent,
    ...     config=ReActConfig(max_iterations=10),
    ... )
    >>> result = workflow.run_sync("Find the bug in main.py")
    >>> print(result.output)
"""

from mamba_agents.workflows.react.config import ReActConfig
from mamba_agents.workflows.react.hooks import ReActHooks
from mamba_agents.workflows.react.state import ReActState, ScratchpadEntry
from mamba_agents.workflows.react.workflow import ReActWorkflow

__all__ = [
    "ReActConfig",
    "ReActHooks",
    "ReActState",
    "ReActWorkflow",
    "ScratchpadEntry",
]
