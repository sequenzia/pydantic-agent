"""Tests for WorkflowHooks."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest

from pydantic_agent.workflows import (
    Workflow,
    WorkflowConfig,
    WorkflowHooks,
    WorkflowResult,
    WorkflowState,
    WorkflowStep,
)


class TestWorkflowHooks:
    """Tests for WorkflowHooks class."""

    def test_create_hooks_with_defaults(self) -> None:
        """Test creating hooks with all defaults (None)."""
        hooks: WorkflowHooks[None, str] = WorkflowHooks()

        assert hooks.on_workflow_start is None
        assert hooks.on_workflow_complete is None
        assert hooks.on_workflow_error is None
        assert hooks.on_step_start is None
        assert hooks.on_step_complete is None
        assert hooks.on_step_error is None
        assert hooks.on_iteration_start is None
        assert hooks.on_iteration_complete is None

    def test_create_hooks_with_callbacks(self) -> None:
        """Test creating hooks with callback functions."""
        calls: list[str] = []

        def on_start(state: WorkflowState[None]) -> None:
            calls.append("start")

        def on_complete(result: WorkflowResult[str, None]) -> None:
            calls.append("complete")

        hooks: WorkflowHooks[None, str] = WorkflowHooks(
            on_workflow_start=on_start,
            on_workflow_complete=on_complete,
        )

        assert hooks.on_workflow_start is on_start
        assert hooks.on_workflow_complete is on_complete

    @pytest.mark.asyncio
    async def test_trigger_workflow_start_sync(self) -> None:
        """Test triggering workflow start with sync callback."""
        calls: list[str] = []

        def on_start(state: WorkflowState[None]) -> None:
            calls.append(f"start:{state.current_step}")

        hooks: WorkflowHooks[None, str] = WorkflowHooks(on_workflow_start=on_start)
        state: WorkflowState[None] = WorkflowState()

        await hooks.trigger_workflow_start(state)

        assert calls == ["start:1"]

    @pytest.mark.asyncio
    async def test_trigger_workflow_start_async(self) -> None:
        """Test triggering workflow start with async callback."""
        calls: list[str] = []

        async def on_start(state: WorkflowState[None]) -> None:
            calls.append(f"async_start:{state.current_step}")

        hooks: WorkflowHooks[None, str] = WorkflowHooks(on_workflow_start=on_start)
        state: WorkflowState[None] = WorkflowState()

        await hooks.trigger_workflow_start(state)

        assert calls == ["async_start:1"]

    @pytest.mark.asyncio
    async def test_trigger_workflow_start_none(self) -> None:
        """Test triggering workflow start with no callback (does nothing)."""
        hooks: WorkflowHooks[None, str] = WorkflowHooks()
        state: WorkflowState[None] = WorkflowState()

        # Should not raise
        await hooks.trigger_workflow_start(state)

    @pytest.mark.asyncio
    async def test_trigger_workflow_complete(self) -> None:
        """Test triggering workflow complete."""
        calls: list[str] = []

        def on_complete(result: WorkflowResult[str, None]) -> None:
            calls.append(f"complete:{result.success}")

        hooks: WorkflowHooks[None, str] = WorkflowHooks(on_workflow_complete=on_complete)
        result: WorkflowResult[str, None] = WorkflowResult.ok(
            output="done",
            state=WorkflowState(),
            duration=1.0,
        )

        await hooks.trigger_workflow_complete(result)

        assert calls == ["complete:True"]

    @pytest.mark.asyncio
    async def test_trigger_workflow_error(self) -> None:
        """Test triggering workflow error."""
        calls: list[tuple[str, str]] = []

        def on_error(state: WorkflowState[None], error: Exception) -> None:
            calls.append(("error", str(error)))

        hooks: WorkflowHooks[None, str] = WorkflowHooks(on_workflow_error=on_error)
        state: WorkflowState[None] = WorkflowState()
        error = ValueError("test error")

        await hooks.trigger_workflow_error(state, error)

        assert calls == [("error", "test error")]

    @pytest.mark.asyncio
    async def test_trigger_step_start(self) -> None:
        """Test triggering step start."""
        calls: list[tuple[int, str]] = []

        def on_step_start(state: WorkflowState[None], step_number: int, step_type: str) -> None:
            calls.append((step_number, step_type))

        hooks: WorkflowHooks[None, str] = WorkflowHooks(on_step_start=on_step_start)
        state: WorkflowState[None] = WorkflowState()

        await hooks.trigger_step_start(state, 1, "agent_call")

        assert calls == [(1, "agent_call")]

    @pytest.mark.asyncio
    async def test_trigger_step_complete(self) -> None:
        """Test triggering step complete."""
        calls: list[str] = []

        def on_step_complete(state: WorkflowState[None], step: WorkflowStep[Any]) -> None:
            calls.append(step.description)

        hooks: WorkflowHooks[None, str] = WorkflowHooks(on_step_complete=on_step_complete)
        state: WorkflowState[None] = WorkflowState()
        step: WorkflowStep[str] = WorkflowStep(
            step_number=1,
            step_type="test",
            description="Test step",
            input_data=None,
        )

        await hooks.trigger_step_complete(state, step)

        assert calls == ["Test step"]

    @pytest.mark.asyncio
    async def test_trigger_step_error(self) -> None:
        """Test triggering step error."""
        calls: list[tuple[int, str]] = []

        def on_step_error(
            state: WorkflowState[None], step: WorkflowStep[Any], error: Exception
        ) -> None:
            calls.append((step.step_number, str(error)))

        hooks: WorkflowHooks[None, str] = WorkflowHooks(on_step_error=on_step_error)
        state: WorkflowState[None] = WorkflowState()
        step: WorkflowStep[str] = WorkflowStep(
            step_number=1,
            step_type="test",
            description="Test step",
            input_data=None,
        )
        error = RuntimeError("step failed")

        await hooks.trigger_step_error(state, step, error)

        assert calls == [(1, "step failed")]

    @pytest.mark.asyncio
    async def test_trigger_iteration_start(self) -> None:
        """Test triggering iteration start."""
        calls: list[int] = []

        def on_iteration_start(state: WorkflowState[None], iteration: int) -> None:
            calls.append(iteration)

        hooks: WorkflowHooks[None, str] = WorkflowHooks(on_iteration_start=on_iteration_start)
        state: WorkflowState[None] = WorkflowState()

        await hooks.trigger_iteration_start(state, 1)
        await hooks.trigger_iteration_start(state, 2)

        assert calls == [1, 2]

    @pytest.mark.asyncio
    async def test_trigger_iteration_complete(self) -> None:
        """Test triggering iteration complete."""
        calls: list[int] = []

        def on_iteration_complete(state: WorkflowState[None], iteration: int) -> None:
            calls.append(iteration)

        hooks: WorkflowHooks[None, str] = WorkflowHooks(on_iteration_complete=on_iteration_complete)
        state: WorkflowState[None] = WorkflowState()

        await hooks.trigger_iteration_complete(state, 1)

        assert calls == [1]


class HookedWorkflow(Workflow[None, str, dict[str, Any]]):
    """Workflow implementation for testing hook integration."""

    def __init__(
        self,
        config: WorkflowConfig | None = None,
        hooks: WorkflowHooks[dict[str, Any], str] | None = None,
        should_fail: bool = False,
    ) -> None:
        super().__init__(config, hooks)
        self._should_fail = should_fail

    @property
    def name(self) -> str:
        return "hooked"

    def _create_initial_state(self, prompt: str) -> WorkflowState[dict[str, Any]]:
        return WorkflowState(context={"prompt": prompt})

    async def _execute(
        self,
        prompt: str,
        state: WorkflowState[dict[str, Any]],
        deps: None = None,
    ) -> str:
        if self._should_fail:
            raise ValueError("Workflow failed")

        step = WorkflowStep(
            step_number=state.current_step,
            step_type="process",
            description="Process",
            input_data=prompt,
            output_data="result",
            completed_at=datetime.now(UTC),
        )
        state.add_step(step)
        return "result"


class TestWorkflowHooksIntegration:
    """Integration tests for hooks with workflow execution."""

    @pytest.mark.asyncio
    async def test_hooks_called_on_success(self) -> None:
        """Test that hooks are called during successful workflow."""
        events: list[str] = []

        def on_start(state: WorkflowState[dict[str, Any]]) -> None:
            events.append("start")

        def on_complete(result: WorkflowResult[str, dict[str, Any]]) -> None:
            events.append(f"complete:{result.success}")

        hooks: WorkflowHooks[dict[str, Any], str] = WorkflowHooks(
            on_workflow_start=on_start,
            on_workflow_complete=on_complete,
        )
        workflow = HookedWorkflow(hooks=hooks)
        result = await workflow.run("test")

        assert result.success is True
        assert events == ["start", "complete:True"]

    @pytest.mark.asyncio
    async def test_hooks_called_on_error(self) -> None:
        """Test that error hook is called on workflow failure."""
        events: list[str] = []

        def on_start(state: WorkflowState[dict[str, Any]]) -> None:
            events.append("start")

        def on_error(state: WorkflowState[dict[str, Any]], error: Exception) -> None:
            events.append(f"error:{error!s}")

        hooks: WorkflowHooks[dict[str, Any], str] = WorkflowHooks(
            on_workflow_start=on_start,
            on_workflow_error=on_error,
        )
        workflow = HookedWorkflow(hooks=hooks, should_fail=True)
        result = await workflow.run("test")

        assert result.success is False
        assert events == ["start", "error:Workflow failed"]

    @pytest.mark.asyncio
    async def test_hooks_disabled_via_config(self) -> None:
        """Test that hooks are not called when disabled."""
        events: list[str] = []

        def on_start(state: WorkflowState[dict[str, Any]]) -> None:
            events.append("start")

        def on_complete(result: WorkflowResult[str, dict[str, Any]]) -> None:
            events.append("complete")

        config = WorkflowConfig(enable_hooks=False)
        hooks: WorkflowHooks[dict[str, Any], str] = WorkflowHooks(
            on_workflow_start=on_start,
            on_workflow_complete=on_complete,
        )
        workflow = HookedWorkflow(config=config, hooks=hooks)
        result = await workflow.run("test")

        assert result.success is True
        assert events == []  # No hooks should be called

    @pytest.mark.asyncio
    async def test_async_hooks(self) -> None:
        """Test that async hooks work correctly."""
        events: list[str] = []

        async def on_start(state: WorkflowState[dict[str, Any]]) -> None:
            events.append("async_start")

        async def on_complete(result: WorkflowResult[str, dict[str, Any]]) -> None:
            events.append("async_complete")

        hooks: WorkflowHooks[dict[str, Any], str] = WorkflowHooks(
            on_workflow_start=on_start,
            on_workflow_complete=on_complete,
        )
        workflow = HookedWorkflow(hooks=hooks)
        result = await workflow.run("test")

        assert result.success is True
        assert events == ["async_start", "async_complete"]
