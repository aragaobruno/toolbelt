# 🛠️ toolbelt

A curated collection of modular, production-ready **AI Agent Skills** and utility scripts designed to supercharge autonomous developer workflows. Built with an SRE (Site Reliability Engineering) and Unix-like philosophy: highly cohesive, loosely coupled, and token-efficient.

This repository serves as a portfolio demonstrating advanced concepts in **AI Engineering**, context optimization, secure automation, and robust error-handling.

---

## 🗂️ Registry of Skills

Here are the developed skills structured logically and sequentially:

### 🧠 Category: Context Engineering & Quality (Phase 1)
*   **[`ai-slop-detector`](skills/context/ai-slop-detector):** Prose and code auditor. Detects generic AI-generated jargon ("AI-slop") and sanitizes output files to make them sound human, natural, and direct.
*   **[`context-compactor`](skills/context/context-compactor):** Source code compactor. Scans large file trees and generates lightweight structural maps containing only classes, methods, signatures, and docstrings for token context window optimization.

### 🛠️ Category: DevOps & Git Workflows (Phase 2)
*   *Coming soon:* **`smart-pr-generator`** (Auto PR and commit message generator with built-in anti-slop rules).
*   *Coming soon:* **`unit-test-bootstrapper`** (Unit test boilerplates generator from compacted code outlines).

### 🌐 Category: Data Integration & APIs (Phase 3)
*   *Coming soon:* **`structured-news-harvester`** (Real-time tech discussion harvester and noise cleaner).
*   *Coming soon:* **`schema-markup-builder`** (JSON-LD structured schema builder for technical SEO).

---

## 🚀 How It Works

Each skill in this collection is packaged in its own directory under `skills/` following the Google Antigravity standard structure:

```text
skills/[category]/[skill-name]/
├── SKILL.md        # Behavior declarations, triggers, and metadata
└── scripts/        # CLI scripts (Python with uv, or Node.js)
```

### Adopted Engineering Principles:
1.  **Token Efficiency:** LLM context windows are expensive. Our tools minimize the volume of raw code and text sent to agents.
2.  **Declarative Rate Limiting:** All API integrations enforce exponential backoff and structured handling of HTTP 429 status codes.
3.  **Prose Cleanliness:** Output files are audited to ensure direct, human-written style, free of AI conversational clutter.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
