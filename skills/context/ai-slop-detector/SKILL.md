---
name: ai-slop-detector
description: >-
  Audits files for common AI-generated jargon, clichés, and throat-clearing sentences, and sanitizes the content to make it sound natural, human, and concise.
---

# 🧠 ai-slop-detector

## Overview
AI-generated text is often bloated with repetitive words, formal clichés ("throat-clearing" intros), and structural patterns that make it instantly recognizable as machine-generated. The `ai-slop-detector` audits your prose, documents, and code comments, highlights these patterns, and sanitizes them to produce clean, natural, and human-like writing.

## Quick Start
To scan a markdown file for AI jargon:
```bash
node skills/context/ai-slop-detector/scripts/detector.js check README.md
```

To automatically rewrite a document to remove AI slop:
```bash
export GEMINI_API_KEY="your-gemini-key"
node skills/context/ai-slop-detector/scripts/detector.js clean draft.md --output final.md
```

## Utility Scripts

### `detector.js` (CLI)
A Node.js tool to detect and clean AI writing patterns.

#### Subcommand: `check`
Scans the target file against a set of heuristic rules representing common AI writing flaws.
*   **Arguments:** `<file_path>`
*   **Example:**
    ```bash
    node detector.js check blog_draft.md
    ```

#### Subcommand: `clean`
Invokes the Gemini API to intelligently rewrite the file, stripping all slop while preserving the original intent and technical accuracy.
*   **Arguments:** `<file_path> --output <output_file_path>`
*   **Example:**
    ```bash
    node detector.js clean raw_draft.md --output clean_prose.md
    ```

## Common Pitfalls (Slop Dictionary)
Below are the primary patterns targeted by this skill:
1.  **Introductory Clichés ("Throat-clearing"):** 
    *   *Avoid:* "In today's fast-paced digital landscape...", "It is important to note that...", "In this article, we will delve into..."
    *   *Write:* Direct, punchy openers.
2.  **Robotic Transitions:**
    *   *Avoid:* "Furthermore", "Moreover", "Additionally", "In summary", "Ultimately", "It is testament to..."
    *   *Write:* Standard, conversational transitions.
3.  **Vague AI-isms:**
    *   *Avoid:* "Delve", "Tapestry", "Bespoke", "Revolutionize", "Beacon", "Pivotal".
    *   *Write:* "Explore", "Structure", "Custom", "Improve", "Key".
