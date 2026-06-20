---
name: unit-test-bootstrapper
description: >-
  Analyzes source code files (Python, JS, TS) and auto-generates comprehensive, robust unit tests covering happy paths, edge cases, and exceptions.
---

# 🧪 unit-test-bootstrapper

## Overview
Writing unit tests is one of the most repetitive parts of software development, yet it is essential to ensure system stability. The `unit-test-bootstrapper` automatically reads your source files, analyzes the functions and classes, and leverages the Gemini API to produce robust, production-grade test suites:
*   **Python:** Generates assertions and fixtures using `pytest`.
*   **JavaScript/TypeScript:** Generates tests using `Jest` or `Vitest`.
*   The generated tests cover success cases, boundary conditions, edge cases, and error handling.

## Quick Start
To generate PyTest assertions for a Python script:
```bash
export GEMINI_API_KEY="your-gemini-key"
uv run --with google-genai skills/devops/unit-test-bootstrapper/scripts/bootstrapper.py skills/context/context-compactor/scripts/compactor.py
```
This will automatically generate a `skills/context/context-compactor/scripts/test_compactor.py` file.

To specify a custom output path:
```bash
uv run --with google-genai skills/devops/unit-test-bootstrapper/scripts/bootstrapper.py src/utils.js --output tests/utils.test.js
```

## Utility Scripts

### `bootstrapper.py` (CLI)
A Python script to generate unit tests.

*   **Arguments:** `<file_path>` (required), `-o` / `--output <path>` (optional)
*   **Examples:**
    ```bash
    # Generate test_compactor.py in the same folder as compactor.py
    python bootstrapper.py compactor.py
    
    # Save Jest test to a specific tests folder
    python bootstrapper.py src/auth.ts -o tests/auth.test.ts
    ```
