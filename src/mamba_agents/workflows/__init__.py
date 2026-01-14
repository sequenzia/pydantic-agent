"""Agentic workflow orchestration.

Workflows provide structured execution patterns that orchestrate Agent instances
through multi-step reasoning, planning, and reflection patterns.

Example:
    >>> from mamba_agents import Agent
    >>> from mamba_agents.workflows import Workflow, WorkflowConfig, WorkflowHooks
    >>>
    >>> # Create a custom workflow by extending Workflow
    >>> class MyWorkflow(Workflow[None, str, dict]):
    ...     @property
    ...     def name(self) -> str:
    ...         return "my_workflow"
    ...
    ...     def _create_initial_state(self, prompt: str) -> WorkflowState[dict]:
    ...         return WorkflowState(context={"prompt": prompt})
    ...
    ...     async def _execute(self, prompt, state, deps):
    ...         # Implement workflow logic
    ...         return "result"

ReAct Workflow Example:
    >>> from mamba_agents import Agent
    >>> from mamba_agents.workflows import ReActWorkflow, ReActConfig
    >>>
    >>> agent = Agent("gpt-4o", tools=[read_file, run_bash])
    >>> workflow = ReActWorkflow(agent, config=ReActConfig(max_iterations=10))
    >>> result = workflow.run_sync("Find the bug in main.py")
    >>> print(result.output)
"""

from mamba_agents.workflows.base import (
    Workflow,
    WorkflowResult,
    WorkflowState,
    WorkflowStep,
)
from mamba_agents.workflows.config import WorkflowConfig
from mamba_agents.workflows.errors import (
    WorkflowError,
    WorkflowExecutionError,
    WorkflowMaxIterationsError,
    WorkflowMaxStepsError,
    WorkflowTimeoutError,
)
from mamba_agents.workflows.hooks import WorkflowHooks
from mamba_agents.workflows.react import (
    ReActConfig,
    ReActHooks,
    ReActState,
    ReActWorkflow,
    ScratchpadEntry,
)

__all__ = [
    "ReActConfig",
    "ReActHooks",
    "ReActState",
    "ReActWorkflow",
    "ScratchpadEntry",
    "Workflow",
    "WorkflowConfig",
    "WorkflowError",
    "WorkflowExecutionError",
    "WorkflowHooks",
    "WorkflowMaxIterationsError",
    "WorkflowMaxStepsError",
    "WorkflowResult",
    "WorkflowState",
    "WorkflowStep",
    "WorkflowTimeoutError",
]
