"""Agentic workflow orchestration.

Workflows provide structured execution patterns that orchestrate Agent instances
through multi-step reasoning, planning, and reflection patterns.

Example:
    >>> from pydantic_agent import Agent
    >>> from pydantic_agent.workflows import Workflow, WorkflowConfig, WorkflowHooks
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
"""

from pydantic_agent.workflows.base import (
    Workflow,
    WorkflowResult,
    WorkflowState,
    WorkflowStep,
)
from pydantic_agent.workflows.config import WorkflowConfig
from pydantic_agent.workflows.errors import (
    WorkflowError,
    WorkflowExecutionError,
    WorkflowMaxIterationsError,
    WorkflowMaxStepsError,
    WorkflowTimeoutError,
)
from pydantic_agent.workflows.hooks import WorkflowHooks

__all__ = [
    # Base abstractions
    "Workflow",
    "WorkflowConfig",
    "WorkflowHooks",
    # Results and state
    "WorkflowResult",
    "WorkflowState",
    "WorkflowStep",
    # Errors
    "WorkflowError",
    "WorkflowExecutionError",
    "WorkflowMaxIterationsError",
    "WorkflowMaxStepsError",
    "WorkflowTimeoutError",
]
