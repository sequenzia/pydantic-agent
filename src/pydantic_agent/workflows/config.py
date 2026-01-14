"""Workflow configuration."""

from __future__ import annotations

from pydantic import BaseModel, Field


class WorkflowConfig(BaseModel):
    """Configuration for workflow execution.

    Attributes:
        max_steps: Maximum workflow steps before termination.
        max_iterations: Maximum iterations per step.
        timeout_seconds: Total workflow timeout in seconds (None for unlimited).
        step_timeout_seconds: Per-step timeout in seconds (None for unlimited).
        enable_hooks: Whether to invoke hooks during execution.
        track_state: Whether to track detailed state history.
    """

    max_steps: int = Field(
        default=50,
        gt=0,
        description="Maximum workflow steps before termination",
    )
    max_iterations: int = Field(
        default=10,
        gt=0,
        description="Maximum iterations per step",
    )
    timeout_seconds: float | None = Field(
        default=300.0,
        description="Total workflow timeout in seconds (None for unlimited)",
    )
    step_timeout_seconds: float | None = Field(
        default=30.0,
        description="Per-step timeout in seconds (None for unlimited)",
    )
    enable_hooks: bool = Field(
        default=True,
        description="Whether to invoke hooks during execution",
    )
    track_state: bool = Field(
        default=True,
        description="Whether to track detailed state history",
    )
