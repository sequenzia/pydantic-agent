# ReActWorkflow

Built-in implementation of the ReAct (Reasoning and Acting) pattern.

## Quick Example

```python
from mamba_agents import Agent
from mamba_agents.workflows import ReActWorkflow, ReActConfig, ReActHooks
from mamba_agents.tools import read_file, run_bash

agent = Agent("gpt-4o", tools=[read_file, run_bash])

config = ReActConfig(
    max_iterations=15,
    expose_reasoning=True,
    auto_compact_in_workflow=True,
)

hooks = ReActHooks(
    on_thought=lambda s, t: print(f"Thought: {t}"),
    on_action=lambda s, tool, args: print(f"Action: {tool}"),
)

workflow = ReActWorkflow(agent=agent, config=config, hooks=hooks)
result = await workflow.run("Analyze the codebase")

# Access scratchpad
for entry in result.state.context.scratchpad:
    print(f"[{entry.entry_type}] {entry.content}")
```

## Classes

### ReActWorkflow

The main workflow class.

### ReActConfig

Configuration extending WorkflowConfig.

### ReActState

State tracking for ReAct execution.

### ReActHooks

Callbacks extending WorkflowHooks.

## API Reference

::: mamba_agents.workflows.react.workflow.ReActWorkflow
    options:
      show_root_heading: true
      show_source: true

::: mamba_agents.workflows.react.config.ReActConfig
    options:
      show_root_heading: true
      show_source: true

::: mamba_agents.workflows.react.state.ReActState
    options:
      show_root_heading: true
      show_source: true

::: mamba_agents.workflows.react.hooks.ReActHooks
    options:
      show_root_heading: true
      show_source: true
