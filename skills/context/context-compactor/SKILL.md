---
name: context-compactor
description: >-
  Scans codebase directories and generates a high-level, token-efficient structural overview of all classes, functions, and docstrings, omitting implementation details.
---

# 📦 context-compactor

## Overview
Feeding raw source files into an LLM context window is expensive and introduces noise. The `context-compactor` recursively scans a codebase, parses files (supporting Python, JavaScript, and TypeScript), and extracts only the structural elements—classes, methods, function signatures, and docstrings—while omitting the actual body implementations. 

This results in a lightweight, token-efficient structural map of your codebase that agents can use to understand the architecture without reading thousands of lines of code.

## Quick Start
To scan the current directory and generate a codebase map:
```bash
uv run skills/context/context-compactor/scripts/compactor.py C:\Users\araga\.gemini\antigravity\scratch\toolbelt --output map.txt
```

## Utility Scripts

### `compactor.py` (CLI)
A Python utility that recursively processes directories and extracts structural code elements.

*   **Arguments:**
    *   `<directory_path>` (Required)
    *   `--output` (Required): The file path where the output will be saved.
    *   `--exclude` (Optional): Glob patterns to exclude (e.g., `*.test.js,node_modules`).
*   **Example:**
    ```bash
    uv run compactor.py C:\Users\araga\.gemini\antigravity\scratch\toolbelt --output codebase_summary.txt --exclude "node_modules,*.spec.js"
    ```

## Output Format Example
For a Python file, the compactor will extract:
```text
File: auth.py
----------------------------------------
class Authenticator:
    """Manages user sessions and OAuth flows."""

    def __init__(self, client_id: str):
        ...

    def get_token(self, code: str) -> str:
        """Exchanges authorization code for an access token."""
        ...
```
