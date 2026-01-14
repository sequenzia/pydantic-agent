# OpenTelemetry Integration

OpenTelemetry tracing and metrics.

## Prerequisites

```bash
uv add mamba-agents[otel]
```

## Quick Example

```python
from mamba_agents.observability import get_otel_integration

otel = get_otel_integration()

# Initialize
if otel.initialize():
    print("OpenTelemetry initialized")

# Trace operations
with otel.trace_agent_run(prompt, model="gpt-4o") as span:
    result = await agent.run(prompt)
    span.set_attribute("tokens", result.usage().total_tokens)
```

## Exporters

### Jaeger

```python
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

otel.add_span_processor(BatchSpanProcessor(
    JaegerExporter(agent_host_name="localhost", agent_port=6831)
))
```

### OTLP

```python
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

otel.add_span_processor(BatchSpanProcessor(
    OTLPSpanExporter(endpoint="https://otlp.example.com:4317")
))
```

## Configuration

```python
from mamba_agents.config import ObservabilityConfig

config = ObservabilityConfig(
    enable_tracing=True,
    service_name="my-agent",
)
```

## API Reference

::: mamba_agents.observability.otel.OTelIntegration
    options:
      show_root_heading: true
      show_source: true

::: mamba_agents.observability.otel.get_otel_integration
    options:
      show_root_heading: true
