---
name: smart-pr-generator
description: >-
  Analyzes Git diffs (staged or unstaged) and generates conventional commit messages and detailed, slop-free Pull Request descriptions.
---

# 🚀 smart-pr-generator

## Overview
Writing detailed commit messages and Pull Request descriptions is critical for clean codebases, but it creates significant cognitive load and context-switching overhead. The `smart-pr-generator` automates this process. It reads your git workspace diff, sends it to Gemini for SRE-grade analysis, and formats a conventional commit message alongside a detailed description. It strictly filters out AI jargon ("AI-slop"), ensuring all output looks natural and human-authored.

## Quick Start
To review a generated commit message and PR description for your changes:
```bash
node skills/devops/smart-pr-generator/scripts/generator.js show
```

To automatically stage your files and commit them using the generated conventional commit message:
```bash
git add .
export GEMINI_API_KEY="your-gemini-key"
node skills/devops/smart-pr-generator/scripts/generator.js commit
```

To save the generated PR description to a Markdown file:
```bash
node skills/devops/smart-pr-generator/scripts/generator.js save --output PR.md
```

## Utility Scripts

### `generator.js` (CLI)
A Node.js tool to automate git commits and PR formatting.

#### Subcommand: `show` (default)
Prints the conventional commit message suggestion and a fully formatted PR description (Goal, Proposed Changes, Verification) in Markdown.
*   **Example:**
    ```bash
    node generator.js show
    ```

#### Subcommand: `commit`
Automatically commits the changes (executes `git commit -m "<suggested_message>"`) directly in your workspace.
*   **Example:**
    ```bash
    node generator.js commit
    ```

#### Subcommand: `save`
Saves the PR description block into a markdown file.
*   **Arguments:** `[--output <path>]` (defaults to `PR_DESCRIPTION.md`)
*   **Example:**
    ```bash
    node generator.js save --output docs/PR-102.md
    ```
