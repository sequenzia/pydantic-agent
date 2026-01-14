"""Workflow-specific exceptions."""

from __future__ import annotations


class WorkflowError(Exception):
    """Base exception for workflow errors."""

    pass


class WorkflowTimeoutError(WorkflowError):
    """Raised when workflow exceeds timeout."""

    pass


class WorkflowMaxStepsError(WorkflowError):
    """Raised when workflow exceeds max steps."""

    pass


class WorkflowMaxIterationsError(WorkflowError):
    """Raised when workflow exceeds max iterations."""

    pass


class WorkflowExecutionError(WorkflowError):
    """Raised when workflow execution fails."""

    pass
