# Filesystem Tools

File operations tools.

## Available Functions

| Function | Description |
|----------|-------------|
| `read_file` | Read file contents |
| `write_file` | Write/overwrite file |
| `append_file` | Append to file |
| `list_directory` | List directory contents |
| `file_info` | Get file metadata |
| `delete_file` | Delete file |
| `move_file` | Move/rename file |
| `copy_file` | Copy file |

## Quick Example

```python
from mamba_agents.tools import (
    read_file,
    write_file,
    list_directory,
    file_info,
)

# Read file
content = read_file("config.json")

# Write file
write_file("output.txt", "Hello!")

# List directory
entries = list_directory("/project", recursive=True)

# Get file info
info = file_info("README.md")
print(f"Size: {info.size}")
```

## Security

```python
from mamba_agents.tools.filesystem import FilesystemSecurity

security = FilesystemSecurity(
    sandbox_mode=True,
    base_directory="/safe/path",
    allowed_extensions=[".txt", ".json"],
)

# Use with tools
content = read_file("data.txt", security=security)
```

## API Reference

::: mamba_agents.tools.filesystem.read.read_file
    options:
      show_root_heading: true

::: mamba_agents.tools.filesystem.write.write_file
    options:
      show_root_heading: true

::: mamba_agents.tools.filesystem.directory.list_directory
    options:
      show_root_heading: true

::: mamba_agents.tools.filesystem.info.file_info
    options:
      show_root_heading: true
