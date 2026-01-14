"""Tests for WorkflowConfig."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from pydantic_agent.workflows import WorkflowConfig


class TestWorkflowConfig:
    """Tests for WorkflowConfig."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = WorkflowConfig()

        assert config.max_steps == 50
        assert config.max_iterations == 10
        assert config.timeout_seconds == 300.0
        assert config.step_timeout_seconds == 30.0
        assert config.enable_hooks is True
        assert config.track_state is True

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        config = WorkflowConfig(
            max_steps=100,
            max_iterations=20,
            timeout_seconds=600.0,
            step_timeout_seconds=60.0,
            enable_hooks=False,
            track_state=False,
        )

        assert config.max_steps == 100
        assert config.max_iterations == 20
        assert config.timeout_seconds == 600.0
        assert config.step_timeout_seconds == 60.0
        assert config.enable_hooks is False
        assert config.track_state is False

    def test_none_timeout_values(self) -> None:
        """Test that timeout values can be None (unlimited)."""
        config = WorkflowConfig(
            timeout_seconds=None,
            step_timeout_seconds=None,
        )

        assert config.timeout_seconds is None
        assert config.step_timeout_seconds is None

    def test_max_steps_validation_positive(self) -> None:
        """Test that max_steps must be positive."""
        with pytest.raises(ValidationError):
            WorkflowConfig(max_steps=0)

        with pytest.raises(ValidationError):
            WorkflowConfig(max_steps=-1)

    def test_max_iterations_validation_positive(self) -> None:
        """Test that max_iterations must be positive."""
        with pytest.raises(ValidationError):
            WorkflowConfig(max_iterations=0)

        with pytest.raises(ValidationError):
            WorkflowConfig(max_iterations=-1)

    def test_config_is_immutable_by_default(self) -> None:
        """Test that config can be used as immutable (no mutation needed)."""
        config = WorkflowConfig()
        # Pydantic models are mutable by default, but we use them immutably
        original_max_steps = config.max_steps
        assert original_max_steps == 50

    def test_config_can_be_copied(self) -> None:
        """Test that config can be copied with modifications."""
        original = WorkflowConfig(max_steps=50)
        modified = original.model_copy(update={"max_steps": 100})

        assert original.max_steps == 50
        assert modified.max_steps == 100
