"""Tests for workflow base classes."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest

from mamba_agents.workflows import (
    Workflow,
    WorkflowConfig,
    WorkflowHooks,
    WorkflowResult,
    WorkflowState,
    WorkflowStep,
)


class TestWorkflowStep:
    """Tests for WorkflowStep dataclass."""

    def test_create_step(self) -> None:
        """Test creating a workflow step."""
        step = WorkflowStep(
            step_number=1,
            step_type="agent_call",
            description="Call the agent",
            input_data="test input",
        )

        assert step.step_number == 1
        assert step.step_type == "agent_call"
        assert step.description == "Call the agent"
        assert step.input_data == "test input"
        assert step.output_data is None
        assert step.agent_result is None
        assert step.error is None
        assert step.completed_at is None
        assert isinstance(step.started_at, datetime)
        assert step.metadata == {}

    def test_step_duration_none_when_not_completed(self) -> None:
        """Test duration is None when step not completed."""
        step = WorkflowStep(
            step_number=1,
            step_type="test",
            description="Test step",
            input_data=None,
        )

        assert step.duration_seconds is None

    def test_step_duration_calculated(self) -> None:
        """Test duration calculation when completed."""
        started = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        completed = datetime(2024, 1, 1, 12, 0, 5, tzinfo=UTC)

        step = WorkflowStep(
            step_number=1,
            step_type="test",
            description="Test step",
            input_data=None,
            started_at=started,
            completed_at=completed,
        )

        assert step.duration_seconds == 5.0

    def test_step_success_true_when_completed(self) -> None:
        """Test success is True when completed without error."""
        step = WorkflowStep(
            step_number=1,
            step_type="test",
            description="Test step",
            input_data=None,
            output_data="result",
            completed_at=datetime.now(UTC),
        )

        assert step.success is True

    def test_step_success_false_when_error(self) -> None:
        """Test success is False when error exists."""
        step = WorkflowStep(
            step_number=1,
            step_type="test",
            description="Test step",
            input_data=None,
            error="Something went wrong",
            completed_at=datetime.now(UTC),
        )

        assert step.success is False

    def test_step_success_false_when_not_completed(self) -> None:
        """Test success is False when not completed."""
        step = WorkflowStep(
            step_number=1,
            step_type="test",
            description="Test step",
            input_data=None,
        )

        assert step.success is False


class TestWorkflowState:
    """Tests for WorkflowState dataclass."""

    def test_create_state(self) -> None:
        """Test creating workflow state."""
        state: WorkflowState[dict[str, Any]] = WorkflowState()

        assert state.current_step == 1
        assert state.total_steps == 0
        assert state.iteration_count == 0
        assert state.is_complete is False
        assert state.is_failed is False
        assert state.steps == []
        assert state.context is None
        assert state.metadata == {}

    def test_state_with_context(self) -> None:
        """Test state with custom context type."""
        context = {"key": "value", "count": 42}
        state: WorkflowState[dict[str, Any]] = WorkflowState(context=context)

        assert state.context == {"key": "value", "count": 42}

    def test_add_step(self) -> None:
        """Test adding steps to state."""
        state: WorkflowState[None] = WorkflowState()

        step1 = WorkflowStep(
            step_number=1,
            step_type="test",
            description="First step",
            input_data=None,
        )
        state.add_step(step1)

        assert state.total_steps == 1
        assert state.current_step == 2
        assert len(state.steps) == 1
        assert state.steps[0] == step1

        step2 = WorkflowStep(
            step_number=2,
            step_type="test",
            description="Second step",
            input_data=None,
        )
        state.add_step(step2)

        assert state.total_steps == 2
        assert state.current_step == 3
        assert len(state.steps) == 2

    def test_get_latest_step(self) -> None:
        """Test getting the latest step."""
        state: WorkflowState[None] = WorkflowState()

        assert state.get_latest_step() is None

        step = WorkflowStep(
            step_number=1,
            step_type="test",
            description="A step",
            input_data=None,
        )
        state.add_step(step)

        assert state.get_latest_step() == step

    def test_get_step_by_number(self) -> None:
        """Test getting step by number (1-indexed)."""
        state: WorkflowState[None] = WorkflowState()

        step1 = WorkflowStep(
            step_number=1,
            step_type="test",
            description="First",
            input_data=None,
        )
        step2 = WorkflowStep(
            step_number=2,
            step_type="test",
            description="Second",
            input_data=None,
        )

        state.add_step(step1)
        state.add_step(step2)

        assert state.get_step(1) == step1
        assert state.get_step(2) == step2
        assert state.get_step(0) is None
        assert state.get_step(3) is None
        assert state.get_step(-1) is None


class TestWorkflowResult:
    """Tests for WorkflowResult dataclass."""

    def test_ok_factory(self) -> None:
        """Test creating successful result with ok()."""
        state: WorkflowState[None] = WorkflowState()
        state.add_step(
            WorkflowStep(
                step_number=1,
                step_type="test",
                description="Test",
                input_data=None,
            )
        )
        state.iteration_count = 3

        result = WorkflowResult.ok(
            output="success",
            state=state,
            duration=1.5,
            reason="completed",
        )

        assert result.success is True
        assert result.output == "success"
        assert result.state == state
        assert result.error is None
        assert result.total_steps == 1
        assert result.total_iterations == 3
        assert result.duration_seconds == 1.5
        assert result.termination_reason == "completed"

    def test_fail_factory(self) -> None:
        """Test creating failed result with fail()."""
        state: WorkflowState[None] = WorkflowState()
        state.total_steps = 2
        state.iteration_count = 5

        result = WorkflowResult.fail(
            error="Something went wrong",
            state=state,
            duration=2.0,
            reason="error",
        )

        assert result.success is False
        assert result.output is None
        assert result.state == state
        assert result.error == "Something went wrong"
        assert result.total_steps == 2
        assert result.total_iterations == 5
        assert result.duration_seconds == 2.0
        assert result.termination_reason == "error"

    def test_fail_without_state(self) -> None:
        """Test creating failed result without state."""
        result = WorkflowResult.fail(
            error="Early failure",
            duration=0.1,
        )

        assert result.success is False
        assert result.state is None
        assert result.total_steps == 0
        assert result.total_iterations == 0


class SimpleWorkflow(Workflow[None, str, dict[str, Any]]):
    """Simple workflow implementation for testing."""

    def __init__(
        self,
        config: WorkflowConfig | None = None,
        hooks: WorkflowHooks[dict[str, Any], str] | None = None,
        should_fail: bool = False,
        return_value: str = "success",
    ) -> None:
        super().__init__(config, hooks)
        self._should_fail = should_fail
        self._return_value = return_value

    @property
    def name(self) -> str:
        return "simple"

    def _create_initial_state(self, prompt: str) -> WorkflowState[dict[str, Any]]:
        return WorkflowState(context={"prompt": prompt})

    async def _execute(
        self,
        prompt: str,
        state: WorkflowState[dict[str, Any]],
        deps: None = None,
    ) -> str:
        if self._should_fail:
            raise ValueError("Workflow failed intentionally")

        step = WorkflowStep(
            step_number=state.current_step,
            step_type="process",
            description="Process prompt",
            input_data=prompt,
            output_data=self._return_value,
            completed_at=datetime.now(UTC),
        )
        state.add_step(step)

        return self._return_value


class TestWorkflow:
    """Tests for Workflow abstract base class."""

    @pytest.mark.asyncio
    async def test_run_success(self) -> None:
        """Test successful workflow run."""
        workflow = SimpleWorkflow(return_value="hello")
        result = await workflow.run("test prompt")

        assert result.success is True
        assert result.output == "hello"
        assert result.termination_reason == "completed"
        assert result.state is not None
        assert result.state.is_complete is True
        assert result.state.is_failed is False
        assert result.total_steps == 1

    @pytest.mark.asyncio
    async def test_run_failure(self) -> None:
        """Test workflow run with failure."""
        workflow = SimpleWorkflow(should_fail=True)
        result = await workflow.run("test prompt")

        assert result.success is False
        assert result.output is None
        assert result.error == "Workflow failed intentionally"
        assert result.termination_reason == "error"
        assert result.state is not None
        assert result.state.is_failed is True

    @pytest.mark.asyncio
    async def test_run_timeout(self) -> None:
        """Test workflow run with timeout."""
        import asyncio

        class SlowWorkflow(SimpleWorkflow):
            async def _execute(
                self,
                prompt: str,
                state: WorkflowState[dict[str, Any]],
                deps: None = None,
            ) -> str:
                await asyncio.sleep(10)  # Sleep longer than timeout
                return "done"

        config = WorkflowConfig(timeout_seconds=0.1)
        workflow = SlowWorkflow(config=config)
        result = await workflow.run("test")

        assert result.success is False
        assert "timeout" in result.error.lower()
        assert result.termination_reason == "timeout"
        assert result.state is not None
        assert result.state.is_failed is True

    def test_run_sync(self) -> None:
        """Test synchronous workflow run."""
        workflow = SimpleWorkflow(return_value="sync result")
        result = workflow.run_sync("test prompt")

        assert result.success is True
        assert result.output == "sync result"

    def test_workflow_name(self) -> None:
        """Test workflow name property."""
        workflow = SimpleWorkflow()
        assert workflow.name == "simple"

    def test_workflow_config(self) -> None:
        """Test workflow config property."""
        config = WorkflowConfig(max_steps=100)
        workflow = SimpleWorkflow(config=config)

        assert workflow.config.max_steps == 100

    def test_workflow_default_config(self) -> None:
        """Test workflow uses default config when none provided."""
        workflow = SimpleWorkflow()

        assert workflow.config.max_steps == 50
        assert workflow.config.enable_hooks is True

    def test_workflow_hooks_property(self) -> None:
        """Test workflow hooks property."""
        hooks: WorkflowHooks[dict[str, Any], str] = WorkflowHooks()
        workflow = SimpleWorkflow(hooks=hooks)

        assert workflow.hooks is hooks

    @pytest.mark.asyncio
    async def test_run_without_timeout(self) -> None:
        """Test workflow run without timeout (unlimited)."""
        config = WorkflowConfig(timeout_seconds=None)
        workflow = SimpleWorkflow(config=config, return_value="no timeout")
        result = await workflow.run("test")

        assert result.success is True
        assert result.output == "no timeout"

    @pytest.mark.asyncio
    async def test_initial_state_created(self) -> None:
        """Test that initial state is created with prompt context."""
        workflow = SimpleWorkflow()
        result = await workflow.run("my prompt")

        assert result.state is not None
        assert result.state.context is not None
        assert result.state.context["prompt"] == "my prompt"
